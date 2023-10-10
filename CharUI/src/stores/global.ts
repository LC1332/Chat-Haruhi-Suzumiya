import { ref } from "vue";
import { defineStore } from "pinia";

export const useGlobalStore = defineStore("global", () => {
  // ===================== State =====================
  const selfAvatar = ref(""); // 用户头像
  const keyword = ref(""); // 搜索关键词
  const openMask = ref(false); // 是否打开遮罩层

  return { selfAvatar, keyword, openMask };
});
