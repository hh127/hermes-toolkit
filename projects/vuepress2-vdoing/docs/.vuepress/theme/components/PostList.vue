<template>
  <div class="post-list" ref="postListRef">
    <div
      class="post card-box"
      :class="{ 'iconfont icon-zhiding': item.frontmatter?.sticky }"
      v-for="item in displayPosts"
      :key="item.key"
    >
      <div class="title-wrapper">
        <h2>
          <RouterLink :to="item.path">
            {{ item.title }}
            <span
              class="title-tag"
              v-if="item.frontmatter?.titleTag"
            >{{ item.frontmatter.titleTag }}</span>
          </RouterLink>
        </h2>
        <div class="article-info">
          <a
            title="作者"
            class="iconfont icon-touxiang"
            target="_blank"
            v-if="item.author?.href"
            :href="item.author.href"
          >{{ item.author?.name || item.author }}</a>
          <span
            title="作者"
            class="iconfont icon-touxiang"
            v-else-if="item.author"
          >{{ item.author?.name || item.author }}</span>

          <span
            title="创建时间"
            class="iconfont icon-riqi"
            v-if="item.frontmatter?.date"
          >{{ item.frontmatter.date.split(' ')[0] }}</span>
          <span
            title="分类"
            class="iconfont icon-wenjian"
            v-if="themeConfig.category !== false && item.frontmatter?.categories"
          >
            <RouterLink
              :to="`/categories/?category=${encodeURIComponent(c)}`"
              v-for="(c, index) in item.frontmatter.categories"
              :key="index"
            >{{ c }}</RouterLink>
          </span>
          <span
            title="标签"
            class="iconfont icon-biaoqian tags"
            v-if="themeConfig.tag !== false && item.frontmatter?.tags && item.frontmatter.tags[0]"
          >
            <RouterLink
              :to="`/tags/?tag=${encodeURIComponent(t)}`"
              v-for="(t, index) in item.frontmatter.tags"
              :key="index"
            >{{ t }}</RouterLink>
          </span>
        </div>
      </div>
      <div class="excerpt-wrapper" v-if="item.excerpt">
        <div class="excerpt" v-html="item.excerpt" />
        <RouterLink
          :to="item.path"
          class="readmore iconfont icon-jiantou-you"
        >阅读全文</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useSiteData, useRoute, useRouter } from 'vuepress/client'

const props = withDefaults(defineProps<{
  category?: string
  tag?: string
  currentPage?: number
  perPage?: number
  posts?: any[]
}>(), {
  category: '',
  tag: '',
  currentPage: 1,
  perPage: 10,
  posts: () => []
})

const site = useSiteData()
const route = useRoute()
const router = useRouter()

const postListRef = ref<HTMLElement | null>(null)

const themeConfig = computed(() => site.value?.themeConfig || {})

const displayPosts = computed(() => {
  let filteredPosts = props.posts || []

  // 按分类筛选
  if (props.category) {
    filteredPosts = filteredPosts.filter(post => {
      return post.frontmatter?.categories?.includes(props.category)
    })
  }

  // 按标签筛选
  if (props.tag) {
    filteredPosts = filteredPosts.filter(post => {
      return post.frontmatter?.tags?.includes(props.tag)
    })
  }

  // 分页
  const start = (props.currentPage - 1) * props.perPage
  const end = start + props.perPage
  return filteredPosts.slice(start, end)
})

// 监听页码变化
watch(
  () => props.currentPage,
  (newPage) => {
    if (route.query.p != String(newPage)) {
      router.push({
        query: {
          ...route.query,
          p: String(newPage)
        }
      })
    }
  }
)
</script>

<style lang="scss">
.post-list {
  .post {
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-radius: 0;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 2px 16px rgba(0, 0, 0, 0.1);
    }

    &.icon-zhiding::before {
      content: '置顶';
      color: var(--accentColor);
      font-size: 0.85rem;
      margin-right: 0.5rem;
    }

    .title-wrapper {
      h2 {
        margin: 0;
        font-size: 1.3rem;

        a {
          color: var(--textColor);
          text-decoration: none;

          &:hover {
            color: var(--accentColor);
          }
        }

        .title-tag {
          height: 1.3rem;
          line-height: 1.3rem;
          border: 1px solid var(--accentColor);
          color: var(--accentColor);
          font-size: 0.85rem;
          padding: 0 0.3rem;
          border-radius: 0.2rem;
          margin-left: 0.5rem;
          transform: translate(0, -0.15rem);
          display: inline-block;
        }
      }

      .article-info {
        font-size: 0.85rem;
        color: var(--textColor);
        opacity: 0.7;
        margin-top: 0.5rem;

        span, a {
          margin-right: 1rem;

          &::before {
            margin-right: 0.3rem;
          }

          a {
            color: inherit;
            text-decoration: none;
            margin-right: 0.5rem;

            &:hover {
              color: var(--accentColor);
            }
          }
        }
      }
    }

    .excerpt-wrapper {
      margin-top: 1rem;

      .excerpt {
        font-size: 0.95rem;
        color: var(--textColor);
        opacity: 0.8;
      }

      .readmore {
        display: inline-block;
        margin-top: 0.5rem;
        color: var(--accentColor);
        text-decoration: none;
        font-size: 0.9rem;

        &::after {
          margin-left: 0.3rem;
        }

        &:hover {
          color: var(--accentColorDark);
        }
      }
    }
  }
}
</style>
