#!/usr/bin/env python3
"""
自动导入价格数据
扫描目录中的新JSON文件并导入数据库
"""
import json
import os
import glob
import shutil
from datetime import date
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, '/home/hh127/material-price-tracker')

from models import init_db, get_connection, get_categories


# 配置
WATCH_DIR = '/home/hh127/material-price-tracker'
PROCESSED_DIR = '/home/hh127/material-price-tracker/imported'


def ensure_dirs():
    """确保目录存在"""
    Path(PROCESSED_DIR).mkdir(exist_ok=True)


def find_new_files():
    """查找新的价格文件"""
    pattern = os.path.join(WATCH_DIR, '*_prices_*.json')
    return glob.glob(pattern)


def import_file(json_file):
    """导入单个文件"""
    print(f"导入: {os.path.basename(json_file)}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            prices = json.load(f)
        
        if not prices:
            print("  ⚠️ 文件为空")
            return 0
        
        init_db()
        categories = {cat['name']: cat['id'] for cat in get_categories()}
        
        conn = get_connection()
        cursor = conn.cursor()
        
        saved = 0
        for p in prices:
            category_id = categories.get('钢筋', 1)
            
            material_name = p['name']
            if p.get('spec'):
                material_name += f" {p['spec']}"
            if p.get('brand'):
                material_name += f" ({p['brand']})"
            
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
                    category_id, material_name, p['price'],
                    p.get('spec', ''), p.get('brand', ''),
                    p.get('city', '西安'), '我的钢铁网', collect_date
                ))
                saved += 1
        
        conn.commit()
        conn.close()
        
        print(f"  ✅ 导入 {saved} 条数据")
        
        # 移动到已处理目录
        processed_file = os.path.join(PROCESSED_DIR, os.path.basename(json_file))
        shutil.move(json_file, processed_file)
        
        return saved
        
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        return 0


def main():
    """主函数"""
    ensure_dirs()
    
    files = find_new_files()
    
    if not files:
        print("没有新文件需要导入")
        return
    
    print(f"找到 {len(files)} 个新文件")
    
    total = 0
    for f in files:
        total += import_file(f)
    
    print(f"\n总计导入 {total} 条数据")


if __name__ == '__main__':
    main()
