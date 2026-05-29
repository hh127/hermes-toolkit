#!/bin/bash
# 预警自动检查脚本
# 用法: 
#   手动运行: ./check_alerts.sh
#   定时任务: */30 * * * * cd /home/hh127/material-price-tracker && ./check_alerts.sh >> alert.log 2>&1

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/alert.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> "$LOG_FILE"
echo "预警检查时间: $DATE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# 激活虚拟环境
source .venv/bin/activate

# 执行预警检查
python3 << 'EOF' >> "$LOG_FILE" 2>&1
from alert_manager import check_alerts
from datetime import datetime

print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

triggered = check_alerts()

if triggered:
    print(f"⚠️ 发现 {len(triggered)} 个触发的预警:")
    for t in triggered:
        print(f"  - {t['message']}")
else:
    print("✅ 无触发的预警")
EOF

echo "检查完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
