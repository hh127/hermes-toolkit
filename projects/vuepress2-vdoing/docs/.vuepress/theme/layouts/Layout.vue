<template>
  <div
    class="theme-container"
    :class="pageClasses"
    @touchstart="onTouchStart"
    @touchend="onTouchEnd"
  >
    <Navbar v-if="shouldShowNavbar" @toggle-sidebar="toggleSidebar" />

    <div class="sidebar-mask" @click="toggleSidebar(false)" />

    <div
      v-if="themeConfig.sidebarHoverTriggerOpen !== false"
      class="sidebar-hover-trigger"
    />

    <Sidebar
      :items="sidebarItems"
      @toggle-sidebar="toggleSidebar"
      v-show="isSidebarOpen"
    >
      <template #top>
        <div
          v-if="sidebarSlotTop"
          class="sidebar-slot sidebar-slot-top"
          v-html="sidebarSlotTop"
        />
      </template>
      <template #bottom>
        <div
          v-if="sidebarSlotBottom"
          class="sidebar-slot sidebar-slot-bottom"
          v-html="sidebarSlotBottom"
        />
      </template>
    </Sidebar>

    <!-- 首页 -->
    <Home v-if="frontmatter.home" />

    <!-- 分类页 -->
    <CategoriesPage v-else-if="frontmatter.categoriesPage" />

    <!-- 标签页 -->
    <TagsPage v-else-if="frontmatter.tagsPage" />

    <!-- 归档页 -->
    <ArchivesPage v-else-if="frontmatter.archivesPage" />

    <!-- 文章页或其他页 -->
    <Page v-else :sidebar-items="sidebarItems">
      <template #top>
        <div v-if="pageSlotTop" class="page-slot page-slot-top" v-html="pageSlotTop" />
      </template>
      <template #bottom>
        <div v-if="pageSlotBottom" class="page-slot page-slot-bottom" v-html="pageSlotBottom" />
      </template>
    </Page>

    <Footer />

    <Buttons ref="buttonsRef" @toggle-theme-mode="toggleThemeMode" />

    <BodyBgImg v-if="themeConfig.bodyBgImg" />

    <!-- 自定义html插入左右下角的小窗口 -->
    <div
      class="custom-html-window custom-html-window-lb"
      v-if="windowLB"
      v-show="showWindowLB"
    >
      <div class="custom-wrapper">
        <span class="close-but" @click="showWindowLB = false">×</span>
        <div v-html="windowLB" />
      </div>
    </div>
    <div
      class="custom-html-window custom-html-window-rb"
      v-if="windowRB"
      v-show="showWindowRB"
    >
      <div class="custom-wrapper">
        <span class="close-but" @click="showWindowRB = false">×</span>
        <div v-html="windowRB" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { usePageData, usePageFrontmatter, useSiteData, useRoute, useRouter } from 'vuepress/client'

import storage from '../utils/storage'

import Home from '../components/Home.vue'
import Navbar from '../components/Navbar.vue'
import Page from '../components/Page.vue'
import CategoriesPage from '../components/CategoriesPage.vue'
import TagsPage from '../components/TagsPage.vue'
import ArchivesPage from '../components/ArchivesPage.vue'
import Sidebar from '../components/Sidebar.vue'
import Buttons from '../components/Buttons.vue'
import Footer from '../components/Footer.vue'
import BodyBgImg from '../components/BodyBgImg.vue'
import { resolveSidebarItems } from '../utils/index'

const MOBILE_DESKTOP_BREAKPOINT = 719
const NAVBAR_HEIGHT = 58

// 响应式状态
const hideNavbar = ref(false)
const isSidebarOpen = ref(true)
const themeMode = ref('auto')
const showWindowLB = ref(true)
const showWindowRB = ref(true)
const buttonsRef = ref(null)

// 获取 VuePress 数据
const page = usePageData()
const frontmatter = usePageFrontmatter()
const site = useSiteData()
const route = useRoute()
const router = useRouter()

// 主题配置
const themeConfig = computed(() => site.value?.themeConfig || {})

// 侧边栏数据
const sidebarItems = computed(() => {
  return resolveSidebarItems(
    page.value,
    page.value.path,
    site.value,
    '/'
  )
})

