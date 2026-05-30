#!/usr/bin/env python3
"""
增强版分析报告模块
支持多种报告类型、图表、导出
"""
import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
import json
import os

from models import get_connection
from analyzer import (
    get_price_data, calculate_price_change, get_category_summary,
    get_material_list
)


def get_report_data(material_name: str = None, days: int = 30) -> Dict:
    """
    获取报告所需的所有数据
    
    Args:
        material_name: 指定材料名称（可选）
        days: 统计天数
    
    Returns:
        报告数据字典
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'period_days': days,
        'target_material': material_name
    }
    
    # 1. 获取最新日期
    cursor.execute("SELECT MAX(collect_date) FROM material_prices")
    data['latest_date'] = cursor.fetchone()[0]
    
    # 2. 获取各分类摘要
    data['category_summary'] = get_category_summary()
    
    # 3. 获取所有材料列表
    all_materials = get_material_list()
    
    # 4. 计算涨跌幅
    material_changes = []
    for m in all_materials:
        change = calculate_price_change(m, days)
        if 'error' not in change and change.get('change_pct') is not None:
            material_changes.append({
                'material': m,
                'current_price': change['current_price'],
                'previous_price': change.get('previous_price'),
                'change': change.get('change', 0),
                'change_pct': change.get('change_pct', 0),
                'current_date': change.get('current_date'),
                'previous_date': change.get('previous_date')
            })
    
    # 按涨跌幅排序
    material_changes.sort(key=lambda x: x['change_pct'], reverse=True)
    
    data['top_gainers'] = material_changes[:10]
    data['top_losers'] = material_changes[-10:] if len(material_changes) > 10 else []
    data['all_changes'] = material_changes
    
    # 5. 如果指定了材料，获取详细数据
    if material_name:
        price_data = get_price_data(material_name, days)
        if price_data:
            prices = [p['price'] for p in price_data]
            data['material_detail'] = {
                'name': material_name,
                'prices': prices,
                'dates': [p['collect_date'] for p in price_data],
                'stats': {
                    'min': min(prices),
                    'max': max(prices),
                    'avg': sum(prices) / len(prices),
                    'std': (sum((p - sum(prices)/len(prices))**2 for p in prices) / len(prices)) ** 0.5,
                    'count': len(prices),
                    'first': prices[0],
                    'last': prices[-1],
                    'change': prices[-1] - prices[0],
                    'change_pct': ((prices[-1] - prices[0]) / prices[0] * 100) if prices[0] > 0 else 0
                }
            }
    
    # 6. 计算整体市场统计
    if material_changes:
        all_changes_pct = [m['change_pct'] for m in material_changes]
        data['market_overview'] = {
            'total_materials': len(material_changes),
            'avg_change_pct': sum(all_changes_pct) / len(all_changes_pct),
            'up_count': len([x for x in all_changes_pct if x > 0]),
            'down_count': len([x for x in all_changes_pct if x < 0]),
            'flat_count': len([x for x in all_changes_pct if x == 0]),
            'max_increase': max(all_changes_pct),
            'max_decrease': min(all_changes_pct)
        }
    
    conn.close()
    return data


def generate_daily_report(material_name: str = None, days: int = 7) -> str:
    """
    生成每日报告
    
    Args:
        material_name: 指定材料（可选）
        days: 统计天数
    
    Returns:
        报告文本
    """
    data = get_report_data(material_name, days)
    
    lines = []
    lines.append("=" * 60)
    lines.append("📊 工程材料价格每日报告")
    lines.append(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"📅 数据日期: {data.get('latest_date', '-')}")
    lines.append(f"📅 统计周期: 近{days}天")
    lines.append("=" * 60)
    
    # 市场概览
    if 'market_overview' in data:
        overview = data['market_overview']
        lines.append("")
        lines.append("📈 市场概览")
        lines.append("-" * 40)
        lines.append(f"  监控材料: {overview['total_materials']} 种")
        lines.append(f"  平均涨跌幅: {overview['avg_change_pct']:+.2f}%")
        lines.append(f"  上涨材料: {overview['up_count']} 种")
        lines.append(f"  下跌材料: {overview['down_count']} 种")
        lines.append(f"  持平材料: {overview['flat_count']} 种")
        lines.append(f"  最大涨幅: {overview['max_increase']:+.2f}%")
        lines.append(f"  最大跌幅: {overview['max_decrease']:+.2f}%")
    
    # 涨幅排行
    lines.append("")
    lines.append("🔴 涨幅排行 TOP 10")
    lines.append("-" * 40)
    for i, item in enumerate(data.get('top_gainers', [])[:10], 1):
        lines.append(f"  {i:2d}. {item['material']}")
        lines.append(f"      当前: ¥{item['current_price']:.2f} | 涨幅: +{item['change_pct']:.2f}%")
    
    # 跌幅排行
    lines.append("")
    lines.append("🟢 跌幅排行 TOP 10")
    lines.append("-" * 40)
    for i, item in enumerate(data.get('top_losers', [])[:10], 1):
        lines.append(f"  {i:2d}. {item['material']}")
        lines.append(f"      当前: ¥{item['current_price']:.2f} | 跌幅: {item['change_pct']:.2f}%")
    
    # 材料详情
    if material_name and 'material_detail' in data:
        detail = data['material_detail']
        stats = detail['stats']
        lines.append("")
        lines.append(f"📊 {material_name} 详细分析")
        lines.append("-" * 40)
        lines.append(f"  当前价格: ¥{stats['last']:.2f}")
        lines.append(f"  {days}天前价格: ¥{stats['first']:.2f}")
        lines.append(f"  价格变化: ¥{stats['change']:+.2f} ({stats['change_pct']:+.2f}%)")
        lines.append("")
        lines.append(f"  统计信息:")
        lines.append(f"    最高价: ¥{stats['max']:.2f}")
        lines.append(f"    最低价: ¥{stats['min']:.2f}")
        lines.append(f"    平均价: ¥{stats['avg']:.2f}")
        lines.append(f"    标准差: ¥{stats['std']:.2f}")
        lines.append(f"    波动率: {(stats['std']/stats['avg']*100):.2f}%")
        lines.append(f"    数据点: {stats['count']} 个")
    
    # 分类统计
    lines.append("")
    lines.append("📦 分类统计")
    lines.append("-" * 40)
    for cat in data.get('category_summary', []):
        lines.append(f"  【{cat['category']}】")
        lines.append(f"    材料数: {cat['material_count']} | 单位: {cat['unit']}")
        lines.append(f"    均价: ¥{cat['avg_price']:.2f} | 区间: ¥{cat['min_price']:.2f} ~ ¥{cat['max_price']:.2f}")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("报告结束")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def generate_weekly_report() -> str:
    """生成周报"""
    return generate_daily_report(days=7)


def generate_monthly_report() -> str:
    """生成月报"""
    return generate_daily_report(days=30)


def get_report_html_data(material_name: str = None, days: int = 30) -> Dict:
    """
    获取用于前端展示的报告数据（JSON格式）
    
    Returns:
        包含图表数据和统计数据的字典
    """
    data = get_report_data(material_name, days)
    
    # 准备图表数据
    chart_data = {
        'category_pie': {
            'labels': [c['category'] for c in data.get('category_summary', [])],
            'values': [c['material_count'] for c in data.get('category_summary', [])]
        },
        'gainers_bar': {
            'labels': [g['material'][:15] for g in data.get('top_gainers', [])[:5]],
            'values': [g['change_pct'] for g in data.get('top_gainers', [])[:5]]
        },
        'losers_bar': {
            'labels': [l['material'][:15] for l in data.get('top_losers', [])[:5]],
            'values': [l['change_pct'] for l in data.get('top_losers', [])[:5]]
        }
    }
    
    # 如果有材料详情，添加趋势数据
    if material_name and 'material_detail' in data:
        chart_data['material_trend'] = {
            'dates': data['material_detail']['dates'],
            'prices': data['material_detail']['prices']
        }
    
    return {
        'report_data': data,
        'chart_data': chart_data,
        'summary': {
            'total_materials': data.get('market_overview', {}).get('total_materials', 0),
            'avg_change': data.get('market_overview', {}).get('avg_change_pct', 0),
            'up_count': data.get('market_overview', {}).get('up_count', 0),
            'down_count': data.get('market_overview', {}).get('down_count', 0),
            'latest_date': data.get('latest_date', '')
        }
    }


if __name__ == '__main__':
    print(generate_daily_report())
