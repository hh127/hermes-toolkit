<template>
  <div class="catalogue-page">
    <div class="catalogue-header">
      <h1 class="catalogue-title">{{ title }}</h1>
      <p class="catalogue-desc" v-if="description">{{ description }}</p>
    </div>
    <div class="catalogue-content">
      <div v-for="group in groups" :key="group.title" class="catalogue-group">
        <h2 class="group-title">{{ group.title }}</h2>
        <div class="group-items">
          <RouterLink
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="catalogue-item"
          >
            <div class="item-icon" v-if="item.icon">{{ item.icon }}</div>
            <div class="item-info">
              <div class="item-title">{{ item.title }}</div>
              <div class="item-desc" v-if="item.desc">{{ item.desc }}</div>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePageFrontmatter } from 'vuepress/client'

const frontmatter = usePageFrontmatter()

const title = computed(() => (frontmatter.value as any).title || '')
const description = computed(() => (frontmatter.value as any).description || '')

const groups = computed(() => {
  const fm = frontmatter.value as any
  return fm.catalogue || []
})
</script>

<style lang="scss" scoped>
.catalogue-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;

  .catalogue-header {
    margin-bottom: 2rem;

    .catalogue-title {
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }

    .catalogue-desc {
      color: var(--c-text-lighter);
    }
  }

  .catalogue-group {
    margin-bottom: 2rem;

    .group-title {
      font-size: 1.3rem;
      color: var(--c-brand);
      border-bottom: 2px solid var(--c-brand);
      padding-bottom: 0.5rem;
      margin-bottom: 1rem;
    }
  }

  .group-items {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }

  .catalogue-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    border: 1px solid var(--c-border);
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.2s;

    &:hover {
      border-color: var(--c-brand);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      transform: translateY(-2px);
    }

    .item-icon {
      font-size: 2rem;
      margin-right: 1rem;
    }

    .item-title {
      font-size: 1rem;
      color: var(--c-text);
      font-weight: 500;
    }

    .item-desc {
      font-size: 0.85rem;
      color: var(--c-text-lightest);
      margin-top: 0.25rem;
    }
  }
}
</style>
