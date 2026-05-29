#!/bin/bash
# 我的钢铁网定时采集脚本
# 用法: 
#   首页快速采集: ./mysteel_collect.sh --homepage
#   全品种采集: ./mysteel_collect.sh --all
#   指定品种: ./mysteel_collect.sh 螺纹钢 热轧板卷
#
# 定时任务（每小时采集一次）:
#   0 * * * * cd /home/hh127/material-price-tracker && ./mysteel_collect.sh --homepage >> mysteel_collect.log 2>&1

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/mysteel_collect.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> "$LOG_FILE"
echo "采集时间: $DATE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# 激活虚拟环境
source .venv/bin/activate

# 执行采集
if [ "$1" = "--homepage" ] || [ -z "$1" ]; then
    echo "模式: 首页快速采集" >> "$LOG_FILE"
    python mysteel_smart_collector.py --homepage >> "$LOG_FILE" 2>&1
elif [ "$1" = "--all" ]; then
    echo "模式: 全品种采集" >> "$LOG_FILE"
    python mysteel_smart_collector.py --all >> "$LOG_FILE" 2>&1
else
    echo "模式: 指定品种采集 - $@" >> "$LOG_FILE"
    python mysteel_smart_collector.py "$@" >> "$LOG_FILE" 2>&1
fi

echo "采集完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
