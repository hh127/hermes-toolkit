import { getDirname, path } from '@vuepress/utils'
import type { Theme } from 'vuepress/core'
import { createSidebarData } from './node/sidebar'

const __dirname = getDirname(import.meta.url)

/**
 * Vdoing2 Theme - VuePress 2.x 版本
 * 基于 xugaoyi/vuepress-theme-vdoing 完整复刻
 */
export const vdoing2Theme = (options: Record<string, any> = {}): Theme => {
  return (app) => {
    const themeConfig = { ...options }

    // 自动生成结构化侧边栏
    const sidebar = themeConfig.sidebar
    if (sidebar === 'structuring' || (sidebar && sidebar.mode === 'structuring')) {
      const collapsable = themeConfig.sidebar?.collapsable !== false
      try {
        const sidebarData = createSidebarData(app.dir.source(), collapsable)
        if (Object.keys(sidebarData).length > 0) {
          themeConfig.sidebar = sidebarData
          console.log('tip: sidebar data generated successfully')
        } else {
          themeConfig.sidebar = 'auto'
          console.log('warning: no sidebar data generated, switch to "auto"')
        }
      } catch (e) {
        themeConfig.sidebar = 'auto'
        console.log('warning: failed to generate sidebar data:', e)
      }
    }

    return {
      name: 'vuepress-theme-vdoing2',

      // 主题别名
      alias: {
        '@theme': path.resolve(__dirname),
      },

      // 主题布局
      layouts: {
        Layout: path.resolve(__dirname, 'layouts/Layout.vue'),
        NotFound: path.resolve(__dirname, 'layouts/404.vue'),
      },

      // 客户端配置文件
      clientConfigFile: path.resolve(__dirname, 'client.ts'),

      // 插件配置
      plugins: [
        // 搜索插件
        ['@vuepress/plugin-search'],

        // 返回顶部
        ['@vuepress/plugin-back-to-top'],

        // 进度条
        ['@vuepress/plugin-nprogress'],

        // 图片缩放
        ['@vuepress/plugin-medium-zoom'],

        // 活动标题链接
        ['@vuepress/plugin-active-header-links'],

        // 自定义容器
        ['@vuepress/plugin-container', {
          type: 'tip',
          defaultTitle: {
            '/': '提示',
            '/en/': 'TIP'
          }
        }],
        ['@vuepress/plugin-container', {
          type: 'warning',
          defaultTitle: {
            '/': '注意',
            '/en/': 'WARNING'
          }
        }],
        ['@vuepress/plugin-container', {
          type: 'danger',
          defaultTitle: {
            '/': '警告',
            '/en/': 'WARNING'
          }
        }],
        ['@vuepress/plugin-container', {
          type: 'details',
          before: (info: string) => `<details class="custom-block details">${info ? `<summary>${info}</summary>` : ''}\n`,
          after: () => '</details>\n',
          defaultTitle: {
            '/': '点击查看',
            '/en/': 'DETAILS'
          }
        }],
        ['@vuepress/plugin-container', {
          type: 'right',
          defaultTitle: ''
        }],
        ['@vuepress/plugin-container', {
          type: 'theorem',
          before: (info: string) => `<div class="custom-block theorem"><p class="title">${info}</p>`,
          after: '</div>'
        }],
        ['@vuepress/plugin-container', {
          type: 'center',
          before: () => '<div class="center-container">',
          after: () => '</div>'
        }],
        ['@vuepress/plugin-container', {
          type: 'note',
          defaultTitle: {
            '/': '笔记',
            '/en/': 'NOTE'
          }
        }],
      ],

      // 主题配置
      themeConfig,
    }
  }
}

export default vdoing2Theme
