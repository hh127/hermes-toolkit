#!/usr/bin/env python3
"""
我的钢铁网自动采集脚本 - 从首页提取价格数据
"""
import requests
import json
import re
import os
import sys
from datetime import date
from bs4 import BeautifulSoup

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_db, insert_price, get_categories

COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'mysteel_cookies.json')

# 材料分类映射
CATEGORY_MAP = {
    '大宗商品': '钢筋',
    '普钢': '钢筋',
    '特钢': '钢筋',
    '螺纹钢': '钢筋',
    '热轧板卷': '钢筋',
    '冷轧板卷': '钢筋',
    '中厚板': '钢筋',
    '焦炭': '其他',
    '硅锰': '其他',
    '废钢': '其他',
    '铸造生铁': '其他',
}


def load_cookies():
    """加载 Cookie"""
    if not os.path.exists(COOKIES_FILE):
        return {}
    
    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_prices_from_homepage():
    """从我的钢铁网首页提取价格数据"""
    cookies = load_cookies()
    
    if not cookies:
        print("❌ 未找到 Cookie，请先设置")
        return []
    
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    })
    
    try:
        response = session.get('https://www.mysteel.com/', timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        prices = []
        seen = set()
        
        # 查找所有 index-item 相关的元素
        items = soup.find_all(class_=re.compile(r'index-item'))
        
        for item in items:
            text = item.get_text()
            
            # 使用正则提取材料名和价格
            matches = re.findall(r'([\u4e00-\u9fa5]{2,6})\s*(\d{4}\.\d+)', text)
            
            for name, price_str in matches:
                price = float(price_str)
                key = f'{name}_{price}'
                
                if key not in seen and price > 1000:
                    seen.add(key)
                    prices.append({
                        'name': name,
                        'price': price,
                        'date': date.today().isoformat()
                    })
        
        return prices
        
    except Exception as e:
        print(f"❌ 采集失败: {e}")
        return []


def save_to_database(prices):
    """保存价格数据到数据库"""
    init_db()
    categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    saved = 0
    for p in prices:
        name = p['name']
        price = p['price']
        
        category_name = CATEGORY_MAP.get(name, '钢筋')
        category_id = categories.get(category_name, 1)
        
        success = insert_price(
            category_id=category_id,
            material_name=name,
            price=price,
            specification='',
            brand='',
            city='全国',
            source='我的钢铁网',
            collect_date=p['date']
        )
        
        if success:
            saved += 1
    
    return saved


def main():
    """主函数"""
    print("=== 我的钢铁网自动采集 ===\n")
    
    # 提取价格
    prices = extract_prices_from_homepage()
    
    if not prices:
        print("⚠️ 未提取到价格数据")
        return
    
    print(f"提取到 {len(prices)} 条价格数据:")
    for p in prices:
        print(f"  {p['name']}: ¥{p['price']}")
    
    # 保存到数据库
    saved = save_to_database(prices)
    
    print(f"\n✅ 成功保存 {saved} 条数据到数据库")


if __name__ == '__main__':
    main()
