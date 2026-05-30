import { computed } from 'vue'
import { usePageData, usePageFrontmatter, useSiteData } from 'vuepress/client'
import type { VdoingThemeOptions } from '../../index'

/**
 * 获取主题配置
 */
export function useThemeData() {
  const site = useSiteData()
  return computed(() => {
    // VuePress 2 中主题配置通过 site.themeConfig 传递
    return (site.value.themeConfig || {}) as VdoingThemeOptions
  })
}

/**
 * 获取文章列表（用于分类、标签、归档）
 */
export function usePosts() {
  const site = useSiteData()
  const themeData = useThemeData()

  const posts = computed(() => {
    const pages = site.value.pages || []
    return pages
      .filter((page: any) => {
        // 过滤掉非文章页面
        const path = page.path
        if (!path) return false
        // 排除目录页、分类页、标签页、归档页
        if (
          path.startsWith('/categories/') ||
          path.startsWith('/tags/') ||
          path.startsWith('/archives/') ||
          path === '/' ||
          path.endsWith('/README.html')
        ) {
          return false
        }
        return true
      })
      .map((page: any) => ({
        title: page.title || '',
        path: page.path,
        frontmatter: page.frontmatter || {},
        date: page.git?.updatedTime
          ? new Date(page.git.updatedTime).toISOString().split('T')[0]
          : '',
        excerpt: page.excerpt || '',
      }))
      .sort((a: any, b: any) => {
        if (a.date && b.date) {
          return new Date(b.date).getTime() - new Date(a.date).getTime()
        }
        return 0
      })
  })

  /**
   * 按分类分组
   */
  const categories = computed(() => {
    const map: Record<string, any[]> = {}
    posts.value.forEach((post: any) => {
      const cat = post.frontmatter.categories || ['未分类']
      cat.forEach((c: string) => {
        if (!map[c]) map[c] = []
        map[c].push(post)
      })
    })
    return map
  })

  /**
   * 按标签分组
   */
  const tags = computed(() => {
    const map: Record<string, any[]> = {}
    posts.value.forEach((post: any) => {
      const tagList = post.frontmatter.tags || []
      tagList.forEach((t: string) => {
        if (!map[t]) map[t] = []
        map[t].push(post)
      })
    })
    return map
  })

  /**
   * 按年份分组（归档）
   */
  const archives = computed(() => {
    const map: Record<string, any[]> = {}
    posts.value.forEach((post: any) => {
      const year = post.date ? post.date.substring(0, 4) : '未知'
      if (!map[year]) map[year] = []
      map[year].push(post)
    })
    return map
  })

  return {
    posts,
    categories,
    tags,
    archives,
  }
}

/**
 * 获取当前页面信息
 */
export function usePageInfo() {
  const page = usePageData()
  const frontmatter = usePageFrontmatter()

  const isHome = computed(() => {
    return frontmatter.value.home === true
  })

  const isArticle = computed(() => {
    const fm = frontmatter.value as any
    return !fm.home && !fm.pageComponent
  })

  const title = computed(() => {
    return (page.value as any).title || ''
  })

  return {
    page,
    frontmatter,
    isHome,
    isArticle,
    title,
  }
}
