# 工程材料价格跟踪系统

自动采集工程大宗材料价格，分析价格变化趋势，支持 Web 仪表盘和命令行两种方式。

## 功能特点

- 📊 **10大类材料**：钢筋、水泥、混凝土、砂石、木材、玻璃、铝合金、沥青、电缆、管材
- 📈 **价格趋势分析**：折线图展示价格走势
- 🔍 **材料搜索**：快速查找材料价格
- 📋 **分析报告**：自动生成价格分析报告
- 💾 **本地存储**：SQLite 数据库，无需额外配置
- 🌐 **Web 仪表盘**：图形化界面，支持多种图表
- 🔔 **价格预警**：设置阈值，超限提醒
- 📥 **数据导出**：支持 CSV/JSON 格式

## 快速开始

### 方式一：Web 仪表盘（推荐）

```bash
# 1. 安装依赖
pip install -r requirements.txt
pip install -r requirements-web.txt

# 2. 初始化并生成示例数据
python main.py init
python main.py seed

# 3. 启动 Web 服务
python app.py

# 4. 访问浏览器
# http://localhost:5000
```

### 方式二：命令行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化并生成示例数据
python main.py init
python main.py seed

# 3. 使用命令
python main.py list          # 查看材料分类
python main.py latest        # 查看最新价格
python main.py price "HRB400 Φ18-25"  # 价格分析
python main.py trend "HRB400 Φ18-25"  # 生成趋势图
python main.py report        # 生成报告
```

## Web 仪表盘功能

### 1. 仪表盘
- 今日价格概览
- 涨跌幅排行榜
- 材料分类饼图
- 价格走势图

### 2. 价格列表
- 所有材料最新价格
- 支持搜索和筛选
- 可查看详情和趋势

### 3. 价格趋势
- 选择材料查看历史走势
- 支持 7天/30天/60天/90天
- 显示统计信息（最高/最低/平均）

### 4. 材料对比
- 同类材料价格走势对比
- 多材料曲线叠加显示

### 5. 价格预警
- 设置价格阈值
- 支持高于/低于条件
- 触发预警提醒

### 6. 分析报告
- 生成文字分析报告
- 包含涨跌幅排行
- 统计信息汇总

### 7. 数据导出
- 导出 CSV（Excel 可直接打开）
- 导出 JSON（程序处理）

## 命令行命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `init` | 初始化数据库 | `python main.py init` |
| `seed` | 生成示例数据 | `python main.py seed` |
| `list` | 列出材料分类 | `python main.py list` |
| `latest` | 查看最新价格 | `python main.py latest [分类]` |
| `price` | 材料价格分析 | `python main.py price <材料名>` |
| `trend` | 价格趋势图 | `python main.py trend <材料名> [天数]` |
| `compare` | 同类对比图 | `python main.py compare <分类> [天数]` |
| `report` | 文字分析报告 | `python main.py report [材料名]` |
| `search` | 搜索材料 | `python main.py search <关键词>` |
| `collect` | 采集今日价格 | `python main.py collect` |

## 定时采集

### 方式一：使用 cron

```bash
# 编辑 crontab
crontab -e

# 添加：每天早上8点采集
0 8 * * * cd /home/hh127/material-price-tracker && ./auto_collect.sh >> collect.log 2>&1
```

### 方式二：手动运行

```bash
./auto_collect.sh
```

## 文件结构

```
material-price-tracker/
├── app.py              # Web API 服务
├── main.py             # 命令行主程序
├── models.py           # 数据库模型
├── collector.py        # 数据采集模块
├── analyzer.py         # 分析和可视化模块
├── seed_data.py        # 示例数据生成
├── templates/
│   └── index.html      # Web 仪表盘页面
├── static/             # 静态资源
├── requirements.txt    # Python 依赖
├── requirements-web.txt # Web 依赖
├── auto_collect.sh     # 自动采集脚本
├── start_web.sh        # Web 启动脚本
├── README.md           # 说明文档
└── *.db                # SQLite 数据库文件
```

## 数据采集

系统支持以下数据源（需根据实际网站结构调整爬虫）：

- 造价通 (zjtcy.com)
- 水泥网 (cement3c.com)
- 我的钢铁网 (mysteel.com)

当无法获取真实数据时，系统会使用模拟数据进行演示。

## API 接口

Web 服务提供以下 RESTful API：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/dashboard` | GET | 仪表盘数据 |
| `/api/categories` | GET | 材料分类列表 |
| `/api/latest` | GET | 最新价格 |
| `/api/price/<name>` | GET | 材料价格分析 |
| `/api/trend/<name>` | GET | 价格趋势数据 |
| `/api/compare/<category>` | GET | 同类材料对比 |
| `/api/search?q=` | GET | 搜索材料 |
| `/api/report` | GET | 生成报告 |
| `/api/export/csv` | GET | 导出 CSV |
| `/api/export/json` | GET | 导出 JSON |
| `/api/alerts` | GET/POST | 预警管理 |
| `/api/check-alerts` | GET | 检查触发预警 |
| `/api/collect` | POST | 手动触发采集 |

## 注意事项

- 示例数据仅供演示，实际价格请以市场行情为准
- 爬虫请遵守网站使用条款，合理设置采集频率
- 建议定期备份 SQLite 数据库文件
- Web 服务默认端口 5000，可通过修改 `app.py` 更改

## 许可证

MIT License
