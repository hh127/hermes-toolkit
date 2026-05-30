<template>
  <div class="archives-page">
    <h1 class="page-title">归档</h1>
    <p class="archive-stats">共 {{ posts.length }} 篇文章</p>
    <div v-for="(yearPosts, year) in archives" :key="year" class="archive-year">
      <h2 class="year-title">{{ year }} <span class="year-count">({{ yearPosts.length }})</span></h2>
      <ul class="archive-list">
        <li v-for="post in yearPosts" :key="post.path" class="archive-item">
          <span class="archive-date">{{ post.date.substring(5) }}</span>
          <RouterLink :to="post.path" class="archive-title">{{ post.title }}</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePosts } from '../composables'

const { posts, archives } = usePosts()
</script>

<style lang="scss" scoped>
.archives-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;

  .page-title {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: var(--c-text);
  }

  .archive-stats {
    color: var(--c-text-lightest);
    margin-bottom: 2rem;
  }

  .archive-year {
    margin-bottom: 2rem;

    .year-title {
      font-size: 1.5rem;
      color: var(--c-brand);
      border-bottom: 2px solid var(--c-brand);
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;

      .year-count {
        font-size: 1rem;
        color: var(--c-text-lightest);
      }
    }
  }

  .archive-list {
    list-style: none;
    padding: 0;

    .archive-item {
      display: flex;
      align-items: baseline;
      padding: 0.5rem 0;
      border-bottom: 1px dashed var(--c-border);

      .archive-date {
        font-family: monospace;
        color: var(--c-text-lighter);
        margin-right: 1rem;
        min-width: 3rem;
      }

      .archive-title {
        color: var(--c-text);
        text-decoration: none;

        &:hover {
          color: var(--c-brand);
        }
      }
    }
  }
}
</style>
