<script setup lang="ts">
import IconSearch from "~icons/ph/magnifying-glass-light";
import IconAdd from "~icons/clarity/plus-line";
import IconClear from "~icons/material-symbols/cancel";
import { useGlobalStore } from "../stores/global";

const globalStore = useGlobalStore();

const newSession = (): void => {
  globalStore.openMask = true;
};
</script>

<template>
  <div class="content">
    <a-input
      v-model:value="globalStore.keyword"
      placeholder="搜索"
      class="session-search"
      allow-clear
    >
      <template #prefix>
        <IconSearch class="icon-search" />
      </template>
      <template #clearIcon>
        <div class="flex flex-items-center">
          <IconClear class="icon-clear" />
        </div>
      </template>
    </a-input>
    <a-button class="button-search" @click="newSession">
      <template #icon>
        <IconAdd class="icon-add" />
      </template>
    </a-button>
  </div>
</template>

<style scoped>
.content {
  --at-apply: flex items-center p-1rem bg-dark-2;
}

.session-search:hover {
  border-color: rgb(52, 211, 153);
}

.button-search:hover {
  border-color: rgb(52, 211, 153);
}

.icon-add {
  --at-apply: text-base text-gray-4;
}

.icon-search {
  --at-apply: text-base text-gray-4;
}

.icon-clear {
  --at-apply: text-base text-gray-2;
}

.button-search {
  --at-apply: ml-0.5rem flex flex-none items-center justify-center border-dark
    bg-dark;
}
</style>

<style>
.session-search {
  --at-apply: bg-dark border-dark;
}

.session-search input {
  --at-apply: bg-dark placeholder-gray-4 text-gray-2 caret-blue;
}
</style>
