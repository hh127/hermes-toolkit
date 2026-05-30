<template>
  <div class="tags-page">
    <h1 class="page-title">标签</h1>
    <div class="tags-cloud">
      <button
        v-for="(posts, name) in tags"
        :key="name"
        :class="['tag-btn', { active: activeTag === name }]"
        @click="activeTag = name"
      >
        {{ name }} ({{ posts.length }})
      </button>
    </div>
    <div class="tag-content" v-if="activeTag && tags[activeTag]">
      <h2>{{ activeTag }}</h2>
      <ul class="post-list">
        <li v-for="post in tags[activeTag]" :key="post.path" class="post-item">
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

const { tags } = usePosts()
const route = useRoute()
const activeTag = ref('')

onMounted(() => {
  const query = route.query
  if (query.tag) {
    activeTag.value = decodeURIComponent(query.tag as string)
  } else {
    const keys = Object.keys(tags.value)
    if (keys.length) {
      activeTag.value = keys[0]
    }
  }
})

watch(
  () => route.query.tag,
  (val) => {
    if (val) {
      activeTag.value = decodeURIComponent(val as string)
    }
  }
)
</script>

<style lang="scss" scoped>
.tags-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;

  .page-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .tags-cloud {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 2rem;

    .tag-btn {
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

  .tag-content {
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
