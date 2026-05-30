<template>
  <div class="categories-page">
    <h1 class="page-title">分类</h1>
    <div class="categories-nav">
      <button
        v-for="(posts, name) in categories"
        :key="name"
        :class="['category-btn', { active: activeCategory === name }]"
        @click="activeCategory = name"
      >
        {{ name }} ({{ posts.length }})
      </button>
    </div>
    <div class="category-content" v-if="activeCategory && categories[activeCategory]">
      <h2>{{ activeCategory }}</h2>
      <ul class="post-list">
        <li v-for="post in categories[activeCategory]" :key="post.path" class="post-item">
          <span class="post-date">{{ post.date }}</span>
          <RouterLink :to="post.path" class="post-title">{{ post.title }}</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vuepress/client'
import { usePosts } from '../composables'

const { categories } = usePosts()
const route = useRoute()
const activeCategory = ref('')

onMounted(() => {
  const query = route.query
  if (query.category) {
    activeCategory.value = decodeURIComponent(query.category as string)
  } else {
    const keys = Object.keys(categories.value)
    if (keys.length) {
      activeCategory.value = keys[0]
    }
  }
})

watch(
  () => route.query.category,
  (val) => {
    if (val) {
      activeCategory.value = decodeURIComponent(val as string)
    }
  }
)
</script>

<style lang="scss" scoped>
.categories-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;

  .page-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .categories-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 2rem;

    .category-btn {
      padding: 0.4rem 1rem;
      border: 1px solid var(--c-border);
      border-radius: 1.5rem;
      background: var(--c-bg);
      color: var(--c-text-lighter);
      cursor: pointer;
      transition: all 0.2s;

      &:hover,
      &.active {
        background: var(--c-brand);
        color: #fff;
        border-color: var(--c-brand);
      }
    }
  }

  .category-content {
    h2 {
      font-size: 1.3rem;
      color: var(--c-brand);
      margin-bottom: 1rem;
    }
  }

  .post-list {
    list-style: none;
    padding: 0;

    .post-item {
      display: flex;
      align-items: baseline;
      padding: 0.6rem 0;
      border-bottom: 1px dashed var(--c-border);

      .post-date {
        font-family: monospace;
        color: var(--c-text-lightest);
        margin-right: 1rem;
        font-size: 0.85rem;
      }

      .post-title {
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
