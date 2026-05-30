import { defineClientConfig } from 'vuepress/client'
import { h } from 'vue'

// 全局组件
import Badge from './components/Badge.vue'
import CodeGroup from './components/CodeGroup.vue'
import CodeBlock from './components/CodeBlock.vue'

// 布局
import Layout from './layouts/Layout.vue'
import NotFound from './layouts/404.vue'

// 全局样式
import './styles/index.scss'

export default defineClientConfig({
  // 布局
  layouts: {
    Layout,
    NotFound,
  },

  // 增强
  enhance({ app, router, siteData }) {
    // 注册全局组件
    app.component('Badge', Badge)
    app.component('CodeGroup', CodeGroup)
    app.component('CodeBlock', CodeBlock)

    // 全局属性 - VuePress 2.x 使用 provide/inject
    app.provide('$sortPosts', [])
    app.provide('$groupPosts', { categories: {}, tags: {} })
    app.provide('$categoriesAndTags', { categories: [], tags: [] })
  },

  // 根组件设置
  rootComponents: [],
})
