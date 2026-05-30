import fs from 'fs'
import path from 'path'

/**
 * 生成分类、标签、归档页面
 */
export function generatePages(sourceDir: string) {
  const pagesDir = path.resolve(sourceDir, '@pages')

  // 确保 @pages 目录存在
  if (!fs.existsSync(pagesDir)) {
    fs.mkdirSync(pagesDir, { recursive: true })
  }

  // 分类页
  const categoriesPath = path.join(pagesDir, 'categories.md')
  if (!fs.existsSync(categoriesPath)) {
    fs.writeFileSync(categoriesPath, `---
title: 分类
pageComponent: CategoriesPage
---
`)
  }

  // 标签页
  const tagsPath = path.join(pagesDir, 'tags.md')
  if (!fs.existsSync(tagsPath)) {
    fs.writeFileSync(tagsPath, `---
title: 标签
pageComponent: TagsPage
---
`)
  }

  // 归档页
  const archivesPath = path.join(pagesDir, 'archives.md')
  if (!fs.existsSync(archivesPath)) {
    fs.writeFileSync(archivesPath, `---
title: 归档
pageComponent: ArchivesPage
---
`)
  }
}
