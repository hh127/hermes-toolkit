<template>
  <div class="theme-container">
    <div class="theme-default-content">
      <h1>404</h1>
      <p>{{ getMsg() }}</p>
      <RouterLink to="/">返回首页</RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const msgs = [
  '这里什么都没有。',
  '我们怎么到这来了？',
  '这是一个 404 页面。',
  '看起来我们进入了错误的链接。',
]

function getMsg() {
  return msgs[Math.floor(Math.random() * msgs.length)]
}
</script>

<style lang="scss" scoped>
.theme-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  text-align: center;
}
h1 {
  font-size: 6rem;
  color: var(--c-brand);
  margin-bottom: 1rem;
}
p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}
</style>
