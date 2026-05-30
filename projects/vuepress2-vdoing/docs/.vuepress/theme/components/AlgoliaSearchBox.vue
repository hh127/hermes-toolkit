<template>
  <div class="algolia-search-box">
    <input
      class="algolia-search-input"
      :placeholder="placeholder"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  options: any
}>()

const placeholder = computed(() => {
  return props.options.placeholder || '搜索...'
})
</script>

<style lang="scss">
.algolia-search-box {
  margin-right: 1rem;

  .algolia-search-input {
    width: 200px;
    padding: 0.5rem 1rem;
    border: 1px solid var(--borderColor);
    border-radius: 4px;
    font-size: 0.9rem;
    background: var(--mainBg);
    color: var(--textColor);
    outline: none;
    transition: all 0.2s;

    &:focus {
      border-color: var(--accentColor);
      box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.1);
    }

    &::placeholder {
      color: var(--textColor);
      opacity: 0.5;
    }
  }
}
</style>
