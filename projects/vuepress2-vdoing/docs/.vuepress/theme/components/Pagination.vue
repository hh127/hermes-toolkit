<template>
  <div class="pagination" v-show="totalPages > 1">
    <div class="pagination-list">
      <span
        class="pagination-item"
        :class="{ disabled: currentPage === 1 }"
        @click="handleClick(currentPage - 1)"
      >&lt;</span>
      <span
        class="pagination-item"
        :class="{ active: item === currentPage }"
        v-for="item in displayPages"
        :key="item"
        @click="handleClick(item)"
      >{{ item }}</span>
      <span
        class="pagination-item"
        :class="{ disabled: currentPage === totalPages }"
        @click="handleClick(currentPage + 1)"
      >&gt;</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  total: number
  perPage: number
  currentPage: number
}>()

const emit = defineEmits(['getCurrentPage'])

const totalPages = computed(() => {
  return Math.ceil(props.total / props.perPage)
})

const displayPages = computed(() => {
  const pages: number[] = []
  const maxDisplay = 5
  let start = Math.max(1, props.currentPage - Math.floor(maxDisplay / 2))
  let end = Math.min(totalPages.value, start + maxDisplay - 1)

  if (end - start + 1 < maxDisplay) {
    start = Math.max(1, end - maxDisplay + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

const handleClick = (page: number) => {
  if (page < 1 || page > totalPages.value) return
  emit('getCurrentPage', page)
}
</script>

<style lang="scss">
.pagination {
  margin-top: 1.5rem;
  text-align: center;

  .pagination-list {
    display: inline-flex;
    gap: 0.5rem;
  }

  .pagination-item {
    display: inline-block;
    min-width: 2rem;
    height: 2rem;
    line-height: 2rem;
    text-align: center;
    border: 1px solid var(--borderColor);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;

    &:hover:not(.disabled):not(.active) {
      border-color: var(--accentColor);
      color: var(--accentColor);
    }

    &.active {
      background: var(--accentColor);
      border-color: var(--accentColor);
      color: #fff;
    }

    &.disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}
</style>
