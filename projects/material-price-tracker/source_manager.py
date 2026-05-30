#!/usr/bin/env python3
"""
数据来源管理模块
管理不同数据来源，支持来源筛选、统计
"""
import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional
from models import get_connection

SOURCES_FILE = os.path.join(os.path.dirname(__file__), 'data_sources.json')


def get_default_sources() -> List[Dict]:
    """获取默认数据来源列表"""
    return [
        {
            'id': 'zjtc',
            'name': '造价通',
            'url': 'https://www.zjtcy.com',
            'description': '全国建设工程造价数据平台',
            'category': '综合平台',
            'enabled': True,
            'icon': 'bi-building'
        },
        {
            'id': 'mysteel',
            'name': '我的钢铁网',
            'url': 'https://www.mysteel.com',
            'description': '钢铁行业价格资讯',
            'category': '钢铁',
            'enabled': True,
            'icon': 'bi-gear'
        },
        {
            'id': 'cement3c',
            'name': '水泥网',
            'url': 'http://www.cement3c.com',
            'description': '水泥行业价格信息',
            'category': '水泥',
            'enabled': True,
            'icon': 'bi-box'
        },
        {
            'id': 'local',
            'name': '本地录入',
            'url': '',
            'description': '手动录入的本地数据',
            'category': '本地',
            'enabled': True,
            'icon': 'bi-pencil'
        },
        {
            'id': 'simulated',
            'name': '模拟数据',
            'url': '',
            'description': '系统生成的模拟数据（演示用）',
            'category': '系统',
            'enabled': True,
            'icon': 'bi-robot'
        }
    ]


def load_sources() -> List[Dict]:
    """加载数据来源列表"""
    if not os.path.exists(SOURCES_FILE):
        # 创建默认配置
        sources = get_default_sources()
        save_sources(sources)
        return sources
    
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_sources(sources: List[Dict]):
    """保存数据来源列表"""
    with open(SOURCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)


def add_source(source_data: Dict) -> Dict:
    """添加数据来源"""
    sources = load_sources()
    
    source = {
        'id': source_data.get('id', f'custom_{len(sources)}'),
        'name': source_data.get('name'),
        'url': source_data.get('url', ''),
        'description': source_data.get('description', ''),
        'category': source_data.get('category', '其他'),
        'enabled': source_data.get('enabled', True),
        'icon': source_data.get('icon', 'bi-link'),
        'created_at': datetime.now().isoformat()
    }
    
    sources.append(source)
    save_sources(sources)
    
    return source


def update_source(source_id: str, source_data: Dict) -> bool:
    """更新数据来源"""
    sources = load_sources()
    
    for source in sources:
        if source['id'] == source_id:
            source.update(source_data)
            save_sources(sources)
            return True
    
    return False


def delete_source(source_id: str) -> bool:
    """删除数据来源"""
    sources = load_sources()
    sources = [s for s in sources if s['id'] != source_id]
    save_sources(sources)
    return True


def toggle_source(source_id: str, enabled: bool) -> bool:
    """启用/禁用数据来源"""
    sources = load_sources()
    
    for source in sources:
        if source['id'] == source_id:
            source['enabled'] = enabled
            save_sources(sources)
            return True
    
    return False


def get_source_stats() -> List[Dict]:
    """获取各数据来源的统计信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取各来源的数据量
    cursor.execute("""
        SELECT 
            source,
            COUNT(*) as total_records,
            COUNT(DISTINCT material_name) as material_count,
            MIN(collect_date) as earliest_date,
            MAX(collect_date) as latest_date
        FROM material_prices
        GROUP BY source
        ORDER BY total_records DESC
    """)
    
    stats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # 合并来源配置和统计
    sources = load_sources()
    source_map = {s['id']: s for s in sources}
    
    result = []
    for stat in stats:
        source_name = stat['source'] or '未知'
        # 尝试匹配来源配置
        matched_source = None
        for s in sources:
            if s['name'] == source_name or source_name in s.get('name', ''):
                matched_source = s
                break
        
        result.append({
            'source_id': matched_source['id'] if matched_source else 'unknown',
            'source_name': source_name,
            'total_records': stat['total_records'],
            'material_count': stat['material_count'],
            'earliest_date': stat['earliest_date'],
            'latest_date': stat['latest_date'],
            'enabled': matched_source['enabled'] if matched_source else True,
            'icon': matched_source['icon'] if matched_source else 'bi-question'
        })
    
    return result


def get_materials_by_source(source_name: str = None) -> List[Dict]:
    """根据数据来源获取材料列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if source_name:
        cursor.execute("""
            SELECT DISTINCT material_name, category_id
            FROM material_prices
            WHERE source = ?
            ORDER BY material_name
        """, (source_name,))
    else:
        cursor.execute("""
            SELECT DISTINCT material_name, category_id
            FROM material_prices
            ORDER BY material_name
        """)
    
    materials = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return materials


def get_prices_by_source(source_name: str = None, category: str = None, city: str = None) -> List[Dict]:
    """根据数据来源获取价格列表，支持城市筛选"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT p.*, c.name as category_name, c.unit
        FROM material_prices p
        JOIN material_categories c ON p.category_id = c.id
        WHERE p.collect_date = (SELECT MAX(collect_date) FROM material_prices)
    """
    params = []
    
    if source_name:
        query += " AND p.source = ?"
        params.append(source_name)
    
    if category:
        query += " AND c.name = ?"
        params.append(category)
    
    if city:
        query += " AND p.city = ?"
        params.append(city)
    
    query += " ORDER BY c.name, p.material_name"
    
    cursor.execute(query, params)
    prices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return prices


def get_cities() -> List[str]:
    """获取所有城市列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT city 
        FROM material_prices 
        WHERE city IS NOT NULL AND city != ''
        ORDER BY city
    """)
    
    cities = [row['city'] for row in cursor.fetchall()]
    conn.close()
    
    return cities


def get_city_price_summary(city: str = None) -> List[Dict]:
    """获取城市价格汇总"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if city and city != '全国':
        # 获取指定城市的最新价格
        cursor.execute("""
            SELECT 
                c.name as category_name,
                p.material_name,
                p.price,
                p.specification,
                p.brand,
                p.city,
                p.source,
                p.collect_date,
                c.unit
            FROM material_prices p
            JOIN material_categories c ON p.category_id = c.id
            WHERE p.city = ?
            AND p.collect_date = (SELECT MAX(collect_date) FROM material_prices WHERE city = ?)
            ORDER BY c.name, p.material_name
        """, (city, city))
    else:
        # 获取全国汇总（首页数据）
        cursor.execute("""
            SELECT 
                c.name as category_name,
                p.material_name,
                p.price,
                p.specification,
                p.brand,
                p.city,
                p.source,
                p.collect_date,
                c.unit
            FROM material_prices p
            JOIN material_categories c ON p.category_id = c.id
            WHERE p.collect_date = (SELECT MAX(collect_date) FROM material_prices)
            AND (p.city = '全国' OR p.city IS NULL OR p.city = '')
            ORDER BY c.name, p.material_name
        """)
    
    prices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return prices


if __name__ == '__main__':
    print("数据来源统计:")
    for stat in get_source_stats():
        print(f"  {stat['source_name']}: {stat['total_records']} 条记录, {stat['material_count']} 种材料")
