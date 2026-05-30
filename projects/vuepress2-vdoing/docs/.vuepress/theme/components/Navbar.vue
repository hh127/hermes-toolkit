<template>
  <header class="navbar blur">
    <SidebarButton @toggle-sidebar="$emit('toggle-sidebar')" />

    <RouterLink
      :to="localePath"
      class="home-link"
    >
      <img
        class="logo"
        v-if="site?.themeConfig?.logo"
        :src="withBase(site?.themeConfig?.logo || '')"
        :alt="siteTitle"
      />
      <span
        ref="siteNameRef"
        class="site-name"
        v-if="siteTitle"
        :class="{ 'can-hide': site?.themeConfig?.logo }"
      >{{ siteTitle }}</span>
    </RouterLink>

    <div
      class="links"
      :style="linksWrapMaxWidth ? { 'max-width': linksWrapMaxWidth + 'px' } : {}"
    >
      <AlgoliaSearchBox
        v-if="isAlgoliaSearch"
        :options="algolia"
      />
      <SearchBox
        v-else-if="site?.themeConfig?.search !== false && frontmatter.search !== false"
      />
      <NavLinks class="can-hide" />
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSiteData, usePageFrontmatter, withBase } from 'vuepress/client'

import SidebarButton from './SidebarButton.vue'
import NavLinks from './NavLinks.vue'
import SearchBox from './SearchBox.vue'
import AlgoliaSearchBox from './AlgoliaSearchBox.vue'

defineEmits(['toggle-sidebar'])

const site = useSiteData()
const frontmatter = usePageFrontmatter()

const siteNameRef = ref<HTMLElement | null>(null)
const linksWrapMaxWidth = ref<number | null>(null)

const localePath = computed(() => '/')

const siteTitle = computed(() => site.value?.title || '')

const algolia = computed(() => {
  return site.value?.themeConfig?.algolia || {}
})

const isAlgoliaSearch = computed(() => {
  return algolia.value && algolia.value.apiKey && algolia.value.indexName
})

onMounted(() => {
  const MOBILE_DESKTOP_BREAKPOINT = 719
  const handleLinksWrapWidth = () => {
    if (document.documentElement.clientWidth < MOBILE_DESKTOP_BREAKPOINT) {
      linksWrapMaxWidth.value = null
    } else {
      const navbar = document.querySelector('.navbar')
      if (navbar) {
        const NAVBAR_VERTICAL_PADDING = parseInt(getComputedStyle(navbar).paddingLeft) + parseInt(getComputedStyle(navbar).paddingRight)
        linksWrapMaxWidth.value = navbar.offsetWidth - NAVBAR_VERTICAL_PADDING - (siteNameRef.value?.offsetWidth || 0)
      }
    }
  }
  handleLinksWrapWidth()
  window.addEventListener('resize', handleLinksWrapWidth, false)
})
</script>

<style lang="scss">
$navbar-vertical-padding: 0.7rem;
$navbar-horizontal-padding: 1.5rem;

.navbar {
  padding: $navbar-vertical-padding $navbar-horizontal-padding;
  line-height: calc(var(--navbar-height) - 1.4rem);
  transition: transform 0.3s;

  a, span, img {
    display: inline-block;
  }

  .logo {
    height: calc(var(--navbar-height) - 1.4rem);
    min-width: calc(var(--navbar-height) - 1.4rem);
    margin-right: 0.8rem;
    vertical-align: top;
  }

  .site-name {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--textColor);
    position: relative;
  }

  .links {
    padding-left: 1.5rem;
    box-sizing: border-box;
    white-space: nowrap;
    font-size: 0.9rem;
    position: absolute;
    right: $navbar-horizontal-padding;
    top: $navbar-vertical-padding;
    display: flex;

    .search-box {
      flex: 0 0 auto;
      vertical-align: top;
    }
  }
}

.hide-navbar .navbar {
  transform: translateY(-100%);
}

@media (max-width: 959px) {
  .navbar .site-name {
    display: none;
  }
}

@media (max-width: 719px) {
  .navbar {
    padding-left: 4rem;

    .can-hide {
      display: none;
    }

    .links {
      padding-left: 1.5rem;
    }

    .site-name {
      width: calc(100vw - 9.4rem);
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
  }
}
</style>
