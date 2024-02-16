<script setup lang="ts">
import { getSessionList } from "../api/chat";
import { useSessionListStore } from "../stores/sessionList";
import { useGlobalStore } from "../stores/global";

const globalStore = useGlobalStore();
globalStore.selfAvatar = "https://avatars.githubusercontent.com/u/499270?v=4";

// 获取会话列表
const sessionListStore = useSessionListStore();
sessionListStore.sessionList = getSessionList();

// 关闭遮罩层
const closeMaskByKeyBoard = (event: KeyboardEvent): void => {
  if (event.key === "Escape") {
    globalStore.openMask = false;
  }
};

// 关闭遮罩层
const closeMaskByClick = (event: PointerEvent): void => {
  globalStore.openMask = false;
};

// 全局监听 ESC 按键事件
window.addEventListener("keyup", closeMaskByKeyBoard);
</script>

<template>
  <div class="chat-view">
    <Transition name="mask">
      <div
        v-show="globalStore.openMask"
        class="chat-mask"
        @click="closeMaskByClick"
      ></div>
    </Transition>
    <Transition>
      <CharacterList
        v-show="globalStore.openMask"
        class="character-list"
        @keyup.esc="closeMaskByKeyBoard"
      />
    </Transition>
    <div class="chat-window">
      <SessionManage />
      <SessionTitle class="session-title" />
      <SessionList class="session-list" />
      <MessageList />
      <MessageInput />
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  --at-apply: bg-white;
  --at-apply: w-full min-h-screen;
  --at-apply: flex justify-center items-center;
}

.chat-mask {
  --at-apply: bg-dark bg-opacity-50 absolute z-1 backdrop-blur-sm;
  --at-apply: w-full h-full min-w-840px min-h-540px max-w-65% max-h-85% m-y-3rem;
  --at-apply: rounded-xl overflow-hidden;
}

.chat-window {
  --at-apply: bg-dark;
  --at-apply: w-full h-full min-w-840px min-h-540px max-w-65% max-h-85% m-y-3rem;
  --at-apply: rounded-xl overflow-hidden;
  display: grid;
  grid-template-columns: 270px auto;
  grid-template-rows: 60px auto 190px;
  box-shadow:
    0 1px 2px -2px rgb(0 0 0 / 16%),
    0 3px 6px 0 rgb(0 0 0 / 12%),
    0 5px 12px 4px rgb(0 0 0 / 9%);
}

.session-list {
  grid-row-start: span 2;
}

.character-list {
  --at-apply: absolute z-2;
  --at-apply: w-full h-full min-w-540px min-h-340px max-w-50% max-h-60% m-y-3rem;
  --at-apply: rounded-xl overflow-hidden;
}
</style>

<style>
.v-enter-active,
.v-leave-active {
  --at-apply: transition-all duration-300ms ease-in-out;
}

.v-enter-from,
.v-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

.mask-enter-active,
.mask-leave-active {
  --at-apply: transition-all duration-300ms ease-in-out;
}

.mask-enter-from,
.mask-leave-to {
  opacity: 0;
}
</style>
