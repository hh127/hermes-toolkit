import { defineClientConfig } from 'vuepress/client'
import Layout from './layouts/Layout.vue'
import NotFound from './layouts/NotFound.vue'
import ArchivesPage from './components/ArchivesPage.vue'
import CategoriesPage from './components/CategoriesPage.vue'
import TagsPage from './components/TagsPage.vue'
import PostList from './components/PostList.vue'
import BloggerBar from './components/BloggerBar.vue'
import CategoriesBar from './components/CategoriesBar.vue'
import TagsBar from './components/TagsBar.vue'
import UpdateArticle from './components/UpdateArticle.vue'
import ArticleInfo from './components/ArticleInfo.vue'
import Pagination from './components/Pagination.vue'
import Catalogue from './components/Catalogue.vue'
import RightMenu from './components/RightMenu.vue'
import BodyBgImg from './components/BodyBgImg.vue'
import Buttons from './components/Buttons.vue'
import './styles/index.scss'

export default defineClientConfig({
  layouts: {
    Layout,
    NotFound,
  },
  enhance: ({ app }) => {
    // 注册全局组件
    app.component('ArchivesPage', ArchivesPage)
    app.component('CategoriesPage', CategoriesPage)
    app.component('TagsPage', TagsPage)
    app.component('PostList', PostList)
    app.component('BloggerBar', BloggerBar)
    app.component('CategoriesBar', CategoriesBar)
    app.component('TagsBar', TagsBar)
    app.component('UpdateArticle', UpdateArticle)
    app.component('ArticleInfo', ArticleInfo)
    app.component('Pagination', Pagination)
    app.component('Catalogue', Catalogue)
    app.component('RightMenu', RightMenu)
    app.component('BodyBgImg', BodyBgImg)
    app.component('Buttons', Buttons)
  },
  setup: () => {
    // 主题初始化逻辑
  },
})
