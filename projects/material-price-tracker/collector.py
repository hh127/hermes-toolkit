#!/usr/bin/env python3
"""
建材价格采集模块
从公开网站获取工程材料价格数据
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import time
import random
import json
from typing import List, Dict, Optional
from models import init_db, insert_price, get_categories

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 常见品牌
BRANDS = {
    "钢筋": ["沙钢", "永钢", "中天", "马钢", "鞍钢", "宝钢", "首钢"],
    "水泥": ["海螺", "华润", "中国建材", "冀东", "华新", "山水"],
    "混凝土": ["中建", "中铁", "当地搅拌站"],
    "砂石": ["当地供应商"],
    "木材": ["进口松木", "国产杉木"],
    "玻璃": ["信义", "南玻", "耀皮", "福耀"],
    "铝合金": ["忠旺", "亚铝", "兴发", "凤铝"],
    "沥青": ["中石化", "中石油", "地方炼厂"],
    "电缆": ["远东", "宝胜", "亨通", "中天"],
    "管材": ["联塑", "伟星", "中财", "公元"],
}

# 模拟价格基准（用于无网络或采集失败时生成模拟数据）
BASE_PRICES = {
    "钢筋": {
        "HRB400 Φ18-25": 3850,
        "HRB400 Φ12-14": 3950,
        "HRB400E Φ18-25": 3950,
        "盘螺 HRB400 Φ8-10": 4050,
    },
    "水泥": {
        "P.O 42.5 散装": 420,
        "P.O 42.5 袋装": 460,
        "P.O 52.5 散装": 520,
        "P.C 32.5 散装": 350,
    },
    "混凝土": {
        "C30 商品混凝土": 450,
        "C35 商品混凝土": 480,
        "C40 商品混凝土": 520,
        "C50 商品混凝土": 580,
    },
    "砂石": {
        "中砂": 110,
        "碎石 5-25mm": 95,
        "机制砂": 105,
        "碎石 10-20mm": 100,
    },
}


class MaterialPriceCollector:
    """材料价格采集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.categories = {cat['name']: cat['id'] for cat in get_categories()}
    
    def fetch_page(self, url: str, params: dict = None) -> Optional[BeautifulSoup]:
        """获取页面内容"""
        try:
            # 随机延迟，避免被封
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"获取页面失败 {url}: {e}")
            return None
    
    def collect_from_mysteel(self) -> List[Dict]:
        """
        从我的钢铁网采集钢材价格
        我的钢铁网: https://www.mysteel.com/
        """
        results = []
        
        try:
            # 我的钢铁网 - 螺纹钢价格页面
            url = "https://www.mysteel.com/price/2/0-0-0-0-0-0-0-0-0-0-0-0.html"
            soup = self.fetch_page(url)
            
            if soup:
                print("采集钢材价格...")
                # 解析钢材价格页面
                # 注意：实际网站结构可能需要调整
                
        except Exception as e:
            print(f"采集钢材价格失败: {e}")
        
        return results
    
    def collect_from_zjtcy(self, city: str = "全国") -> List[Dict]:
        """
        从造价通采集材料价格
        造价通网址: https://www.zjtcy.com/
        """
        results = []
        
        # 造价通的材料价格页面
        base_url = "https://www.zjtcy.com"
        
        # 常见材料类型ID
        material_types = {
            "钢筋": "/search?keyword=螺纹钢&type=material",
            "水泥": "/search?keyword=水泥&type=material",
            "混凝土": "/search?keyword=商品混凝土&type=material",
            "砂石": "/search?keyword=中砂&type=material",
        }
        
        for category_name, path in material_types.items():
            try:
                url = base_url + path
                soup = self.fetch_page(url)
                
                if soup:
                    print(f"尝试采集 {category_name} 价格...")
                    # 这里需要根据实际网站结构解析
                    
            except Exception as e:
                print(f"采集 {category_name} 失败: {e}")
        
        return results
    
    def generate_simulated_data(self, days: int = 30) -> List[Dict]:
        """生成模拟数据（当无法采集真实数据时使用）"""
        import random
        from datetime import timedelta
        
        today = date.today()
        results = []
        
        brands_map = {
            "钢筋": "沙钢",
            "水泥": "海螺",
            "混凝土": "中建",
            "砂石": "当地",
            "木材": "进口松",
            "玻璃": "信义",
            "铝合金": "忠旺",
            "沥青": "中石化",
            "电缆": "远东",
            "管材": "联塑",
        }
        
        # 生成过去N天的数据
        for days_ago in range(days, -1, -1):
            collect_date = today - timedelta(days=days_ago)
            
            # 跳过周末
            if collect_date.weekday() >= 5:
                continue
            
            for category, specs in BASE_PRICES.items():
                for spec, base_price in specs.items():
                    # 模拟价格波动（±5%）
                    fluctuation = random.uniform(-0.05, 0.05)
                    
                    # 添加一些趋势
                    trend = (days - days_ago) / days * 0.02
                    
                    price = base_price * (1 + fluctuation + trend)
                    price = round(price, 2)
                    
                    # 获取分类ID
                    category_name = self._get_category_name(spec)
                    category_id = self.categories.get(category_name, 1)
                    
                    results.append({
                        'category_id': category_id,
                        'material_name': spec,
                        'price': price,
                        'specification': spec.split(' ')[-1] if ' ' in spec else '',
                        'brand': brands_map.get(category_name, ''),
                        'city': '全国',
                        'source': '模拟数据',
                        'collect_date': collect_date.isoformat(),
                    })
        
        return results
    
    def _get_category_name(self, spec: str) -> str:
        """根据规格名称推断分类"""
        spec_lower = spec.lower()
        
        if 'hrb' in spec_lower or 'hpb' in spec_lower or '螺纹' in spec_lower:
            return '钢筋'
        elif 'p.o' in spec_lower or 'p.c' in spec_lower or '水泥' in spec_lower:
            return '水泥'
        elif 'c30' in spec_lower or 'c35' in spec_lower or 'c40' in spec_lower:
            return '混凝土'
        elif '砂' in spec_lower or '碎石' in spec_lower:
            return '砂石'
        elif '木' in spec_lower or '模板' in spec_lower:
            return '木材'
        elif '玻璃' in spec_lower:
            return '玻璃'
        elif '铝' in spec_lower:
            return '铝合金'
        elif '沥青' in spec_lower:
            return '沥青'
        elif '电缆' in spec_lower or 'bv' in spec_lower:
            return '电缆'
        elif '管' in spec_lower or 'pvc' in spec_lower:
            return '管材'
        else:
            return '钢筋'  # 默认分类
    
    def save_prices(self, prices: List[Dict], source: str = "网络采集"):
        """保存价格数据到数据库"""
        saved_count = 0
        
        for item in prices:
            try:
                success = insert_price(
                    category_id=item.get('category_id', 1),
                    material_name=item['material_name'],
                    price=item['price'],
                    specification=item.get('specification'),
                    brand=item.get('brand'),
                    city=item.get('city', '全国'),
                    source=source,
                    collect_date=item.get('collect_date', date.today().isoformat())
                )
                
                if success:
                    saved_count += 1
            except Exception as e:
                print(f"保存失败: {e}")
        
        print(f"成功保存 {saved_count}/{len(prices)} 条价格数据")
        return saved_count
    
    def collect_all(self, use_simulated: bool = True):
        """采集所有材料价格"""
        print("开始采集材料价格...")
        
        all_prices = []
        
        # 尝试从网络采集
        try:
            prices = self.collect_from_mysteel()
            if prices:
                all_prices.extend(prices)
                print(f"从我的钢铁网采集到 {len(prices)} 条数据")
        except Exception as e:
            print(f"从我的钢铁网采集失败: {e}")
        
        try:
            prices = self.collect_from_zjtcy()
            if prices:
                all_prices.extend(prices)
                print(f"从造价通采集到 {len(prices)} 条数据")
        except Exception as e:
            print(f"从造价通采集失败: {e}")
        
        # 如果没有采集到数据，使用模拟数据
        if not all_prices and use_simulated:
            print("未采集到真实数据，使用模拟数据...")
            all_prices = self.generate_simulated_data(days=30)
            source = "模拟数据"
        else:
            source = "网络采集"
        
        # 保存数据
        if all_prices:
            self.save_prices(all_prices, source)
            print(f"采集完成！共 {len(all_prices)} 条数据")
        else:
            print("采集失败，未获取到任何数据")


def collect_daily():
    """每日采集任务"""
    init_db()
    collector = MaterialPriceCollector()
    collector.collect_all(use_simulated=True)


if __name__ == "__main__":
    collect_daily()
