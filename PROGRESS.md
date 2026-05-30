# Hermes Toolkit 开发进度

最后更新: 2026-05-30 (vuepress2-vdoing 完整复刻)

---

## 进行中

### material-price-tracker (工程材料价格跟踪系统)
- [x] Web 仪表盘框架 (Flask + Chart.js)
- [x] 数据模型设计 (10类材料)
- [x] 命令行工具 (main.py)
- [x] 价格预警系统
- [x] 数据导出 (CSV/JSON)
- [x] 多种采集器开发
- [ ] **真实数据采集** (阻塞: mysteel城市价格页JS加密)
- [ ] 分城市数据展示
- [ ] 定时自动采集 (cron)

### vuepress2-vdoing (工程造价知识库)
- [x] VuePress 2.x 项目框架
- [x] 自定义 vdoing2 主题
- [x] 18个核心组件
- [x] 基础样式 (含暗色模式)
- [x] 构建流程可运行
- [x] 完整复刻原版 vdoing 主题 (24个组件)
- [x] SCSS 样式系统 (Stylus → SCSS)
- [x] Vue 3 Composition API 重构
- [x] 工具函数 (侧边栏解析/路径/存储)
- [x] 自动侧边栏生成 (node/sidebar.ts)
- [x] 自动frontmatter设置 (node/frontmatter.ts)
- [x] 文章数据聚合 (composables/usePosts.ts)
- [x] 卡片容器 (cardList/cardImgList)
- [x] 标题徽章 (titleBadge)
- [ ] 补充内容页面

---

## 已完成

### 基础设施
- [x] hermes-toolkit 仓库结构
- [x] GitHub 远程仓库配置
- [x] 开发工作流技能 (dev-workflow)
- [x] 自动提交脚本

---

## 待规划

### material-price-tracker
- Windows Selenium + Edge 采集方案
- 自动导入采集数据到 SQLite
- 更多数据源接入 (造价通、水泥网)
- 价格预测模型

### vuepress2-vdoing
- 博客功能
- 评论系统
- 搜索优化
- 部署到 GitHub Pages / Vercel

### 新项目想法
- 工程量计算工具
- 定额查询系统
- 造价指标分析平台

---

## 已知问题

### material-price-tracker
1. **mysteel.com 城市价格加密**: 使用 data-encrypt + JUNI 混淆JS，requests/cookie 无法绕过
   - 临时方案: 首页静态均价可采集
   - 最佳方案: Windows Selenium + Edge
2. **WSL Chromium 下载慢**: Playwright/pyppeteer 下载 ~183MB 超时
   - 方案: 使用 Windows 浏览器

### vuepress2-vdoing
1. **SCSS deprecation 警告**: sass 版本兼容问题
   - 不影响构建，可忽略
2. **插件版本分裂**: VuePress core rc.30 vs plugins rc.130
   - 已锁定版本，可正常工作

---

## 技术栈速查

| 项目 | 技术栈 | 入口文件 |
|------|--------|----------|
| material-price-tracker | Flask + SQLite + Chart.js | app.py / main.py |
| vuepress2-vdoing | VuePress 2.x + Vue 3 + Vite | docs/.vuepress/config.ts |
| hermes-toolkit | Git + Shell | README.md |

---

## 提交规范

```
feat: 新功能
fix: 修复
docs: 文档
refactor: 重构
style: 样式
test: 测试
chore: 构建/工具
auto: 自动提交
```
