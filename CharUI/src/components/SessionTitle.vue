<script setup lang="ts">
import { useActiveSessionStore } from "../stores/activeSession";
import { useSessionListStore } from "../stores/sessionList";
import { Modal } from "ant-design-vue";

const activeSessionStore = useActiveSessionStore();
const sessionListStore = useSessionListStore();

const deleteSession = (sessionId: string): void => {
  Modal.confirm({
    title: "确认删除会话吗？",
    style: { top: "30vh" },
    okText: "确认",
    cancelText: "取消",
    onOk() {
      activeSessionStore.clear();
      sessionListStore.deleteSession(sessionId);
    },
    onCancel() {},
  });
};
</script>

<template>
  <div
    class="flex items-center justify-between border-0 border-b-.5 border-gray-7 border-solid p-1rem"
  >
    <span class="text-2xl font-medium text-gray-2">
      {{ activeSessionStore.sessionTitle }}
    </span>
    <span
      v-show="activeSessionStore.sessionTitle !== ''"
      class="i-icon-park-outline:delete delete"
      @click="deleteSession(activeSessionStore.sessionId)"
    ></span>
  </div>
</template>

<style scoped>
.delete {
  --at-apply: text-xl font-medium text-gray-3;
  cursor: pointer;
}

.delete:hover {
  --at-apply: text-gray-1;
}
</style>
