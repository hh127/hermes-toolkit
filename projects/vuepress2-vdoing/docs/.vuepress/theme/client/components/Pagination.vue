<template>
  <div class="pagination" v-if="total > 1">
    <button
      class="page-btn"
      :disabled="current <= 1"
      @click="emit('update:current', current - 1)"
    >
      &laquo;
    </button>
    <button
      v-for="page in displayPages"
      :key="page"
      :class="['page-btn', { active: page === current }]"
      @click="emit('update:current', page)"
    >
      {{ page }}
    </button>
    <button
      class="page-btn"
      :disabled="current >= total"
      @click="emit('update:current', current + 1)"
    >
      &raquo;
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  current: number
  total: number
}>()

const emit = defineEmits<{
  'update:current': [page: number]
}>()

const displayPages = computed(() => {
  const pages: number[] = []
  const maxShow = 5
  let start = Math.max(1, props.current - Math.floor(maxShow / 2))
  let end = Math.min(props.total, start + maxShow - 1)

  if (end - start + 1 < maxShow) {
    start = Math.max(1, end - maxShow + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>

<style lang="scss" scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin: 2rem 0;

  .page-btn {
    min-width: 2rem;
    height: 2rem;
    padding: 0 0.5rem;
    border: 1px solid var(--c-border);
    border-radius: 4px;
    background: var(--c-bg);
    color: var(--c-text-lighter);
    cursor: pointer;
    transition: all 0.2s;

    &:hover:not(:disabled) {
      border-color: var(--c-brand);
      color: var(--c-brand);
    }

    &.active {
      background: var(--c-brand);
      color: #fff;
      border-color: var(--c-brand);
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}
</style>
