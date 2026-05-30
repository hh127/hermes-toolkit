<template>
  <div class="update-article card-box" v-if="posts.length">
    <h4 class="title">最近更新</h4>
    <div class="article-list">
      <div
        class="article-item"
        v-for="(item, index) in displayPosts"
        :key="index"
      >
        <span class="date">{{ item.date }}</span>
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
import { computed, ref, onMounted } from 'vue'
import { useSiteData } from 'vuepress/client'

const props = withDefaults(defineProps<{
  length?: number
  moreArticle?: string
}>(), {
  length: 5,
  moreArticle: ''
})

const site = useSiteData()

const posts = ref<any[]>([])

const displayPosts = computed(() => {
  return posts.value.slice(0, props.length)
})

onMounted(() => {
  // 需要从实际数据获取最近更新的文章
  posts.value = []
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
