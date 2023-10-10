<template>
  <RouterView />
</template>

<style>
/* FireFox */
* {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Chrome、Edge 和 Safari */
*::-webkit-scrollbar {
  width: 8px;
}

/* 滚动条轨道 */
*::-webkit-scrollbar-track {
  border-radius: 8px;
}

/* 滚动条滑块 */
*::-webkit-scrollbar-thumb {
  border-radius: 8px;
  background-color: rgba(64, 64, 64, 0);
}

/* 鼠标悬停在滚动容器上时显示滚动条 */
*:hover::-webkit-scrollbar-thumb {
  background-color: rgb(64, 64, 64);
}

/* 滚动条滑块悬停时的样式 */
*::-webkit-scrollbar-thumb:hover {
  background-color: rgb(72, 72, 72);
}
</style>
