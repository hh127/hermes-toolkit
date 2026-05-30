// 工具函数

/**
 * 解析侧边栏数据
 */
export function resolveSidebarItems(page: any, regularPath: string, site: any, localePath: string) {
  if (!page || !site) return []

  const { pages = [], themeConfig = {} } = site

  const localeConfig = localePath && themeConfig.locales
    ? (themeConfig.locales[localePath] || themeConfig)
    : themeConfig

  const pageSidebarConfig = page.frontmatter.sidebar || localeConfig.sidebar || themeConfig.sidebar

  if (pageSidebarConfig === 'auto') {
    return resolveHeaders(page)
  }

  const sidebarConfig = localeConfig.sidebar || themeConfig.sidebar

  if (!sidebarConfig) {
    return []
  }

  const { base, config } = resolveMatchingConfig(regularPath, sidebarConfig)

  if (config === 'auto') {
    return resolveHeaders(page)
  }

  return config
    ? config.map((item: any) => resolveItem(item, pages, base))
    : []
}

/**
 * 解析页面标题
 */
function resolveHeaders(page: any) {
  const headers = groupHeaders(page.headers || [])
  return [{
    type: 'group',
    collapsable: false,
    title: page.title,
    path: null,
    children: headers.map((h: any) => ({
      type: 'auto',
      title: h.title,
      basePath: page.path,
      path: page.path + '#' + h.slug,
      children: h.children || []
    }))
  }]
}

/**
 * 分组标题
 */
export function groupHeaders(headers: any[]) {
  headers = headers.map(h => ({ ...h }))
  let lastH2: any

  headers.forEach(h => {
    if (h.level === 2) {
      lastH2 = h
    } else if (lastH2) {
      (lastH2.children || (lastH2.children = [])).push(h)
    }
  })

  return headers.filter(h => h.level === 2)
}

/**
 * 解析导航链接
 */
export function resolveNavLinkItem(linkItem: any) {
  return {
    ...linkItem,
    type: linkItem.items && linkItem.items.length ? 'links' : 'link'
  }
}

/**
 * 解析匹配配置
 */
function resolveMatchingConfig(regularPath: string, config: any) {
  if (Array.isArray(config)) {
    return {
      base: '/',
      config
    }
  }

  for (const base in config) {
    if (ensureEndingSlash(regularPath).indexOf(encodeURI(base)) === 0) {
      return {
        base,
        config: config[base]
      }
    }
  }

  return {}
}

/**
 * 确保路径以斜杠结尾
 */
function ensureEndingSlash(path: string) {
  return /(\.html|\/)$/.test(path)
    ? path
    : path + '/'
}

/**
 * 解析侧边栏项
 */
function resolveItem(item: any, pages: any[], base: string, groupDepth = 1): any {
  if (typeof item === 'string') {
    return resolvePage(pages, item, base)
  } else if (Array.isArray(item)) {
    return {
      ...resolvePage(pages, item[0], base),
      title: item[1]
    }
  } else {
    if (groupDepth > 3) {
      console.error('[vuepress] detected a too deep nested sidebar group.')
    }

    const children = item.children || []

    if (children.length === 0 && item.path) {
      return {
        ...resolvePage(pages, item.path, base),
        title: item.title
      }
    }

    return {
      type: 'group',
      path: item.path,
      title: item.title,
      sidebarDepth: item.sidebarDepth,
      initialOpenGroupIndex: item.initialOpenGroupIndex,
      children: children.map((child: any) => resolveItem(child, pages, base, groupDepth + 1)),
      collapsable: item.collapsable !== false
    }
  }
}

/**
 * 解析页面
 */
function resolvePage(pages: any[], rawPath: string, base: string) {
  if (isExternal(rawPath)) {
    return {
      type: 'external',
      path: rawPath
    }
  }

  if (base) {
    rawPath = resolvePath(rawPath, base)
  }

  const path = normalize(rawPath)

  for (let i = 0; i < pages.length; i++) {
    if (normalize(pages[i].regularPath) === path) {
      return {
        ...pages[i],
        type: 'page',
        path: ensureExt(pages[i].path)
      }
    }
  }

  console.error(`[vuepress] No matching page found for sidebar item "${rawPath}"`)
  return {}
}

/**
 * 解析路径
 */
function resolvePath(relative: string, base: string, append?: boolean) {
  const firstChar = relative.charAt(0)

  if (firstChar === '/') {
    return relative
  }

  if (firstChar === '?' || firstChar === '#') {
    return base + relative
  }

  const stack = base.split('/')

  if (!append || !stack[stack.length - 1]) {
    stack.pop()
  }

  const segments = relative.replace(/^\//, '').split('/')

  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i]
    if (segment === '..') {
      stack.pop()
    } else if (segment !== '.') {
      stack.push(segment)
    }
  }

  if (stack[0] !== '') {
    stack.unshift('')
  }

  return stack.join('/')
}

/**
 * 标准化路径
 */
function normalize(path: string) {
  return decodeURI(path)
    .replace(/#.*$/, '')
    .replace(/\.(md|html)$/, '')
}

/**
 * 确保扩展名
 */
function ensureExt(path: string) {
  if (isExternal(path)) {
    return path
  }

  if (!path) return '404'

  const hashMatch = path.match(/#.*$/)
  const hash = hashMatch ? hashMatch[0] : ''
  const normalized = normalize(path)

  if (/\/$/.test(normalized)) {
    return path
  }

  return normalized + '.html' + hash
}

/**
 * 判断是否为外部链接
 */
function isExternal(path: string) {
  return /^[a-z]+:/i.test(path)
}

/**
 * 类型判断
 */
export function type(o: any): string {
  const s = Object.prototype.toString.call(o)
  return s.match(/\[object (.*?)\]/)![1].toLowerCase()
}

/**
 * 日期格式化
 */
export function dateFormat(date: Date): string {
  if (!(date instanceof Date)) {
    date = new Date(date)
  }
  return `${date.getUTCFullYear()}-${zero(date.getUTCMonth() + 1)}-${zero(date.getUTCDate())}`
}

/**
 * 小于10补0
 */
function zero(d: number): string {
  return d.toString().padStart(2, '0')
}

/**
 * 获取时间的时间戳
 */
export function getTimeNum(post: any): number {
  let dateStr = post.frontmatter.date || post.lastUpdated || new Date()
  let date = new Date(dateStr)

  if (date.toString() === 'Invalid Date' && dateStr) {
    date = new Date(dateStr.replace(/-/g, '/'))
  }

  return date.getTime()
}

/**
 * 比对时间
 */
export function compareDate(a: any, b: any): number {
  return getTimeNum(b) - getTimeNum(a)
}

/**
 * 将特殊符号编码（应用于url）
 */
export function encodeUrl(str: string): string {
  str = str + ''
  str = str.replace(/ |((?=[\x21-\x7e]+)[^A-Za-z0-9])/g, '-')
  return str
}
