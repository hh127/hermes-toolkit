#!/usr/bin/env python3
"""
我的钢铁网智能采集系统
支持多品种、反爬机制、定时采集
"""
import requests
import json
import re
import os
import time
import random
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(BASE_DIR, 'mysteel_cookies.json')
CONFIG_FILE = os.path.join(BASE_DIR, 'collector_config.json')

# ============================================
# 数据源配置 - 各品种价格页面
# ============================================
PRICE_SOURCES = {
    # 建筑钢材
    '建筑钢材': {
        'url': 'https://list1.mysteel.com/market/p-221-----0101-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '螺纹钢': {
        'url': 'https://list1.mysteel.com/market/p-221-----010101-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '线材': {
        'url': 'https://list1.mysteel.com/market/p-222-----010104-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '盘螺': {
        'url': 'https://list1.mysteel.com/market/p-222-----010105-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    
    # 板材
    '热轧板卷': {
        'url': 'https://list1.mysteel.com/market/p-223-----010103-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '冷轧板卷': {
        'url': 'https://list1.mysteel.com/market/p-224-----010104-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '中厚板': {
        'url': 'https://list1.mysteel.com/market/p-225-----010102-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    
    # 型材
    'H型钢': {
        'url': 'https://list1.mysteel.com/market/p-226-----010106-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '工字钢': {
        'url': 'https://list1.mysteel.com/market/p-226-----01010601-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '角钢': {
        'url': 'https://list1.mysteel.com/market/p-226-----01010602-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    '槽钢': {
        'url': 'https://list1.mysteel.com/market/p-226-----01010603-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    
    # 管材
    '无缝管': {
        'url': 'https://list1.mysteel.com/market/p-236-----01010901-0--------1.html',
        'category': '管材',
        'unit': '元/吨',
    },
    '焊管': {
        'url': 'https://list1.mysteel.com/market/p-237-----01010902-0--------1.html',
        'category': '管材',
        'unit': '元/吨',
    },
    '镀锌管': {
        'url': 'https://list1.mysteel.com/market/p-238-----01010903-0--------1.html',
        'category': '管材',
        'unit': '元/吨',
    },
    
    # 不锈钢
    '不锈钢卷板': {
        'url': 'https://list1.mysteel.com/market/p-2261-----01021601-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    
    # 优特钢
    '优特钢': {
        'url': 'https://list1.mysteel.com/market/p-403-----0102-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    
    # 钢坯
    '钢坯': {
        'url': 'https://list1.mysteel.com/market/p-339-----030501-0--------1.html',
        'category': '钢筋',
        'unit': '元/吨',
    },
    
    # 铁矿石
    '铁矿石': {
        'url': 'https://list1.mysteel.com/market/p-886-----0207-0--------1.html',
        'category': '其他',
        'unit': '元/吨',
    },
    
    # 废钢
    '废钢': {
        'url': 'https://list1.mysteel.com/market/p-2133,2299------0--------1.html',
        'category': '其他',
        'unit': '元/吨',
    },
    
    # 焦炭
    '焦炭': {
        'url': 'https://list1.mysteel.com/market/p-299-----050101-0--------1.html',
        'category': '其他',
        'unit': '元/吨',
    },
    
    # 水泥
    '水泥': {
        'url': 'https://list1.mysteel.com/market/p-219-----01011001-0--------1.html',
        'category': '水泥',
        'unit': '元/吨',
    },
    
    # 混凝土
    '混凝土': {
        'url': 'https://list1.mysteel.com/market/p-219-----01011006-0--------1.html',
        'category': '混凝土',
        'unit': '元/立方米',
    },
}

# ============================================
# 随机 User-Agent 列表
# ============================================
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]


class MysteelSmartCollector:
    """我的钢铁网智能采集器"""
    
    def __init__(self, config: Dict = None):
        self.session = requests.Session()
        self.config = config or self._load_config()
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
        }
        
        # 加载 Cookie
        self._load_cookies()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            'min_delay': 2,  # 最小请求间隔（秒）
            'max_delay': 5,  # 最大请求间隔（秒）
            'timeout': 30,   # 请求超时时间
            'retry_times': 3,  # 重试次数
            'retry_delay': 10,  # 重试间隔（秒）
            'batch_size': 5,  # 每批采集数量
            'batch_delay': 30,  # 批次间隔（秒）
        }
        
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                default_config.update(saved_config)
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
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
        delay = random.uniform(
            self.config['min_delay'],
            self.config['max_delay']
        )
        time.sleep(delay)
    
    def _extract_prices_from_html(self, html: str, material_type: str) -> List[Dict]:
        """从 HTML 提取价格数据"""
        prices = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 方法1: 查找表格数据
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 3:
                    try:
                        name = cols[0].get_text(strip=True)
                        spec = cols[1].get_text(strip=True) if len(cols) > 1 else ''
                        price_text = cols[2].get_text(strip=True)
                        
                        # 提取价格
                        price_match = re.search(r'(\d{3,6}(?:\.\d+)?)', price_text)
                        if price_match:
                            price = float(price_match.group(1))
                            if 100 < price < 100000:  # 合理价格范围
                                prices.append({
                                    'material_type': material_type,
                                    'material_name': f'{name} {spec}'.strip(),
                                    'specification': spec,
                                    'brand': name,
                                    'price': price,
                                    'date': date.today().isoformat(),
                                })
                    except (ValueError, IndexError):
                        continue
        
        # 方法2: 查找列表项
        if not prices:
            items = soup.find_all(['div', 'li'], class_=re.compile(r'item|list|row'))
            for item in items:
                text = item.get_text()
                # 匹配材料名和价格
                match = re.search(r'([\u4e00-\u9fa5]{2,15})\s*.*?(\d{4,6}(?:\.\d+)?)', text)
                if match:
                    name = match.group(1)
                    price = float(match.group(2))
                    if 100 < price < 100000:
                        prices.append({
                            'material_type': material_type,
                            'material_name': name,
                            'specification': '',
                            'brand': '',
                            'price': price,
                            'date': date.today().isoformat(),
                        })
        
        # 方法3: 从首页提取（备用）
        if not prices:
            # 查找包含价格的元素
            price_elements = soup.find_all(text=re.compile(r'\d{4}\.\d{2}'))
            for elem in price_elements:
                price_match = re.search(r'(\d{4}\.\d{2})', elem)
                if price_match:
                    price = float(price_match.group(1))
                    if 1000 < price < 100000:
                        prices.append({
                            'material_type': material_type,
                            'material_name': material_type,
                            'specification': '',
                            'brand': '',
                            'price': price,
                            'date': date.today().isoformat(),
                        })
        
        return prices
    
    def collect_single(self, material_type: str) -> List[Dict]:
        """采集单个品种"""
        if material_type not in PRICE_SOURCES:
            print(f"❌ 未知品种: {material_type}")
            return []
        
        source = PRICE_SOURCES[material_type]
        url = source['url']
        
        for attempt in range(self.config['retry_times']):
            try:
                # 随机延迟
                self._random_delay()
                
                # 设置随机请求头
                self.session.headers.update(self._get_headers())
                
                # 发送请求
                response = self.session.get(url, timeout=self.config['timeout'])
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                
                # 提取价格
                prices = self._extract_prices_from_html(response.text, material_type)
                
                if prices:
                    print(f"✅ {material_type}: 提取到 {len(prices)} 条价格")
                    return prices
                else:
                    print(f"⚠️ {material_type}: 未提取到价格数据")
                    return []
                
            except Exception as e:
                print(f"❌ {material_type}: 第 {attempt + 1} 次尝试失败 - {e}")
                if attempt < self.config['retry_times'] - 1:
                    time.sleep(self.config['retry_delay'])
        
        return []
    
    def collect_batch(self, material_types: List[str] = None) -> List[Dict]:
        """批量采集"""
        if material_types is None:
            material_types = list(PRICE_SOURCES.keys())
        
        all_prices = []
        total = len(material_types)
        
        print(f"开始采集 {total} 个品种...")
        print("=" * 50)
        
        for i, material_type in enumerate(material_types, 1):
            print(f"\n[{i}/{total}] 采集 {material_type}...")
            
            prices = self.collect_single(material_type)
            all_prices.extend(prices)
            
            self.stats['total'] += 1
            if prices:
                self.stats['success'] += 1
            else:
                self.stats['failed'] += 1
            
            # 批次间隔
            if i % self.config['batch_size'] == 0 and i < total:
                print(f"\n--- 批次间隔 {self.config['batch_delay']} 秒 ---")
                time.sleep(self.config['batch_delay'])
        
        print("\n" + "=" * 50)
        print(f"采集完成: 成功 {self.stats['success']}, 失败 {self.stats['failed']}")
        
        return all_prices
    
    def collect_homepage(self) -> List[Dict]:
        """从首页提取价格（快速模式）"""
        print("从首页提取价格数据...")
        
        try:
            self.session.headers.update(self._get_headers())
            response = self.session.get('https://www.mysteel.com/', timeout=self.config['timeout'])
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
                        
                        # 确定分类
                        category = '钢筋'
                        if '水泥' in name:
                            category = '水泥'
                        elif '混凝土' in name:
                            category = '混凝土'
                        
                        prices.append({
                            'material_type': name,
                            'material_name': f'{name} (我的钢铁网)',
                            'specification': '',
                            'brand': '',
                            'price': price,
                            'date': date.today().isoformat(),
                            'category': category,
                        })
            
            print(f"✅ 从首页提取到 {len(prices)} 条价格")
            return prices
            
        except Exception as e:
            print(f"❌ 首页提取失败: {e}")
            return []
    
    def update_config(self, new_config: Dict):
        """更新配置"""
        self.config.update(new_config)
        self._save_config()
        print("✅ 配置已更新")


# ============================================
# 独立运行函数
# ============================================
def collect_mysteel_smart(material_types: List[str] = None, use_homepage: bool = True):
    """智能采集"""
    from models import init_db, insert_price, get_categories
    
    init_db()
    categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    collector = MysteelSmartCollector()
    
    if use_homepage:
        prices = collector.collect_homepage()
    else:
        prices = collector.collect_batch(material_types)
    
    if not prices:
        print("⚠️ 未采集到数据")
        return 0
    
    # 保存到数据库
    saved = 0
    for p in prices:
        category_name = p.get('category', '钢筋')
        category_id = categories.get(category_name, 1)
        
        success = insert_price(
            category_id=category_id,
            material_name=p['material_name'],
            price=p['price'],
            specification=p.get('specification', ''),
            brand=p.get('brand', ''),
            city='全国',
            source='我的钢铁网',
            collect_date=p['date']
        )
        
        if success:
            saved += 1
    
    print(f"\n✅ 共保存 {saved} 条数据到数据库")
    return saved


if __name__ == '__main__':
    import sys
    
    # 命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--homepage':
            collect_mysteel_smart(use_homepage=True)
        elif sys.argv[1] == '--all':
            collect_mysteel_smart(use_homepage=False)
        else:
            # 指定品种
            material_types = sys.argv[1:]
            collect_mysteel_smart(material_types=material_types, use_homepage=False)
    else:
        # 默认使用首页快速采集
        collect_mysteel_smart(use_homepage=True)
