#!/usr/bin/env python3
"""
我的钢铁网详细数据采集
获取规格、品牌、价格和页面链接
"""
import requests
import json
import re
import time
import random
from datetime import date
from bs4 import BeautifulSoup
from models import init_db, insert_price, get_categories

# Cookie 文件
COOKIES_FILE = 'mysteel_cookies.json'

# 详细数据源 - 包含规格和品牌信息
DETAILED_SOURCES = {
    '螺纹钢': {
        'url': 'https://index.mysteel.com/price/indexPrice.html',
        'category': '钢筋',
        'unit': '元/吨',
        'specs': ['HRB400 Φ12', 'HRB400 Φ18-25', 'HRB400E Φ18-25'],
        'brands': ['沙钢', '永钢', '中天', '马钢'],
    },
    '热轧板卷': {
        'url': 'https://index.mysteel.com/price/indexPrice.html',
        'category': '钢筋',
        'unit': '元/吨',
        'specs': ['Q235B 5.5*1500*C', 'Q235B 3.0*1250*C'],
        'brands': ['鞍钢', '本钢', '日照'],
    },
    '冷轧板卷': {
        'url': 'https://index.mysteel.com/price/indexPrice.html',
        'category': '钢筋',
        'unit': '元/吨',
        'specs': ['SPCC 1.0*1250*C', 'DC01 1.0*1250*C'],
        'brands': ['鞍钢', '本钢', '首钢'],
    },
    '中厚板': {
        'url': 'https://index.mysteel.com/price/indexPrice.html',
        'category': '钢筋',
        'unit': '元/吨',
        'specs': ['Q235B 20mm', 'Q345B 20mm'],
        'brands': ['鞍钢', '营口', '唐钢'],
    },
    '铜': {
        'url': 'https://index.mysteel.com/price/indexPrice.html',
        'category': '铝合金',
        'unit': '元/吨',
        'specs': ['1#电解铜', '升贴水'],
        'brands': ['江铜', '铜陵', '金川'],
    },
    '铝': {
        'url': 'https://index.mysteel.com/price/indexPrice.html',
        'category': '铝合金',
        'unit': '元/吨',
        'specs': ['A00铝锭', '6063铝棒'],
        'brands': ['中铝', '南山', '忠旺'],
    },
}

# 首页 URL 映射
HOMEPAGE_URL = 'https://www.mysteel.com/'
PRICE_CENTER_URL = 'https://price.mysteel.com/'


def load_cookies():
    """加载 Cookie"""
    try:
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}


def create_session():
    """创建会话"""
    session = requests.Session()
    cookies = load_cookies()
    if cookies:
        session.cookies.update(cookies)
    
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://www.mysteel.com/',
    })
    
    return session


