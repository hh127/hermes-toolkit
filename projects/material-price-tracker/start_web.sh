#!/bin/bash
# 启动工程材料价格跟踪系统 Web 服务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

echo "=================================================="
echo "   工程材料价格跟踪系统 - Web 服务"
echo "=================================================="
echo ""
echo "正在启动服务..."
echo ""

# 激活虚拟环境
source .venv/bin/activate

# 启动 Flask 服务
python app.py
