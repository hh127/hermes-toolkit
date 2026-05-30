<template>
  <div class="custom-page archives-page">
    <MainLayout>
      <template #mainLeft>
        <div class="archives card-box">
          <div class="year-list" v-if="archivesData.length">
            <div
              class="year"
              v-for="(yearItem, index) in archivesData"
              :key="index"
            >
              <h2>{{ yearItem.year }}</h2>
              <div class="post-list">
                <div
                  class="post"
                  v-for="(post, idx) in yearItem.posts"
                  :key="idx"
                >
                  <span class="date">{{ post.date }}</span>
                  <RouterLink
                    :to="post.path"
                    class="title"
                  >{{ post.title }}</RouterLink>
                  <span
                    class="title-tag"
                    v-if="post.titleTag"
                  >{{ post.titleTag }}</span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty">暂无文章</div>
        </div>
      </template>
      <template #mainRight>
        <BloggerBar v-if="themeConfig.blogger" />
        <CategoriesBar
          v-if="themeConfig.category !== false && categoriesAndTagsData.categories.length"
          :categoriesData="categoriesAndTagsData.categories"
          :length="10"
        />
        <TagsBar
          v-if="themeConfig.tag !== false && categoriesAndTagsData.tags.length"
          :tagsData="categoriesAndTagsData.tags"
          :length="30"
        />
      </template>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSiteData } from 'vuepress/client'
import { usePosts } from '../composables/usePosts'

import MainLayout from './MainLayout.vue'
import BloggerBar from './BloggerBar.vue'
import CategoriesBar from './CategoriesBar.vue'
import TagsBar from './TagsBar.vue'

const site = useSiteData()
const themeConfig = computed(() => site.value?.themeConfig || {})

// 使用文章数据 composable
const { sortPosts: sortPostsData, categoriesAndTags: categoriesAndTagsData } = usePosts()

// 按年份分组归档数据
const archivesData = computed(() => {
  const yearMap: Record<string, any[]> = {}

  sortPostsData.value.forEach(post => {
    const date = post.frontmatter?.date
    if (!date) return

    const year = date.split('-')[0]
    if (!yearMap[year]) {
      yearMap[year] = []
    }
    yearMap[year].push({
      title: post.title,
      path: post.path,
      date: date.split(' ')[0],
      titleTag: post.frontmatter?.titleTag
    })
  })

  // 按年份倒序
  return Object.keys(yearMap)
    .sort((a, b) => Number(b) - Number(a))
    .map(year => ({
      year,
      posts: yearMap[year]
    }))
})
</script>

<style lang="scss">
.archives-page {
  .archives {
    padding: 1.5rem;

    .empty {
      text-align: center;
      color: var(--textColor);
      opacity: 0.5;
      padding: 2rem;
    }

    .year-list {
      .year {
        margin-bottom: 2rem;

        h2 {
          font-size: 1.5rem;
          margin: 0 0 1rem;
          padding-bottom: 0.5rem;
          border-bottom: 2px solid var(--accentColor);
        }

        .post-list {
          .post {
            padding: 0.5rem 0;
            display: flex;
            align-items: center;

            .date {
              font-size: 0.85rem;
              color: var(--textColor);
              opacity: 0.6;
              margin-right: 1rem;
              min-width: 5rem;
            }

            .title {
              color: var(--textColor);
              text-decoration: none;
              flex: 1;

              &:hover {
                color: var(--accentColor);
              }
            }

            .title-tag {
              height: 1.2rem;
              line-height: 1.2rem;
              border: 1px solid var(--accentColor);
              color: var(--accentColor);
              font-size: 0.75rem;
              padding: 0 0.3rem;
              border-radius: 0.2rem;
              margin-left: 0.5rem;
            }
          }
        }
      }
    }
  }
}
</style>
