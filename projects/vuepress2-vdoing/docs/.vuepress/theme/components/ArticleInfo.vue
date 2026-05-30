<template>
  <div class="article-info card-box" v-if="frontmatter.article !== false">
    <div class="info-item" v-if="frontmatter.date">
      <span class="iconfont icon-riqi" />
      <span class="label">创建时间：</span>
      <span class="value">{{ frontmatter.date.split(' ')[0] }}</span>
    </div>
    <div class="info-item" v-if="frontmatter.categories && frontmatter.categories.length">
      <span class="iconfont icon-wenjian" />
      <span class="label">分类：</span>
      <span class="value">
        <RouterLink
          :to="`/categories/?category=${encodeURIComponent(c)}`"
          v-for="(c, index) in frontmatter.categories"
          :key="index"
        >{{ c }}</RouterLink>
      </span>
    </div>
    <div class="info-item" v-if="frontmatter.tags && frontmatter.tags[0]">
      <span class="iconfont icon-biaoqian" />
      <span class="label">标签：</span>
      <span class="value">
        <RouterLink
          :to="`/tags/?tag=${encodeURIComponent(t)}`"
          v-for="(t, index) in frontmatter.tags"
          :key="index"
        >{{ t }}</RouterLink>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { usePageFrontmatter } from 'vuepress/client'

const frontmatter = usePageFrontmatter()
</script>

<style lang="scss">
.article-info {
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;

  .info-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.3rem;

    &:last-child {
      margin-bottom: 0;
    }

    .iconfont {
      margin-right: 0.5rem;
      color: var(--accentColor);
    }

    .label {
      color: var(--textColor);
      opacity: 0.7;
      margin-right: 0.5rem;
    }

    .value {
      color: var(--textColor);

      a {
        color: var(--accentColor);
        text-decoration: none;
        margin-right: 0.5rem;

        &:hover {
          color: var(--accentColorDark);
        }
      }
    }
  }
}
</style>
