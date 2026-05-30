<template>
  <div class="tags-bar card-box">
    <h4 class="title">标签</h4>
    <div class="tags" ref="tagsRef">
      <RouterLink
        :to="`/tags/?tag=${encodeURIComponent(item.name)}`"
        class="tag-item"
        :class="{ active: item.name === tag }"
        v-for="(item, index) in displayData"
        :key="index"
      >
        {{ item.name }}
        <span class="count">{{ item.length }}</span>
      </RouterLink>
    </div>
    <RouterLink
      v-if="tagsData.length > length"
      to="/tags/"
      class="more"
    >查看更多</RouterLink>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'

const props = withDefaults(defineProps<{
  tagsData: any[]
  tag?: string
  length?: number
}>(), {
  tag: '',
  length: 30
})

const tagsRef = ref<HTMLElement | null>(null)

const displayData = computed(() => {
  return props.tagsData.slice(0, props.length)
})

onMounted(() => {
  // 滚动条定位到当前标签
  if (props.tag && tagsRef.value) {
    const activeEl = tagsRef.value.querySelector('.active')
    if (activeEl) {
      setTimeout(() => {
        activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 300)
    }
  }
})
</script>

<style lang="scss">
.tags-bar {
  padding: 1.5rem;
  margin-bottom: 1rem;

  .title {
    margin: 0 0 1rem;
    font-size: 1.1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accentColor);
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    max-height: 300px;
    overflow-y: auto;

    .tag-item {
      display: inline-flex;
      align-items: center;
      padding: 0.3rem 0.6rem;
      background: var(--mainBg);
      border: 1px solid var(--borderColor);
      border-radius: 4px;
      color: var(--textColor);
      text-decoration: none;
      font-size: 0.85rem;
      transition: all 0.2s;

      &:hover,
      &.active {
        background: var(--accentColor);
        border-color: var(--accentColor);
        color: #fff;
      }

      .count {
        margin-left: 0.3rem;
        font-size: 0.75rem;
        opacity: 0.8;
      }
    }

    &::-webkit-scrollbar-track-piece {
      background-color: rgba(0, 0, 0, 0.05);
    }

    &::-webkit-scrollbar-thumb:vertical {
      background-color: rgba(0, 0, 0, 0.15);
    }
  }

  .more {
    display: block;
    text-align: center;
    margin-top: 1rem;
    color: var(--accentColor);
    text-decoration: none;
    font-size: 0.9rem;

    &:hover {
      color: var(--accentColorDark);
    }
  }
}
</style>
