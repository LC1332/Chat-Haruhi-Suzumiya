<script setup lang="ts">
import { useActiveSessionStore } from "../stores/activeSession";
import { useGlobalStore } from "../stores/global";
import { type MessageItem } from "./MessageItem.vue";

const globalStore = useGlobalStore();
const activeSessionStore = useActiveSessionStore();

const message = ref<string>("");

const sendMessage = (event: KeyboardEvent): void => {
  // 如果按下了 shift, 不触发
  if (event.shiftKey) {
    return;
  }
  // 否则，如按下 Enter，阻止换行
  event.preventDefault();

  // TODO: 发送消息
  const messageItem = createMessageItem(message.value);
  activeSessionStore.addMessage(messageItem);

  // 清空输入框
  message.value = "";
};

const createMessageItem = (message: string): MessageItem => {
  return {
    id: Date.now(),
    avatar: globalStore.selfAvatar,
    message,
    time: new Date(),
    isFromMe: true,
  };
};
</script>

<template>
  <div class="border-0 border-t-.5 border-gray-7 border-solid p-.5rem p-t-1rem">
    <a-textarea
      v-model:value="message"
      :bordered="false"
      class="max-h-full font-size-1em tracking-wide text-white subpixel-antialiased min-h-full! resize-none!"
      @press-enter="sendMessage"
    />
  </div>
</template>

<style scoped></style>
