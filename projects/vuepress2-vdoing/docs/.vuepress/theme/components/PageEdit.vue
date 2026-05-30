<template>
  <div class="page-edit">
    <div class="edit-link" v-if="editLink">
      <a :href="editLink" target="_blank" rel="noopener noreferrer">
        {{ editLinkText }}
      </a>
    </div>
    <div class="last-updated" v-if="lastUpdated">
      <span class="prefix">{{ lastUpdatedText }}：</span>
      <span class="time">{{ lastUpdated }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePageData, useSiteData, usePageFrontmatter } from 'vuepress/client'

const page = usePageData()
const site = useSiteData()
const frontmatter = usePageFrontmatter()

const editLink = computed(() => {
  const { editLinks, docsRepo, docsBranch, docsDir } = site.value.themeConfig || {}
  if (!editLinks || !docsRepo) return null

  const base = docsRepo.includes('github.com')
    ? `https://github.com/${docsRepo}/edit/${docsBranch || 'main'}/`
    : docsRepo

  return base + (docsDir ? docsDir + '/' : '') + page.value.relativePath
})

const editLinkText = computed(() => {
  return site.value.themeConfig.editLinkText || 'Edit this page'
})

const lastUpdated = computed(() => {
  return page.value.lastUpdated || null
})

const lastUpdatedText = computed(() => {
  return site.value.themeConfig.lastUpdatedText || 'Last Updated'
})
</script>

<style lang="scss">
.page-edit {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  margin-top: 2rem;
  border-top: 1px solid var(--borderColor);
  font-size: 0.85rem;

  .edit-link {
    a {
      color: var(--accentColor);
      text-decoration: none;

      &:hover {
        color: var(--accentColorDark);
      }
    }
  }

  .last-updated {
    color: var(--textColor);
    opacity: 0.7;

    .prefix {
      font-weight: 500;
    }
  }
}

@media (max-width: 719px) {
  .page-edit {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
