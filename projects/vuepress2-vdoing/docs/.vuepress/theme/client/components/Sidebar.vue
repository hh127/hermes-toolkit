<template>
  <aside class="sidebar">
    <slot name="top" />
    <nav class="sidebar-nav">
      <ul class="sidebar-links" v-if="items.length">
        <li v-for="item in items" :key="item.link || item.text">
          <SidebarLink :item="item" />
        </li>
      </ul>
      <p v-else class="sidebar-empty">暂无侧边栏</p>
    </nav>
    <slot name="bottom" />
  </aside>
</template>

<script setup lang="ts">
import SidebarLink from './SidebarLink.vue'

defineProps<{
  items: any[]
}>()

defineEmits<{
  'close-sidebar': []
}>()
</script>

<style lang="scss" scoped>
.sidebar {
  position: fixed;
  z-index: 10;
  top: 3.6rem;
  left: 0;
  bottom: 0;
  width: 220px;
  padding: 1rem 0;
  overflow-y: auto;
  background: var(--c-bg);
  border-right: 1px solid var(--c-border);
  transform: translateX(-100%);
  transition: transform 0.2s ease;

  .sidebar-open & {
    transform: translateX(0);
  }

  @media (min-width: 960px) {
    transform: translateX(0);
  }

  .sidebar-nav {
    padding: 0 0.5rem;
  }

  .sidebar-links {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .sidebar-empty {
    color: var(--c-text-lightest);
    font-size: 0.85rem;
    text-align: center;
    padding: 1rem;
  }
}
</style>
