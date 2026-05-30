<template>
  <ul class="sidebar-links" v-if="items.length">
    <li v-for="(item, index) in items" :key="index">
      <SidebarGroup
        v-if="item.type === 'group'"
        :item="item"
        :open="index === openGroupIndex"
        :depth="depth"
        @toggle="toggleGroup(index)"
      />
      <SidebarLink
        v-else
        :item="item"
        :sidebarDepth="sidebarDepth"
      />
    </li>
  </ul>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vuepress/client'

import SidebarGroup from './SidebarGroup.vue'
import SidebarLink from './SidebarLink.vue'

const props = withDefaults(defineProps<{
  items: any[]
  depth?: number
  sidebarDepth?: number
}>(), {
  depth: 0,
  sidebarDepth: 1
})

const route = useRoute()
const openGroupIndex = ref(0)

const toggleGroup = (index: number) => {
  openGroupIndex.value = index === openGroupIndex.value ? -1 : index
}

// 根据当前路由路径找到对应的分组
const resolveOpenGroupIndex = (items: any[], route: any) => {
  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.type === 'group' && item.children) {
      for (const child of item.children) {
        if (child.path && route.path.startsWith(child.path)) {
          return i
        }
      }
    }
  }
  return 0
}

watch(
  () => route.path,
  () => {
    openGroupIndex.value = resolveOpenGroupIndex(props.items, route)
  },
  { immediate: true }
)
</script>

<style lang="scss">
.sidebar-links {
  padding: 0;
  margin: 0;
  list-style-type: none;
}
</style>
