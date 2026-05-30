#!/usr/bin/env python3
"""
使用 pyppeteer 获取解密后的价格数据
"""
import asyncio
import json
import re
import os
from datetime import date
from bs4 import BeautifulSoup
from models import init_db, get_connection, get_categories

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(BASE_DIR, 'mysteel_cookies.json')

# 城市价格页面
CITY_URLS = {
    '西安': 'https://jiancai.mysteel.com/m/26052910/892658956BF3E75C.html',
}


async def collect_with_browser():
    """使用浏览器采集价格"""
    from pyppeteer import launch
    
    print("="*60)
    print("使用Pyppeteer采集西安钢材价格")
    print("="*60)
    
    # 加载Cookie
    with open(COOKIES_FILE, 'r') as f:
        cookies = json.load(f)
    
    print(f"\n加载 {len(cookies)} 个Cookie")
    
    # 启动浏览器
    print("启动浏览器...")
    browser = await launch({
        'headless': True,
        'args': ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    })
    
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    
    # 设置Cookie
    for name, value in cookies.items():
        await page.setCookie({
            'name': name,
            'value': value,
            'domain': '.mysteel.com',
            'path': '/',
        })
    
    # 访问西安价格页面
    url = CITY_URLS['西安']
    print(f"\n访问: {url}")
    
    await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})
    
    # 等待JS解密
    print("等待JavaScript解密...")
    await asyncio.sleep(5)
    
    # 获取解密后的内容
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    
    # 解析表格
    tables = soup.find_all('table')
    all_prices = []
    
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) <= 5:
            continue
        
        print(f"\n找到表格: {len(rows)} 行")
        
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) < 5:
                continue
            
            name = cells[0].get_text(strip=True)
            spec = cells[1].get_text(strip=True)
            material = cells[2].get_text(strip=True)
            brand = cells[3].get_text(strip=True)
            price_text = cells[4].get_text(strip=True)
            change_text = cells[5].get_text(strip=True) if len(cells) > 5 else ''
            
            # 提取价格
            price_match = re.search(r'(\d{3,4}(?:\.\d+)?)', price_text)
            if price_match and name:
                price = float(price_match.group(1))
                
                # 提取涨跌
                change = 0
                change_match = re.search(r'([+-]?\d+(?:\.\d+)?)', change_text)
                if change_match:
                    change = float(change_match.group(1))
                
                all_prices.append({
                    'name': name,
                    'spec': spec,
                    'material': material,
                    'brand': brand,
                    'price': price,
                    'change': change,
                    'city': '西安',
                })
    
    await browser.close()
    
    print(f"\n✅ 采集到 {len(all_prices)} 条价格数据")
    
    # 显示前10条
    if all_prices:
        print("\n前10条数据:")
        for i, p in enumerate(all_prices[:10]):
            print(f"  {i+1}. {p['name']} {p['spec']} {p['brand']}: ¥{p['price']}")
    
    return all_prices


def save_prices(prices):
    """保存到数据库"""
    if not prices:
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
        
        # 检查是否已存在
        cursor.execute("""
            SELECT id FROM material_prices 
            WHERE material_name = ? AND city = ? AND collect_date = ?
        """, (material_name, p['city'], date.today().isoformat()))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO material_prices 
                (category_id, material_name, price, specification, brand, city, source, collect_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                category_id, material_name, p['price'],
                p.get('spec', ''), p.get('brand', ''),
                p['city'], '我的钢铁网', date.today().isoformat()
            ))
            saved += 1
    
    conn.commit()
    conn.close()
    
    return saved


if __name__ == '__main__':
    prices = asyncio.run(collect_with_browser())
    saved = save_prices(prices)
    print(f"\n✅ 保存 {saved} 条数据到数据库")
