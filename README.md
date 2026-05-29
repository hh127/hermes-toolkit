# Hermes Toolkit

Hermes Agent 自动化脚本和工具集合，适用于 NAS 和服务器环境。

## 目录结构

```
hermes-toolkit/
├── scripts/
│   ├── networking/      # 网络、代理、VPN、DNS
│   ├── monitoring/      # 监控、日志、报警、健康检查
│   ├── media/          # 媒体处理、下载、转码
│   ├── system/         # 系统运维、备份、清理
│   ├── devtools/       # 开发工具、构建、部署
│   └── utilities/      # 杂项工具、数据处理
├── projects/           # 完整项目
│   └── material-price-tracker/  # 工程材料价格跟踪系统
├── docs/               # 文档、使用说明
└── README.md
```

## 使用方式

### 克隆仓库
```bash
git clone https://github.com/hh127/hermes-toolkit.git
```

### 在 Hermes 中使用
将脚本链接到 PATH 或直接调用：
```bash
# 例如运行监控脚本
python3 /path/to/hermes-toolkit/scripts/monitoring/check_services.py
```

## 脚本规范

每个脚本遵循以下规范：
1. 包含完整的文档注释（用途、参数、示例）
2. 错误处理和日志输出
3. 配置文件使用 YAML 或环境变量
4. 支持 `--help` 参数（Python 脚本）

## 许可证

MIT License