// 侧边栏插槽
const sidebarSlotTop = computed(() => {
  const { htmlModules } = themeConfig.value
  return htmlModules ? htmlModules.sidebarT : ''
})

const sidebarSlotBottom = computed(() => {
  const { htmlModules } = themeConfig.value
  return htmlModules ? htmlModules.sidebarB : ''
})

// 页面插槽
const pageSlotTop = computed(() => {
  const { htmlModules } = themeConfig.value
  return htmlModules ? htmlModules.pageT : ''
})

const pageSlotBottom = computed(() => {
  const { htmlModules } = themeConfig.value
  return htmlModules ? htmlModules.pageB : ''
})

// 自定义窗口
const windowLB = computed(() => {
  const { htmlModules } = themeConfig.value
  return htmlModules ? htmlModules.windowLB : ''
})

const windowRB = computed(() => {
  const { htmlModules } = themeConfig.value
  return htmlModules ? htmlModules.windowRB : ''
})

// 是否显示导航栏
const shouldShowNavbar = computed(() => {
  const { frontmatter: fm } = page.value
  if (fm.navbar === false || themeConfig.value.navbar === false) {
    return false
  }
  return (
    page.value.title ||
    themeConfig.value.logo ||
    themeConfig.value.repo ||
    themeConfig.value.nav
  )
})

// 是否显示侧边栏
const shouldShowSidebar = computed(() => {
  const { frontmatter: fm } = page.value
  return (
    !fm.home &&
    fm.sidebar !== false &&
    sidebarItems.value.length &&
    fm.showSidebar !== false
  )
})

// 页面样式类
const pageClasses = computed(() => {
  const userPageClass = frontmatter.value.pageClass
  return [
    {
      'no-navbar': !shouldShowNavbar.value,
      'hide-navbar': hideNavbar.value,
      'sidebar-open': isSidebarOpen.value,
      'no-sidebar': !shouldShowSidebar.value,
      'have-rightmenu': showRightMenu.value,
      'theme-mode-dark': themeMode.value === 'dark',
      'theme-mode-light': themeMode.value === 'light',
      'theme-style-line': themeConfig.value.themeStyle === 'line',
      'only-sidebarItem': sidebarItems.value.length === 1,
    },
    userPageClass,
  ]
})

// 是否显示右侧菜单
const showRightMenu = computed(() => {
  const { headers } = page.value
  return (
    !frontmatter.value.home &&
    themeConfig.value.rightMenuBar !== false &&
    headers &&
    headers.length &&
    frontmatter.value.sidebar !== false
  )
})

// 切换侧边栏
const toggleSidebar = (to?: boolean) => {
  isSidebarOpen.value = typeof to === 'boolean' ? to : !isSidebarOpen.value
}

// 切换主题模式
const toggleThemeMode = (mode: string) => {
  themeMode.value = mode
  storage.set('themeMode', mode)
}

// 触摸事件
let touchStart = { x: 0, y: 0 }
const onTouchStart = (e: TouchEvent) => {
  touchStart = {
    x: e.changedTouches[0].clientX,
    y: e.changedTouches[0].clientY,
  }
}

const onTouchEnd = (e: TouchEvent) => {
  const dx = e.changedTouches[0].clientX - touchStart.x
  const dy = e.changedTouches[0].clientY - touchStart.y
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 40) {
    if (dx > 0 && touchStart.x <= 80) {
      toggleSidebar(true)
    } else {
      toggleSidebar(false)
    }
  }
}

// 滚动事件 - 隐藏导航栏
let lastScrollTop = 0
const handleScroll = () => {
  const scrollTop = document.documentElement.scrollTop || document.body.scrollTop
  hideNavbar.value = scrollTop > NAVBAR_HEIGHT && scrollTop > lastScrollTop
  lastScrollTop = scrollTop
}

// 初始化主题模式
onMounted(() => {
  const savedMode = storage.get('themeMode', 'auto')
  themeMode.value = savedMode

  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// 监听路由变化
watch(
  () => route.path,
  () => {
    isSidebarOpen.value = false
  }
)
</script>
