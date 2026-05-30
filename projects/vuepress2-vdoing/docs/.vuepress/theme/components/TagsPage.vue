<template>
  <div class="custom-page tags-page">
    <MainLayout>
      <template #mainLeft>
        <TagsBar
          v-if="tagsData.length"
          :tagsData="tagsData"
          :tag="tag"
        />
        <PostList
          :currentPage="currentPage"
          :perPage="perPage"
          :tag="tag"
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
        <TagsBar
          v-if="tagsData.length"
          :tagsData="tagsData"
          :tag="tag"
        />
      </template>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vuepress/client'

import MainLayout from './MainLayout.vue'
import PostList from './PostList.vue'
import Pagination from './Pagination.vue'
import TagsBar from './TagsBar.vue'

const route = useRoute()

const tag = ref('')
const total = ref(0)
const perPage = ref(10)
const currentPage = ref(1)

const tagsData = computed(() => {
  // 从页面数据中提取标签
  return []
})

const handlePagination = (i: number) => {
  currentPage.value = i
}

watch(
  () => route.query.tag,
  (newTag) => {
    tag.value = newTag ? decodeURIComponent(newTag as string) : ''
    currentPage.value = 1
  }
)

onMounted(() => {
  const queryTag = route.query.tag
  if (queryTag) {
    tag.value = decodeURIComponent(queryTag as string)
  }
  if (route.query.p) {
    currentPage.value = Number(route.query.p)
  }
})
</script>

<style lang="scss">
.tags-page {
  .tags-wrapper {
    position: sticky;
    top: calc(var(--navbar-height) + 0.9rem);
    max-height: calc(100vh - 10rem);
    min-height: 4.2rem;

    @media (max-width: 719px) {
      display: none;
    }

    .tags {
      max-height: calc(100vh - 14rem);
      min-height: 2.2rem;
      overflow-x: hidden;
      overflow-y: auto;
      transition: all 0.2s;

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
    .tags-wrapper {
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

      .tags {
        max-height: 11.5rem;
      }
    }
  }
}
</style>
