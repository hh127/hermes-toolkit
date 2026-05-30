<template>
  <div class="update-article card-box" v-if="displayPosts.length">
    <h4 class="title">最近更新</h4>
    <div class="article-list">
      <div
        class="article-item"
        v-for="(item, index) in displayPosts"
        :key="index"
      >
        <span class="date">{{ item.frontmatter?.date?.split(' ')[0] || '' }}</span>
        <RouterLink
          :to="item.path"
          class="title"
        >{{ item.title }}</RouterLink>
      </div>
    </div>
    <RouterLink
      v-if="moreArticle"
      :to="moreArticle"
      class="more"
    >查看更多</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  length?: number
  moreArticle?: string
  posts?: any[]
}>(), {
  length: 5,
  moreArticle: '',
  posts: () => []
})

const displayPosts = computed(() => {
  return (props.posts || []).slice(0, props.length)
})
</script>

<style lang="scss">
.update-article {
  padding: 1.5rem;
  margin-bottom: 1rem;

  .title {
    margin: 0 0 1rem;
    font-size: 1.1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accentColor);
  }

  .article-list {
    .article-item {
      display: flex;
      align-items: baseline;
      padding: 0.4rem 0;

      .date {
        font-size: 0.8rem;
        color: var(--textColor);
        opacity: 0.6;
        margin-right: 1rem;
        min-width: 5rem;
      }

      .title {
        flex: 1;
        font-size: 0.9rem;
        color: var(--textColor);
        text-decoration: none;
        border-bottom: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;

        &:hover {
          color: var(--accentColor);
        }
      }
    }
  }

  .more {
    display: block;
    text-align: center;
    margin-top: 1rem;
    color: var(--accentColor);
    text-decoration: none;
    font-size: 0.9rem;

    &:hover {
      color: var(--accentColorDark);
    }
  }
}
</style>
