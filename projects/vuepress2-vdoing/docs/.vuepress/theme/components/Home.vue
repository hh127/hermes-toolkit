<template>
  <div class="home-wrapper">
    <!-- banner块 -->
    <div
      class="banner"
      :class="{ 'hide-banner': !showBanner }"
      :style="bannerBgStyle"
    >
      <div
        class="banner-conent"
        :style="!homeData.features && !homeData.heroImage && 'padding-top: 7rem'"
      >
        <header class="hero">
          <img
            v-if="homeData.heroImage"
            :src="withBase(homeData.heroImage)"
            :alt="homeData.heroAlt"
          />
          <h1 v-if="homeData.heroText" id="main-title">
            {{ homeData.heroText }}
          </h1>
          <p v-if="homeData.tagline" class="description">
            {{ homeData.tagline }}
          </p>
          <p class="action" v-if="homeData.actionText && homeData.actionLink">
            <RouterLink class="action-button" :to="homeData.actionLink">
              {{ homeData.actionText }}
            </RouterLink>
          </p>
        </header>

        <!-- PC端features块 -->
        <div class="features" v-if="hasFeatures">
          <div
            class="feature"
            v-for="(feature, index) in homeData.features"
            :key="index"
          >
            <RouterLink v-if="feature.link" :to="feature.link">
              <img
                class="feature-img"
                v-if="feature.imgUrl"
                :src="withBase(feature.imgUrl)"
                :alt="feature.title"
              />
              <h2>{{ feature.title }}</h2>
              <p>{{ feature.details }}</p>
            </RouterLink>
            <a v-else href="javascript:;">
              <img
                class="feature-img"
                v-if="feature.imgUrl"
                :src="withBase(feature.imgUrl)"
                :alt="feature.title"
              />
              <h2>{{ feature.title }}</h2>
              <p>{{ feature.details }}</p>
            </a>
          </div>
        </div>
      </div>
    </div>

    <MainLayout>
      <template #mainLeft>
        <!-- 简约版文章列表 -->
        <UpdateArticle
          class="card-box"
          v-if="homeData.postList === 'simple'"
          :length="homeData.simplePostListLength || 10"
        />

        <!-- 详情版文章列表 -->
        <template v-else-if="!homeData.postList || homeData.postList === 'detailed'">
          <PostList :currentPage="currentPage" :perPage="perPage" />
          <Pagination
            :total="total"
            :perPage="perPage"
            :currentPage="currentPage"
            @getCurrentPage="handlePagination"
            v-show="Math.ceil(total / perPage) > 1"
          />
        </template>
      </template>

      <template v-if="!homeData.hideRightBar" #mainRight>
        <BloggerBar v-if="themeConfig.blogger" />
        <CategoriesBar
          v-if="themeConfig.category !== false && categoriesData.length"
          :categoriesData="categoriesData"
          :length="10"
        />
        <TagsBar
          v-if="themeConfig.tag !== false && tagsData.length"
          :tagsData="tagsData"
          :length="30"
        />
      </template>
    </MainLayout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { usePageFrontmatter, useSiteData, useRoute, withBase } from 'vuepress/client'

import MainLayout from './MainLayout.vue'
import PostList from './PostList.vue'
import UpdateArticle from './UpdateArticle.vue'
import Pagination from './Pagination.vue'
import BloggerBar from './BloggerBar.vue'
import CategoriesBar from './CategoriesBar.vue'
import TagsBar from './TagsBar.vue'

const frontmatter = usePageFrontmatter()
const site = useSiteData()
const route = useRoute()

const total = ref(0)
const perPage = ref(10)
const currentPage = ref(1)

const themeConfig = computed(() => site.value?.themeConfig || {})
const homeData = computed(() => ({ ...frontmatter.value }))
const hasFeatures = computed(() => !!(homeData.value.features && homeData.value.features.length))

