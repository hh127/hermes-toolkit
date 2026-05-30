---
# ═══════════════════════════════════════════════════════
# 法规文件通用 Frontmatter 模板
# 兼容：VuePress Vdoing 主题 + Obsidian
# ═══════════════════════════════════════════════════════
#
# 【Vdoing 必需字段】
title: 中华人民共和国XXXX法
date: 2025-01-01 00:00:00          # 创建时间（Vdoing 格式：YYYY-MM-DD HH:mm:ss）
permalink: /pages/xxxxxx/          # 永久链接（6位随机码，自动生成）
categories:                        # 按目录层级，与文件夹对应
  - 现行法律                       # → 10.现行法律/
  - 民法商法                       # → 30.民法商法/
tags: []                           # 自定义标签（如：建设工程, 合同, 招投标）

# 【Vdoing 可选字段】
author:
  name: Lin
  link: https://github.com/hh127
sidebar: false                     # 法规页不显示侧边栏
article: false                     # 标记为非文章页（不显示面包屑、时间等）
comment: false                     # 关闭评论
editLink: false                    # 关闭编辑链接

# ═══════════════════════════════════════════════════════
# 以下为法规元数据（Vdoing 会忽略未知字段，Obsidian 识别为 Properties）
# ═══════════════════════════════════════════════════════

# 【法规身份信息】
issuer: 国务院                      # 制定机关
doc_number: 国务院令第709号          # 发文字号
announced: 2019-03-02               # 公布日期
effective: 2019-03-02               # 实施日期
status: 现行有效                    # 时效性：现行有效 / 已废止 / 暂行
legal_level: 行政法规               # 效力位阶（与目录名对应）
regulation_type: 建设综合规定        # 法规类别
last_modified: 2024-01-12           # 最后修改时间
source: https://xxx.gov.cn/xxx      # 原文链接（可选）

# 【Obsidian 兼容字段】
aliases:                            # 别名（Obsidian 搜索/跳转用）
  - 简称1
  - 简称2
created: 2025-01-01                 # 创建日期（Obsidian 格式：YYYY-MM-DD）
updated: 2025-01-01                 # 更新日期
---
