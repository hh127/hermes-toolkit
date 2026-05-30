<template>
  <div class="page-nav">
    <div class="inner">
      <div class="prev" v-if="prev">
        <RouterLink :to="prev.path" class="link">
          <span class="hint">← 上一篇</span>
          <span class="title">{{ prev.title }}</span>
        </RouterLink>
      </div>
      <div class="next" v-if="next">
        <RouterLink :to="next.path" class="link">
          <span class="hint">下一篇 →</span>
          <span class="title">{{ next.title }}</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePageData, useSiteData } from 'vuepress/client'

const props = defineProps<{
  sidebarItems: any[]
}>()

const page = usePageData()
const site = useSiteData()

const prev = computed(() => {
  const { prev: prevConfig } = site.value.themeConfig || {}
  if (prevConfig === false) return null
  if (typeof prevConfig === 'object') return prevConfig
  return null
})

const next = computed(() => {
  const { next: nextConfig } = site.value.themeConfig || {}
  if (nextConfig === false) return null
  if (typeof nextConfig === 'object') return nextConfig
  return null
})
</script>

<style lang="scss">
.page-nav {
  .inner {
    display: flex;
    justify-content: space-between;
    padding: 1.5rem 0;
    border-top: 1px solid var(--borderColor);
    margin-top: 2rem;
  }

  .prev,
  .next {
    flex: 1;

    .link {
      display: block;
      padding: 0.8rem 1rem;
      border-radius: 4px;
      text-decoration: none;
      transition: all 0.2s;

      &:hover {
        background: var(--mainBg);
      }

      .hint {
        display: block;
        font-size: 0.8rem;
        color: var(--textColor);
        opacity: 0.6;
        margin-bottom: 0.3rem;
      }

      .title {
        display: block;
        font-size: 0.95rem;
        color: var(--accentColor);
      }
    }
  }

  .prev {
    margin-right: 1rem;
    text-align: left;
  }

  .next {
    margin-left: 1rem;
    text-align: right;
  }
}

@media (max-width: 719px) {
  .page-nav .inner {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
