import { ref } from "vue";
import { defineStore } from "pinia";
import type { MessageItem } from "../components/MessageItem.vue";

export const useActiveSessionStore = defineStore("activeSession", () => {
  // ===================== State =====================
  const sessionId = ref("");
  const sessionTitle = ref("");
  const messageList = ref<MessageItem[]>([]);

  // ===================== Action =====================
  // 增加一条消息
  function addMessage(message: MessageItem): void {
    if (sessionTitle.value === "") {
      return;
    }
    messageList.value.push(message);
  }

  // 清空
  function clear(): void {
    sessionId.value = "";
    sessionTitle.value = "";
    messageList.value = [];
  }

  return { sessionId, sessionTitle, messageList, addMessage, clear };
});
