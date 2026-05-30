<template>
  <div class="article-info" v-if="isArticle">
    <div class="info-item" v-if="author">
      <span class="info-label">作者：</span>
      <a v-if="author.link" :href="author.link" target="_blank">{{ author.name }}</a>
      <span v-else>{{ author.name }}</span>
    </div>
    <div class="info-item" v-if="frontmatter.date">
      <span class="info-label">发表于：</span>
      <span>{{ frontmatter.date }}</span>
    </div>
    <div class="info-item" v-if="lastUpdated">
      <span class="info-label">最后更新：</span>
      <span>{{ lastUpdated }}</span>
    </div>
    <div class="info-item" v-if="categories.length">
      <span class="info-label">分类：</span>
      <RouterLink
        v-for="cat in categories"
        :key="cat"
        :to="`/categories/?category=${encodeURIComponent(cat)}`"
        class="info-link"
      >{{ cat }}</RouterLink>
    </div>
    <div class="info-item" v-if="tags.length">
      <span class="info-label">标签：</span>
      <RouterLink
        v-for="tag in tags"
        :key="tag"
        :to="`/tags/?tag=${encodeURIComponent(tag)}`"
        class="info-link tag"
      >#{{ tag }}</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePageData, usePageFrontmatter } from 'vuepress/client'
import { useThemeData } from '../composables'

const page = usePageData()
const frontmatter = usePageFrontmatter()
const themeData = useThemeData()

const isArticle = computed(() => {
  const fm = frontmatter.value as any
  return !fm.home && !fm.pageComponent
})

const author = computed(() => {
  const fm = frontmatter.value as any
  return fm.author || themeData.value.author
})

const lastUpdated = computed(() => {
  return (page.value as any).git?.updatedTime
    ? new Date((page.value as any).git.updatedTime).toLocaleString('zh-CN')
    : ''
})

const categories = computed(() => {
  return (frontmatter.value as any).categories || []
})

const tags = computed(() => {
  return (frontmatter.value as any).tags || []
})
</script>

<style lang="scss" scoped>
.article-info {
  padding: 1rem 0;
  border-bottom: 1px solid var(--c-border);
  margin-bottom: 1.5rem;
  font-size: 0.85rem;
  color: var(--c-text-lighter);

  .info-item {
    margin-bottom: 0.3rem;

    .info-label {
      color: var(--c-text-lightest);
    }

    .info-link {
      color: var(--c-text-lighter);
      text-decoration: none;
      margin-right: 0.5rem;

      &:hover {
        color: var(--c-brand);
      }

      &.tag {
        color: var(--c-text-lightest);

        &:hover {
          color: var(--c-brand);
        }
      }
    }
  }
}
</style>
