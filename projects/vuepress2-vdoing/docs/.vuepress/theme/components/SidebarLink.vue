<template>
  <RouterLink
    v-if="item.path"
    :to="item.path"
    class="sidebar-link"
    :class="{ active: isActive }"
  >
    <img
      v-if="titleBadgeSrc"
      :src="titleBadgeSrc"
      class="title-badge"
    />
    {{ item.title }}
    <span
      v-if="item.titleTag"
      class="title-tag"
    >{{ item.titleTag }}</span>
  </RouterLink>
  <a
    v-else-if="item.link"
    :href="item.link"
    class="sidebar-link external"
    target="_blank"
    rel="noopener noreferrer"
  >
    {{ item.title }}
    <OutboundLink />
  </a>
  <span v-else class="sidebar-link">
    {{ item.title }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vuepress/client'

const props = withDefaults(defineProps<{
  item: any
  sidebarDepth?: number
}>(), {
  sidebarDepth: 1
})

const route = useRoute()

const isActive = computed(() => {
  if (props.item.path) {
    return route.path === props.item.path
  }
  return false
})

const titleBadgeSrc = computed(() => {
  // 根据文件类型显示不同的徽章
  const { titleTag } = props.item
  if (titleTag) {
    return null
  }
  return null
})
</script>

<style lang="scss">
.sidebar-link {
  font-size: 0.95em;
  padding: 0.25rem 1.5rem 0.25rem 1.25rem;
  display: block;
  color: var(--textColor);
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.2s;

  &:hover {
    color: var(--accentColor);
    border-left-color: var(--accentColor);
  }

  &.active {
    color: var(--accentColor);
    border-left-color: var(--accentColor);
    font-weight: 600;
  }

  &.external {
    &:hover {
      color: var(--accentColor);
    }
  }

  .title-badge {
    max-width: 1.4rem;
    max-height: 1.4rem;
    vertical-align: middle;
    margin-right: 0.3rem;
    margin-bottom: 0.1rem;
  }

  .title-tag {
    height: 1.2rem;
    line-height: 1.2rem;
    border: 1px solid var(--accentColor);
    color: var(--accentColor);
    font-size: 0.75rem;
    padding: 0 0.3rem;
    border-radius: 0.2rem;
    margin-left: 0.3rem;
    transform: translate(0, -0.15rem);
    display: inline-block;
  }
}
</style>
