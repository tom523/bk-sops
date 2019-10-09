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

import functools

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from auth_backend.plugins.decorators import verify_perms

from gcloud.contrib.analysis.permissions import statistics_resource
from gcloud.core.constant import AE
from gcloud.core.constant import TASK_CATEGORY
from gcloud.core.utils import check_and_rename_params
from gcloud.contrib.analysis.analyse_items import app_maker, task_flow_instance, task_template


@require_GET
def get_task_category(request):
    """
    @summary 获取所有模板分类列表
    :param request:
    :return:
    """
    groups = []
    for category in TASK_CATEGORY:
        groups.append({
            'value': category[0],
            'name': category[1],
        })
    return JsonResponse({'result': True, 'data': groups})


@verify_perms(auth_resource=statistics_resource, resource_get=None, actions=[statistics_resource.actions.view])
def analysis_home(request):
    """
    @param request:
    """
    context = {
        'view_mode': 'analysis',
    }
    return render(request, "core/base_vue.html", context)


def standardize_params(func):
    @functools.wraps(func)
    def wrapper(request):
        conditions = request.POST.get('conditions', {})
        page_index = int(request.POST.get('pageIndex', 1))
        limit = int(request.POST.get('limit', 10))
        group_by = request.POST.get('group_by', None)
        # 参数校验
        result_dict = check_and_rename_params(conditions, group_by)
        if not result_dict['success']:
            return JsonResponse({'result': False, 'message': result_dict['content']})
        conditions = result_dict['conditions']
        group_by = result_dict['group_by']
        # 过滤参数填写
        filters = {'is_deleted': False}
        filters.update(conditions)
        # 根据不同的view_funciton进行不同的处理
        inner_args = (group_by, filters, page_index, limit)
        success, content = func(*inner_args)
        # 统一处理返回逻辑
        if not success:
            return JsonResponse({'result': False, 'message': content})
        return JsonResponse({'result': True, 'data': content})
    return wrapper


@require_POST
@verify_perms(auth_resource=statistics_resource, resource_get=None, actions=[statistics_resource.actions.view])
@standardize_params
def query_instance_by_group(*args):
    """
    @summary 按起始时间、业务（可选）查询各类型任务实例个数和占比
    :param args: (group_by, filters, page_index, limit)
    """
    success, content = task_flow_instance.dispatch(*args)
    return success, content


@require_POST
@verify_perms(auth_resource=statistics_resource, resource_get=None, actions=[statistics_resource.actions.view])
@standardize_params
def query_template_by_group(*args):
    """
    @summary 查询模板相关信息
    :param args: (group_by, filters, page_index, limit)
    """
    success, content = task_template.dispatch(*args)
    return success, content


@require_POST
@verify_perms(auth_resource=statistics_resource, resource_get=None, actions=[statistics_resource.actions.view])
@standardize_params
def query_atom_by_group(*args):
    """
    @summary 查询标准插件相关信息
    :param args: (group_by, filters, page_index, limit)
    """
    group_by = args[0]
    if group_by in [
        AE.atom_execute, AE.atom_instance, AE.atom_execute_times,
        AE.atom_execute_fail_times, AE.atom_avg_execute_time,
        AE.atom_fail_percent
    ]:
        success, content = task_flow_instance.dispatch(*args)
    else:
        success, content = task_template.dispatch(*args)
    return success, content


@require_POST
@verify_perms(auth_resource=statistics_resource, resource_get=None, actions=[statistics_resource.actions.view])
@standardize_params
def query_appmaker_by_group(*args):
    """
    查询appmaker信息
    :param args: (group_by, filters, page_index, limit)
    """
    group_by = args[0]
    filters = args[1]
    if group_by == AE.appmaker_instance:
        # 如果是查询标准插件流程相关 需要加上 create_method = app_maker 的条件
        filters[AE.create_method] = AE.app_maker
        success, content = task_flow_instance.dispatch(*args)
    else:
        # 根据类型分组
        success, content = app_maker.dispatch(group_by, filters)
    return success, content
