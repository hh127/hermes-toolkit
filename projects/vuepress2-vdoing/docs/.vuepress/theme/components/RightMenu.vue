<template>
  <div class="right-menu-wrapper" :class="{ show: showMenu }">
    <div class="right-menu-title">
      <span>目录</span>
      <span class="arrow" @click="toggleMenu" />
    </div>
    <div class="right-menu-content" v-show="showMenu">
      <ul class="menu-list">
        <li
          class="menu-item"
          :class="{ active: item.active }"
          :style="{ paddingLeft: (item.level - 1) * 0.8 + 'rem' }"
          v-for="(item, index) in headers"
          :key="index"
          @click="scrollToHeader(item.slug)"
        >
          {{ item.title }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePageData } from 'vuepress/client'

const page = usePageData()
const showMenu = ref(true)

const headers = computed(() => {
  const { headers } = page.value
  if (!headers) return []

  const result: any[] = []
  const addHeaders = (items: any[], level: number) => {
    for (const item of items) {
      result.push({
        title: item.title,
        slug: item.slug || item.id,
        level: level,
        active: false
      })
      if (item.children) {
        addHeaders(item.children, level + 1)
      }
    }
  }

  addHeaders(headers, 1)
  return result
})

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const scrollToHeader = (slug: string) => {
  const el = document.getElementById(slug)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

// 监听滚动，高亮当前标题
let scrollTimer: number | null = null
const handleScroll = () => {
  if (scrollTimer) return
  scrollTimer = window.setTimeout(() => {
    const scrollTop = window.scrollY
    const offset = 100

    for (let i = headers.value.length - 1; i >= 0; i--) {
      const item = headers.value[i]
      const el = document.getElementById(item.slug)
      if (el && el.offsetTop - offset <= scrollTop) {
        headers.value.forEach((h: any) => h.active = false)
        item.active = true
        break
      }
    }

    scrollTimer = null
  }, 100)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss">
.right-menu-wrapper {
  position: fixed;
  top: calc(var(--navbar-height) + 1.5rem);
  right: 2rem;
  width: 200px;
  z-index: 5;
  transition: all 0.3s;

  .right-menu-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.8rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--textColor);
    border-bottom: 1px solid var(--borderColor);

    .arrow {
      cursor: pointer;
      width: 0;
      height: 0;
      border: 6px solid transparent;
      border-top-color: var(--textColor);

      &.collapsed {
        border-top-color: transparent;
        border-bottom-color: var(--textColor);
      }
    }
  }

  .right-menu-content {
    max-height: calc(100vh - 15rem);
    overflow-y: auto;
    padding: 0.5rem 0;

    .menu-list {
      list-style: none;
      padding: 0;
      margin: 0;

      .menu-item {
        padding: 0.3rem 0.8rem;
        font-size: 0.85rem;
        color: var(--textColor);
        cursor: pointer;
        transition: all 0.2s;
        border-left: 3px solid transparent;

        &:hover {
          color: var(--accentColor);
        }

        &.active {
          color: var(--accentColor);
          border-left-color: var(--accentColor);
          font-weight: 600;
        }
      }
    }

    &::-webkit-scrollbar-track-piece {
      background-color: rgba(0, 0, 0, 0.05);
    }

    &::-webkit-scrollbar-thumb:vertical {
      background-color: rgba(0, 0, 0, 0.15);
    }
  }
}

@media (max-width: 1279px) {
  .right-menu-wrapper {
    display: none;
  }
}
</style>
