<template>
  <div class="theme-buttons">
    <button
      class="btn btn-mode"
      @click="toggleMode"
      :title="modeTitle"
    >
      <span v-if="isDark">🌙</span>
      <span v-else>☀️</span>
    </button>
    <button
      class="btn btn-top"
      v-show="showBackToTop"
      @click="scrollToTop"
      title="返回顶部"
    >
      ⬆
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const isDark = ref(false)
const showBackToTop = ref(false)

const modeTitle = computed(() => isDark.value ? '切换为亮色模式' : '切换为暗色模式')

function toggleMode() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('vd-theme', isDark.value ? 'dark' : 'light')
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleScroll() {
  showBackToTop.value = window.scrollY > 300
}

onMounted(() => {
  // 读取保存的主题
  const saved = localStorage.getItem('vd-theme')
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }

  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.theme-buttons {
  position: fixed;
  right: 2rem;
  bottom: 2rem;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  .btn {
    width: 40px;
    height: 40px;
    border: 1px solid var(--c-border);
    border-radius: 50%;
    background: var(--c-bg);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    &:hover {
      border-color: var(--c-brand);
      transform: scale(1.1);
    }
  }
}

@media (max-width: 959px) {
  .theme-buttons {
    right: 1rem;
    bottom: 1rem;

    .btn {
      width: 36px;
      height: 36px;
      font-size: 1rem;
    }
  }
}
</style>
