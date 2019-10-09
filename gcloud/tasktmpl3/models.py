# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import re
import json
import logging
import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from pipeline.component_framework.models import ComponentModel
from pipeline.contrib.statistics.models import ComponentInTemplate, TemplateInPipeline
from pipeline.contrib.periodic_task.models import PeriodicTask
from pipeline.models import PipelineInstance, TemplateRelationship
from pipeline.parser.utils import replace_all_id
from auth_backend.resources import resource_type_lib

from gcloud.commons.template.models import BaseTemplate, BaseTemplateManager
from gcloud.core.constant import TASK_CATEGORY, AE
from gcloud.core.models import Project
from gcloud.core.utils import (
    timestamp_to_datetime,
    format_datetime,
    camel_case_to_underscore_naming
)

logger = logging.getLogger("root")

TEMPLATE_REGEX = re.compile(r'^name|creator_name|editor_name|'
                            r'create_time|edit_time|edit_finish_time|finish_time')


class TaskTemplateManager(BaseTemplateManager):

    def create(self, **kwargs):
        pipeline_template = self.create_pipeline_template(**kwargs)
        task_template = self.model(
            project=kwargs['project'],
            category=kwargs['category'],
            pipeline_template=pipeline_template,
            notify_type=kwargs['notify_type'],
            notify_receivers=kwargs['notify_receivers'],
            time_out=kwargs['time_out'],
        )
        task_template.save()
        return task_template

    def export_templates(self, template_id_list, project_id):
        if self.filter(id__in=template_id_list, project_id=project_id).count() != len(template_id_list):
            raise self.model.DoesNotExist()
        data = super(TaskTemplateManager, self).export_templates(template_id_list)
        return data

    def import_operation_check(self, template_data, project_id):
        data = super(TaskTemplateManager, self).import_operation_check(template_data)

        template = template_data['template']

        relate_project_ids = self.filter(id__in=template.keys(),
                                         is_deleted=False
                                         ).values_list('project_id', flat=True)
        is_multiple_relate = len(set(relate_project_ids)) > 1
        is_across_override = relate_project_ids and relate_project_ids[0] != int(project_id)
        has_common_template = not all([tmpl.get('project_id') for _, tmpl in template_data['template'].items()])

        can_override = not (is_multiple_relate or is_across_override or has_common_template)

        if not can_override:
            data['override_template'] = []

        result = {
            'can_override': can_override,
            'new_template': data['new_template'],
            'override_template': data['override_template']
        }
        return result

    def import_templates(self, template_data, override, project_id):
        project = Project.objects.get(id=project_id)
        check_info = self.import_operation_check(template_data, project_id)

        # operation validation check
        if override and (not check_info['can_override']):
            return {
                'result': False,
                'message': 'Unable to override flows across project',
                'data': 0
            }

        def defaults_getter(template_dict):
            return {
                'project': project,
                'category': template_dict['category'],
                'notify_type': template_dict['notify_type'],
                'notify_receivers': template_dict['notify_receivers'],
                'time_out': template_dict['time_out'],
                'pipeline_template_id': template_dict['pipeline_template_id'],
                'is_deleted': False
            }

        return super(TaskTemplateManager, self)._perform_import(template_data=template_data,
                                                                check_info=check_info,
                                                                override=override,
                                                                defaults_getter=defaults_getter,
                                                                resource=resource_type_lib['flow'])

    def general_filter(self, filters=None):
        """
        @summary: 通用过滤
        @param filters:
        @return:
        """
        prefix_filters = {}
        for cond, value in filters.items():
            # component_code不加入查询条件中
            if value in ['None', ''] or cond in ['component_code', 'order_by', 'type']:
                continue
            if TEMPLATE_REGEX.match(cond):
                filter_cond = 'pipeline_template__%s' % cond
                # 时间需要大于小于
                if cond == 'create_time':
                    filter_cond = '%s__gte' % filter_cond
                    prefix_filters.update({filter_cond: timestamp_to_datetime(value)})
                    continue
                elif cond == 'finish_time':
                    filter_cond = 'pipeline_template__create_time__lt'
                    prefix_filters.update(
                        {filter_cond: timestamp_to_datetime(value) + datetime.timedelta(days=1)})
                    continue
            else:
                filter_cond = cond
            prefix_filters.update({filter_cond: value})

        try:
            tasktmpl = self.filter(**prefix_filters)
            return True, None, tasktmpl, prefix_filters
        except Exception as e:
            message = u"query_task_list params conditions[%s] have invalid key or value: %s" % (filters, e)
            return False, message, None, None

    def group_by_state(self, tasktmpl, *args):
        # 按流程模板执行状态查询流程个数
        total = tasktmpl.count()
        groups = [
            {
                'code': 'CREATED',
                'name': _(u"未执行"),
                'value': tasktmpl.filter(pipeline_template__is_started=False).count()
            },
            {
                'code': 'EXECUTING',
                'name': _(u"执行中"),
                'value': tasktmpl.filter(pipeline_template__is_started=True,
                                         pipeline_template__is_finished=False).count()
            },
            {
                'code': 'FINISHED',
                'name': _(u"已完成"),
                'value': tasktmpl.filter(pipeline_template__is_finished=True).count()
            }
        ]
        return total, groups

    def group_by_biz_cc_id(self, tasktmpl, *args):
        # 查询不同业务的模板个数
        total = tasktmpl.count()
        template_list = tasktmpl.values(AE.project_id, AE.project__name).annotate(
            value=Count('business__cc_id')).order_by("value")
        groups = []
        for data in template_list:
            groups.append({
                'code': data.get(AE.project_id),
                'name': data.get(AE.project__name),
                'value': data.get('value', 0)
            })
        return total, groups

    def group_by_atom_cite(self, tasktmpl, *args):
        # 查询不同原子引用的个数
        # 获得标准插件dict列表
        component_dict = ComponentModel.objects.get_component_dict()
        template_list = tasktmpl.values_list("pipeline_template__template_id")
        component_list = ComponentModel.objects.filter(status=True).values("code")
        # 用 template_id 列表获取所有符合条件的总数
        other_component_list = ComponentInTemplate.objects.filter(template_id__in=template_list).values(
            "component_code").annotate(value=Count("component_code")).order_by()
        components_dict = {}
        total = component_list.count()
        for component in other_component_list:
            value = component["value"]
            components_dict[component["component_code"]] = value
            # 总数不能通过查询获得，需要通过循环计数
        groups = []
        # 循环聚合信息
        for data in component_list:
            code = data.get("code")
            groups.append({
                'code': code,
                'name': component_dict.get(code, None),
                'value': components_dict.get(code, 0)
            })
        return total, groups

    def group_by_atom_template(self, tasktmpl, filters, page, limit):
        # 按起始时间、业务（可选）、类型（可选）、标准插件查询被引用的流程模板列表(dataTable)

        # 获得所有类型的dict列表
        category_dict = dict(TASK_CATEGORY)

        # 获取标准插件code
        component_code = filters.get("component_code")
        # 获取到组件code对应的template_id_list
        if component_code:
            template_id_list = ComponentInTemplate.objects.filter(
                component_code=component_code).distinct().values_list("template_id")
        else:
            template_id_list = ComponentInTemplate.objects.all().values_list("template_id")
        template_list = tasktmpl.filter(pipeline_template__template_id__in=template_id_list)
        total = template_list.count()
        order_by = filters.get("order_by", '-templateId')
        if order_by == '-templateId':
            template_list = template_list.order_by('-id')
        if order_by == 'templateId':
            template_list = template_list.order_by('id')
        template_list = template_list.values(
            "id",
            "business__cc_id",
            "business__cc_name",
            "pipeline_template__name",
            "category",
            "pipeline_template__create_time",
            "pipeline_template__creator"
        )[(page - 1) * limit:page * limit]
        groups = []
        # 循环聚合信息
        for data in template_list:
            groups.append({
                'templateId': data.get("id"),
                'businessId': data.get("business__cc_id"),
                'businessName': data.get("business__cc_name"),
                'templateName': data.get("pipeline_template__name"),
                'category': category_dict[data.get("category")],  # 需要将code转为名称
                "createTime": format_datetime(data.get("pipeline_template__create_time")),
                "creator": data.get("pipeline_template__creator")
            })
        return total, groups

    def group_by_atom_execute(self, tasktmpl, filters, page, limit):
        # 需要获得符合的查询的对应 template_id 列表

        # 获得所有类型的dict列表
        category_dict = dict(TASK_CATEGORY)

        # 获取标准插件code
        component_code = filters.get("component_code")
        # 获取到组件code对应的template_id
        template_id_list = ComponentInTemplate.objects.filter(component_code=component_code).values_list(
            "template_id")
        total = template_id_list.count()
        template_list = tasktmpl.filter(pipeline_template__template_id__in=template_id_list).values(
            "id",
            "business__cc_name",
            "business__cc_id",
            "pipeline_template__name",
            "category",
            "pipeline_template__edit_time",
            "pipeline_template__editor")[(page - 1) * limit:page * limit]
        groups = []
        # 循环聚合信息
        for data in template_list:
            groups.append({
                'templateId': data.get("id"),
                'businessId': data.get("business__cc_id"),
                'businessName': data.get("business__cc_name"),
                'templateName': data.get("pipeline_template__name"),
                'category': category_dict[data.get("category")],
                "editTime": data.get("pipeline_template__edit_time").strftime("%Y-%m-%d %H:%M:%S"),
                "editor": data.get("pipeline_template__editor")
            })
        return total, groups

    def _group_by_template_node_sorting(self, filtered_list, filtered_id_list, order_by, page, limit):
        other_template = TemplateInPipeline.objects.exclude(template_id__in=filtered_id_list)
        other_template_id_list = [template.template_id for template in other_template]
        if order_by[0] == '-':
            # 倒序则把未创建任务的流程放在数组后面
            filtered_count = filtered_list.count()
            item_range = page * limit - filtered_count if page * limit > filtered_count else 0
            other_template_id_list = other_template_id_list[:item_range]
            template_id_list = filtered_id_list + other_template_id_list
            template_id_list = template_id_list[(page - 1) * limit:page * limit]
        else:
            # 正序则把未创建任务的流程放在数组前面
            other_count = other_template.count()
            item_range = page * limit - other_count if page * limit > other_count else 0
            filtered_id_list = filtered_id_list[:item_range]
            template_id_list = other_template_id_list + filtered_id_list
            template_id_list = template_id_list[(page - 1) * limit:page * limit]
        return template_id_list

    def group_by_template_node(self, tasktmpl, filters, page, limit):
        # 按起始时间、业务（可选）、类型（可选）查询各流程模板标准插件节点个数、子流程节点个数、网关节点数
        total = tasktmpl.count()
        groups = []

        # 获得所有类型的dict列表
        category_dict = dict(TASK_CATEGORY)

        # 过滤得到所有符合查询条件的流程
        template_id_list = tasktmpl.values("pipeline_template__template_id")
        id_list = tasktmpl.values("pipeline_template__id", "pipeline_template__template_id")
        template_pipeline_data = TemplateInPipeline.objects.filter(template_id__in=template_id_list)
        # 查询所有的流程引用，并统计引用数量
        relationship_list = TemplateRelationship.objects.filter(descendant_template_id__in=template_id_list).values(
            "descendant_template_id").annotate(relationship_total=Count("descendant_template_id"))
        # 构造id： template_id字典，方便后面对不同model进行查询
        template_id_map = {template['pipeline_template__id']: template['pipeline_template__template_id']
                           for template in id_list}
        # 查询所有的任务，并统计每个template创建了多少个任务
        taskflow_list = PipelineInstance.objects.filter(template_id__in=template_id_map.keys()).values(
            "template_id").annotate(instance_total=Count("template_id")).order_by()
        # 查询所有归档的周期任务，并统计每个template创建了多少个周期任务
        periodic_list = PeriodicTask.objects.filter(template__template_id__in=template_id_list).values(
            "template__template_id").annotate(periodic_total=Count("template__id"))

        order_by = filters.get("order_by", "-templateId")
        # 使用驼峰转下划线进行转换order_by
        camel_order_by = camel_case_to_underscore_naming(order_by)
        # 排列获取分页后的数据
        if order_by in '-relationshipTotal':
            # 计算流程被引用为子流程的数量
            filtered_relationship_list = relationship_list.order_by(camel_order_by)
            filtered_id_list = [template.template_id for template in filtered_relationship_list]
            template_id_list = self._group_by_template_node_sorting(
                filtered_relationship_list, filtered_id_list, order_by, page, limit)
        elif order_by in '-instanceTotal':
            # 计算流程创建的任务数
            filtered_taskflow_list = taskflow_list.order_by(camel_order_by)
            filtered_id_list = [template_id_map[template["template_id"]] for template in filtered_taskflow_list]
            template_id_list = self._group_by_template_node_sorting(
                filtered_taskflow_list, filtered_id_list, order_by, page, limit)
        elif order_by in '-periodicTotal':
            # 计算流程创建的周期任务数
            filtered_periodic_list = periodic_list.order_by(camel_order_by)
            filtered_id_list = [template["template__template_id"] for template in filtered_periodic_list]
            template_id_list = self._group_by_template_node_sorting(
                filtered_periodic_list, filtered_id_list, order_by, page, limit)
        else:
            filtered_pipeline_data = template_pipeline_data.order_by(camel_order_by)[(page - 1) * limit:page * limit]
            template_id_list = [template.template_id for template in filtered_pipeline_data]
        tasktmpl = tasktmpl.filter(pipeline_template__template_id__in=template_id_list)

        pipeline_dict = {}
        pipeline_data = template_pipeline_data.filter(template_id__in=template_id_list)
        for pipeline in pipeline_data:
            pipeline_dict[pipeline.template_id] = {"atom_total": pipeline.atom_total,
                                                   "subprocess_total": pipeline.subprocess_total,
                                                   "gateways_total": pipeline.gateways_total}
        relationship_dict = {}
        relationship_list = relationship_list.filter(descendant_template_id__in=template_id_list)
        for relationship in relationship_list:
            relationship_dict[relationship["descendant_template_id"]] = relationship["relationship_total"]

        taskflow_dict = {}
        taskflow_list = taskflow_list.filter(template__template_id__in=template_id_list)
        for taskflow in taskflow_list:
            taskflow_dict[template_id_map[taskflow["template_id"]]] = taskflow["instance_total"]

        periodic_dict = {}
        periodic_list = periodic_list.filter(template__template_id__in=template_id_list)
        for periodic_task in periodic_list:
            periodic_dict[periodic_task["template__template_id"]] = periodic_task["periodic_total"]

        # 需要循环执行计算相关节点
        for template in tasktmpl:
            pipeline_template = template.pipeline_template
            template_id = template.id
            pipeline_template_id = pipeline_template.template_id
            # 插入信息
            groups.append({
                'templateId': template_id,
                'businessId': template.business.cc_id,
                'businessName': template.business.cc_name,
                'templateName': pipeline_template.name,
                'category': category_dict[template.category],
                "createTime": format_datetime(pipeline_template.create_time),
                "creator": pipeline_template.creator,
                "atomTotal": pipeline_dict[pipeline_template_id]["atom_total"],
                "subprocessTotal": pipeline_dict[pipeline_template_id]["subprocess_total"],
                "gatewaysTotal": pipeline_dict[pipeline_template_id]["gateways_total"],
                "relationshipTotal": relationship_dict.get(pipeline_template_id, 0),
                "instanceTotal": taskflow_dict.get(pipeline_template_id, 0),
                "periodicTotal": periodic_dict.get(pipeline_template_id, 0)
            })
        if order_by[0] == "-":
            # 需要去除负号
            order_by = order_by[1:]
            groups = sorted(groups, key=lambda group: -group.get(order_by))
        else:
            groups = sorted(groups, key=lambda group: group.get(order_by))
        return total, groups

    def general_group_by(self, prefix_filters, group_by):
        try:
            total, groups = self.classified_count(prefix_filters, group_by)
            return True, None, total, groups
        except Exception as e:
            message = u"query_task_list params conditions[%s] have invalid key or value: %s" % (prefix_filters, e)
            return False, message, None, None

    def replace_all_template_tree_node_id(self):
        templates = self.filter(is_deleted=False)
        success = 0
        for template in templates:
            tree_data = template.pipeline_template.data
            try:
                replace_all_id(tree_data)
            except Exception:
                continue
            template.pipeline_template.update_template(tree_data)
            success += 1
        return len(templates), success

    def get_collect_template(self, project_id, username):
        user_model = get_user_model()
        collected_templates = user_model.objects.get(username=username).tasktemplate_set.values_list('id', flat=True)
        collected_templates_list = []
        template_list = self.filter(is_deleted=False, project_id=project_id, id__in=list(collected_templates))
        for template in template_list:
            collected_templates_list.append({
                'id': template.id,
                'name': template.name
            })
        return True, collected_templates_list


class TaskTemplate(BaseTemplate):
    project = models.ForeignKey(Project,
                                verbose_name=_(u"所属项目"),
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)

    objects = TaskTemplateManager()

    def __unicode__(self):
        return u'%s_%s' % (self.project, self.pipeline_template)

    class Meta(BaseTemplate.Meta):
        verbose_name = _(u"流程模板 TaskTemplate")
        verbose_name_plural = _(u"流程模板 TaskTemplate")

    def get_notify_receivers_list(self, username):
        notify_receivers = json.loads(self.notify_receivers)
        receiver_group = notify_receivers.get('receiver_group', [])  # noqa
        more_receiver = notify_receivers.get('more_receiver', '')  # noqa
        receivers = [username]  # TODO get project notify receivers
        return receivers
