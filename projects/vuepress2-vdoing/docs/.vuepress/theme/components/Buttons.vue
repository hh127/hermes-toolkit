<template>
  <div class="buttons">
    <!-- 返回顶部 -->
    <div
      class="button blur"
      :class="{ show: showBackToTop }"
      @click="scrollToTop"
      title="返回顶部"
    >
      <svg class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z" fill="currentColor"/>
      </svg>
    </div>

    <!-- 主题切换 -->
    <div
      class="button blur"
      @click="toggleTheme"
      :title="isDark ? '切换到亮色模式' : '切换到暗色模式'"
    >
      <svg v-if="isDark" class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z" fill="currentColor"/>
      </svg>
      <svg v-else class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M9.37 5.51A7.35 7.35 0 009.1 7.5c0 4.08 3.32 7.4 7.4 7.4.68 0 1.35-.09 1.99-.27A7.014 7.014 0 0112 19c-3.86 0-7-3.14-7-7 0-2.93 1.81-5.45 4.37-6.49zM12 3a9 9 0 109 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 01-4.4 2.26 5.403 5.403 0 01-3.14-9.8c-.44-.06-.9-.1-1.36-.1z" fill="currentColor"/>
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['toggle-theme-mode'])

const showBackToTop = ref(false)
const isDark = ref(false)

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  emit('toggle-theme-mode', isDark.value ? 'dark' : 'light')
  document.documentElement.classList.toggle('theme-mode-dark', isDark.value)
}

const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })

  // 检查系统主题偏好
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  isDark.value = prefersDark
  document.documentElement.classList.toggle('theme-mode-dark', prefersDark)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss">
.buttons {
  position: fixed;
  right: 2rem;
  bottom: 2.5rem;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  .button {
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--mainBg);
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s;
    opacity: 0;
    transform: translateY(10px);

    &:hover {
      background: var(--accentColor);
      color: #fff;
    }

    &.show {
      opacity: 1;
      transform: translateY(0);
    }

    .icon {
      width: 1.2rem;
      height: 1.2rem;
      color: var(--textColor);
    }

    &:hover .icon {
      color: #fff;
    }
  }
}

@media (max-width: 719px) {
  .buttons {
    right: 1rem;
    bottom: 1.5rem;
  }
}
</style>
