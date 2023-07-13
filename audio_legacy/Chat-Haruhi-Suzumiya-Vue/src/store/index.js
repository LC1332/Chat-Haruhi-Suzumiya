import  Vue from 'vue'
import  Vuex from 'vuex'
import {getRequest, postRequest} from "../utils/api";
import SockJS from '../utils/sockjs'
import  '../utils/stomp'
import { Notification } from 'element-ui';

Vue.use(Vuex);

const now = new Date();

const store =  new Vuex.Store({
  state:sessionStorage.getItem('state') ? JSON.parse(sessionStorage.getItem('state')) :{
    routes:[],
    sessions:{},//聊天记录
    users:[],//用户列表
    currentUser:null,//当前登录用户
    currentSession:{username:'群聊',nickname:'群聊'},//当前选中的用户，默认为群聊
    currentList:'群聊',//当前聊天窗口列表
    filterKey:'',
    stomp:null,
    isDot:{},//两用户之间是否有未读信息
    errorImgUrl:"http://39.108.169.57/group1/M00/00/00/J2ypOV7wJkyAAv1fAAANuXp4Wt8303.jpg",//错误提示图片
    shotHistory:{}//拍一拍的记录历史
  },
  mutations:{
    initRoutes(state,data){
      state.routes=data;
    },
    changeCurrentSession (state,currentSession) {
      //切换到当前用户就标识消息已读
      Vue.set(state.isDot,state.currentUser.username+"#"+currentSession.username,false);
      //更新当前选中的用户
      state.currentSession =currentSession;
    },
    //修改当前聊天窗口列表
    changeCurrentList(state,currentList){
      state.currentList=currentList;
    },
    //保存群聊消息记录
    addGroupMessage(state,msg){
      let message=state.sessions['群聊'];
      if (!message){
        //state.sessions[state.currentHr.username+"#"+msg.to]=[];
        Vue.set(state.sessions,'群聊',[]);
      }
      state.sessions['群聊'].push({
        fromId:msg.fromId,
        fromName:msg.fromName,
        fromProfile:msg.fromProfile,
        content:msg.content,
        messageTypeId:msg.messageTypeId,
        createTime: msg.createTime,
      })
    },
    //保存单聊数据
    addMessage (state,msg) {
      let message=state.sessions[state.currentUser.username+"#"+msg.to];
      if (!message){
        //创建保存消息记录的数组
        Vue.set(state.sessions,state.currentUser.username+"#"+msg.to,[]);
      }
      state.sessions[state.currentUser.username+"#"+msg.to].push({
        content:msg.content,
        date: new Date(),
        fromNickname:msg.fromNickname,
        messageTypeId:msg.messageTypeId,
        self:!msg.notSelf
      })
    },
    /**
     *  获取本地聊天记录，同步数据库的记录保存到localStorage中。
     *  不刷新情况下都是读取保存再localStorage中的记录
     * @param state
     * @constructor
     */
    INIT_DATA (state) {
        //同步数据库中的群聊数据
        getRequest("/groupMsgContent/").then(resp=>{
          if (resp){
            Vue.set(state.sessions,'群聊',resp);
          }
        })
    },
    //保存系统所有用户
    INIT_USER(state,data){
      state.users=data;
    },
    //请求并保存所有系统用户
    GET_USERS(state){
      getRequest("/chat/users").then(resp=>{
        if (resp){
          state.users=resp;
        }
      })
    }
  },
  actions:{
    /**
     * 作用：初始化数据
     * action函数接受一个与store实例具有相同方法和属性的context对象
     * @param context
     */
    initData (context) {
      //初始化聊天记录
      context.commit('INIT_DATA')
      //获取用户列表
      context.commit('GET_USERS')
    },
    /**
     * 实现连接服务端连接与消息订阅
     * @param context 与store实例具有相同方法和属性的context对象
     */
    connect(context){
      //连接Stomp站点
      context.state.stomp=Stomp.over(new SockJS('/ws/ep'));
      context.state.stomp.connect({},success=>{
        /**
         * 订阅系统广播通知消息
         */
        context.state.stomp.subscribe("/topic/notification",msg=>{
          //判断是否是系统广播通知
            Notification.info({
              title: '系统消息',
              message: msg.body.substr(5),
              position:"top-right"
            });
            //更新用户列表（的登录状态）
            context.commit('GET_USERS');
        });
        /**
         * 订阅凉宫春日回复消息
         */
        context.state.stomp.subscribe("/user/queue/robot",msg=>{
          //接收到的消息
          let receiveMsg=JSON.parse(msg.body);
          //标记为凉宫春日回复
          receiveMsg.notSelf=true;
          receiveMsg.to='凉宫春日';
          receiveMsg.messageTypeId=1;
          //添加到消息记录保存
          context.commit('addMessage',receiveMsg);
        })
        /**
         * 订阅私人消息
         */
        context.state.stomp.subscribe('/user/queue/chat',msg=>{
          //接收到的消息数据
          let receiveMsg=JSON.parse(msg.body);
          //没有选中用户或选中用户不是发来消息的那一方
          if (!context.state.currentSession||receiveMsg.from!=context.state.currentSession.username){
            Notification.info({
              title:'【'+receiveMsg.fromNickname+'】发来一条消息',
              message:receiveMsg.content.length<8?receiveMsg.content:receiveMsg.content.substring(0,8)+"...",
              position:"bottom-right"
            });
            //默认为消息未读
            Vue.set(context.state.isDot,context.state.currentUser.username+"#"+receiveMsg.from,true);
          }
          //标识这个消息不是自己发的
          receiveMsg.notSelf=true;
          //获取发送方
          receiveMsg.to=receiveMsg.from;
          //提交消息记录
          context.commit('addMessage',receiveMsg);
        })
      },error=>{
        Notification.info({
          title: '系统消息',
          message: "无法与服务端建立连接，请尝试重新登陆系统~",
          position:"top-right"
        });
      })
    },
    //与Websocket服务端断开连接
    disconnect(context){
     if (context.state.stomp!=null) {
       context.state.stomp.disconnect();
       console.log("关闭连接~");
     }
    },
  }
})

/**
 * 监听state.sessions，有变化就重新保存到local Storage中chat-session中
 */
store.watch(function (state) {
  return state.sessions
},function (val) {
  console.log('CHANGE: ', val);
  localStorage.setItem('chat-session', JSON.stringify(val));
},{
  deep:true/*这个貌似是开启watch监测的判断,官方说明也比较模糊*/
});


export default store;
