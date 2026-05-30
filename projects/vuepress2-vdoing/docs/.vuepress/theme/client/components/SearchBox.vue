<template>
  <div class="search-box">
    <input
      v-model="query"
      type="text"
      placeholder="搜索..."
      class="search-input"
      @focus="showResults = true"
      @blur="hideResults"
    />
    <div class="search-results" v-if="showResults && query">
      <div v-if="results.length" class="results-list">
        <RouterLink
          v-for="result in results"
          :key="result.path"
          :to="result.path"
          class="result-item"
          @click="showResults = false"
        >
          <div class="result-title">{{ result.title }}</div>
          <div class="result-excerpt" v-if="result.excerpt">{{ result.excerpt }}</div>
        </RouterLink>
      </div>
      <div v-else class="no-results">
        没有找到相关结果
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useSiteData } from 'vuepress/client'

const site = useSiteData()
const query = ref('')
const showResults = ref(false)

const results = computed(() => {
  if (!query.value) return []

  const q = query.value.toLowerCase()
  const pages = site.value.pages || []

  return pages
    .filter((page: any) => {
      const title = (page.title || '').toLowerCase()
      const content = (page.content || '').toLowerCase()
      return title.includes(q) || content.includes(q)
    })
    .slice(0, 10)
    .map((page: any) => ({
      title: page.title || '无标题',
      path: page.path,
      excerpt: '',
    }))
})

function hideResults() {
  setTimeout(() => {
    showResults.value = false
  }, 200)
}
</script>

<style lang="scss" scoped>
.search-box {
  position: relative;

  .search-input {
    width: 200px;
    padding: 0.4rem 0.8rem;
    border: 1px solid var(--c-border);
    border-radius: 4px;
    background: var(--c-bg);
    color: var(--c-text);
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.2s;

    &:focus {
      border-color: var(--c-brand);
    }

    &::placeholder {
      color: var(--c-text-lightest);
    }
  }

  .search-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    min-width: 300px;
    margin-top: 0.5rem;
    background: var(--c-bg);
    border: 1px solid var(--c-border);
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 100;
  }

  .results-list {
    max-height: 400px;
    overflow-y: auto;
  }

  .result-item {
    display: block;
    padding: 0.75rem 1rem;
    color: var(--c-text);
    text-decoration: none;
    border-bottom: 1px solid var(--c-border-light);

    &:hover {
      background: var(--c-bg-lighter);
    }

    &:last-child {
      border-bottom: none;
    }
  }

  .result-title {
    font-weight: 500;
    margin-bottom: 0.25rem;
  }

  .result-excerpt {
    font-size: 0.85rem;
    color: var(--c-text-lighter);
  }

  .no-results {
    padding: 1rem;
    text-align: center;
    color: var(--c-text-lightest);
  }
}
</style>
