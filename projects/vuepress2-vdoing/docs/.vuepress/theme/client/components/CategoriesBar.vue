<template>
  <div class="categories-bar sidebar-section" v-if="Object.keys(categories).length">
    <h3 class="sidebar-heading">分类</h3>
    <ul class="sidebar-links">
      <li v-for="(posts, name) in categories" :key="name">
        <RouterLink :to="`/categories/?category=${encodeURIComponent(name)}`" class="sidebar-link">
          <span class="category-name">{{ name }}</span>
          <span class="category-count">{{ posts.length }}</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { usePosts } from '../composables'

const { categories } = usePosts()
</script>

<style lang="scss" scoped>
.categories-bar {
  padding: 0.5rem 0;

  .category-name {
    flex: 1;
  }

  .category-count {
    font-size: 0.75rem;
    color: var(--c-text-lightest);
    background: var(--c-bg-lighter);
    padding: 0 0.4rem;
    border-radius: 0.75rem;
    min-width: 1.2rem;
    text-align: center;
  }
}
</style>
