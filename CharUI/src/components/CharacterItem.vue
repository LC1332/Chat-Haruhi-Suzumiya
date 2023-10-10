<script setup lang="ts">
export interface CharacterItem {
  id: number;
  avatar: string;
  name: string;
  desc: string;
  tags: string[];
  opening: string;
}

const props = defineProps<CharacterItem>();
</script>

<template>
  <div class="card">
    <div class="cover" :style="`background-image: url(${props.avatar})`"></div>
    <span class="title">{{ props.name }}</span>
    <span class="desc">
      {{ props.desc }}
    </span>
    <div class="tags">
      <el-tag
        v-for="tag in props.tags"
        :key="tag"
        effect="plain"
        size="small"
        color="#ffffff00"
        :hit="true"
        round
      >
        {{ tag }}
      </el-tag>
    </div>
  </div>
</template>

<style scoped>
.card {
  --at-apply: flex flex-col w-full p-3px p-b-10px transition-all;
}

.card:hover {
  --at-apply: bg-dark-1;
  border-radius: 10px;
}

.cover {
  width: 100%;
  padding-top: 100%; /* 设置纵横比为1:1 */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  border-radius: 10px;
}

.title {
  --at-apply: w-full grid-self-center truncate text-base tracking-wide
    text-white subpixel-antialiased text-shadow-md p-t-0.7rem p-x-5px;
}

.desc {
  --at-apply: w-full grid-self-center h-3rem text-xs text-gray-4
    subpixel-antialiased text-shadow-md p-t-1rem p-x-5px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.tags {
  --at-apply: p-t-0.7rem p-x-5px;
}
</style>