def extract_detailed_from_homepage(session):
    """从首页提取详细数据"""
    print("从首页提取详细数据...")
    
    response = session.get(HOMEPAGE_URL, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    prices = []
    today = date.today().isoformat()
    
    # 材料名称和价格的映射
    material_price_map = {
        '螺纹钢': {'category': '钢筋', 'unit': '元/吨'},
        '热轧板卷': {'category': '钢筋', 'unit': '元/吨'},
        '冷轧板卷': {'category': '钢筋', 'unit': '元/吨'},
        '中厚板': {'category': '钢筋', 'unit': '元/吨'},
        '铜': {'category': '铝合金', 'unit': '元/吨'},
        '铝': {'category': '铝合金', 'unit': '元/吨'},
        '锌': {'category': '铝合金', 'unit': '元/吨'},
        '铅': {'category': '铝合金', 'unit': '元/吨'},
        '镍': {'category': '铝合金', 'unit': '元/吨'},
        '硅锰': {'category': '其他', 'unit': '元/吨'},
        '铸造生铁': {'category': '其他', 'unit': '元/吨'},
    }
    
    # 提取价格
    price_numbers = re.findall(r'(\d{4}\.\d{2})', html)
    seen = set()
    
    for price_str in price_numbers:
        if price_str in seen:
            continue
        
        price = float(price_str)
        idx = html.find(price_str)
        if idx < 0:
            continue
        
        # 获取上下文
        context = html[max(0, idx-200):idx]
        
        # 查找匹配的材料
        for material_name, info in material_price_map.items():
            if material_name in context:
                key = f"{material_name}_{price}"
                if key not in seen and 1000 < price < 100000:
                    seen.add(key)
                    
                    # 查找相关链接
                    link_pattern = rf'href="([^"]*{re.escape(material_name)}[^"]*)"'
                    link_match = re.search(link_pattern, html)
                    source_url = link_match.group(1) if link_match else HOMEPAGE_URL
                    
                    # 确定规格（根据材料类型）
                    spec = ''
                    if material_name == '螺纹钢':
                        spec = 'HRB400 Φ18-25'
                    elif material_name == '热轧板卷':
                        spec = 'Q235B 5.5mm'
                    elif material_name == '冷轧板卷':
                        spec = 'SPCC 1.0mm'
                    elif material_name == '中厚板':
                        spec = 'Q235B 20mm'
                    elif material_name == '铜':
                        spec = '1#电解铜'
                    elif material_name == '铝':
                        spec = 'A00铝锭'
                    
                    prices.append({
                        'name': material_name,
                        'price': price,
                        'spec': spec,
                        'brand': '',
                        'category': info['category'],
                        'unit': info['unit'],
                        'source_url': source_url,
                        'date': today,
                    })
                break
    
    return prices


def extract_from_index_page(session):
    """从指数页面提取数据"""
    print("从指数页面提取数据...")
    
    try:
        response = session.get('https://index.mysteel.com/price/indexPrice.html', timeout=30)
        response.encoding = 'utf-8'
        html = response.text
        
        prices = []
        today = date.today().isoformat()
        
        # 查找价格数据
        # 模式: 品种名 价格 涨跌
        pattern = r'([\u4e00-\u9fa5]{2,6})\s*(\d{4,6}\.\d+)\s*([+-]?\d+\.?\d*)'
        matches = re.findall(pattern, html)
        
        for name, price_str, change_str in matches:
            try:
                price = float(price_str)
                change = float(change_str) if change_str else 0
                
                if 1000 < price < 100000:
                    # 确定分类
                    category = '钢筋'
                    if name in ['铜', '铝', '锌', '铅', '镍']:
                        category = '铝合金'
                    
                    prices.append({
                        'name': name,
                        'price': price,
                        'spec': '',
                        'brand': '',
                        'category': category,
                        'unit': '元/吨',
                        'source_url': 'https://index.mysteel.com/price/indexPrice.html',
                        'change_amount': change,
                        'change_percent': round(change / price * 100, 2) if price > 0 else 0,
                        'date': today,
                    })
            except:
                continue
        
        return prices
        
    except Exception as e:
        print(f"指数页面提取失败: {e}")
        return []


def save_detailed_prices(prices):
    """保存详细价格数据"""
    init_db()
    categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    saved = 0
    for p in prices:
        cat_id = categories.get(p.get('category', '钢筋'), 1)
        
        success = insert_price(
            category_id=cat_id,
            material_name=p['name'],
            price=p['price'],
            specification=p.get('spec', ''),
            brand=p.get('brand', ''),
            city='全国',
            source='我的钢铁网',
            collect_date=p['date'],
            source_url=p.get('source_url', ''),
            unit=p.get('unit', '元/吨'),
            change_amount=p.get('change_amount'),
            change_percent=p.get('change_percent'),
        )
        
        if success:
            saved += 1
    
    return saved


def main():
    """主函数"""
    print("=" * 60)
    print("我的钢铁网 - 详细数据采集")
    print("=" * 60)
    
    session = create_session()
    all_prices = []
    
    # 1. 从首页提取
    homepage_prices = extract_detailed_from_homepage(session)
    all_prices.extend(homepage_prices)
    print(f"  首页提取: {len(homepage_prices)} 条")
    
    time.sleep(2)
    
    # 2. 从指数页面提取
    index_prices = extract_from_index_page(session)
    all_prices.extend(index_prices)
    print(f"  指数页面提取: {len(index_prices)} 条")
    
    # 去重
    seen = set()
    unique_prices = []
    for p in all_prices:
        key = f"{p['name']}_{p['price']}"
        if key not in seen:
            seen.add(key)
            unique_prices.append(p)
    
    print(f"\n总计: {len(unique_prices)} 条唯一数据")
    
    # 显示数据
    print("\n" + "=" * 60)
    print("采集的数据:")
    print("=" * 60)
    
    for p in unique_prices:
        change_str = ''
        if p.get('change_amount'):
            change = p['change_amount']
            if change > 0:
                change_str = f" ↑{change:.2f}"
            elif change < 0:
                change_str = f" ↓{abs(change):.2f}"
        
        print(f"\n{p['name']}:")
        print(f"  价格: ¥{p['price']:.2f}{change_str}")
        if p.get('spec'):
            print(f"  规格: {p['spec']}")
        print(f"  来源: {p.get('source_url', '-')}")
    
    # 保存到数据库
    if unique_prices:
        print("\n" + "=" * 60)
        print("保存到数据库...")
        print("=" * 60)
        
        saved = save_detailed_prices(unique_prices)
        print(f"\n✅ 成功保存 {saved} 条数据")
    
    return unique_prices


if __name__ == '__main__':
    main()
