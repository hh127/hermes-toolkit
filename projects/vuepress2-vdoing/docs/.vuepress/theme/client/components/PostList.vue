<template>
  <div class="post-list">
    <article v-for="post in displayPosts" :key="post.path" class="post-item">
      <div class="post-meta">
        <span class="post-date" v-if="post.date">
          <span class="meta-icon">📅</span> {{ post.date }}
        </span>
        <span class="post-categories" v-if="post.frontmatter.categories">
          <span class="meta-icon">📂</span>
          <RouterLink
            v-for="cat in post.frontmatter.categories"
            :key="cat"
            :to="`/categories/?category=${encodeURIComponent(cat)}`"
          >{{ cat }}</RouterLink>
        </span>
      </div>
      <h2 class="post-title">
        <RouterLink :to="post.path">{{ post.title }}</RouterLink>
      </h2>
      <p class="post-excerpt" v-if="post.excerpt" v-html="post.excerpt"></p>
      <div class="post-tags" v-if="post.frontmatter.tags?.length">
        <RouterLink
          v-for="tag in post.frontmatter.tags"
          :key="tag"
          :to="`/tags/?tag=${encodeURIComponent(tag)}`"
          class="tag-link"
        >#{{ tag }}</RouterLink>
      </div>
    </article>
    <Pagination
      v-if="totalPages > 1"
      :current="currentPage"
      :total="totalPages"
      @update:current="currentPage = $event"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Pagination from './Pagination.vue'

const props = defineProps<{
  posts: any[]
  pageSize?: number
}>()

const currentPage = ref(1)
const pageSize = computed(() => props.pageSize || 10)

const totalPages = computed(() => Math.ceil(props.posts.length / pageSize.value))

const displayPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return props.posts.slice(start, start + pageSize.value)
})
</script>

<style lang="scss" scoped>
.post-list {
  .post-item {
    padding: 1.5rem 0;
    border-bottom: 1px solid var(--c-border);

    &:last-child {
      border-bottom: none;
    }
  }

  .post-meta {
    font-size: 0.85rem;
    color: var(--c-text-lightest);
    margin-bottom: 0.5rem;

    .meta-icon {
      margin-right: 0.25rem;
    }

    a {
      color: var(--c-text-lighter);
      text-decoration: none;

      &:hover {
        color: var(--c-brand);
      }
    }
  }

  .post-title {
    font-size: 1.3rem;
    margin: 0.5rem 0;

    a {
      color: var(--c-text);
      text-decoration: none;

      &:hover {
        color: var(--c-brand);
      }
    }
  }

  .post-excerpt {
    color: var(--c-text-lighter);
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0.5rem 0;
  }

  .post-tags {
    margin-top: 0.5rem;

    .tag-link {
      display: inline-block;
      margin-right: 0.5rem;
      font-size: 0.8rem;
      color: var(--c-text-lightest);
      text-decoration: none;

      &:hover {
        color: var(--c-brand);
      }
    }
  }
}
</style>
