#!/usr/bin/env python3
"""生成示例数据"""
import random
from datetime import date, timedelta
from models import init_db, insert_price, get_categories, get_connection


def generate_sample_data():
    """生成30天的示例价格数据"""
    init_db()
    
    # 获取分类ID映射
    categories = get_categories()
    cat_map = {cat['name']: cat['id'] for cat in categories}
    
    # 基准价格（2024-2025年参考价）
    base_prices = {
        "钢筋": [
            ("HRB400 Φ18-25 螺纹钢", 3850, "吨"),
            ("HRB400 Φ12-14 螺纹钢", 3950, "吨"),
            ("HRB400E Φ18-25 抗震螺纹钢", 3950, "吨"),
            ("HRB400 Φ8-10 盘螺", 4050, "吨"),
            ("HPB300 Φ6-10 高线", 4100, "吨"),
        ],
        "水泥": [
            ("P.O 42.5 散装水泥", 420, "吨"),
            ("P.O 42.5 袋装水泥", 460, "吨"),
            ("P.O 52.5 散装水泥", 520, "吨"),
            ("P.C 32.5 散装水泥", 350, "吨"),
            ("P.C 32.5 袋装水泥", 390, "吨"),
        ],
        "混凝土": [
            ("C25 商品混凝土", 420, "m³"),
            ("C30 商品混凝土", 450, "m³"),
            ("C35 商品混凝土", 480, "m³"),
            ("C40 商品混凝土", 520, "m³"),
            ("C50 商品混凝土", 580, "m³"),
            ("C60 商品混凝土", 650, "m³"),
        ],
        "砂石": [
            ("中砂", 110, "吨"),
            ("碎石 5-25mm", 95, "吨"),
            ("机制砂", 105, "吨"),
            ("碎石 10-20mm", 100, "吨"),
            ("碎石 16-31.5mm", 92, "吨"),
            ("天然砂 细砂", 125, "吨"),
        ],
        "木材": [
            ("方木 4m×100×100mm", 1850, "m³"),
            ("覆膜板 1830×915×15mm", 65, "张"),
            ("松木方 4m×50×100mm", 1900, "m³"),
            ("木模板 1220×2440×12mm", 58, "张"),
        ],
        "玻璃": [
            ("浮法玻璃 5mm", 35, "m²"),
            ("浮法玻璃 8mm", 55, "m²"),
            ("浮法玻璃 10mm", 72, "m²"),
            ("钢化玻璃 5mm", 50, "m²"),
            ("钢化玻璃 8mm", 75, "m²"),
            ("中空玻璃 5+9A+5", 120, "m²"),
        ],
        "铝合金": [
            ("6063 铝型材", 18500, "吨"),
            ("1060 铝板 2mm", 17800, "吨"),
            ("6061 铝管", 19200, "吨"),
            ("铝合金门窗型材", 285, "m²"),
        ],
        "沥青": [
            ("70# 道路石油沥青", 3800, "吨"),
            ("90# 道路石油沥青", 3750, "吨"),
            ("SBS改性沥青 I-D", 4500, "吨"),
            ("SBS改性沥青 I-C", 4600, "吨"),
        ],
        "电缆": [
            ("YJV 3×10mm² 电力电缆", 45, "米"),
            ("YJV 3×25mm² 电力电缆", 95, "米"),
            ("YJV 3×50mm² 电力电缆", 165, "米"),
            ("BV 2.5mm² 铜芯线", 2.5, "米"),
            ("BV 4mm² 铜芯线", 3.8, "米"),
            ("RVV 3×2.5mm² 护套线", 5.5, "米"),
        ],
        "管材": [
            ("PVC排水管 Φ110×3.2mm", 18, "米"),
            ("PVC排水管 Φ75×2.3mm", 12, "米"),
            ("PE给水管 Φ63×5.8mm SDR11", 25, "米"),
            ("PPR热水管 Φ25×3.5mm", 12, "米"),
            ("镀锌钢管 DN100", 85, "米"),
            ("焊接钢管 DN50", 45, "米"),
        ],
    }
    
    # 品牌映射
    brands_map = {
        "钢筋": ["沙钢", "永钢", "中天", "马钢"],
        "水泥": ["海螺", "华润", "冀东", "华新"],
        "混凝土": ["中建商砼", "中铁商砼"],
        "砂石": ["当地供应商"],
        "木材": ["进口松", "国产杉"],
        "玻璃": ["信义", "南玻", "耀皮"],
        "铝合金": ["忠旺", "亚铝", "兴发", "凤铝"],
        "沥青": ["中石化", "中石油"],
        "电缆": ["远东", "宝胜", "亨通"],
        "管材": ["联塑", "伟星", "中财"],
    }
    
    # 城市列表
    cities = ["北京", "上海", "广州", "深圳", "成都", "杭州", "武汉", "南京"]
    
    today = date.today()
    conn = get_connection()
    cursor = conn.cursor()
    
    # 先清空旧数据
    cursor.execute("DELETE FROM material_prices")
    conn.commit()
    
    total_saved = 0
    
    # 生成过去60天的数据（更长的趋势）
    for days_ago in range(60, -1, -1):
        collect_date = today - timedelta(days=days_ago)
        
        # 跳过周末
        if collect_date.weekday() >= 5:
            continue
        
        for category, specs in base_prices.items():
            cat_id = cat_map.get(category)
            if not cat_id:
                continue
            
            brands = brands_map.get(category, ["默认"])
            
            for spec_name, base_price, unit in specs:
                # 随机选择品牌
                brand = random.choice(brands)
                
                # 基础价格波动（±3%）
                daily_fluctuation = random.uniform(-0.03, 0.03)
                
                # 趋势：添加一些真实的市场波动模式
                # 钢筋：近期小幅上涨
                if category == "钢筋":
                    trend = (60 - days_ago) / 60 * 0.08  # 60天涨8%
                    seasonal = random.uniform(-0.02, 0.02)
                # 水泥：相对稳定
                elif category == "水泥":
                    trend = (60 - days_ago) / 60 * 0.03  # 60天涨3%
                    seasonal = random.uniform(-0.01, 0.01)
                # 混凝土：跟随水泥和砂石
                elif category == "混凝土":
                    trend = (60 - days_ago) / 60 * 0.05
                    seasonal = random.uniform(-0.02, 0.02)
                # 砂石：波动较大
                elif category == "砂石":
                    trend = (60 - days_ago) / 60 * 0.06
                    seasonal = random.uniform(-0.04, 0.04)
                # 其他：小幅波动
                else:
                    trend = (60 - days_ago) / 60 * 0.04
                    seasonal = random.uniform(-0.02, 0.02)
                
                # 最终价格
                price = base_price * (1 + daily_fluctuation + trend + seasonal)
                price = round(price, 2)
                
                # 只保存全国均价（不按城市拆分）
                try:
                    cursor.execute("""
                    INSERT OR REPLACE INTO material_prices 
                    (category_id, material_name, specification, brand, price, city, source, collect_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        cat_id,
                        spec_name,
                        spec_name.split(' ')[-1] if ' ' in spec_name else '',
                        brand,
                        price,
                        "全国",
                        "示例数据",
                        collect_date.isoformat()
                    ))
                    total_saved += 1
                except Exception as e:
                    print(f"插入失败: {e}")
        
        if days_ago % 10 == 0:
            conn.commit()
            print(f"已处理 {60 - days_ago} 天数据...")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 示例数据生成完成！")
    print(f"📊 共 {total_saved} 条价格记录")
    print(f"📅 覆盖过去60天（跳过周末）")
    print(f"📦 包含 {len(base_prices)} 个分类，{sum(len(v) for v in base_prices.values())} 种材料")


if __name__ == "__main__":
    generate_sample_data()
