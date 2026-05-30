<template>
  <div class="tags-bar sidebar-section" v-if="Object.keys(tags).length">
    <h3 class="sidebar-heading">标签</h3>
    <div class="tags-cloud">
      <RouterLink
        v-for="(posts, name) in tags"
        :key="name"
        :to="`/tags/?tag=${encodeURIComponent(name)}`"
        class="tag-item"
        :style="{ fontSize: getFontSize(posts.length) }"
      >
        {{ name }}
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePosts } from '../composables'

const { tags } = usePosts()

function getFontSize(count: number) {
  const size = 0.75 + Math.min(count * 0.1, 0.5)
  return `${size}rem`
}
</script>

<style lang="scss" scoped>
.tags-bar {
  padding: 0.5rem 0;

  .tags-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    padding: 0.25rem 0;
  }

  .tag-item {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    background: var(--c-bg-lighter);
    border-radius: 0.75rem;
    color: var(--c-text-lighter);
    transition: all 0.2s;

    &:hover {
      background: var(--c-brand);
      color: #fff;
      text-decoration: none;
    }
  }
}
</style>
