<template>
  <div class="body-bg-img" :style="bgStyle"></div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useThemeData } from '../composables'

const themeData = useThemeData()
const currentIndex = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

const bgImg = computed(() => themeData.value.bodyBgImg)
const opacity = computed(() => themeData.value.bodyBgImgOpacity || 0.5)

const bgStyle = computed(() => {
  const img = bgImg.value
  if (!img) return {}

  let currentImg: string
  if (Array.isArray(img)) {
    currentImg = img[currentIndex.value] || img[0]
  } else {
    currentImg = img
  }

  return {
    backgroundImage: `url(${currentImg})`,
    opacity: opacity.value,
  }
})

onMounted(() => {
  const img = bgImg.value
  if (Array.isArray(img) && img.length > 1) {
    const interval = (themeData.value.bodyBgImgInterval || 15) * 1000
    timer = setInterval(() => {
      currentIndex.value = (currentIndex.value + 1) % img.length
    }, interval)
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style lang="scss" scoped>
.body-bg-img {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  transition: opacity 0.5s, background-image 1s;
}
</style>
