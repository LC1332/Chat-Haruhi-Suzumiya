<script setup lang="ts">
import { type MessageItem } from "./MessageItem.vue";

// ======================== props ========================
export interface SessionItem {
  id: string;
  name: string;
  avatar: string;
  messageList: MessageItem[];
}
interface IsActive {
  active: boolean;
}
const props = defineProps<SessionItem & IsActive>();
</script>

<template>
  <div class="session" :class="{ active: props.active }">
    <el-avatar :size="56" :src="props.avatar" class="avatar" />
    <span class="session-name">
      {{ props.name }}
    </span>
    <span class="session-message">
      {{
        props.messageList &&
        (props.messageList[props.messageList.length - 1]?.message ?? "")
      }}
    </span>
  </div>
</template>

<style scoped>
.session {
  --at-apply: w-full p-10px rounded-lg;
  display: grid;
  grid-template-columns: 64px auto;
  grid-template-rows: 28px 28px;
}

.session.active {
  background-image: linear-gradient(
    to right top,
    rgb(52, 211, 153),
    rgb(59, 130, 246)
  );
}

.session-name {
  --at-apply: grid-self-center truncate text-base tracking-wide text-white
    subpixel-antialiased text-shadow-md;
}

.session-message {
  --at-apply: grid-self-center truncate text-sm text-gray-4 subpixel-antialiased
    text-shadow-md;
}

.session.active .session-message {
  --at-apply: text-gray-2;
}

.avatar {
  grid-row-start: span 2;
  --at-apply: shadow-md;
}
</style>
