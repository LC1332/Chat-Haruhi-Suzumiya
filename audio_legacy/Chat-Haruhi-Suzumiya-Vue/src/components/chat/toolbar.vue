<template>
    <div id="toolbar">
        <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
        </div>
        <div id="btnBar">
            <div class="topBtnBar">
                <el-tooltip class="item" effect="dark" content="聊天" placement="right">
                    <el-button @click="chooseChatList('私聊')" class="toolBtn" size="small"><i
                            class="fa fa-address-book-o fa-2x" aria-hidden="true"></i></el-button>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" content="与凉宫春日聊天" placement="right">
                    <el-button @click="chooseChatList('凉宫春日')" class="toolBtn" size="small"><i
                            class="fa fa-android fa-2x" aria-hidden="true"></i></el-button>
                </el-tooltip>
            </div>
            <div class="bottomBtnBar">
                <el-tooltip class="item" effect="dark" content="个人中心" placement="right">
                    <el-button class="toolBtn" size="small"><i class="fa fa-user fa-2x" aria-hidden="true"></i>
                    </el-button>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" content="更多" placement="right">
                    <el-popover
                            placement="right"
                            width="180"
                            trigger="click"
                            popper-class="moreListPopoverClass"
                    >
                        <ul id="moreList">
                            <li @click="showFeedbackDialog">意见反馈</li>
                            <li>举报</li>
                            <li @click="clearChatHistory">清空聊天记录</li>
                        </ul>
                        <el-button slot="reference" class="toolBtn" size="small"><i class="fa fa-bars fa-2x"
                                                                                    aria-hidden="true"></i></el-button>
                    </el-popover>
                </el-tooltip>
                <el-tooltip class="item" effect="dark" content="退出" placement="right">
                    <el-button @click="exitSystem" class="toolBtn" size="small"><i class="fa fa-sign-out fa-2x"
                                                                                   aria-hidden="true"></i></el-button>
                </el-tooltip>
            </div>
        </div>
        <el-dialog title="意见反馈" :visible.sync="feedBackDialogVisible" class="feedbackDialog">
      <textarea class="feedbackInput" v-model="feedBackContent">

      </textarea>
            <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleFeedbackSend">确 定</el-button>
        <el-button @click="feedBackDialogVisible = false">取 消</el-button>
      </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "toolbar",
        data() {
            return {
                user: JSON.parse(window.sessionStorage.getItem('user')),
                feedBackDialogVisible: false,
                feedBackContent: '',
            }
        },
        methods: {
            //退出系统
            exitSystem() {
                this.$confirm('你是否要退出系统吗?', '系统提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.getRequest("/logout");
                    sessionStorage.removeItem("user");
                    //清除SessionStorage中保存的state
                    if (sessionStorage.getItem("state")) {
                        sessionStorage.removeItem("state");
                    }
                    //关闭连接
                    this.$store.dispatch("disconnect");
                    this.$router.replace("/");
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消操作'
                    });
                });
            },
            //选择聊天列表
            chooseChatList(listName) {
                this.$store.commit("changeCurrentList", listName);
            },
            //打开意见反馈对话框
            showFeedbackDialog() {
                this.feedBackContent = '';
                this.feedBackDialogVisible = true;
            },
            //处理反馈消息邮件发送
            handleFeedbackSend() {
                let msgObj = {};
                msgObj.userId = this.user.id;
                msgObj.nickname = this.user.nickname;
                msgObj.username = this.user.username;
                msgObj.content = this.feedBackContent;
                console.log(msgObj)
                this.postRequest("/mail/feedback", msgObj).then(resp => {
                    if (resp) {
                        this.feedBackDialogVisible = false;
                    }
                })
            },
            //清空聊天记录
            clearChatHistory() {
                this.$confirm('此操作将永久删除本地聊天记录(群聊记录会在下次登录时恢复), 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    //清除本地的localStorage中的聊天记录
                    if (localStorage.getItem("chat-session")) {
                        localStorage.removeItem("chat-session");
                    }
                    //清除Vuex中保存的记录
                    this.$store.state.sessionStorage = {};
                    //清除SessionStorage中保存的state
                    if (sessionStorage.getItem("state")) {
                        sessionStorage.removeItem("state");
                    }
                    this.$message({
                        type: 'success',
                        message: '删除成功'
                    });
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            }
        }
    }
</script>

<style lang="scss" scoped>
    #toolbar {
        width: 100%;
        height: 100%;

        #btnBar {
            width: 100%;
            height: 82%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .imgProfile {
            width: 40px;
            height: 40px;
            horiz-align: center;
            margin: 25px 10px;
        }

        .toolBtn {
            background-color: #2e3238;
            border: 0;
            margin: 5px 5px;
        }

        .feedbackDialog {
            width: 1000px;
            height: 800px;
            margin: 10px auto;
            //background-color: #ECEAE8;
        }

        .feedbackInput {
            width: 450px;
            height: 200px;
            resize: none;
            padding: 0;
            margin: 0;
        }
    }


    #moreList {
        margin: 0px;
        padding: 0px;
        background-color: #2e3238;

        li {
            padding-top: 14px;
            padding-bottom: 14px;
            padding-left: 5px;
            //padding-right: 40px;
            //border-bottom: 1px solid #292C33;
            list-style: none;
            cursor: pointer;

            &:hover {
                background-color: #abaaaa;
            }
        }
    }

</style>
<style lang="scss">
    /* el-popover是和app同级的，所以scoped的局部属性设置了无效 */
    /* 需要设置全局style */
    .el-popover.moreListPopoverClass {
        height: 150px;
        width: 150px;
        // margin: 0px;
        margin-left: 10px;
        padding: 0px;
        overflow-x: hidden;
        overflow-y: hidden;
        background-color: #2e3238;
        border: none;
    }
</style>
