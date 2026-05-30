/**
 * 自动设置 frontmatter
 * 给 .md 文件设置标题、日期、永久链接等数据
 */

import fs from 'fs'
import path from 'path'
import { readFileList, dateFormat, getBirthtime, getPermalink } from './utils'

/**
 * 给 md 文件设置 frontmatter
 * @param sourceDir docs 目录路径
 * @param themeConfig 主题配置
 */
export function setFrontmatter(sourceDir: string, themeConfig: any): void {
  const { category: isCategory, tag: isTag, categoryText = '随笔' } = themeConfig
  const files = readFileList(sourceDir)

  files.forEach((file: any) => {
    let dataStr = fs.readFileSync(file.filePath, 'utf8')

    // 检查是否已有 frontmatter
    const matterMatch = dataStr.match(/^---\n([\s\S]*?)\n---/)
    if (!matterMatch) {
      // 没有 frontmatter，创建一个
      const stat = fs.statSync(file.filePath)
      const dateStr = dateFormat(getBirthtime(stat))
      const categories = getCategories(file, categoryText)

      let cateLabelStr = ''
      categories.forEach((item: string) => {
        cateLabelStr += '\n  - ' + item
      })

      let cateStr = ''
      if (isCategory !== false) {
        cateStr = '\ncategories:' + cateLabelStr
      }

      const tagsStr = isTag === false ? '' : '\ntags:\n  - '

      const fmData = `---
title: ${file.name}
date: ${dateStr}
permalink: ${getPermalink()}${cateStr}${tagsStr}
---`

      fs.writeFileSync(file.filePath, `${fmData}\n${dataStr}`)
    }
  })
}

/**
 * 获取分类数据
 */
function getCategories(file: any, categoryText: string): string[] {
  let categories: string[] = []

  if (file.filePath.indexOf('_posts') === -1) {
    const filePathArr = file.filePath.split(path.sep)
    filePathArr.pop()

    let ind = filePathArr.indexOf('docs')
    if (ind !== -1) {
      while (filePathArr[++ind] !== undefined) {
        const item = filePathArr[ind]
        const firstDotIndex = item.indexOf('.')
        categories.push(item.substring(firstDotIndex + 1) || '')
      }
    }
  } else {
    const matchResult = file.filePath.match(/_posts\/(\S*)\//)
    const resultStr = matchResult ? matchResult[1] : ''
    const resultArr = resultStr.split('/').filter(Boolean)

    if (resultArr.length) {
      categories.push(...resultArr)
    } else {
      categories.push(categoryText)
    }
  }

  return categories
}
