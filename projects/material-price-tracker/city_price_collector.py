#!/usr/bin/env python3
"""
城市价格采集器
从我的钢铁网新闻详情页获取城市级别的价格数据
"""
import requests
import json
import re
import os
import time
import random
from datetime import datetime, date
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from models import init_db, get_connection, get_categories


# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(BASE_DIR, 'mysteel_cookies.json')


# 城市和材料的URL映射
# 格式: {城市: {材料: url}}
CITY_MATERIAL_URLS = {}


# 随机 User-Agent 列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]


class CityPriceCollector:
    """城市价格采集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
        }
        
        # 加载 Cookie
        self._load_cookies()
    
    def _load_cookies(self) -> bool:
        """加载 Cookie"""
        if not os.path.exists(COOKIES_FILE):
            return False
        
        with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        self.session.cookies.update(cookies)
        return True
    
    def _get_headers(self) -> Dict:
        """获取随机请求头"""
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.mysteel.com/',
        }
    
    def _random_delay(self):
        """随机延迟，规避反爬"""
        delay = random.uniform(2, 5)
        time.sleep(delay)
    
    def get_city_news_links(self) -> List[Dict]:
        """从首页获取城市价格新闻链接"""
        print("正在从首页获取城市价格新闻链接...")
        
        try:
            self.session.headers.update(self._get_headers())
            response = self.session.get('https://www.mysteel.com/', timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for link in soup.find_all('a'):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # 匹配 "X月X日XX市场XXX价格行情" 格式
                match = re.search(r'(\d+)月(\d+)日([\u4e00-\u9fa5]+)市场([\u4e00-\u9fa5]+)价格行情', text)
                if match and href:
                    month, day, city, material = match.groups()
                    
                    # 过滤掉区域性的（如"东北"、"华中"等）
                    if city in ['国内', '东北', '华中', '华东', '华南', '西南', '西北', '华北']:
                        continue
                    
                    # 构建完整URL
                    if href.startswith('//'):
                        full_url = 'https:' + href
                    elif href.startswith('http'):
                        full_url = href
                    else:
                        full_url = 'https://www.mysteel.com' + href
                    
                    links.append({
                        'text': text,
                        'city': city,
                        'material': material,
                        'url': full_url,
                    })
            
            print(f"✅ 找到 {len(links)} 条城市价格新闻链接")
            return links
            
        except Exception as e:
            print(f"❌ 获取新闻链接失败: {e}")
            return []
    
    def parse_price_table(self, html: str) -> List[Dict]:
        """解析价格表格"""
        prices = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找价格表格
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) <= 2:
                continue
            
            # 获取表头
            header_row = rows[0]
            header_cells = header_row.find_all(['th', 'td'])
            header_text = [cell.get_text(strip=True) for cell in header_cells]
            
            # 检查是否是价格表格
            header_str = ' '.join(header_text)
            if not any(kw in header_str for kw in ['价格', '报价', '元', '品名', '规格']):
                continue
            
            # 解析数据行
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 4:
                    continue
                
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # 查找价格列（通常是第5列）
                price = None
                price_col = -1
                
                for i, text in enumerate(cell_texts):
                    # 尝试提取价格数字
                    price_match = re.search(r'(\d{3,4}(?:\.\d+)?)', text)
                    if price_match:
                        p = float(price_match.group(1))
                        if 200 < p < 10000:  # 合理的价格范围
                            price = p
                            price_col = i
                            break
                
                if price and price_col > 0:
                    # 提取其他信息
                    name = cell_texts[0] if len(cell_texts) > 0 else ''
                    spec = cell_texts[1] if len(cell_texts) > 1 else ''
                    material = cell_texts[2] if len(cell_texts) > 2 else ''
                    brand = cell_texts[3] if len(cell_texts) > 3 else ''
                    
                    # 提取涨跌
                    change = 0
                    if len(cell_texts) > price_col + 1:
                        change_text = cell_texts[price_col + 1]
                        change_match = re.search(r'([+-]?\d+(?:\.\d+)?)', change_text)
                        if change_match:
                            change = float(change_match.group(1))
                    
                    if name:
                        prices.append({
                            'name': name,
                            'spec': spec,
                            'material': material,
                            'brand': brand,
                            'price': price,
                            'change': change,
                        })
        
        return prices
    
    def collect_city_price(self, city: str, material: str, url: str) -> List[Dict]:
        """采集单个城市的价格"""
        try:
            self._random_delay()
            
            self.session.headers.update(self._get_headers())
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return []
            
            # 解析价格表格
            prices = self.parse_price_table(response.text)
            
            # 添加城市信息
            for p in prices:
                p['city'] = city
                p['material_type'] = material
            
            return prices
            
        except Exception as e:
            print(f"  ❌ 采集失败: {e}")
            return []
    
    def collect_all_cities(self, max_cities: int = 10) -> List[Dict]:
        """采集所有城市的价格"""
        # 获取新闻链接
        news_links = self.get_city_news_links()
        
        if not news_links:
            return []
        
        # 按城市分组
        city_links = {}
        for link in news_links:
            city = link['city']
            if city not in city_links:
                city_links[city] = []
            city_links[city].append(link)
        
        print(f"\n共有 {len(city_links)} 个城市")
        
        # 限制采集的城市数量
        cities_to_collect = list(city_links.keys())[:max_cities]
        
        all_prices = []
        
        for city in cities_to_collect:
            links = city_links[city]
            print(f"\n采集 {city} ({len(links)} 条链接)...")
            
            city_prices = []
            
            # 只采集第一个链接（避免太多请求）
            if links:
                link = links[0]
                prices = self.collect_city_price(city, link['material'], link['url'])
                city_prices.extend(prices)
            
            if city_prices:
                print(f"  ✅ 获取 {len(city_prices)} 条价格数据")
                all_prices.extend(city_prices)
                self.stats['success'] += 1
            else:
                print(f"  ⚠️ 未获取到数据")
                self.stats['failed'] += 1
            
            self.stats['total'] += 1
        
        return all_prices


def collect_city_prices(max_cities: int = 5) -> int:
    """采集城市价格并保存到数据库"""
    print("="*60)
    print("城市价格采集器")
    print("="*60)
    
    # 初始化数据库
    init_db()
    categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    # 创建采集器
    collector = CityPriceCollector()
    
    # 采集价格
    prices = collector.collect_all_cities(max_cities=max_cities)
    
    if not prices:
        print("\n⚠️ 未采集到城市价格数据")
        return 0
    
    # 保存到数据库
    print(f"\n正在保存 {len(prices)} 条数据到数据库...")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    saved = 0
    for p in prices:
        # 确定分类
        category_name = '钢筋'  # 默认
        material_type = p.get('material_type', '')
        
        if '水泥' in material_type:
            category_name = '水泥'
        elif '混凝土' in material_type:
            category_name = '混凝土'
        elif '砂石' in material_type:
            category_name = '砂石'
        elif '木材' in material_type:
            category_name = '木材'
        elif '玻璃' in material_type:
            category_name = '玻璃'
        elif '沥青' in material_type:
            category_name = '沥青'
        
        category_id = categories.get(category_name, 1)
        
        # 构建材料名称
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
                category_id,
                material_name,
                p['price'],
                p.get('spec', ''),
                p.get('brand', ''),
                p['city'],
                '我的钢铁网',
                date.today().isoformat()
            ))
            saved += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 成功保存 {saved} 条城市价格数据")
    
    # 统计
    print(f"\n采集统计:")
    print(f"  总计: {collector.stats['total']} 个城市")
    print(f"  成功: {collector.stats['success']} 个")
    print(f"  失败: {collector.stats['failed']} 个")
    
    return saved


if __name__ == '__main__':
    import sys
    
    # 命令行参数
    max_cities = 5
    if len(sys.argv) > 1:
        try:
            max_cities = int(sys.argv[1])
        except:
            pass
    
    collect_city_prices(max_cities=max_cities)
