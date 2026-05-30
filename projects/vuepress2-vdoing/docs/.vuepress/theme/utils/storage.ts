// 简单的本地存储工具

export const storage = {
  get(key: string, defaultValue: any = null): any {
    try {
      const value = localStorage.getItem(key)
      return value ? JSON.parse(value) : defaultValue
    } catch {
      return defaultValue
    }
  },

  set(key: string, value: any): void {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch {
      // 忽略存储错误
    }
  },

  remove(key: string): void {
    try {
      localStorage.removeItem(key)
    } catch {
      // 忽略删除错误
    }
  },

  clear(): void {
    try {
      localStorage.clear()
    } catch {
      // 忽略清空错误
    }
  }
}

export default storage
