<template>
  <nav class="nav-links" v-if="userLinks.length || repoLink">
    <!-- 用户链接 -->
    <div
      class="nav-item"
      v-for="(item, index) in userLinks"
      :key="index"
    >
      <DropdownLink
        v-if="item.type === 'links'"
        :item="item"
      />
      <RouterLink
        v-else-if="item.link"
        :to="item.link"
        class="nav-link"
        :class="{ active: isLinkActive(item) }"
      >{{ item.text }}</RouterLink>
    </div>

    <!-- 仓库链接 -->
    <a
      v-if="repoLink"
      :href="repoLink"
      class="repo-link"
      target="_blank"
      rel="noopener noreferrer"
    >
      <RepoIcon />
      {{ repoLabel }}
    </a>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSiteData, useRoute } from 'vuepress/client'
import DropdownLink from './DropdownLink.vue'

const site = useSiteData()
const route = useRoute()

const userLinks = computed(() => {
  const { nav } = site.value?.themeConfig || {}
  return (nav || []).map((link: any) => {
    return {
      ...link,
      type: link.items && link.items.length ? 'links' : 'link',
    }
  })
})

const repoLink = computed(() => {
  const { repo } = site.value?.themeConfig || {}
  if (repo) {
    return /^https?:\/\//.test(repo) ? repo : `https://github.com/${repo}`
  }
  return null
})

const repoLabel = computed(() => {
 if (!repoLink.value) return ''
  const { repoLabel } = site.value?.themeConfig || {}
  return repoLabel || 'Source'
})

const isLinkActive = (item: any) => {
  if (item.link) {
    return route.path === item.link
  }
  return false
}
</script>

<style lang="scss">
.nav-links {
  display: inline-block;

  a {
    line-height: 1.4rem;
    color: var(--textColor);
    text-decoration: none;
    font-weight: 500;

    &:hover,
    &.active {
      color: var(--accentColor);
    }
  }

  .nav-item {
    position: relative;
    display: inline-block;
    margin-left: 1.5rem;
    line-height: 2rem;

    &:first-child {
      margin-left: 0;
    }
  }

  .repo-link {
    margin-left: 1.5rem;
    display: inline-flex;
    align-items: center;

    .repo-icon {
      width: 1.2rem;
      height: 1.2rem;
      margin-right: 0.3rem;
    }
  }
}

@media (max-width: 719px) {
  .nav-links {
    display: block;

    .nav-item {
      display: block;
      margin-left: 0;
      padding: 0.5rem 0 0.5rem 1.5rem;
    }

    .repo-link {
      display: block;
      margin-left: 0;
      padding: 0.5rem 0 0.5rem 1.5rem;
    }
  }
}
</style>
