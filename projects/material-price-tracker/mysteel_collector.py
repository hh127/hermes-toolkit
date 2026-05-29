#!/usr/bin/env python3
"""
我的钢铁网数据采集模块
支持登录、采集钢材价格数据
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

# 环境变量文件路径
ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


def load_env():
    """加载环境变量"""
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env[key.strip()] = value.strip()
    return env


def save_env(key, value):
    """保存环境变量"""
    env = load_env()
    env[key] = value
    
    with open(ENV_FILE, 'w', encoding='utf-8') as f:
        for k, v in env.items():
            f.write(f'{k}={v}\n')


class MysteelCollector:
    """我的钢铁网采集器"""
    
    BASE_URL = 'https://www.mysteel.com'
    LOGIN_URL = 'https://login.mysteel.com/login/'
    
    # 钢材价格页面
    PRICE_URLS = {
        '螺纹钢': 'https://www.mysteel.com/price/2/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '热轧板卷': 'https://www.mysteel.com/price/3/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '冷轧板卷': 'https://www.mysteel.com/price/4/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '中厚板': 'https://www.mysteel.com/price/5/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '线材': 'https://www.mysteel.com/price/6/0-0-0-0-0-0-0-0-0-0-0-0.html',
        '盘螺': 'https://www.mysteel.com/price/7/0-0-0-0-0-0-0-0-0-0-0-0.html',
    }
    
    def __init__(self, username=None, password=None):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.categories = {cat['name']: cat['id'] for cat in get_categories()}
        self.logged_in = False
        
        # 从环境变量或参数获取登录信息
        env = load_env()
        self.username = username or env.get('MYSTEEL_USERNAME')
        self.password = password or env.get('MYSTEEL_PASSWORD')
        
        # 如果提供了新的登录信息，保存到环境变量
        if username and password:
            save_env('MYSTEEL_USERNAME', username)
            save_env('MYSTEEL_PASSWORD', password)
    
    def login(self) -> bool:
        """
        登录我的钢铁网
        
        Returns:
            是否登录成功
        """
        if not self.username or not self.password:
            print("❌ 未提供登录信息")
            return False
        
        try:
            print(f"正在登录我的钢铁网 (用户: {self.username})...")
            
            # 获取登录页面
            login_page = self.session.get(self.LOGIN_URL, timeout=30)
            login_page.raise_for_status()
            
            soup = BeautifulSoup(login_page.text, 'html.parser')
            
            # 查找登录表单
            # 注意：实际网站结构可能需要调整
            login_data = {
                'username': self.username,
                'password': self.password,
                'remember': '1',
            }
            
            # 尝试提交登录
            # 这里需要根据实际网站的登录接口调整
            login_api = 'https://login.mysteel.com/api/login'
            
            response = self.session.post(
                login_api,
                data=login_data,
                timeout=30,
                allow_redirects=True
            )
            
            # 检查登录状态
            if response.status_code == 200:
                # 尝试访问需要登录的页面验证
                test_url = 'https://www.mysteel.com/member/'
                test_response = self.session.get(test_url, timeout=30)
                
                if 'login' not in test_response.url.lower():
                    self.logged_in = True
                    print("✅ 登录成功")
                    
                    # 保存 cookies
                    self._save_cookies()
                    return True
            
            print("❌ 登录失败，请检查用户名和密码")
            return False
            
        except Exception as e:
            print(f"❌ 登录出错: {e}")
            return False
    
    def _save_cookies(self):
        """保存 cookies 到文件"""
        cookies_file = os.path.join(os.path.dirname(__file__), 'mysteel_cookies.json')
        cookies = self.session.cookies.get_dict()
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f)
    
    def _load_cookies(self) -> bool:
        """从文件加载 cookies"""
        cookies_file = os.path.join(os.path.dirname(__file__), 'mysteel_cookies.json')
        
        if not os.path.exists(cookies_file):
            return False
        
        try:
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            self.session.cookies.update(cookies)
            
            # 验证 cookies 是否有效
            test_url = 'https://www.mysteel.com/member/'
            response = self.session.get(test_url, timeout=30)
            
            if 'login' not in response.url.lower():
                self.logged_in = True
                return True
            
            return False
            
        except Exception:
            return False
    
    def collect_prices(self, material_type: str = 'all') -> List[Dict]:
        """
        采集钢材价格
        
        Args:
            material_type: 材料类型，'all' 表示所有类型
        
        Returns:
            价格数据列表
        """
        results = []
        
        # 尝试加载 cookies
        if not self.logged_in:
            if not self._load_cookies():
                if not self.login():
                    return results
        
        # 确定要采集的类型
        if material_type == 'all':
            types_to_collect = self.PRICE_URLS.keys()
        else:
            types_to_collect = [material_type] if material_type in self.PRICE_URLS else []
        
        for mat_type in types_to_collect:
            url = self.PRICE_URLS.get(mat_type)
            if not url:
                continue
            
            try:
                print(f"采集 {mat_type} 价格...")
                time.sleep(random.uniform(1, 3))  # 随机延迟
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 解析价格数据
                # 注意：这里需要根据实际页面结构调整
                prices = self._parse_prices(soup, mat_type)
                results.extend(prices)
                
                print(f"  ✅ 采集到 {len(prices)} 条数据")
                
            except Exception as e:
                print(f"  ❌ 采集 {mat_type} 失败: {e}")
        
        return results
    
    def _parse_prices(self, soup: BeautifulSoup, material_type: str) -> List[Dict]:
        """
        解析价格页面
        
        Args:
            soup: BeautifulSoup 对象
            material_type: 材料类型
        
        Returns:
            价格数据列表
        """
        prices = []
        
        # 这里需要根据实际页面结构调整选择器
        # 以下是一个示例结构
        
        # 查找价格表格
        price_table = soup.find('table', class_='price-table')
        if not price_table:
            # 尝试其他选择器
            price_table = soup.find('table', {'id': 'priceTable'})
        
        if price_table:
            rows = price_table.find_all('tr')
            
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all('td')
                if len(cols) >= 4:
                    try:
                        material_name = cols[0].get_text(strip=True)
                        specification = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                        brand = cols[2].get_text(strip=True) if len(cols) > 2 else ''
                        price_text = cols[3].get_text(strip=True)
                        
                        # 提取价格数字
                        price = float(price_text.replace('¥', '').replace(',', ''))
                        
                        if material_name and price > 0:
                            prices.append({
                                'material_type': material_type,
                                'material_name': material_name,
                                'specification': specification,
                                'brand': brand,
                                'price': price,
                                'unit': '元/吨',
                                'city': '全国',
                                'date': date.today().isoformat(),
                                'source': '我的钢铁网',
                            })
                    except (ValueError, IndexError):
                        continue
        
        return prices
    
    def save_prices(self, prices: List[Dict]) -> int:
        """
        保存价格数据到数据库
        
        Args:
            prices: 价格数据列表
        
        Returns:
            保存成功的记录数
        """
        saved_count = 0
        
        for item in prices:
            # 确定分类 ID
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
        }
        return category_map.get(material_type, '钢筋')


def collect_mysteel(username=None, password=None, material_type='all'):
    """
    采集我的钢铁网数据
    
    Args:
        username: 用户名
        password: 密码
        material_type: 材料类型
    """
    init_db()
    
    collector = MysteelCollector(username, password)
    
    # 采集数据
    prices = collector.collect_prices(material_type)
    
    if prices:
        # 保存数据
        saved = collector.save_prices(prices)
        print(f"\n✅ 采集完成！共 {saved} 条数据已保存")
    else:
        print("\n⚠️ 未采集到数据")


if __name__ == '__main__':
    import sys
    
    username = sys.argv[1] if len(sys.argv) > 1 else None
    password = sys.argv[2] if len(sys.argv) > 2 else None
    material_type = sys.argv[3] if len(sys.argv) > 3 else 'all'
    
    collect_mysteel(username, password, material_type)
