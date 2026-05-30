#!/usr/bin/env python3
"""
我的钢铁网数据采集模块 - Cookie 方式
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import time
import random
import json
import os
from typing import List, Dict, Optional
from models import init_db, insert_price, get_categories

COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'mysteel_cookies.json')

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.mysteel.com/',
}


def save_cookies_from_string(cookie_str: str):
    """从浏览器复制的 Cookie 字符串保存为字典格式"""
    cookies = {}
    for item in cookie_str.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    
    return cookies


def load_cookies() -> dict:
    """加载保存的 Cookie"""
    if not os.path.exists(COOKIES_FILE):
        return {}
    
    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


class MysteelCookieCollector:
    """我的钢铁网采集器 - Cookie 方式"""
    
    # 价格页面 URL
    PRICE_URLS = {
        '螺纹钢': 'https://www.mysteel.com/price/2/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '热轧板卷': 'https://www.mysteel.com/price/3/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '冷轧板卷': 'https://www.mysteel.com/price/4/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '中厚板': 'https://www.mysteel.com/price/5/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '线材': 'https://www.mysteel.com/price/6/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '盘螺': 'https://www.mysteel.com/price/7/0-0-0-0-0-0-0-0-0-0-0-0.html',
    }
    
    # 更多钢材品种 URL
    MORE_URLS = {
        'H型钢': 'https://www.mysteel.com/price/8/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '工字钢': 'https://www.mysteel.com/price/9/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '角钢': 'https://www.mysteel.com/price/10/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '槽钢': 'https://www.mysteel.com/price/11/0-0-0-0-0-0-0-0-0-0-0-0.html',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.categories = {cat['name']: cat['id'] for cat in get_categories()}
        self.logged_in = False
        
        # 加载 Cookie
        cookies = load_cookies()
        if cookies:
            self.session.cookies.update(cookies)
            self.logged_in = True
    
    def check_login(self) -> bool:
        """检查登录状态"""
        try:
            response = self.session.get('https://www.mysteel.com/', timeout=30)
            # 检查是否包含登录状态标识
            if 'login' not in response.url.lower() and response.status_code == 200:
                return True
            return False
        except:
            return False
    
    def collect_prices(self, material_type: str = 'all') -> List[Dict]:
        """采集钢材价格"""
        results = []
        
        if not self.logged_in:
            print("❌ 未登录，请先设置 Cookie")
            return results
        
        # 确定要采集的类型
        if material_type == 'all':
            urls_to_collect = {**self.PRICE_URLS, **self.MORE_URLS}
        elif material_type in self.PRICE_URLS:
            urls_to_collect = {material_type: self.PRICE_URLS[material_type]}
        elif material_type in self.MORE_URLS:
            urls_to_collect = {material_type: self.MORE_URLS[material_type]}
        else:
            print(f"❌ 未知的材料类型: {material_type}")
            return results
        
        for mat_type, url in urls_to_collect.items():
            try:
                print(f"正在采集 {mat_type}...")
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                
                # 解析页面
                prices = self._parse_page(response.text, mat_type)
                results.extend(prices)
                
                print(f"  ✅ 采集到 {len(prices)} 条数据")
                
            except Exception as e:
                print(f"  ❌ 采集 {mat_type} 失败: {e}")
        
        return results
    
    def _parse_page(self, html: str, material_type: str) -> List[Dict]:
        """解析页面 HTML"""
        prices = []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 尝试多种选择器找到价格表格
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all(['td', 'th'])
                
                if len(cols) >= 3:
                    try:
                        # 尝试提取数据
                        name = cols[0].get_text(strip=True)
                        spec = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                        price_text = cols[2].get_text(strip=True) if len(cols) > 2 else ''
                        
                        # 提取价格
                        price = self._extract_price(price_text)
                        
                        if name and price and price > 0:
                            prices.append({
                                'material_type': material_type,
                                'material_name': f"{material_type} {spec}".strip(),
                                'specification': spec,
                                'brand': name,
                                'price': price,
                                'unit': '元/吨',
                                'city': '全国',
                                'date': date.today().isoformat(),
                                'source': '我的钢铁网',
                            })
                    except:
                        continue
        
        # 如果表格解析失败，尝试其他方式
        if not prices:
            prices = self._parse_alternative(soup, material_type)
        
        return prices
    
    def _extract_price(self, text: str) -> Optional[float]:
        """从文本中提取价格"""
        import re
        
        # 移除货币符号和空格
        text = text.replace('¥', '').replace('￥', '').replace(',', '').strip()
        
        # 尝试提取数字
        match = re.search(r'[\d.]+', text)
        if match:
            try:
                return float(match.group())
            except:
                return None
        return None
    
    def _parse_alternative(self, soup: BeautifulSoup, material_type: str) -> List[Dict]:
        """备用解析方法"""
        prices = []
        
        # 查找包含价格的 div 或其他元素
        price_elements = soup.find_all(['div', 'span'], class_=lambda x: x and ('price' in x.lower() or 'jiage' in x.lower()))
        
        for elem in price_elements:
            text = elem.get_text(strip=True)
            price = self._extract_price(text)
            
            if price and price > 100:  # 过滤明显不是价格的数据
                prices.append({
                    'material_type': material_type,
                    'material_name': material_type,
                    'specification': '',
                    'brand': '',
                    'price': price,
                    'unit': '元/吨',
                    'city': '全国',
                    'date': date.today().isoformat(),
                    'source': '我的钢铁网',
                })
        
        return prices
    
    def save_prices(self, prices: List[Dict]) -> int:
        """保存价格数据到数据库"""
        saved_count = 0
        
        for item in prices:
            category_name = self._get_category(item.get('material_type', ''))
            category_id = self.categories.get(category_name, 1)
            
            success = insert_price(
                category_id=category_id,
                material_name=item['material_name'],
                price=item['price'],
                specification=item.get('specification'),
                brand=item.get('brand'),
                city=item.get('city', '全国'),
                source='我的钢铁网',
                collect_date=item.get('date', date.today().isoformat())
            )
            
            if success:
                saved_count += 1
        
        return saved_count
    
    def _get_category(self, material_type: str) -> str:
        """根据材料类型获取分类名称"""
        category_map = {
            '螺纹钢': '钢筋',
            '热轧板卷': '钢筋',
            '冷轧板卷': '钢筋',
            '中厚板': '钢筋',
            '线材': '钢筋',
            '盘螺': '钢筋',
            'H型钢': '钢筋',
            '工字钢': '钢筋',
            '角钢': '钢筋',
            '槽钢': '钢筋',
        }
        return category_map.get(material_type, '钢筋')


def collect_with_cookie(cookie_str: str = None, material_type: str = 'all'):
    """使用 Cookie 采集数据"""
    init_db()
    
    # 如果提供了新的 Cookie，保存它
    if cookie_str:
        save_cookies_from_string(cookie_str)
        print("✅ Cookie 已保存")
    
    collector = MysteelCookieCollector()
    
    if not collector.logged_in:
        print("❌ 未找到有效的 Cookie，请提供 Cookie")
        return
    
    print("✅ Cookie 有效，开始采集...")
    
    # 采集数据
    prices = collector.collect_prices(material_type)
    
    if prices:
        saved = collector.save_prices(prices)
        print(f"\n✅ 采集完成！共 {saved} 条数据已保存")
    else:
        print("\n⚠️ 未采集到数据，可能页面结构已变化")


if __name__ == '__main__':
    import sys
    
    cookie_str = sys.argv[1] if len(sys.argv) > 1 else None
    material_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
    
    collect_with_cookie(cookie_str, material_type)
