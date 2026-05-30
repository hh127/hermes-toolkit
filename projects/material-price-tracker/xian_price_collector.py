#!/usr/bin/env python3
"""
西安钢材价格采集器
支持Cookie认证和价格解密
"""
import requests
import json
import re
import os
import time
import random
import base64
from datetime import datetime, date
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from models import init_db, get_connection, get_categories


# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(BASE_DIR, 'mysteel_cookies.json')


# 城市价格页面URL
CITY_PRICE_URLS = {
    '西安': 'https://jiancai.mysteel.com/m/26052910/892658956BF3E75C.html',
    # 可以添加更多城市
}


# 随机 User-Agent 列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
]


class XiAnPriceCollector:
    """西安钢材价格采集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'encrypted': 0,
        }
        
        # 加载 Cookie
        self._load_cookies()
    
    def _load_cookies(self) -> bool:
        """加载 Cookie"""
        if not os.path.exists(COOKIES_FILE):
            print("⚠️ 未找到Cookie文件，请先运行 cookie_manager.py 更新Cookie")
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
    
    def parse_price_table(self, html: str, city: str = '西安') -> List[Dict]:
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
                
                # 检查价格是否被加密
                price_cell = cells[4] if len(cells) > 4 else None
                is_encrypted = False
                
                if price_cell:
                    is_encrypted = price_cell.get('data-encrypt', 'false') == 'true'
                
                # 尝试提取价格
                price = None
                change = 0
                
                if not is_encrypted:
                    # 价格未加密，直接提取
                    price_text = cell_texts[4] if len(cell_texts) > 4 else ''
                    price_match = re.search(r'(\d{3,4}(?:\.\d+)?)', price_text)
                    if price_match:
                        price = float(price_match.group(1))
                    
                    # 提取涨跌
                    change_text = cell_texts[5] if len(cell_texts) > 5 else ''
                    change_match = re.search(r'([+-]?\d+(?:\.\d+)?)', change_text)
                    if change_match:
                        change = float(change_match.group(1))
                else:
                    # 价格被加密
                    self.stats['encrypted'] += 1
                    encrypt_v = price_cell.get('data-encrypt-v', '')
                    
                    # 尝试解密（如果知道算法）
                    # 目前无法解密，跳过
                    continue
                
                if price:
                    # 提取其他信息
                    name = cell_texts[0] if len(cell_texts) > 0 else ''
                    spec = cell_texts[1] if len(cell_texts) > 1 else ''
                    material = cell_texts[2] if len(cell_texts) > 2 else ''
                    brand = cell_texts[3] if len(cell_texts) > 3 else ''
                    
                    if name:
                        prices.append({
                            'name': name,
                            'spec': spec,
                            'material': material,
                            'brand': brand,
                            'price': price,
                            'change': change,
                            'city': city,
                        })
        
        return prices
    
    def collect_city_price(self, city: str, url: str) -> List[Dict]:
        """采集单个城市的价格"""
        try:
            self._random_delay()
            
            self.session.headers.update(self._get_headers())
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"  ❌ 请求失败: {response.status_code}")
                return []
            
            # 检查是否被加密
            if 'data-encrypt="true"' in response.text:
                print(f"  ⚠️ 价格数据被加密")
                
                # 统计加密单元格数量
                encrypted_count = response.text.count('data-encrypt="true"')
                print(f"  加密单元格: {encrypted_count} 个")
                
                # 返回空列表，但标记为加密
                return []
            
            # 解析价格表格
            prices = self.parse_price_table(response.text, city)
            
            return prices
            
        except Exception as e:
            print(f"  ❌ 采集失败: {e}")
            return []
    
    def collect_xian(self) -> List[Dict]:
        """采集西安的价格"""
        print(f"采集 西安 建筑钢材价格...")
        
        url = CITY_PRICE_URLS.get('西安')
        if not url:
            print("  ❌ 未找到西安的价格页面URL")
            return []
        
        return self.collect_city_price('西安', url)


def collect_xian_prices() -> int:
    """采集西安价格并保存到数据库"""
    print("="*60)
    print("西安建筑钢材价格采集器")
    print("="*60)
    
    # 初始化数据库
    init_db()
    categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    # 创建采集器
    collector = XiAnPriceCollector()
    
    # 采集价格
    prices = collector.collect_xian()
    
    if not prices:
        print("\n⚠️ 未采集到价格数据")
        
        if collector.stats['encrypted'] > 0:
            print(f"\n检测到 {collector.stats['encrypted']} 个加密的价格单元格")
            print("\n解决方案:")
            print("1. 运行 python cookie_manager.py 更新Cookie（需要会员账号）")
            print("2. 或者使用Playwright模拟浏览器获取解密后的价格")
            print("3. 或者手动录入价格数据")
        
        return 0
    
    # 保存到数据库
    print(f"\n正在保存 {len(prices)} 条数据到数据库...")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    saved = 0
    for p in prices:
        # 确定分类
        category_name = '钢筋'  # 建筑钢材默认为钢筋
        
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
    
    print(f"\n✅ 成功保存 {saved} 条西安价格数据")
    
    return saved


if __name__ == '__main__':
    collect_xian_prices()
