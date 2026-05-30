import { getDirname, path } from 'vuepress/utils'
import type { Theme } from 'vuepress/core'

const __dirname = getDirname(import.meta.url)

export interface VdoingThemeOptions {
  nav?: any[]
  sidebar?: any
  sidebarDepth?: number
  logo?: string
  searchMaxSuggestions?: number
  lastUpdated?: boolean
  lastUpdatedText?: string
  editLinks?: boolean
  editLinkText?: string
  contributors?: boolean
  category?: boolean
  tag?: boolean
  archive?: boolean
  pageStyle?: string
  author?: { name: string; link?: string }
  blogger?: { avatar: string; name: string; slogan: string }
  social?: { icons: any[] }
  footer?: { createYear: number; copyrightInfo: string }
  bodyBgImg?: string | string[]
  bodyBgImgOpacity?: number
  defaultMode?: string
}

export const vdoingTheme: Theme<VdoingThemeOptions> = (options, app) => {
  return {
    name: 'vuepress-theme-vdoing2',

    layouts: path.resolve(__dirname, './client/layouts'),

    plugins: [
      // 搜索插件
      [
        '@vuepress/search',
        {
          maxSuggestions: options.searchMaxSuggestions || 10,
        },
      ],
      // 进度条
      '@vuepress/nprogress',
      // 返回顶部
      '@vuepress/back-to-top',
      // 图片缩放
      '@vuepress/medium-zoom',
      // 活跃标题链接
      [
        '@vuepress/active-header-links',
        {
          headerLinkSelector: '.sidebar-link',
          headerAnchorSelector: '.header-anchor',
        },
      ],
      // Git 信息（最后更新时间）
      ['@vuepress/git', { updatedTime: true }],
    ],

    // 将主题配置注入到 client 端
    clientConfigFile: path.resolve(__dirname, './client/config.ts'),
  }
}

export default vdoingTheme
