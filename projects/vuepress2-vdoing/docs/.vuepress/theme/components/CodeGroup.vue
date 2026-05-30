<template>
  <div class="code-group">
    <div class="code-group-nav">
      <div
        class="code-group-nav-item"
        :class="{ active: index === activeIndex }"
        v-for="(item, index) in tabs"
        :key="index"
        @click="activeIndex = index"
      >{{ item }}</div>
    </div>
    <div class="code-group-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, provide } from 'vue'

const slots = defineSlots<{
  default(): any
}>()

const activeIndex = ref(0)

const tabs = computed(() => {
  // 从子组件中提取标签名
  return []
})

provide('codeGroupActiveIndex', activeIndex)
</script>

<style lang="scss">
.code-group {
  margin: 1rem 0;

  .code-group-nav {
    display: flex;
    background: var(--codeBgColor, #282c34);
    border-radius: 6px 6px 0 0;
    padding: 0 0.5rem;
    overflow-x: auto;

    .code-group-nav-item {
      padding: 0.5rem 1rem;
      font-size: 0.85rem;
      color: rgba(255, 255, 255, 0.7);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      white-space: nowrap;
      transition: all 0.2s;

      &:hover {
        color: #fff;
      }

      &.active {
        color: var(--accentColor);
        border-bottom-color: var(--accentColor);
      }
    }
  }

  .code-group-content {
    .code-block-wrapper {
      &:not(:first-child) {
        display: none;
      }
    }
  }
}
</style>
