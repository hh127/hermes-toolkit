<template>
  <div>
    <RouterLink
      v-if="item.link"
      :to="item.link"
      class="sidebar-link"
      :class="{ active: isActive }"
    >
      {{ item.text }}
    </RouterLink>
    <span v-else class="sidebar-heading">{{ item.text }}</span>

    <ul v-if="item.children?.length" class="sidebar-group-items">
      <li v-for="child in item.children" :key="child.link || child.text">
        <SidebarLink :item="child" />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vuepress/client'

const props = defineProps<{
  item: any
}>()

const route = useRoute()

const isActive = computed(() => {
  return route.path === props.item.link
})
</script>

<style lang="scss" scoped>
.sidebar-link {
  display: block;
  padding: 0.35rem 1rem 0.35rem 1.25rem;
  font-size: 0.9rem;
  color: var(--c-text-lighter);
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s;

  &:hover {
    color: var(--c-brand);
    text-decoration: none;
  }

  &.active {
    color: var(--c-brand);
    border-left-color: var(--c-brand);
    font-weight: 600;
  }
}

.sidebar-heading {
  display: block;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--c-text);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sidebar-group-items {
  list-style: none;
  padding-left: 0;
  margin: 0;
}
</style>
