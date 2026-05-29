#!/bin/bash
# 工程材料价格自动采集脚本
# 用法: 
#   手动运行: ./auto_collect.sh
#   定时任务: 0 8 * * * cd /home/hh127/material-price-tracker && ./auto_collect.sh >> collect.log 2>&1

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/collect.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> "$LOG_FILE"
echo "采集时间: $DATE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# 激活虚拟环境
source .venv/bin/activate

# 执行采集
python main.py collect >> "$LOG_FILE" 2>&1

echo "采集完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
