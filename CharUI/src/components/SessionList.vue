<script setup lang="ts">
import { useSessionListStore } from "../stores/sessionList";
import { useActiveSessionStore } from "../stores/activeSession";
import { useGlobalStore } from "../stores/global";
import { type SessionItem as Session } from "./SessionItem.vue";

const sessionListStore = useSessionListStore();
const activeSessionStore = useActiveSessionStore();
const globalStore = useGlobalStore();
const select = (session: Session): void => {
  activeSessionStore.sessionId = session.id;
  activeSessionStore.$patch({
    sessionId: session.id,
    sessionTitle: session.name,
    messageList: session.messageList,
  });
};
</script>

<template>
  <ul class="infinite-list scroll-container" style="overflow: auto">
    <SessionItem
      v-for="session in sessionListStore.sessionList"
      v-show="session.name.includes(globalStore.keyword)"
      :key="session.id"
      :active="session.id === activeSessionStore.sessionId"
      v-bind="session"
      @click="select(session)"
    />
  </ul>
</template>

<style scoped>
.infinite-list {
  --at-apply: h-full p-x-10px p-b-1rem;
  --at-apply: bg-dark-2;
}

.infinite-list .infinite-list-item + .list-item {
  margin-top: 10px;
}
</style>
