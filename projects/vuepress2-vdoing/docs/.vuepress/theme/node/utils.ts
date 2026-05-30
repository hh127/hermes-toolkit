/**
 * Node 端工具函数
 * 用于自动设置 frontmatter 和生成侧边栏
 */

import fs from 'fs'
import path from 'path'
import { path as vuepressPath } from '@vuepress/utils'

/**
 * 读取所有 md 文件
 */
export function readFileList(dir: string, filesList: any[] = []): any[] {
  const files = fs.readdirSync(dir)
  files.forEach((item) => {
    const filePath = path.join(dir, item)
    const stat = fs.statSync(filePath)
    if (stat.isDirectory() && item !== '.vuepress' && item !== '@pages' && item !== 'node_modules') {
      readFileList(path.join(dir, item), filesList)
    } else {
      if (path.basename(dir) !== 'docs') {
        const filename = path.basename(filePath)
        const fileNameArr = filename.split('.')
        const firstDotIndex = filename.indexOf('.')
        const lastDotIndex = filename.lastIndexOf('.')

        let name: string | null = null
        if (fileNameArr.length === 2) {
          name = fileNameArr[0]
        } else if (fileNameArr.length >= 3) {
          name = filename.substring(firstDotIndex + 1, lastDotIndex)
        }

        if (filename.endsWith('.md')) {
          filesList.push({
            name,
            filePath
          })
        }
      }
    }
  })
  return filesList
}

/**
 * 日期格式化
 */
export function dateFormat(date: Date): string {
  return `${date.getFullYear()}-${zero(date.getMonth() + 1)}-${zero(date.getDate())} ${zero(date.getHours())}:${zero(date.getMinutes())}:${zero(date.getSeconds())}`
}

/**
 * 小于10补0
 */
function zero(d: number): string {
  return d.toString().padStart(2, '0')
}

/**
 * 获取文件创建时间
 */
export function getBirthtime(stat: fs.Stats): Date {
  return stat.birthtime.getFullYear() !== 1970 ? stat.birthtime : stat.atime
}

/**
 * 类型判断
 */
export function type(o: any): string {
  const s = Object.prototype.toString.call(o)
  return s.match(/\[object (.*?)\]/)![1].toLowerCase()
}

/**
 * 生成永久链接
 */
export function getPermalink(): string {
  return `/pages/${(Math.random() + Math.random()).toString(16).slice(2, 8)}/`
}
