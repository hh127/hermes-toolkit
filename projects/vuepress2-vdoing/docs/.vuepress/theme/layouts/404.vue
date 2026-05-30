<template>
  <div class="theme-container">
    <Navbar />
    <div class="theme-vdoing-content">
      <div class="not-found">
        <h1>404</h1>
        <p>{{ getMsg() }}</p>
        <RouterLink to="/" class="back-home">返回首页</RouterLink>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const messages = [
  '这里什么都没有。',
  '我们是怎么来到这儿的？',
  '这是一个 404 页面',
  '看起来我们进入了错误的链接'
]

const getMsg = () => {
  return messages[Math.floor(Math.random() * messages.length)]
}
</script>

<style lang="scss">
.not-found {
  text-align: center;
  padding: 10rem 2rem;

  h1 {
    font-size: 6rem;
    margin: 0;
    color: var(--accentColor);
  }

  p {
    font-size: 1.5rem;
    color: var(--textColor);
    opacity: 0.7;
    margin: 1rem 0 2rem;
  }

  .back-home {
    display: inline-block;
    padding: 0.8rem 2rem;
    background: var(--accentColor);
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
    transition: background 0.2s;

    &:hover {
      background: var(--accentColorDark);
    }
  }
}
</style>
