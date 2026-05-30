import { defineClientConfig } from 'vuepress/client'
import { computed, provide } from 'vue'

// 全局组件
import Badge from './components/Badge.vue'
import CodeGroup from './components/CodeGroup.vue'
import CodeBlock from './components/CodeBlock.vue'

// 布局
import Layout from './layouts/Layout.vue'
import NotFound from './layouts/404.vue'

// 数据处理
import { filterPosts, sortPosts, sortPostsByDate, groupPosts, categoriesAndTags } from './utils/postData'

// 全局样式
import './styles/index.scss'

export default defineClientConfig({
  // 布局
  layouts: {
    Layout,
    NotFound,
  },

  // 增强 - 在客户端运行
  enhance({ app, router, siteData }) {
    // 注册全局组件
    app.component('Badge', Badge)
    app.component('CodeGroup', CodeGroup)
    app.component('CodeBlock', CodeBlock)

    // 修复ISO8601时间格式为普通时间格式，以及添加作者信息
    if (siteData.pages) {
      siteData.pages.map((item: any) => {
        const { frontmatter } = item
        if (!frontmatter) return item

        const { date, author } = frontmatter
        if (typeof date === 'string' && date.charAt(date.length - 1) === 'Z') {
          item.frontmatter.date = repairUTCDate(date)
        }
        if (author) {
          item.author = author
        } else if (siteData.themeConfig?.author) {
          item.author = siteData.themeConfig.author
        }
        return item
      })
    }
  },

  // 根组件 - 用于提供全局数据
  rootComponents: [GlobalDataProvider],
})

// 全局数据提供组件
function GlobalDataProvider() {
  // 这个组件不渲染任何内容，只负责提供全局数据
  return null
}

// 修复ISO8601时间格式为普通时间格式
function repairUTCDate(date: string | Date): string {
  if (!(date instanceof Date)) {
    date = new Date(date)
  }
  return `${date.getUTCFullYear()}-${zero(date.getUTCMonth() + 1)}-${zero(date.getUTCDate())} ${zero(date.getUTCHours())}:${zero(date.getUTCMinutes())}:${zero(date.getUTCSeconds())}`
}

// 小于10补0
function zero(d: number): string {
  return d.toString().padStart(2, '0')
}