const categoriesData = computed(() => {
  // 从页面数据中提取分类
  const categories: any[] = []
  return categories
})

const tagsData = computed(() => {
  // 从页面数据中提取标签
  const tags: any[] = []
  return tags
})

const showBanner = computed(() => {
  return route.query.p && route.query.p != 1 && (!homeData.value.postList || homeData.value.postList === 'detailed')
    ? false
    : true
})

const bannerBgStyle = computed(() => {
  const bannerBg = homeData.value.bannerBg
  if (!bannerBg || bannerBg === 'auto') {
    if (themeConfig.value.bodyBgImg) {
      return ''
    } else {
      return 'background: rgb(40,40,45) url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAjCAYAAAAe2bNZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABOSURBVFhH7c6xCQAgDAVRR9A6E4hLu4uLiWJ7tSnuQcIvr2TRYsw3/zOGGEOMIcYQY4gxxBhiDDGGGEOMIcYQY4gxxBhiDLkx52W4Gn1tuslCtHJvL54AAAAASUVORK5CYII=)'
    }
  } else if (bannerBg === 'none') {
    if (themeConfig.value.bodyBgImg) {
      return ''
    } else {
      return 'background: var(--mainBg);color: var(--textColor)'
    }
  } else if (bannerBg.indexOf('background:') > -1) {
    return bannerBg
  } else if (bannerBg.indexOf('.') > -1) {
    return `background: url(${withBase(bannerBg)}) center center / cover no-repeat`
  }
  return ''
})

const handlePagination = (i: number) => {
  currentPage.value = i
}

onMounted(() => {
  total.value = 100 // 需要从实际数据获取
  if (route.query.p) {
    currentPage.value = Number(route.query.p)
  }
})
</script>

<style lang="scss">
.home-wrapper {
  .banner {
    width: 100%;
    min-height: 450px;
    margin: 0 auto;
    padding: 0 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;

    &.hide-banner {
      min-height: 0;
      padding: 0;
    }

    .banner-conent {
      max-width: 1200px;
      margin: 0 auto;
      padding-top: 5rem;
    }

    .hero {
      text-align: center;

      img {
        max-width: 100%;
        max-height: 280px;
        display: block;
        margin: 0 auto 1.5rem;
      }

      h1 {
        font-size: 3rem;
        margin: 0;
      }

      .description {
        max-width: 35rem;
        font-size: 1.6rem;
        line-height: 1.3;
        color: var(--textColor);
        opacity: 0.8;
        margin: 0 auto;
      }

      .action-button {
        display: inline-block;
        padding: 0.8rem 1.6rem;
        border-radius: 4px;
        background-color: var(--accentColor);
        color: #fff;
        text-decoration: none;
        transition: background-color 0.2s;

        &:hover {
          background-color: var(--accentColorDark);
        }
      }
    }

    .features {
      display: flex;
      flex-wrap: wrap;
      margin-top: 2.5rem;
      padding: 1.2rem 0;
      border-top: 1px solid var(--borderColor);

      .feature {
        flex: 1;
        padding: 0 1rem;
        text-align: center;
        min-width: 200px;

        a {
          color: var(--textColor);
          text-decoration: none;

          &:hover {
            color: var(--accentColor);
          }
        }

        .feature-img {
          max-width: 100%;
          max-height: 100px;
          margin: 0 auto 1rem;
        }

        h2 {
          font-size: 1.2rem;
          margin: 0;
        }

        p {
          font-size: 0.9rem;
          opacity: 0.7;
          margin: 0.5rem 0 0;
        }
      }
    }
  }
}

@media (max-width: 719px) {
  .home-wrapper .banner {
    min-height: 350px;
    padding: 0 1.5rem;

    .hero h1 {
      font-size: 2rem;
    }

    .features {
      display: block;

      .feature {
        padding: 1rem 0;
        border-bottom: 1px solid var(--borderColor);
      }
    }
  }
}
</style>
