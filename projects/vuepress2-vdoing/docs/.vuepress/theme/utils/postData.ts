/**
 * 文章数据处理工具
 * 用于过滤、排序、分组文章数据
 */

/**
 * 过滤非文章页
 * @param posts 所有页面数据
 * @returns 过滤后的文章数据
 */
export function filterPosts(posts: any[]): any[] {
  return posts.filter(item => {
    const { frontmatter } = item
    if (!frontmatter) return false
    const { pageComponent, article, home } = frontmatter
    // 存在页面组件、article字段为false，以及首页都排除
    return !(pageComponent || article === false || home === true)
  })
}

/**
 * 按置顶和时间排序
 * @param posts 过滤非文章页之后的文章数据
 * @returns 排序后的文章数据
 */
export function sortPosts(posts: any[]): any[] {
  return [...posts].sort((prev, next) => {
    const prevSticky = prev.frontmatter?.sticky
    const nextSticky = next.frontmatter?.sticky
    if (prevSticky && nextSticky) {
      return prevSticky === nextSticky ? compareDate(prev, next) : (prevSticky - nextSticky)
    } else if (prevSticky && !nextSticky) {
      return -1
    } else if (!prevSticky && nextSticky) {
      return 1
    }
    return compareDate(prev, next)
  })
}

/**
 * 仅按时间排序
 * @param posts 过滤非文章页之后的文章数据
 * @returns 排序后的文章数据
 */
export function sortPostsByDate(posts: any[]): any[] {
  return [...posts].sort((prev, next) => compareDate(prev, next))
}

/**
 * 按分类和标签分组
 * @param posts 按时间排序之后的文章数据
 * @returns 分组后的数据
 */
export function groupPosts(posts: any[]): { categories: Record<string, any[]>, tags: Record<string, any[]> } {
  const categoriesObj: Record<string, any[]> = {}
  const tagsObj: Record<string, any[]> = {}

  for (let i = 0; i < posts.length; i++) {
    const { frontmatter } = posts[i]
    if (!frontmatter) continue

    const { categories, tags } = frontmatter

    if (Array.isArray(categories)) {
      categories.forEach(item => {
        if (item) {
          if (!categoriesObj[item]) {
            categoriesObj[item] = []
          }
          categoriesObj[item].push(posts[i])
        }
      })
    }

    if (Array.isArray(tags)) {
      tags.forEach(item => {
        if (item) {
          if (!tagsObj[item]) {
            tagsObj[item] = []
          }
          tagsObj[item].push(posts[i])
        }
      })
    }
  }

  return {
    categories: categoriesObj,
    tags: tagsObj
  }
}

/**
 * 获取所有分类和标签
 * @param groupedPosts 按分类和标签分组之后的文章数据
 * @returns 分类和标签数组
 */
export function categoriesAndTags(groupedPosts: { categories: Record<string, any[]>, tags: Record<string, any[]> }): { categories: any[], tags: any[] } {
  const categoriesArr: any[] = []
  const tagsArr: any[] = []

  for (const key in groupedPosts.categories) {
    categoriesArr.push({
      name: key,
      length: groupedPosts.categories[key].length
    })
  }

  for (const key in groupedPosts.tags) {
    tagsArr.push({
      name: key,
      length: groupedPosts.tags[key].length
    })
  }

  return {
    categories: categoriesArr,
    tags: tagsArr
  }
}

/**
 * 获取时间的时间戳
 */
export function getTimeNum(post: any): number {
  let dateStr = post.frontmatter?.date || post.lastUpdated || new Date()
  let date = new Date(dateStr)

  if (date.toString() === 'Invalid Date' && dateStr) {
    date = new Date(dateStr.replace(/-/g, '/'))
  }

  return date.getTime()
}

/**
 * 比对时间（新的在前）
 */
export function compareDate(a: any, b: any): number {
  return getTimeNum(b) - getTimeNum(a)
}
