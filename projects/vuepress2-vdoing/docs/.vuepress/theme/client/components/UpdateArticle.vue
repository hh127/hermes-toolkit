<template>
  <div class="update-article" v-if="posts.length">
    <div class="update-header">
      <span class="update-icon">📝</span>
      <span class="update-title">最近更新</span>
    </div>
    <ul class="update-list">
      <li v-for="post in recentPosts" :key="post.path" class="update-item">
        <RouterLink :to="post.path">{{ post.title }}</RouterLink>
        <span class="update-date">{{ post.date }}</span>
      </li>
    </ul>
    <RouterLink to="/archives/" class="more-link">查看更多 &raquo;</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePosts } from '../composables'

const { posts } = usePosts()

const recentPosts = computed(() => posts.value.slice(0, 5))
</script>

<style lang="scss" scoped>
.update-article {
  padding: 1rem 0;
  border-top: 1px solid var(--c-border);

  .update-header {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;

    .update-icon {
      margin-right: 0.5rem;
    }

    .update-title {
      font-size: 1rem;
      font-weight: 600;
      color: var(--c-text);
    }
  }

  .update-list {
    list-style: none;
    padding: 0;
    margin: 0;

    .update-item {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding: 0.3rem 0;

      a {
        color: var(--c-text-lighter);
        text-decoration: none;
        font-size: 0.9rem;

        &:hover {
          color: var(--c-brand);
        }
      }

      .update-date {
        font-size: 0.75rem;
        color: var(--c-text-lightest);
        font-family: monospace;
      }
    }
  }

  .more-link {
    display: block;
    text-align: right;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: var(--c-text-lightest);
    text-decoration: none;

    &:hover {
      color: var(--c-brand);
    }
  }
}
</style>
