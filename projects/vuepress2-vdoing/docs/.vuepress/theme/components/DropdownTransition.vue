<template>
  <transition
    name="dropdown"
    @enter="onEnter"
    @after-enter="onAfterEnter"
    @leave="onLeave"
    @after-leave="onAfterLeave"
  >
    <slot />
  </transition>
</template>

<script setup lang="ts">
const onEnter = (el: Element) => {
  const htmlEl = el as HTMLElement
  htmlEl.style.height = 'auto'
  const height = getComputedStyle(el).height
  htmlEl.style.height = '0'
  getComputedStyle(el)
  htmlEl.style.height = height
}

const onAfterEnter = (el: Element) => {
  const htmlEl = el as HTMLElement
  htmlEl.style.height = 'auto'
}

const onLeave = (el: Element) => {
  const htmlEl = el as HTMLElement
  htmlEl.style.height = getComputedStyle(el).height
  getComputedStyle(el)
  htmlEl.style.height = '0'
}

const onAfterLeave = (el: Element) => {
  const htmlEl = el as HTMLElement
  htmlEl.style.height = 'auto'
}
</script>

<style lang="scss">
.dropdown-enter-active,
.dropdown-leave-active {
  transition: height 0.1s ease-out;
  overflow: hidden;
}

.dropdown-enter-from,
.dropdown-leave-to {
  height: 0;
}
</style>
