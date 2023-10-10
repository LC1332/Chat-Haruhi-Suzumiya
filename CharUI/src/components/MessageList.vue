<script setup lang="ts">
import { useActiveSessionStore } from "../stores/activeSession";

const activeSessionStore = useActiveSessionStore();
</script>

<template>
  <ul class="infinite-list" style="overflow: auto">
    <MessageItem
      v-for="message in activeSessionStore.messageList"
      :key="message.id"
      v-bind="message"
    />
  </ul>
</template>

<style scoped>
.infinite-list {
  --at-apply: h-full p-x-10px p-1rem;
}
</style>
