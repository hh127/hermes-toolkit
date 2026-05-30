<template>
  <div class="vdoing-theme" :class="pageClasses">
    <Navbar v-if="showNavbar" @toggle-sidebar="toggleSidebar" />

    <div class="sidebar-mask" @click="toggleSidebar(false)" />

    <Sidebar :items="sidebarItems" @close-sidebar="toggleSidebar(false)">
      <template #top>
        <slot name="sidebar-top" />
      </template>
      <template #bottom>
        <BloggerBar v-if="showBlogger" />
        <CategoriesBar />
        <TagsBar />
        <slot name="sidebar-bottom" />
      </template>
    </Sidebar>

    <main class="page">
      <div class="theme-default-content">
        <slot name="page-top" />
        <Content />
        <ArticleInfo />
        <slot name="page-bottom" />
        <UpdateArticle />
      </div>
    </main>

    <RightMenu />
    <BodyBgImg v-if="bodyBgImg" />
    <Buttons />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, provide } from 'vue'
import { usePageData, usePageFrontmatter, useSiteData, useRoute } from 'vuepress/client'
import { useThemeData } from '../composables'
import Navbar from '../components/Navbar.vue'
import Sidebar from '../components/Sidebar.vue'
import BloggerBar from '../components/BloggerBar.vue'
import CategoriesBar from '../components/CategoriesBar.vue'
import TagsBar from '../components/TagsBar.vue'
import UpdateArticle from '../components/UpdateArticle.vue'
import ArticleInfo from '../components/ArticleInfo.vue'
import RightMenu from '../components/RightMenu.vue'
import BodyBgImg from '../components/BodyBgImg.vue'
import Buttons from '../components/Buttons.vue'

const themeData = useThemeData()
const page = usePageData()
const frontmatter = usePageFrontmatter()
const site = useSiteData()
const route = useRoute()

const isSidebarOpen = ref(false)

const showNavbar = computed(() => {
  const fm = frontmatter.value as any
  return fm.navbar !== false
})

const showBlogger = computed(() => !!themeData.value.blogger)
const bodyBgImg = computed(() => themeData.value.bodyBgImg)

const sidebarItems = computed(() => {
  // 侧边栏配置
  const sidebar = themeData.value.sidebar
  if (sidebar === 'auto') {
    return []
  }
  return sidebar || []
})

const pageClasses = computed(() => {
  const classes: string[] = []
  const fm = frontmatter.value as any

  if (fm.pageComponent) {
    classes.push('page-component')
  }

  if (isSidebarOpen.value) {
    classes.push('sidebar-open')
  }

  return classes
})

function toggleSidebar(to?: boolean) {
  isSidebarOpen.value = typeof to === 'boolean' ? to : !isSidebarOpen.value
}

provide('toggleSidebar', toggleSidebar)
</script>

<style lang="scss">
@import '../styles/index.scss';
</style>
