#!/usr/bin/env python3
"""
导入城市价格数据
将Windows采集的JSON数据导入数据库
"""
import json
import sys
import os
from datetime import date
from models import init_db, get_connection, get_categories


def import_prices(json_file):
    """导入价格数据"""
    print("="*60)
    print("导入城市价格数据")
    print("="*60)
    
    # 读取JSON文件
    if not os.path.exists(json_file):
        print(f"❌ 文件不存在: {json_file}")
        return 0
    
    with open(json_file, 'r', encoding='utf-8') as f:
        prices = json.load(f)
    
    print(f"读取到 {len(prices)} 条数据")
    
    if not prices:
        return 0
    
    # 初始化数据库
    init_db()
    categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    conn = get_connection()
    cursor = conn.cursor()
    
    saved = 0
    for p in prices:
        # 确定分类
        category_id = categories.get('钢筋', 1)
        
        # 构建材料名称
        material_name = p['name']
        if p.get('spec'):
            material_name += f" {p['spec']}"
        if p.get('brand'):
            material_name += f" ({p['brand']})"
        
        # 获取日期
        collect_date = p.get('date', date.today().isoformat())
        
        # 检查是否已存在
        cursor.execute("""
            SELECT id FROM material_prices 
            WHERE material_name = ? AND city = ? AND collect_date = ?
        """, (material_name, p.get('city', '西安'), collect_date))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO material_prices 
                (category_id, material_name, price, specification, brand, city, source, collect_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                category_id,
                material_name,
                p['price'],
                p.get('spec', ''),
                p.get('brand', ''),
                p.get('city', '西安'),
                '我的钢铁网',
                collect_date
            ))
            saved += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 成功导入 {saved} 条数据")
    
    # 显示统计
    print(f"\n数据统计:")
    cities = {}
    for p in prices:
        city = p.get('city', '西安')
        cities[city] = cities.get(city, 0) + 1
    
    for city, count in cities.items():
        print(f"  {city}: {count} 条")
    
    return saved


if __name__ == '__main__':
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        # 查找最新的JSON文件
        import glob
        files = glob.glob('xian_prices_*.json')
        if files:
            json_file = max(files)
        else:
            print("用法: python import_prices.py <json_file>")
            print("示例: python import_prices.py xian_prices_2026-05-29.json")
            sys.exit(1)
    
    import_prices(json_file)
