<template>
  <div class="search-box">
    <input
      class="search-input"
      v-model="query"
      :placeholder="placeholder"
      @focus="focused = true"
      @blur="handleBlur"
      @input="handleSearch"
    />
    <div class="search-results" v-show="focused && results.length">
      <div
        class="result-item"
        v-for="(item, index) in results"
        :key="index"
        @mousedown="goToResult(item)"
      >
        <span class="title">{{ item.title }}</span>
        <span class="path" v-if="item.path">{{ item.path }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vuepress/client'

const router = useRouter()

const query = ref('')
const focused = ref(false)
const results = ref<any[]>([])

const placeholder = computed(() => '搜索...')

const handleSearch = () => {
  if (!query.value) {
    results.value = []
    return
  }
  // 需要实现实际的搜索逻辑
  results.value = []
}

const handleBlur = () => {
  setTimeout(() => {
    focused.value = false
  }, 200)
}

const goToResult = (item: any) => {
  if (item.path) {
    router.push(item.path)
  }
  focused.value = false
  query.value = ''
}
</script>

<style lang="scss">
.search-box {
  position: relative;
  margin-right: 1rem;

  .search-input {
    width: 200px;
    padding: 0.5rem 1rem;
    border: 1px solid var(--borderColor);
    border-radius: 4px;
    font-size: 0.9rem;
    background: var(--mainBg);
    color: var(--textColor);
    outline: none;
    transition: all 0.2s;

    &:focus {
      border-color: var(--accentColor);
      box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.1);
    }

    &::placeholder {
      color: var(--textColor);
      opacity: 0.5;
    }
  }

  .search-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    margin-top: 0.5rem;
    background: var(--mainBg);
    border: 1px solid var(--borderColor);
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    max-height: 300px;
    overflow-y: auto;
    z-index: 100;

    .result-item {
      padding: 0.8rem 1rem;
      cursor: pointer;
      transition: background 0.2s;

      &:hover {
        background: var(--accentColor);
        color: #fff;
      }

      .title {
        display: block;
        font-size: 0.95rem;
      }

      .path {
        display: block;
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.2rem;
      }
    }
  }
}

@media (max-width: 719px) {
  .search-box .search-input {
    width: 150px;
  }
}
</style>
