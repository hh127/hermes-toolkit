/**
 * VuePress 2.x 组合式函数
 * 替代 VuePress 1.x 的 mixin 方式
 */
import { computed } from 'vue'
import { useSiteData } from 'vuepress/client'
import { filterPosts, sortPosts, sortPostsByDate, groupPosts, categoriesAndTags } from '../utils/postData'

/**
 * 文章数据组合式函数
 * 提供 $sortPosts, $groupPosts, $categoriesAndTags 等数据
 */
export function usePosts() {
  const site = useSiteData()

  // 过滤非文章页和首页的文章数据
  const filterPostsData = computed(() => {
    return filterPosts(site.value?.pages || [])
  })

  // 按置顶和时间排序的文章数据
  const sortPostsData = computed(() => {
    return sortPosts(filterPostsData.value)
  })

  // 仅按时间排序的文章数据
  const sortPostsByDateData = computed(() => {
    return sortPostsByDate(filterPostsData.value)
  })

  // 按分类和标签分组的文章数据
  const groupPostsData = computed(() => {
    return groupPosts(sortPostsData.value)
  })

  // 所有分类和标签数据
  const categoriesAndTagsData = computed(() => {
    return categoriesAndTags(groupPostsData.value)
  })

  // 文章总数
  const postCount = computed(() => filterPostsData.value.length)

  // 分类总数
  const categoriesCount = computed(() => categoriesAndTagsData.value.categories.length)

  // 标签总数
  const tagsCount = computed(() => categoriesAndTagsData.value.tags.length)

  return {
    filterPosts: filterPostsData,
    sortPosts: sortPostsData,
    sortPostsByDate: sortPostsByDateData,
    groupPosts: groupPostsData,
    categoriesAndTags: categoriesAndTagsData,
    postCount,
    categoriesCount,
    tagsCount
  }
}
