/**
 * 卡片容器 markdown-it 插件
 * 支持 cardList 和 cardImgList 容器
 */
import type { PluginSimple } from 'markdown-it'
import type Token from 'markdown-it/lib/token.mjs'

const CARD_LIST = 'cardList'
const CARD_IMG_LIST = 'cardImgList'

/**
 * 简单的 YAML 解析（不依赖外部库）
 */
function parseYamlSimple(yamlStr: string): any {
  try {
    // 尝试使用 JSON 解析（如果 YAML 格式兼容）
    // 否则返回简单的键值对解析
    const lines = yamlStr.trim().split('\n')
    const result: any = {}
    let currentKey = ''
    let currentArray: any[] = []
    let isArray = false

    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed || trimmed.startsWith('#')) continue

      if (trimmed.startsWith('- ')) {
        // 数组项
        if (!isArray) {
          isArray = true
          currentArray = []
        }
        const value = trimmed.substring(2).trim()
        // 解析对象
        if (value.includes(':')) {
          const obj: any = {}
          const pairs = value.split(',')
          pairs.forEach((pair: string) => {
            const [k, ...v] = pair.split(':')
            if (k && v.length) {
              obj[k.trim()] = v.join(':').trim().replace(/^['"]|['"]$/g, '')
            }
          })
          currentArray.push(obj)
        } else {
          currentArray.push(value.replace(/^['"]|['"]$/g, ''))
        }
      } else if (trimmed.includes(':')) {
        // 保存之前的数组
        if (isArray && currentKey) {
          result[currentKey] = currentArray
          isArray = false
          currentArray = []
        }

        const colonIndex = trimmed.indexOf(':')
        const key = trimmed.substring(0, colonIndex).trim()
        const value = trimmed.substring(colonIndex + 1).trim()

        if (value === '' || value === '|' || value === '>') {
          currentKey = key
          isArray = false
        } else {
          result[key] = value.replace(/^['"]|['"]$/g, '')
          currentKey = key
        }
      } else if (isArray && currentKey) {
        // 继续数组
        currentArray.push(trimmed.replace(/^['"]|['"]$/g, ''))
      }
    }

    // 保存最后的数组
    if (isArray && currentKey) {
      result[currentKey] = currentArray
    }

    return result
  } catch {
    return null
  }
}

/**
 * 渲染普通卡片列表
 */
function getCardListDOM(dataList: any[], row: number, config: any): string {
  const { target = '_blank' } = config
  let listDOM = ''

  dataList.forEach(item => {
    const linkStart = item.link ? `<a href="${item.link}" target="${target}"` : '<span'
    const linkEnd = item.link ? '</a>' : '</span>'
    const bgColorStyle = item.bgColor ? `background-color:${item.bgColor};--randomColor:${item.bgColor};` : '--randomColor: var(--bodyBg);'
    const textColorStyle = item.textColor ? `color:${item.textColor};` : ''
    const avatarHtml = item.avatar ? `<img src="${item.avatar}" class="no-zoom">` : ''

    listDOM += `
      ${linkStart} class="card-item ${row ? 'row-' + row : ''}"
         style="${bgColorStyle}${textColorStyle}"
      >
        ${avatarHtml}
        <div>
          <p class="name">${item.name || ''}</p>
          <p class="desc">${item.desc || ''}</p>
        </div>
      ${linkEnd}
    `
  })

  return listDOM
}

/**
 * 渲染图文卡片列表
 */
function getCardImgListDOM(dataList: any[], row: number, config: any): string {
  const { imgHeight = 'auto', objectFit = 'cover', lineClamp = 1, target = '_blank' } = config

  let listDOM = ''
  dataList.forEach(item => {
    const footerHtml = (item.avatar || item.author) ? `<div class="box-footer">
        ${item.avatar ? `<img src="${item.avatar}" class="no-zoom">` : ''}
        ${item.author ? `<span>${item.author}</span>` : ''}
    </div>` : ''

    listDOM += `
      <div class="card-item ${row ? 'row-' + row : ''}">
        <a href="${item.link}" target="${target}">
          <div class="box-img" style="height: ${imgHeight}">
              <img src="${item.img}" class="no-zoom" style="object-fit: ${objectFit}">
          </div>
          <div class="box-info">
              <p class="name">${item.name || ''}</p>
              ${item.desc ? `<p class="desc" style="-webkit-line-clamp: ${lineClamp}">${item.desc}</p>` : ''}
          </div>
          ${footerHtml}
        </a>
      </div>
    `
  })

  return listDOM
}

/**
 * 卡片容器插件
 */
export const cardListPlugin: PluginSimple = (md) => {
  // 注册 cardList 容器
  md.use((md) => {
    const defaultRender = md.renderer.rules.fence!.bind(md.renderer.rules)

    // 处理 cardList 容器
    md.core.ruler.after('block', 'cardList', (state) => {
      const tokens = state.tokens
      const newTokens: Token[] = []
      let i = 0

      while (i < tokens.length) {
        const token = tokens[i]

        // 检查是否是容器开始
        if (token.type === 'container_cardList_open' || token.type === 'container_cardImgList_open') {
          const containerType = token.type === 'container_cardList_open' ? CARD_LIST : CARD_IMG_LIST
          const END_TYPE = `container_${containerType}_close`

          // 查找容器结束
          let yamlStr = ''
          let endIndex = -1
          let nesting = 0

          for (let j = i; j < tokens.length; j++) {
            if (tokens[j].type === token.type.replace('_open', '')) {
              nesting++
            }
            if (tokens[j].type === END_TYPE) {
              nesting--
              if (nesting === 0) {
                endIndex = j
                break
              }
            }
            // 提取 YAML 内容
            if (tokens[j].type === 'fence' && tokens[j].info.trim() === 'yaml') {
              yamlStr = tokens[j].content
            }
          }

          if (endIndex !== -1 && yamlStr) {
            // 解析 YAML 数据
            const dataObj = parseYamlSimple(yamlStr)
            let dataList: any[] = []
            let config: any = {}

            if (dataObj) {
              if (Array.isArray(dataObj)) {
                dataList = dataObj
              } else {
                config = dataObj.config || {}
                dataList = dataObj.data || []
              }
            }

            if (dataList && dataList.length) {
              // 每行显示几个
              const infoParts = token.info.trim().split(' ')
              let row = Number(infoParts[infoParts.length - 1])
              if (!row || row > 4 || row < 1) {
                row = 3
              }

              let listDOM = ''
              if (containerType === CARD_LIST) {
                listDOM = getCardListDOM(dataList, row, config)
              } else {
                listDOM = getCardImgListDOM(dataList, row, config)
              }

              // 创建 HTML token
              const htmlToken = new state.Token('html_block', '', 0)
              htmlToken.content = `<div class="${containerType}Container"><div class="card-list">${listDOM}</div></div>`
              newTokens.push(htmlToken)

              i = endIndex + 1
              continue
            }
          }
        }

        newTokens.push(token)
        i++
      }

      state.tokens = newTokens
    })
  })
}

export default cardListPlugin
