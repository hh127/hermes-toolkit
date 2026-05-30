import fs from 'fs'
import path from 'path'

interface SidebarItem {
  text: string
  link?: string
  children?: SidebarItem[]
  collapsible?: boolean
}

/**
 * 自动生成结构化侧边栏
 * 扫描 docs 目录，根据文件夹结构生成侧边栏配置
 */
export function generateSidebar(sourceDir: string): Record<string, SidebarItem[]> {
  const sidebar: Record<string, SidebarItem[]> = {}
  const docsDir = path.resolve(sourceDir)

  // 排除的目录
  const excludeDirs = ['.vuepress', 'node_modules', '@pages', '_posts']

  // 扫描一级目录
  const topDirs = fs.readdirSync(docsDir).filter(item => {
    const fullPath = path.join(docsDir, item)
    return fs.statSync(fullPath).isDirectory() && !excludeDirs.includes(item)
  })

  for (const dir of topDirs) {
    const dirPath = path.join(docsDir, dir)
    const prefix = `/${dir}/`
    const items = scanDirectory(dirPath, prefix, docsDir)

    if (items.length) {
      sidebar[prefix] = items
    }
  }

  return sidebar
}

/**
 * 递归扫描目录
 */
function scanDirectory(
  dirPath: string,
  prefix: string,
  docsDir: string
): SidebarItem[] {
  const items: SidebarItem[] = []

  if (!fs.existsSync(dirPath)) return items

  const entries = fs.readdirSync(dirPath).sort()

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry)
    const stat = fs.statSync(fullPath)

    if (stat.isDirectory()) {
      // 子目录 - 递归处理
      const children = scanDirectory(fullPath, `${prefix}${entry}/`, docsDir)
      if (children.length) {
        items.push({
          text: entry.replace(/^\d+\./, ''), // 去掉序号前缀
          children,
          collapsible: true,
        })
      }
    } else if (entry.endsWith('.md') && entry !== 'README.md') {
      // Markdown 文件
      const title = getTitleFromMd(fullPath) || entry.replace(/\.md$/, '').replace(/^\d+\./, '')
      const relativePath = path.relative(docsDir, fullPath)
      const link = '/' + relativePath.replace(/\.md$/, '.html')

      items.push({
        text: title,
        link,
      })
    }
  }

  return items
}

/**
 * 从 Markdown 文件中提取标题
 */
function getTitleFromMd(filePath: string): string | null {
  try {
    const content = fs.readFileSync(filePath, 'utf-8')

    // 检查 frontmatter 中的 title
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/)
    if (frontmatterMatch) {
      const titleMatch = frontmatterMatch[1].match(/^title:\s*(.+)$/m)
      if (titleMatch) {
        return titleMatch[1].trim().replace(/^['"]|['"]$/g, '')
      }
    }

    // 检查第一个 # 标题
    const h1Match = content.match(/^#\s+(.+)$/m)
    if (h1Match) {
      return h1Match[1].trim()
    }

    return null
  } catch {
    return null
  }
}
