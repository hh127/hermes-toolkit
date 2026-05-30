#!/bin/bash
# 自动提交并推送 hermes-toolkit
# 用法: ./auto-commit.sh "提交信息"

REPO_DIR="/mnt/d/github/Hermes/hermes-toolkit"
cd "$REPO_DIR" || exit 1

# 检查是否有变更
if [ -z "$(git status --porcelain)" ]; then
    echo "✓ 没有变更需要提交"
    exit 0
fi

# 显示变更文件
echo "=== 变更文件 ==="
git status --short
echo ""

# 生成提交信息
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
DEFAULT_MSG="auto: 更新于 $TIMESTAMP"
COMMIT_MSG="${1:-$DEFAULT_MSG}"

# 执行推送
echo "=== 提交信息 ==="
echo "$COMMIT_MSG"
echo ""

git add -A
git commit -m "$COMMIT_MSG"

echo ""
echo "=== 推送到远程 ==="
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 推送成功: $COMMIT_MSG"
else
    echo ""
    echo "✗ 推送失败，请检查网络或权限"
    exit 1
fi
