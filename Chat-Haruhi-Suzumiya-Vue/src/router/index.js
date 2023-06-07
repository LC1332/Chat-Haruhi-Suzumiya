import Vue from 'vue'
import VueRouter from 'vue-router'
import ChatRoom from '../views/chat/ChatRoom'

Vue.use(VueRouter)

const routes = [
    {
        path: '/chatroom',
        name: 'ChatRoom',
        component: ChatRoom,
        hidden: true
    }

    // {
    //   path: '/about',
    //   name: 'About',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    // }
];
//解决重复访问路由地址报错
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
};

const router = new VueRouter({
    routes
});

export default router
