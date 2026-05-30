<template>
  <div class="categories-bar card-box">
    <h4 class="title">分类</h4>
    <div class="categories" ref="categoriesRef">
      <RouterLink
        :to="`/categories/?category=${encodeURIComponent(item.name)}`"
        class="category-item"
        :class="{ active: item.name === category }"
        v-for="(item, index) in displayData"
        :key="index"
      >
        <span class="name">{{ item.name }}</span>
        <span class="count">{{ item.length }}</span>
      </RouterLink>
    </div>
    <RouterLink
      v-if="categoriesData.length > length"
      to="/categories/"
      class="more"
    >查看更多</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'

const props = withDefaults(defineProps<{
  categoriesData: any[]
  category?: string
  length?: number
}>(), {
  category: '',
  length: 10
})

const categoriesRef = ref<HTMLElement | null>(null)

const displayData = computed(() => {
  return props.categoriesData.slice(0, props.length)
})

onMounted(() => {
  // 滚动条定位到当前分类
  if (props.category && categoriesRef.value) {
    const activeEl = categoriesRef.value.querySelector('.active')
    if (activeEl) {
      setTimeout(() => {
        activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 300)
    }
  }
})
</script>

<style lang="scss">
.categories-bar {
  padding: 1.5rem;
  margin-bottom: 1rem;

  .title {
    margin: 0 0 1rem;
    font-size: 1.1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accentColor);
  }

  .categories {
    max-height: 300px;
    overflow-y: auto;

    .category-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 0.8rem;
      color: var(--textColor);
      text-decoration: none;
      border-radius: 4px;
      transition: all 0.2s;

      &:hover,
      &.active {
        background: var(--accentColor);
        color: #fff;
      }

      .name {
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .count {
        min-width: 1.5rem;
        text-align: center;
        font-size: 0.85rem;
        opacity: 0.8;
      }
    }

    &::-webkit-scrollbar-track-piece {
      background-color: rgba(0, 0, 0, 0.05);
    }

    &::-webkit-scrollbar-thumb:vertical {
      background-color: rgba(0, 0, 0, 0.15);
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
