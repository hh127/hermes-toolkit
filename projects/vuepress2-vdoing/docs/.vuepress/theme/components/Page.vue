<template>
  <div>
    <main class="page">
      <div :class="`theme-vdoing-wrapper ${bgStyle}`">
        <ArticleInfo v-if="isArticle" />
        <div v-else class="placeholder" />

        <div class="content-wrapper">
          <RightMenu v-if="showRightMenu" />

          <h1 v-if="showTitle">
            <img
              v-if="titleBadgeSrc"
              :src="titleBadgeSrc"
            />{{ page.title }}<span
              class="title-tag"
              v-if="frontmatter.titleTag"
            >{{ frontmatter.titleTag }}</span>
          </h1>

          <slot name="top" />

          <Content class="theme-vdoing-content" />
        </div>

        <slot name="bottom" />
        <PageEdit />
        <PageNav v-bind="{ sidebarItems }" />
      </div>

      <UpdateArticle
        :length="3"
        v-if="isShowUpdateBar"
      />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePageData, usePageFrontmatter, useSiteData } from 'vuepress/client'

import PageEdit from './PageEdit.vue'
import PageNav from './PageNav.vue'
import ArticleInfo from './ArticleInfo.vue'
import UpdateArticle from './UpdateArticle.vue'
import RightMenu from './RightMenu.vue'

const props = defineProps<{
  sidebarItems: any[]
}>()

const page = usePageData()
const frontmatter = usePageFrontmatter()
const site = useSiteData()

const themeConfig = computed(() => site.value?.themeConfig || {})

const bgStyle = computed(() => {
  const { contentBgStyle } = themeConfig.value
  return contentBgStyle ? 'bg-style-' + contentBgStyle : ''
})

const isShowUpdateBar = computed(() => {
  const { updateBar } = themeConfig.value
  return updateBar && updateBar.showToArticle === false ? false : true
})

const showTitle = computed(() => {
  return !frontmatter.value.pageComponent
})

const showRightMenu = computed(() => {
  const { headers } = page.value
  return (
    themeConfig.value.rightMenuBar !== false &&
    headers &&
    headers.length &&
    frontmatter.value.sidebar !== false
  )
})

const isArticle = computed(() => {
  return frontmatter.value.article !== false
})

const titleBadgeSrc = computed(() => {
  if (themeConfig.value.titleBadge === false) return null
  return null
})
</script>

<style lang="scss">
.page {
  padding-bottom: 2rem;
  display: block;

  @media (max-width: 719px) {
    padding-top: var(--navbar-height);
  }

  @media (min-width: 720px) {
    padding-top: calc(var(--navbar-height) + 1.5rem);
  }
}

.theme-vdoing-wrapper {
  .content-wrapper {
    position: relative;
  }

  h1 {
    .title-tag {
      height: 1.5rem;
      line-height: 1.5rem;
      border: 1px solid var(--accentColor);
      color: var(--accentColor);
      font-size: 1rem;
      padding: 0 0.4rem;
      border-radius: 0.2rem;
      margin-left: 0.5rem;
      transform: translate(0, -0.25rem);
      display: inline-block;
    }

    img {
      margin-bottom: -0.2rem;
      margin-right: 0.2rem;
      max-width: 2.2rem;
      max-height: 2.2rem;
    }
  }

  --linesColor: rgba(50, 0, 0, 0.05);

  &.bg-style-1 {
    background-image: linear-gradient(90deg, var(--linesColor) 3%, transparent 3%), linear-gradient(0deg, var(--linesColor) 3%, transparent 3%);
    background-position: center center;
    background-size: 20px 20px;
  }

  &.bg-style-2 {
    background-image: repeating-linear-gradient(0, var(--linesColor) 0, var(--linesColor) 1px, transparent 0, transparent 50%);
    background-size: 30px 30px;
  }

  &.bg-style-3 {
    background-image: repeating-linear-gradient(90deg, var(--linesColor) 0, var(--linesColor) 1px, transparent 0, transparent 50%);
    background-size: 30px 30px;
  }

  &.bg-style-4 {
    background-image: repeating-linear-gradient(-45deg, var(--linesColor) 0, var(--linesColor) 1px, transparent 0, transparent 50%);
    background-size: 20px 20px;
  }

  &.bg-style-5 {
    background-image: repeating-linear-gradient(45deg, var(--linesColor) 0, var(--linesColor) 1px, transparent 0, transparent 50%);
    background-size: 20px 20px;
  }

  &.bg-style-6 {
    background-image: radial-gradient(var(--linesColor) 1px, transparent 1px);
    background-size: 10px 10px;
  }
}

.theme-mode-dark .theme-vdoing-wrapper {
  --linesColor: rgba(125, 125, 125, 0.05);
}
</style>
