import { defineStore } from "pinia";
import { ref } from "vue";
import type { SessionItem } from "../components/SessionItem.vue";

export const useSessionListStore = defineStore("sessionList", () => {
  // ===================== State =====================
  const sessionList = ref<SessionItem[]>([]);

  // ===================== Action =====================
  // 增加一个会话
  function addSession(session: SessionItem): void {
    sessionList.value.push(session);
  }

  // 删除一个会话
  function deleteSession(sessionId: string): void {
    const index = sessionList.value.findIndex(
      (session) => session.id === sessionId
    );
    if (index !== -1) {
      sessionList.value.splice(index, 1);
    }
  }

  return { sessionList, addSession, deleteSession };
});
