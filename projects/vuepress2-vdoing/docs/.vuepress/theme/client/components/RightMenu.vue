<template>
  <div class="right-menu" v-if="headers.length" ref="menuRef">
    <div class="right-menu-title">目录</div>
    <ul class="right-menu-list">
      <li
        v-for="header in headers"
        :key="header.slug"
        :class="[
          'right-menu-item',
          `level-${header.level}`,
          { active: activeSlug === header.slug }
        ]"
      >
        <a :href="`#${header.slug}`" @click.prevent="scrollTo(header.slug)">
          {{ header.title }}
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePageData } from 'vuepress/client'

const page = usePageData()
const activeSlug = ref('')
const menuRef = ref<HTMLElement>()

const headers = computed(() => {
  return (page.value as any).headers || []
})

function scrollTo(slug: string) {
  const el = document.getElementById(slug)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
    activeSlug.value = slug
  }
}

let observer: IntersectionObserver | null = null

onMounted(() => {
  // 监听标题元素的可见性
  const headerEls = headers.value
    .map((h: any) => document.getElementById(h.slug))
    .filter(Boolean)

  if (headerEls.length) {
    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            activeSlug.value = entry.target.id
            break
          }
        }
      },
      { rootMargin: '-80px 0px -80% 0px' }
    )

    headerEls.forEach((el: HTMLElement) => observer!.observe(el))
  }
})

onUnmounted(() => {
  observer?.disconnect()
})
</script>

<style lang="scss" scoped>
.right-menu {
  position: fixed;
  right: 2rem;
  top: 100px;
  width: 200px;
  max-height: calc(100vh - 150px);
  overflow-y: auto;
  font-size: 0.85rem;

  .right-menu-title {
    font-weight: 600;
    color: var(--c-text);
    margin-bottom: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--c-border);
  }

  .right-menu-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .right-menu-item {
    a {
      display: block;
      padding: 0.25rem 0;
      color: var(--c-text-lighter);
      text-decoration: none;
      border-left: 2px solid transparent;
      padding-left: 0.5rem;
      transition: all 0.2s;

      &:hover {
        color: var(--c-brand);
      }
    }

    &.active a {
      color: var(--c-brand);
      border-left-color: var(--c-brand);
    }

    &.level-3 a { padding-left: 1rem; }
    &.level-4 a { padding-left: 1.5rem; }
    &.level-5 a { padding-left: 2rem; }
    &.level-6 a { padding-left: 2.5rem; }
  }
}

@media (max-width: 1300px) {
  .right-menu {
    display: none;
  }
}
</style>
