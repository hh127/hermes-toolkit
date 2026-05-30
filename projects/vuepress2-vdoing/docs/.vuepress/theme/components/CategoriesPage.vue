<template>
  <div class="custom-page categories-page">
    <MainLayout>
      <template #mainLeft>
        <CategoriesBar
          v-if="categoriesAndTagsData.categories.length"
          :categoriesData="categoriesAndTagsData.categories"
          :category="category"
        />
        <PostList
          :currentPage="currentPage"
          :perPage="perPage"
          :category="category"
          :posts="sortPostsData"
        />
        <Pagination
          :total="total"
          :perPage="perPage"
          :currentPage="currentPage"
          @getCurrentPage="handlePagination"
          v-show="Math.ceil(total / perPage) > 1"
        />
      </template>
      <template #mainRight>
        <CategoriesBar
          v-if="categoriesAndTagsData.categories.length"
          :categoriesData="categoriesAndTagsData.categories"
          :category="category"
        />
      </template>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vuepress/client'
import { usePosts } from '../composables/usePosts'

import MainLayout from './MainLayout.vue'
import PostList from './PostList.vue'
import Pagination from './Pagination.vue'
import CategoriesBar from './CategoriesBar.vue'

const route = useRoute()

// 使用文章数据 composable
const { sortPosts: sortPostsData, groupPosts: groupPostsData, categoriesAndTags: categoriesAndTagsData } = usePosts()

const category = ref('')
const perPage = ref(10)
const currentPage = ref(1)

const total = computed(() => {
  if (category.value && groupPostsData.value.categories[category.value]) {
    return groupPostsData.value.categories[category.value].length
  }
  return sortPostsData.value.length
})

const handlePagination = (i: number) => {
  currentPage.value = i
}

watch(
  () => route.query.category,
  (newCategory) => {
    category.value = newCategory ? decodeURIComponent(newCategory as string) : ''
    currentPage.value = 1
  }
)

onMounted(() => {
  const queryCategory = route.query.category
  if (queryCategory) {
    category.value = decodeURIComponent(queryCategory as string)
  }
  if (route.query.p) {
    currentPage.value = Number(route.query.p)
  }
})
</script>

<style lang="scss">
.categories-page {
  .categories-wrapper {
    position: sticky;
    top: calc(var(--navbar-height) + 0.9rem);
    max-height: calc(100vh - 10rem);
    min-height: 4.2rem;

    @media (max-width: 719px) {
      display: none;
    }

    .categories {
      max-height: calc(100vh - 14rem);
      min-height: 2.2rem;
      overflow-y: auto;
      transition: all 0.2s;
      position: relative;

      a {
        padding-right: 1.8rem;

        span {
          right: 0.4rem;
        }
      }

      &::-webkit-scrollbar-track-piece {
        background-color: rgba(0, 0, 0, 0.05);
      }

      &::-webkit-scrollbar-thumb:vertical {
        background-color: rgba(0, 0, 0, 0.15);
      }

      &:hover {
        &::-webkit-scrollbar-track-piece {
          background-color: rgba(0, 0, 0, 0.1);
        }

        &::-webkit-scrollbar-thumb:vertical {
          background-color: rgba(0, 0, 0, 0.25);
        }
      }
    }
  }

  .main-left {
    .categories-wrapper {
      position: relative;
      top: 0;
      padding: 0.9rem 1.5rem;
      margin-bottom: 0.9rem;
      max-height: 15rem;
      border-radius: 0;
      display: none;

      @media (max-width: 719px) {
        display: block;
      }

      .categories {
        max-height: 12.3rem;
      }
    }
  }
}
</style>
