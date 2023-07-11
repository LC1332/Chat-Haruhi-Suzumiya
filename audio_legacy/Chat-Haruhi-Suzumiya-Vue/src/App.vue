<template>
    <div id="app">
        <router-view/>
    </div>
</template>

<script>
    export default {
        name: 'App',
        mounted() {
            setTimeout(() => {
                window.L2Dwidget.init({
                    pluginRootPath: '../live2dw/',
                    pluginJsPath: 'lib/',
                    pluginModelPath: 'live2d-widget-model-haru_2/assets/', //中间这个haru_2就是你的老婆,想换个老婆,换这个就可以了
                    tagMode: false,
                    debug: false,
                    model: {jsonPath: '../live2dw/live2d-widget-model-haru_2/assets/haru02.model.json'},
                    display: {position: 'right', width: 400, height: 900},  //调整大小,和位置
                    mobile: {show: true},   //要不要盯着你的鼠标看
                    log: false,
                })
            }, 1)
        }
    }
</script>
