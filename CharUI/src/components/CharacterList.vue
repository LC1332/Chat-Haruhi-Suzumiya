<script setup lang="ts">
import { getCharacterList } from "../api/chat";
import { useSessionListStore } from "../stores/sessionList";
import { useActiveSessionStore } from "../stores/activeSession";
import { useGlobalStore } from "../stores/global";

// 获取角色列表
const characterList = getCharacterList();

// 会话
const sessionListStore = useSessionListStore();
// 全局
const globalStore = useGlobalStore();
// 当前选中的 会话
const activeSessionStore = useActiveSessionStore();

// 选中角色
const select = (character: CharacterItem): void => {
  // 创建会话对象
  const session: SessionItem = {
    // 随机字符串 ID
    id: Math.random().toString(36).substr(2),
    name: character.name,
    avatar: character.avatar,
    messageList: [
      {
        id: Date.now(),
        avatar: character.avatar,
        message: character.opening,
        time: new Date(),
        isFromMe: false,
      },
    ],
  };
  // 加入会话列表
  globalStore.openMask = false;
  sessionListStore.addSession(session);
  activeSessionStore.sessionId = session.id;
  activeSessionStore.$patch({
    sessionId: session.id,
    sessionTitle: session.name,
    messageList: session.messageList,
  });
};
</script>

<template>
  <div class="modal">
    <div class="title">新的聊天</div>
    <div class="body">
      <CharacterItem
        v-for="character in characterList"
        :key="character.id"
        v-bind="character"
        @click="select(character)"
      />
    </div>
  </div>
</template>

<style scoped>
.modal {
  --at-apply: bg-dark-3 border-solid border-1 border-gray-6 rounded-2xl;
  --at-apply: p-t-1rem p-l-28px p-b-4rem shadow-xs shadow-gray-500 p-r-20px;
}

.title {
  --at-apply: font-bold text-gray-1 font-size-1.1em m-b-1rem;
}

.body {
  --at-apply: grid gap-0.5rem h-full overflow-y-auto overflow-x-hidden;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  grid-auto-rows: min-content;
}
</style>
