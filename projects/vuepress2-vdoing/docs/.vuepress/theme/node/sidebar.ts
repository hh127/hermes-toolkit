/**
 * 自动生成结构化侧边栏
 */

import fs from 'fs'
import path from 'path'

/**
 * 生成侧边栏数据
 * @param sourceDir docs 目录路径
 * @param collapsable 是否可折叠
 * @returns 侧边栏数据
 */
export function createSidebarData(sourceDir: string, collapsable = true): Record<string, any> {
  const sidebarData: Record<string, any> = {}
  const tocs = readTocs(sourceDir)

  tocs.forEach(toc => {
    if (toc.endsWith('_posts')) {
      // 碎片化文章不需要生成结构化侧边栏
    } else {
      const sidebarObj = mapTocToSidebar(toc, collapsable)
      if (sidebarObj.sidebar.length) {
        sidebarData[`/${path.basename(toc)}/`] = sidebarObj.sidebar
      }
    }
  })

  return sidebarData
}

/**
 * 读取指定目录下的文件夹路径
 */
function readTocs(root: string): string[] {
  const result: string[] = []
  const files = fs.readdirSync(root)
  files.forEach(name => {
    const file = path.resolve(root, name)
    if (fs.statSync(file).isDirectory() && name !== '.vuepress' && name !== '@pages' && name !== 'node_modules') {
      result.push(file)
    }
  })
  return result
}

/**
 * 将目录映射为侧边栏配置数据
 */
function mapTocToSidebar(root: string, collapsable: boolean, prefix = ''): { sidebar: any[] } {
  let sidebar: any[] = []
  const files = fs.readdirSync(root)

  files.forEach(filename => {
    if (filename === '.DS_Store' || filename === 'node_modules') return

    const file = path.resolve(root, filename)
    const stat = fs.statSync(file)

    const fileNameArr = filename.split('.')
    const isDir = stat.isDirectory()
    let order = '', title = '', type = ''

    if (fileNameArr.length === 2) {
      order = fileNameArr[0]
      title = fileNameArr[1]
    } else {
      const firstDotIndex = filename.indexOf('.')
      const lastDotIndex = filename.lastIndexOf('.')
      order = filename.substring(0, firstDotIndex)
      type = filename.substring(lastDotIndex + 1)
      if (isDir) {
        title = filename.substring(firstDotIndex + 1)
      } else {
        title = filename.substring(firstDotIndex + 1, lastDotIndex)
      }
    }

    const orderNum = parseInt(order, 10)
    if (isNaN(orderNum) || orderNum < 0) return

    if (sidebar[orderNum]) {
      // 序号重复，会被覆盖
    }

    if (isDir) {
      sidebar[orderNum] = {
        title,
        collapsable,
        children: mapTocToSidebar(file, collapsable, prefix + filename + '/').sidebar
      }
    } else {
      if (type !== 'md') return

      // 读取 frontmatter 获取 title 和 titleTag
      let titleFromFrontmatter = title
      let titleTag = ''
      try {
        const content = fs.readFileSync(file, 'utf8')
        const matterMatch = content.match(/^---\n([\s\S]*?)\n---/)
        if (matterMatch) {
          const titleMatch = matterMatch[1].match(/title:\s*(.+)/)
          if (titleMatch) {
            titleFromFrontmatter = titleMatch[1].trim().replace(/^['"]|['"]$/g, '')
          }
          const titleTagMatch = matterMatch[1].match(/titleTag:\s*(.+)/)
          if (titleTagMatch) {
            titleTag = titleTagMatch[1].trim().replace(/^['"]|['"]$/g, '')
          }
        }
      } catch {
        // 读取失败使用文件名
      }

      const item: any[] = [prefix + filename, titleFromFrontmatter]
      if (titleTag) item.push(titleTag)
      sidebar[orderNum] = item
    }
  })

  sidebar = sidebar.filter(item => item !== null && item !== undefined)
  return { sidebar }
}
