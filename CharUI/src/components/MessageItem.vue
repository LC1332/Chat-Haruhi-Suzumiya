<script setup lang="ts">
export interface MessageItem {
  id: number;
  avatar: string;
  message: string;
  time: Date;
  isFromMe: boolean;
}

const props = defineProps<MessageItem>();
</script>

<template>
  <div class="chat-bubble-container" :class="isFromMe ? 'right' : 'left'">
    <template v-if="!isFromMe">
      <img class="avatar" :src="props.avatar" />
      <div class="w-6px"></div>
    </template>
    <div class="chat-bubble">
      {{ props.message }}
    </div>
    <template v-if="isFromMe">
      <div class="w-6px"></div>
      <img class="avatar" :src="props.avatar" />
    </template>
  </div>
</template>

<style scoped>
:host {
  display: block;
}

.chat-bubble-container {
  display: flex;
  width: 100%;
  margin: 12px 0;
  align-items: flex-start;
  --at-apply: subpixel-antialiased text-base tracking-wide;
}

.chat-bubble-container.left {
  flex-direction: row;
}

.chat-bubble-container.left .avatar {
  margin-right: 5px;
}

.chat-bubble {
  white-space: pre-wrap;
  position: relative;
  max-width: 60%;
  padding: 10px;
  border-radius: 7px;
  font-size: 14px;
  --at-apply: bg-dark-1 text-white;
}

.chat-bubble-container.left .chat-bubble::before {
  content: "";
  position: absolute;
  left: -5px;
  top: 10px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 5px 7px 5px 0;
  border-color: transparent rgba(60, 60, 60, var(--un-bg-opacity)) transparent
    transparent;
}

.chat-bubble-container.right {
  justify-content: flex-end;
}

.chat-bubble-container.right .avatar {
  margin-left: 5px;
}

.chat-bubble-container.right .chat-bubble {
  background-image: linear-gradient(
    to right top,
    rgb(52, 211, 153),
    rgb(59, 130, 246)
  );
  --at-apply: text-white;
}

.chat-bubble-container.right .chat-bubble::before {
  content: "";
  position: absolute;
  right: -5px;
  top: 10px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 5px 0 5px 7px;
  border-color: transparent transparent transparent rgb(59, 130, 246);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
