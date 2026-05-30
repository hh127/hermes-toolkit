import { defineUserConfig } from 'vuepress'
import { viteBundler } from '@vuepress/bundler-vite'
import { vdoing2Theme as vdoingTheme } from './theme/index'

const DOMAIN_NAME = 'wiki.mrlining.cn'
const WEB_SITE = `https://${DOMAIN_NAME}`

export default defineUserConfig({
  lang: 'zh-CN',
  title: '工程造价知识库',
  description: '个人Wiki知识库，记录工程造价、合约管理、法律法规等专业知识。',

  base: '/',

  bundler: viteBundler(),

  theme: vdoingTheme({
    // 导航配置
    nav: [
      { text: '首页', link: '/' },
      { text: '计量', link: '/01.计量/' },
      { text: '计价', link: '/02.计价/' },
      { text: '法规', link: '/08.法规/' },
      { text: '收藏', link: '/06.收藏夹/' },
      {
        text: '索引',
        link: '/archives/',
        items: [
          { text: '分类', link: '/categories/' },
          { text: '标签', link: '/tags/' },
          { text: '归档', link: '/archives/' },
        ],
      },
      { text: '关于', link: '/05.关于/' },
    ],

    sidebarDepth: 2,
    logo: '/img/logo.png',
    searchMaxSuggestions: 10,
    lastUpdated: true,
    lastUpdatedText: '上次更新',
    editLinks: true,
    editLinkText: '编辑',
    contributors: false,

    // Vdoing 主题特有配置
    category: true,
    tag: true,
    archive: true,
    pageStyle: 'line',

    sidebar: 'structuring',

    author: {
      name: 'Lin',
      link: 'https://github.com/hh127',
    },

    blogger: {
      avatar: '/img/avatar.png',
      name: 'Lin',
      slogan: '一个浑浑噩噩的造价小透明',
    },

    social: {
      icons: [
        {
          iconClass: 'icon-github',
          title: 'GitHub',
          link: 'https://github.com/hh127',
        },
      ],
    },

    footer: {
      createYear: 2021,
      copyrightInfo:
        'Lin | MIT License',
    },
  }),

  head: [
    ['link', { rel: 'icon', href: '/img/favicon.ico' }],
    [
      'meta',
      {
        name: 'keywords',
        content: '工程造价,预算编制,合约管理,法律法规,计量,计价,造价知识库',
      },
    ],
    ['meta', { name: 'theme-color', content: '#11a8cd' }],
  ],

  markdown: {
    lineNumbers: true,
    headers: {
      level: [2, 3, 4, 5, 6],
    },
  },
})
