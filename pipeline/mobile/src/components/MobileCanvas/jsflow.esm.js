import{jsPlumb as e}from"jsplumb";function t(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function n(e){for(var n=1;n<arguments.length;n++){var o=null!=arguments[n]?arguments[n]:{},i=Object.keys(o);"function"==typeof Object.getOwnPropertySymbols&&(i=i.concat(Object.getOwnPropertySymbols(o).filter(function(e){return Object.getOwnPropertyDescriptor(o,e).enumerable}))),i.forEach(function(n){t(e,n,o[n])})}return e}function o(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=[],o=!0,i=!1,s=void 0;try{for(var a,r=e[Symbol.iterator]();!(o=(a=r.next()).done)&&(n.push(a.value),!t||n.length!==t);o=!0);}catch(e){i=!0,s=e}finally{try{o||null==r.return||r.return()}finally{if(i)throw s}}return n}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()}var i=function(e,t,n,o,i,s,a,r,c,d){"boolean"!=typeof a&&(c=r,r=a,a=!1);var l,h="function"==typeof n?n.options:n;if(e&&e.render&&(h.render=e.render,h.staticRenderFns=e.staticRenderFns,h._compiled=!0,i&&(h.functional=!0)),o&&(h._scopeId=o),s?(l=function(e){(e=e||this.$vnode&&this.$vnode.ssrContext||this.parent&&this.parent.$vnode&&this.parent.$vnode.ssrContext)||"undefined"==typeof __VUE_SSR_CONTEXT__||(e=__VUE_SSR_CONTEXT__),t&&t.call(this,c(e)),e&&e._registeredComponents&&e._registeredComponents.add(s)},h._ssrRegister=l):t&&(l=a?function(){t.call(this,d(this.$root.$options.shadowRoot))}:function(e){t.call(this,r(e))}),l)if(h.functional){var f=h.render;h.render=function(e,t){return l.call(t),f(e,t)}}else{var u=h.beforeCreate;h.beforeCreate=u?[].concat(u,l):[l]}return n},s="undefined"!=typeof navigator&&/msie [6-9]\\b/.test(navigator.userAgent.toLowerCase());var a=document.head||document.getElementsByTagName("head")[0],r={};var c=function(e){return function(e,t){return function(e,t){var n=s?t.media||"default":e,o=r[n]||(r[n]={ids:new Set,styles:[]});if(!o.ids.has(e)){o.ids.add(e);var i=t.source;if(t.map&&(i+="\n/*# sourceURL="+t.map.sources[0]+" */",i+="\n/*# sourceMappingURL=data:application/json;base64,"+btoa(unescape(encodeURIComponent(JSON.stringify(t.map))))+" */"),o.element||(o.element=document.createElement("style"),o.element.type="text/css",t.media&&o.element.setAttribute("media",t.media),a.appendChild(o.element)),"styleSheet"in o.element)o.styles.push(i),o.element.styleSheet.cssText=o.styles.filter(Boolean).join("\n");else{var c=o.ids.size-1,d=document.createTextNode(i),l=o.element.childNodes;l[c]&&o.element.removeChild(l[c]),l.length?o.element.insertBefore(d,l[c]):o.element.appendChild(d)}}}(e,t)}},d=i({render:function(){var e=this.$createElement;return(this._self._c||e)("div",{staticClass:"palette-panel"},[this._t("palette",[this._m(0)])],2)},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("ul",{staticClass:"palette-group"},[t("li",[t("div",{staticClass:"palette-default-item type-a"},[this._v("start")])]),t("li",[t("div",{staticClass:"palette-default-item type-b"},[this._v("end")])]),t("li",[t("div",{staticClass:"palette-default-item type-c"},[this._v("C")])]),t("li",[t("div",{staticClass:"palette-default-item type-d"},[this._v("D")])])])}]},function(e){e&&e("data-v-0fd10652_0",{source:".palette-group{margin:0;padding:0;background:#fcfcfc;text-align:center;list-style:none}.palette-group>li{padding:14px 0}.palette-default-item{display:inline-block;width:40px;height:40px;line-height:40px;font-size:12px;color:#888;border:1px solid #999;border-radius:2px;cursor:pointer;user-select:none}.palette-default-item:hover{box-shadow:0 0 8px rgba(50,50,50,.3)}.type-a{border-radius:50%}.type-b{border-radius:50%}.type-c{height:30px;line-height:30px;border:1px solid #999}",map:void 0,media:void 0})},{name:"PalettePanel",props:["selector"],data:function(){return{}},mounted:function(){this.$emit("registerPaletteEvent")}},void 0,!1,void 0,c,void 0),l=i({render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"tool-panel"},e._l(e.tools,function(t,o){return n("div",{key:o,class:["tool-item",t.cls,{actived:"frameSelect"===t.type&&e.isFrameSelecting}],on:{click:function(n){return e.onToolClick(t)}}},[e._v("\n        "+e._s(t.name||t.type)+"\n    ")])}),0)},staticRenderFns:[]},function(e){e&&e("data-v-17c0bb40_0",{source:".tool-item{display:inline-block;margin-right:10px;cursor:pointer;user-select:none}.tool-item:last-child{margin-right:0}.tool-item.actived{color:#3a84ff}",map:void 0,media:void 0})},{name:"ToolPanel",props:["tools","isFrameSelecting"],data:function(){return{}},methods:{onToolClick:function(e){this.$emit("onToolClick",e)}}},void 0,!1,void 0,c,void 0);function h(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"",t="",n=0;n<7;n++)t+=Math.floor(65536*(1+Math.random())).toString(16).substring(1);return e+t}var f={showPalette:{type:Boolean,default:!0},showTool:{type:Boolean,default:!0},tools:{type:Array,default:function(){return[{type:"zoomIn",name:"放大",cls:"tool-item"},{type:"zoomOut",name:"缩小",cls:"tool-item"},{type:"resetPosition",name:"重置",cls:"tool-item"},{type:"frameSelect",name:"框选",cls:"tool-item"}]}},editable:{type:Boolean,default:!0},selector:{type:String,default:"palette-item"},data:{type:Object,default:function(){return{nodes:[],lines:[]}}},nodeOptions:{grid:[5,5]},connectorOptions:{type:Object,default:function(){return{paintStyle:{fill:"transparent",stroke:"#a9adb6",strokeWidth:2},hoverPaintStyle:{fill:"transparent",stroke:"#3a84ff"}}}},endpointOptions:{type:Object,default:function(){return{endpoint:"Dot",connector:["Flowchart",{stub:[1,6],alwaysRespectStub:!0,gap:8,cornerRadius:2}],connectorOverlays:[["PlainArrow",{width:8,length:6,location:1,id:"arrow"}]],anchor:["Left","Right","Top","Bottom"],isSource:!0,isTarget:!0}}}},u={mousedown:"ontouchstart"in document.documentElement?"touchstart":"mousedown",mousemove:"ontouchmove"in document.documentElement?"touchmove":"mousemove",mouseup:"ontouchend"in document.documentElement?"touchend":"mouseup"},p=i({render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"jsflow"},[n("div",{staticClass:"canvas-area"},[e.showTool?n("div",{staticClass:"tool-panel-wrap"},[e._t("toolPanel",[n("tool-panel",{attrs:{tools:e.tools,"is-frame-selecting":e.isFrameSelecting},on:{onToolClick:e.onToolClick}})])],2):e._e(),e.showPalette?n("div",{staticClass:"palette-panel-wrap"},[e._t("palettePanel",[n("palette-panel",{ref:"palettePanel",attrs:{selector:e.selector},on:{registerPaletteEvent:e.registerPaletteEvent}})])],2):e._e(),n("div",{ref:"canvasFlowWrap",staticClass:"canvas-flow-wrap",style:e.canvasWrapStyle,on:e._d({},[e.mousedown,e.onCanvasMouseDown,e.mouseup,e.onCanvasMouseUp])},[n("div",{ref:"canvasFlow",staticClass:"canvas-flow",style:e.canvasStyle,attrs:{id:"canvas-flow"}},e._l(e.nodes,function(t){return n("div",{key:t.id,staticClass:"jsflow-node",style:e.setNodeInitialPos(t),attrs:{id:t.id}},[e._t("nodeTemplate",[n("div",{staticClass:"node-default"})],{node:t})],2)}),0),e.isFrameSelecting?n("div",{staticClass:"canvas-frame-selector",style:e.frameSelectorStyle}):e._e()]),e.showAddingNode?n("div",{staticClass:"jsflow-node adding-node",style:e.setNodeInitialPos(e.addingNodeConfig)},[e._t("nodeTemplate",[n("div",{staticClass:"node-default"})],{node:e.addingNodeConfig})],2):e._e()])])},staticRenderFns:[]},function(e){e&&e("data-v-22fa7eb4_0",{source:".jsflow{border:1px solid #ccc}.jsflow .canvas-area{position:relative;height:600px;min-height:600px}.jsflow .tool-panel-wrap{position:absolute;top:20px;left:70px;padding:10px 20px;background:#c4c6cc;opacity:.65;border-radius:4px;z-index:4}.jsflow .palette-panel-wrap{float:left;width:60px;height:100%;border-right:1px solid #ccc}.jsflow .canvas-flow-wrap{position:relative;height:100%;overflow:hidden}.jsflow .canvas-flow{position:relative;min-width:100%;min-height:100%}.jsflow .canvas-frame-selector{position:absolute;border:1px solid #3a84ff;background:rgba(58,132,255,.15)}.jsflow .jsflow-node{position:absolute}.jsflow .jsflow-node .node-default{width:120px;height:80px;line-height:80px;border:1px solid #ccc;border-radius:2px;text-align:center}.jsflow .jsflow-node.selected{border:1px solid #3a84ff}.jsflow .adding-node{opacity:.8}",map:void 0,media:void 0})},{name:"JsFlow",components:{PalettePanel:d,ToolPanel:l},model:{prop:"data",event:"change"},props:f,data:function(){var e=this.data;return n({nodes:e.nodes,lines:e.lines,canvasGrabbing:!1,isFrameSelecting:!1,mouseDownPos:{},canvasPos:{x:0,y:0},canvasOffset:{x:0,y:0},frameSelectorPos:{x:0,y:0},frameSelectorRect:{width:0,height:0},selectedNodes:[],showAddingNode:!1,addingNodeConfig:{},addingNodeRect:{},canvasRect:{},paletteRect:{},zoom:1},u)},computed:{canvasWrapStyle:function(){return{cursor:this.isFrameSelecting?"crosshair":this.canvasGrabbing?"-webkit-grabbing":"-webkit-grab"}},canvasStyle:function(){return{left:"".concat(this.canvasOffset.x,"px"),top:"".concat(this.canvasOffset.y,"px")}},frameSelectorStyle:function(){return{left:"".concat(this.frameSelectorPos.x,"px"),top:"".concat(this.frameSelectorPos.y,"px"),width:"".concat(this.frameSelectorRect.width,"px"),height:"".concat(this.frameSelectorRect.height,"px")}}},watch:{data:{handler:function(e){var t=e.nodes,n=e.lines;this.nodes=t,this.lines=n},deep:!0}},mounted:function(){this.initCanvas(),this.registerEvent(),this.renderData(),this.canvasRect=this.$refs.canvasFlow.getBoundingClientRect(),this.paletteRect=this.$refs.palettePanel?this.$refs.palettePanel.$el.getBoundingClientRect():{}},beforeDestroy:function(){this.$refs.palettePanel.$el.removeEventListener(this.mousedown,this.nodeCreateHandler),this.$el.removeEventListener(this.mousemove,this.nodeMovingHandler),document.removeEventListener(this.mouseup,this.nodeMoveEndHandler)},methods:{initCanvas:function(){this.instance=e.getInstance({container:"canvas-flow"})},registerEvent:function(){var e=this;this.instance.bind("beforeDrag",function(e){return console.log("beforeDrag:",e),!0}),this.instance.bind("beforeDrop",function(e){return!0}),this.instance.bind("connection",function(e){console.log("connection")}),this.instance.bind("beforeDetach",function(e){return console.log("beforeDetach"),!0}),this.instance.bind("connectionDetached",function(t,n){var o=e.lines.filter(function(e){return e.source.id!==t.sourceId&&e.target.id!==t.targetId});e.lines=o,console.log("connectionDetached")}),this.instance.bind("connectionMoved",function(e,t){console.log("connectionMoved")}),this.instance.bind("click",function(e,t){console.log(e,t)}),this.instance.bind("dblclick",function(e,t){console.log(e,t)})},renderData:function(){var e=this;this.instance.batch(function(){e.nodes.forEach(function(t){e.setNodeDraggable(t,e.nodeOptions),e.setNodeEndPoint(t,e.endpointOptions)}),e.lines.forEach(function(t){e.createConnector(t,e.connectorOptions)})})},createNode:function(e){var t=this;this.nodes.push(e),this.$nextTick(function(){t.setNodeDraggable(e,t.nodeOptions),t.setNodeEndPoint(e,t.endpointOptions)})},removeNode:function(e){var t=this.nodes.findIndex(function(t){return t.id===e.id});this.nodes.splice(t,1),this.instance.remove(e.id)},setNodeEndPoint:function(e,t){var o=this;(e.endpoints||["Top","Right","Bottom","Left"]).forEach(function(i){o.instance.addEndpoint(e.id,n({anchor:i,uuid:i+e.id},t))})},setNodeDraggable:function(e,t){if(this.editable){var i=this;this.instance.draggable(e.id,n({grid:[20,20],stop:function(t){var n=i.nodes.findIndex(function(t){return t.id===e.id}),s=Object.assign({},e),a=o(t.pos,2),r=a[0],c=a[1];s.x=r,s.y=c,i.nodes.splice(n,1,s),i.$emit("onNodeMove",s,t)}},t))}},setNodeInitialPos:function(e){return{left:"".concat(e.x,"px"),top:"".concat(e.y,"px")}},createConnector:function(e,t){var o=e.options||{};return this.instance.connect({source:e.source.id,target:e.target.id,uuids:[e.source.arrow+e.source.id,e.target.arrow+e.target.id]},n({},t,o))},removeConnector:function(e){var t=this;this.instance.getConnections({source:e.source.id,target:e.target.id}).forEach(function(e){t.instance.detach(e)})},addLineOverlay:function(e,t){var n=this.instance.getConnections({source:e.source.id,target:e.target.id});console.log(n),n.forEach(function(e){e.addOverlay([t.type,{label:t.name,location:t.location,cssClass:t.cls}])})},removeLineOverlay:function(){},onCanvasMouseDown:function(e){this.isFrameSelecting?this.frameSelectHandler(e):(this.canvasGrabbing=!0,this.mouseDownPos={x:e.pageX,y:e.pageY},this.$refs.canvasFlowWrap.addEventListener(this.mousemove,this.canvasFlowMoveHandler,!1))},canvasFlowMoveHandler:function(e){this.canvasOffset={x:this.canvasPos.x+e.pageX-this.mouseDownPos.x,y:this.canvasPos.y+e.pageY-this.mouseDownPos.y}},onCanvasMouseUp:function(e){this.isFrameSelecting?this.frameSelectEndHandler(e):(this.canvasGrabbing=!1,this.$refs.canvasFlowWrap.removeEventListener(this.mousemove,this.canvasFlowMoveHandler),this.canvasPos={x:this.canvasOffset.x,y:this.canvasOffset.y})},registerPaletteEvent:function(){this.$refs.palettePanel.$el.addEventListener(this.mousedown,this.nodeCreateHandler,!1)},nodeCreateHandler:function(e){var t=this;console.info("mousedown:",e.target);var o=function e(t,n){return 1===t.nodeType&&t.classList.contains(n)?t:"HTML"!==t.parentNode.nodeName?e(t.parentNode,n):null}(e.target,this.selector);if(!o)return!1;var i=o.dataset.type?o.dataset.type:"",s=o.dataset?o.dataset.config:{};this.showAddingNode=!0,this.addingNodeConfig.id=h("node"),this.addingNodeConfig.type=i,this.$nextTick(function(){var o=t.$el.querySelector(".adding-node");t.addingNodeRect=o.getBoundingClientRect();var a=t.getAddingNodePos(e);t.addingNodeConfig=n({id:h("node"),type:i,x:a.x,y:a.y},s),t.$el.addEventListener(t.mousemove,t.nodeMovingHandler,!1),document.addEventListener(t.mouseup,t.nodeMoveEndHandler,!1)})},nodeMovingHandler:function(e){console.log("moving:",e.pageX,e.pageY);var t=this.getAddingNodePos(e);this.$set(this.addingNodeConfig,"x",t.x),this.$set(this.addingNodeConfig,"y",t.y)},nodeMoveEndHandler:function(e){if(this.$el.removeEventListener(this.mousemove,this.nodeMovingHandler),document.removeEventListener(this.mouseup,this.nodeMoveEndHandler),this.showAddingNode=!1,e.pageX>this.paletteRect.left+this.paletteRect.width){var t=this.addingNodeConfig.x-this.paletteRect.width-this.canvasOffset.x,n=this.addingNodeConfig.y-this.canvasOffset.y;this.$set(this.addingNodeConfig,"x",t),this.$set(this.addingNodeConfig,"y",n),this.createNode(this.addingNodeConfig)}this.addingNodeConfig={},this.addingNodeRect={},console.info("move end:",e.pageX,e.pageY)},getAddingNodePos:function(e){return{x:e.pageX-this.paletteRect.left-this.addingNodeRect.width/2,y:e.pageY-this.paletteRect.top-this.addingNodeRect.height/2}},onToolClick:function(e){"function"==typeof this[e.type]&&this[e.type](),this.$emit("onToolClick",e)},setZoom:function(e){this.instance.setContainer("canvas-flow");this.$refs.canvasFlow.style.transform="matrix("+e+",0,0,"+e+",0,0)",this.$refs.canvasFlow.style.transformOrigin="0 0",this.$refs.canvasFlow.zoom=e,this.zoom=e,this.instance.setZoom(e)},zoomIn:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1.1;this.setZoom(this.zoom*e)},zoomOut:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:.9;this.setZoom(this.zoom*e)},resetPosition:function(){this.setZoom(1),this.setCanvasPosition(0,0)},setCanvasPosition:function(e,t){this.canvasOffset={x:e,y:t},this.canvasPos={x:e,y:t}},frameSelect:function(){this.isFrameSelecting=!0},frameSelectHandler:function(e){this.mouseDownPos={x:e.pageX-this.canvasRect.left,y:e.pageY-this.canvasRect.top},this.$refs.canvasFlowWrap.addEventListener(this.mousemove,this.frameSelectMovingHandler,!1)},frameSelectMovingHandler:function(e){var t=e.pageX-this.mouseDownPos.x-this.canvasRect.left,n=e.pageY-this.mouseDownPos.y-this.canvasRect.top;this.frameSelectorRect={width:Math.abs(t),height:Math.abs(n)},this.frameSelectorPos={x:t>0?this.mouseDownPos.x:this.mouseDownPos.x+t,y:n>0?this.mouseDownPos.y:this.mouseDownPos.y+n}},frameSelectEndHandler:function(e){this.$refs.canvasFlowWrap.removeEventListener(this.mousemove,this.frameSelectMovingHandler),this.$refs.canvasFlowWrap.removeEventListener(this.mouseup,this.frameSelectEndHandler),document.addEventListener("keydown",this.nodeLineCopyhandler,!1),document.addEventListener("keydown",this.nodeLinePastehandler,!1),document.addEventListener("keydown",this.nodeLineDeletehandler,!1),document.addEventListener(this.mousedown,this.cancelFrameSelectorHandler,{capture:!1,once:!0});var t=this.getSelectedNodes();this.isFrameSelecting=!1,this.frameSelectorPos={x:0,y:0},this.frameSelectorRect={width:0,height:0},console.log(t),this.selectedNodes=t,this.$emit("frameSelectNodes",t.slice(0))},getSelectedNodes:function(){var e=this,t=this.frameSelectorPos,n=t.x,o=t.y,i=this.frameSelectorRect,s=i.width,a=i.height;return this.nodes.filter(function(t){var i=document.querySelector("#".concat(t.id)),r=i.getBoundingClientRect(),c=r.left-e.canvasRect.left,d=r.top-e.canvasRect.top;if(n<c&&n+s>c&&o<d&&o+a>d)return i.classList.add("selected"),!0})},cancelFrameSelectorHandler:function(e){this.selectedNodes.forEach(function(e){var t=document.querySelector("#".concat(e.id));t&&t.classList.remove("selected")}),this.selectedNodes=[]},nodeLineCopyhandler:function(e){(e.ctrlKey||e.metaKey)&&67===e.keyCode&&this.$emit("onNodeCopy",this.selectedNodes)},nodeLinePastehandler:function(e){(e.ctrlKey||e.metaKey)&&86===e.keyCode&&this.$emit("onNodePaste")},nodeLineDeletehandler:function(e){var t=this;46!==e.keyCode&&8!==e.keyCode||(this.selectedNodes.forEach(function(e){t.removeNode(e)}),this.cancelFrameSelectorHandler())}}},void 0,!1,void 0,c,void 0);"undefined"!=typeof window&&"Vue"in window&&window.Vue.component("js-flow",p);export default p;
