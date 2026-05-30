<template>
  <div class="body-bg-img" :style="bgStyle" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSiteData, withBase } from 'vuepress/client'

const site = useSiteData()

const bgStyle = computed(() => {
  const { bodyBgImg } = site.value?.themeConfig || {}
  if (!bodyBgImg) return {}

  if (typeof bodyBgImg === 'string') {
    return {
      background: `url(${withBase(bodyBgImg)}) center center / cover no-repeat fixed`
    }
  }

  return {
    background: `url(${withBase(bodyBgImg.img)}) center center / cover no-repeat fixed`,
    opacity: bodyBgImg.opacity || 1
  }
})
</script>

<style lang="scss">
.body-bg-img {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}
</style>
