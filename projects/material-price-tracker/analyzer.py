#!/usr/bin/env python3
"""
材料价格分析与可视化模块
生成价格趋势图表和分析报告
"""
import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
import os
import numpy as np

# 尝试导入绘图库
try:
    import matplotlib
    matplotlib.use('Agg')  # 无头模式
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.font_manager import FontProperties
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

from models import get_connection


# 设置中文字体
if HAS_MATPLOTLIB:
    # 尝试使用系统中文字体
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        'C:/Windows/Fonts/msyh.ttc',  # Windows
    ]
    
    FONT_PROP = None
    for fp in font_paths:
        if os.path.exists(fp):
            FONT_PROP = FontProperties(fname=fp)
            break
    
    if FONT_PROP:
        plt.rcParams['font.family'] = FONT_PROP.get_name()
    else:
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'SimHei', 'Arial Unicode MS']
    
    plt.rcParams['axes.unicode_minus'] = False


def get_price_data(material_name: str, days: int = 30, city: str = None) -> List[Dict]:
    """获取价格数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        collect_date,
        material_name,
        specification,
        brand,
        price,
        city,
        source
    FROM material_prices 
    WHERE material_name LIKE ?
    AND collect_date >= date('now', ?)
    """
    params = [f"%{material_name}%", f"-{days} days"]
    
    if city:
        query += " AND city = ?"
        params.append(city)
    
    query += " ORDER BY collect_date ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_material_list() -> List[str]:
    """获取所有材料名称列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT DISTINCT material_name 
    FROM material_prices 
    ORDER BY material_name
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [row['material_name'] for row in rows]


def get_category_summary() -> List[Dict]:
    """获取各分类价格摘要"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        c.name as category,
        c.unit,
        COUNT(DISTINCT p.material_name) as material_count,
        ROUND(AVG(p.price), 2) as avg_price,
        ROUND(MIN(p.price), 2) as min_price,
        ROUND(MAX(p.price), 2) as max_price,
        p.collect_date as latest_date
    FROM material_prices p
    JOIN material_categories c ON p.category_id = c.id
    WHERE p.collect_date = (SELECT MAX(collect_date) FROM material_prices)
    GROUP BY c.name, c.unit
    ORDER BY c.name
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def calculate_price_change(material_name: str, days: int = 7) -> Dict:
    """计算价格变化"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取最新价格
    cursor.execute("""
    SELECT price, collect_date
    FROM material_prices
    WHERE material_name LIKE ?
    ORDER BY collect_date DESC
    LIMIT 1
    """, (f"%{material_name}%",))
    
    latest = cursor.fetchone()
    if not latest:
        conn.close()
        return {"error": "未找到材料"}
    
    # 获取N天前价格
    cursor.execute("""
    SELECT price, collect_date
    FROM material_prices
    WHERE material_name LIKE ?
    AND collect_date <= date('now', ?)
    ORDER BY collect_date DESC
    LIMIT 1
    """, (f"%{material_name}%", f"-{days} days"))
    
    previous = cursor.fetchone()
    conn.close()
    
    if not previous:
        return {
            "material": material_name,
            "current_price": latest['price'],
            "current_date": latest['collect_date'],
            "previous_price": None,
            "change": None,
            "change_pct": None,
            "days": days,
        }
    
    change = latest['price'] - previous['price']
    change_pct = (change / previous['price']) * 100
    
    return {
        "material": material_name,
        "current_price": latest['price'],
        "current_date": latest['collect_date'],
        "previous_price": previous['price'],
        "previous_date": previous['collect_date'],
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "days": days,
    }


def plot_price_trend(material_name: str, days: int = 30, save_path: str = None) -> str:
    """绘制价格趋势图"""
    if not HAS_MATPLOTLIB:
        print("❌ 需要安装 matplotlib: pip install matplotlib")
        return ""
    
    # 获取数据
    data = get_price_data(material_name, days)
    
    if not data:
        print(f"❌ 未找到 '{material_name}' 的价格数据")
        return ""
    
    # 提取日期和价格
    dates = [datetime.strptime(d['collect_date'], '%Y-%m-%d') for d in data]
    prices = [d['price'] for d in data]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制价格线
    ax.plot(dates, prices, 'b-', linewidth=2, marker='o', markersize=4, label='价格')
    
    # 添加趋势线
    if len(dates) > 1:
        z = np.polyfit(range(len(dates)), prices, 1)
        p = np.poly1d(z)
        ax.plot(dates, p(range(len(dates))), "r--", alpha=0.5, label='趋势线')
    
    # 计算统计信息
    avg_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)
    
    # 添加统计线
    ax.axhline(y=avg_price, color='g', linestyle=':', alpha=0.5, label=f'均价: {avg_price:.2f}')
    
    # 填充价格区间
    ax.fill_between(dates, min_price, max_price, alpha=0.1, color='blue')
    
    # 设置图表
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('价格（元）', fontsize=12)
    ax.set_title(f'{material_name} 价格趋势（近{days}天）', fontsize=14, fontweight='bold')
    
    # 格式化x轴日期
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    # 添加图例
    ax.legend(loc='best')
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    
    # 添加价格注释
    ax.annotate(f'最高: {max_price}', xy=(dates[prices.index(max_price)], max_price),
                xytext=(10, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='red'))
    
    ax.annotate(f'最低: {min_price}', xy=(dates[prices.index(min_price)], min_price),
                xytext=(10, -15), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='green'))
    
    plt.tight_layout()
    
    # 保存图表
    if save_path is None:
        save_path = f"/home/hh127/material-price-tracker/{material_name.replace(' ', '_')}_trend.png"
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 图表已保存: {save_path}")
    return save_path


def plot_category_comparison(category: str, days: int = 30, save_path: str = None) -> str:
    """绘制同类材料价格对比图"""
    if not HAS_MATPLOTLIB:
        print("❌ 需要安装 matplotlib: pip install matplotlib")
        return ""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取该分类下所有材料
    cursor.execute("""
    SELECT DISTINCT p.material_name
    FROM material_prices p
    JOIN material_categories c ON p.category_id = c.id
    WHERE c.name = ?
    AND p.collect_date >= date('now', ?)
    ORDER BY p.material_name
    """, (category, f"-{days} days"))
    
    materials = [row['material_name'] for row in cursor.fetchall()]
    conn.close()
    
    if not materials:
        print(f"❌ 未找到分类 '{category}' 的数据")
        return ""
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(materials)))
    
    for i, material in enumerate(materials):
        data = get_price_data(material, days)
        if data:
            dates = [datetime.strptime(d['collect_date'], '%Y-%m-%d') for d in data]
            prices = [d['price'] for d in data]
            
            # 归一化价格（以第一天为基准）
            if prices[0] > 0:
                normalized = [p / prices[0] * 100 for p in prices]
                ax.plot(dates, normalized, color=colors[i], linewidth=2, 
                       marker='o', markersize=3, label=material[:20])
    
    # 设置图表
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('价格指数（基准=100）', fontsize=12)
    ax.set_title(f'{category} - 各规格价格走势对比（近{days}天）', fontsize=14, fontweight='bold')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = f"/home/hh127/material-price-tracker/{category}_comparison.png"
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 对比图已保存: {save_path}")
    return save_path


def generate_text_report(material_name: str = None, days: int = 30) -> str:
    """生成文字报告（不依赖绘图库）"""
    report = []
    report.append("=" * 60)
    report.append("工程材料价格分析报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)
    
    if material_name:
        # 单一材料报告
        report.append(f"\n📊 {material_name} 价格分析（近{days}天）")
        report.append("-" * 40)
        
        change = calculate_price_change(material_name, days)
        
        if "error" in change:
            report.append(f"❌ {change['error']}")
        else:
            report.append(f"当前价格: ¥{change['current_price']}")
            report.append(f"数据日期: {change['current_date']}")
            
            if change['previous_price']:
                report.append(f"{days}天前价格: ¥{change['previous_price']}")
                report.append(f"价格变化: ¥{change['change']:+.2f} ({change['change_pct']:+.2f}%)")
                
                if change['change'] > 0:
                    report.append("📈 价格上涨")
                elif change['change'] < 0:
                    report.append("📉 价格下跌")
                else:
                    report.append("➡️ 价格持平")
            
            # 获取详细数据
            data = get_price_data(material_name, days)
            if data:
                prices = [d['price'] for d in data]
                report.append(f"\n统计信息:")
                report.append(f"  最高价: ¥{max(prices):.2f}")
                report.append(f"  最低价: ¥{min(prices):.2f}")
                report.append(f"  平均价: ¥{sum(prices)/len(prices):.2f}")
                report.append(f"  价格波动: {(max(prices)-min(prices))/min(prices)*100:.2f}%")
    else:
        # 全部分类摘要
        report.append("\n📦 各分类价格概览")
        report.append("-" * 40)
        
        summaries = get_category_summary()
        
        for s in summaries:
            report.append(f"\n【{s['category']}】")
            report.append(f"  材料种类: {s['material_count']}")
            report.append(f"  计价单位: {s['unit']}")
            report.append(f"  平均价格: ¥{s['avg_price']}")
            report.append(f"  价格区间: ¥{s['min_price']} ~ ¥{s['max_price']}")
        
        # 涨跌幅排行
        report.append("\n\n📈 近7天涨跌幅排行")
        report.append("-" * 40)
        
        materials = get_material_list()
        changes = []
        
        for m in materials[:20]:  # 只取前20个
            change = calculate_price_change(m, 7)
            if "error" not in change and change['change_pct'] is not None:
                changes.append((m, change['change_pct'], change['current_price']))
        
        # 排序
        changes.sort(key=lambda x: x[1], reverse=True)
        
        if changes:
            report.append("\n涨幅前5:")
            for name, pct, price in changes[:5]:
                report.append(f"  {name}: {pct:+.2f}% (¥{price})")
            
            report.append("\n跌幅前5:")
            for name, pct, price in changes[-5:]:
                report.append(f"  {name}: {pct:+.2f}% (¥{price})")
    
    report.append("\n" + "=" * 60)
    report.append("报告结束")
    report.append("=" * 60)
    
    return "\n".join(report)


if __name__ == "__main__":
    import numpy as np
    
    # 生成报告
    report = generate_text_report()
    print(report)
    
    # 保存报告
    with open("/home/hh127/material-price-tracker/report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n报告已保存到 report.txt")
