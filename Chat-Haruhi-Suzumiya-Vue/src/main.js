import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import store from './store/index';
import 'font-awesome/css/font-awesome.min.css'

/*
封装请求方法,供全局调用
 */
import {postKeyValueRequest} from "./utils/api";
import {postRequest} from "./utils/api";
import {getRequest} from "./utils/api";
import {putRequest} from "./utils/api";
import {deleteRequest} from "./utils/api";

Vue.prototype.postKeyValueRequest=postKeyValueRequest;
Vue.prototype.postRequest=postRequest;
Vue.prototype.getRequest=getRequest;
Vue.prototype.putRequest=putRequest;
Vue.prototype.deleteRequest=deleteRequest;

/*路由前置守卫
to：去哪，from：从哪来，调用next()：通过本次路由请求*/
router.beforeEach((to,from,next)=>{
  if (to.path=="/"||to.path=="/adminlogin"){//首页不需要请求菜单
    next();
  }else if (to.path=="/home"&&!window.sessionStorage.getItem('admin')) {
    ElementUI.Message.error({message:"不具有访问权限！"});
    next(from)
  }
  else{
    if (window.sessionStorage.getItem('user')||window.sessionStorage.getItem('admin')){   //登录后才请求菜单
      next();
    }else {//没登录就跳转到登陆页
      //如果先前写了请求路径（to中路径）则记录下来
      ElementUI.Message.error({message:"请登录后访问！"});
      next('/?redirect='+to.path);
    }
  }
})

Vue.config.productionTip = false
Vue.use(ElementUI);

new Vue({
  router,
  store,//这里需要注意
  render: h => h(App)
}).$mount('#app')
