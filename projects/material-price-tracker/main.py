#!/usr/bin/env python3
"""
工程材料价格跟踪系统 - 主程序
用法:
  python main.py init          # 初始化数据库
  python main.py seed          # 生成示例数据
  python main.py list          # 列出所有材料
  python main.py price <材料名> # 查看材料价格
  python main.py trend <材料名> # 生成价格趋势图
  python main.py report        # 生成价格报告
  python main.py compare <分类> # 对比同类材料
  python main.py search <关键词> # 搜索材料
"""
import sys
import os

# 确保当前目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_db, get_categories, get_latest_prices, search_materials
from seed_data import generate_sample_data
from collector import collect_daily
from analyzer import (
    get_material_list, get_category_summary, calculate_price_change,
    plot_price_trend, plot_category_comparison, generate_text_report,
    get_price_data
)


def print_table(headers, rows, widths=None):
    """打印表格"""
    if not widths:
        widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) 
                  for i, h in enumerate(headers)]
    
    # 表头
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    print(header_line)
    print("-" * len(header_line))
    
    # 数据行
    for row in rows:
        print(" | ".join(str(r).ljust(w) for r, w in zip(row, widths)))


def cmd_init():
    """初始化数据库"""
    init_db()
    print("✅ 数据库初始化完成")


def cmd_seed():
    """生成示例数据"""
    generate_sample_data()


def cmd_list():
    """列出所有材料"""
    categories = get_categories()
    
    print("\n📦 工程材料分类列表")
    print("=" * 50)
    
    for cat in categories:
        print(f"\n【{cat['name']}】单位: {cat['unit']}")
        if cat['description']:
            print(f"  说明: {cat['description']}")


def cmd_latest(category=None, city=None):
    """查看最新价格"""
    prices = get_latest_prices(category, city)
    
    if not prices:
        print("❌ 未找到价格数据，请先运行: python main.py seed")
        return
    
    print(f"\n📊 最新材料价格（{prices[0]['collect_date']}）")
    print("=" * 70)
    
    headers = ["材料名称", "规格", "品牌", "价格", "单位", "城市"]
    rows = []
    
    for p in prices:
        rows.append([
            p['material_name'][:25],
            p['specification'] or '-',
            p['brand'] or '-',
            f"¥{p['price']}",
            p['unit'],
            p['city'],
        ])
    
    print_table(headers, rows)


def cmd_price(material_name):
    """查看特定材料价格"""
    change7 = calculate_price_change(material_name, 7)
    change30 = calculate_price_change(material_name, 30)
    
    if "error" in change7:
        print(f"❌ 未找到材料: {material_name}")
        print("提示: 使用 'python main.py search <关键词>' 搜索材料")
        return
    
    print(f"\n📈 {material_name} 价格分析")
    print("=" * 50)
    print(f"当前价格: ¥{change7['current_price']}")
    print(f"数据日期: {change7['current_date']}")
    
    if change7['previous_price']:
        print(f"\n近7天变化:")
        print(f"  7天前价格: ¥{change7['previous_price']}")
        print(f"  价格变化: ¥{change7['change']:+.2f} ({change7['change_pct']:+.2f}%)")
        
        if change7['change'] > 0:
            print("  📈 上涨趋势")
        elif change7['change'] < 0:
            print("  📉 下跌趋势")
        else:
            print("  ➡️ 价格持平")
    
    if change30['previous_price']:
        print(f"\n近30天变化:")
        print(f"  30天前价格: ¥{change30['previous_price']}")
        print(f"  价格变化: ¥{change30['change']:+.2f} ({change30['change_pct']:+.2f}%)")
    
    # 统计信息
    data = get_price_data(material_name, 30)
    if data:
        prices = [d['price'] for d in data]
        print(f"\n30天统计:")
        print(f"  最高价: ¥{max(prices):.2f}")
        print(f"  最低价: ¥{min(prices):.2f}")
        print(f"  平均价: ¥{sum(prices)/len(prices):.2f}")
        print(f"  波动幅度: {(max(prices)-min(prices))/min(prices)*100:.2f}%")


def cmd_trend(material_name, days=30):
    """生成价格趋势图"""
    try:
        import numpy as np
        path = plot_price_trend(material_name, days)
        if path:
            print(f"\n✅ 趋势图已生成: {path}")
    except ImportError:
        print("❌ 需要安装依赖: pip install matplotlib numpy")
        print("或使用文字报告: python main.py report")


def cmd_compare(category, days=30):
    """对比同类材料"""
    try:
        import numpy as np
        path = plot_category_comparison(category, days)
        if path:
            print(f"\n✅ 对比图已生成: {path}")
    except ImportError:
        print("❌ 需要安装依赖: pip install matplotlib numpy")


def cmd_report(material_name=None, days=30):
    """生成文字报告"""
    report = generate_text_report(material_name, days)
    print(report)
    
    # 保存到文件
    report_path = "/home/hh127/material-price-tracker/price_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n报告已保存: {report_path}")


def cmd_collect():
    """采集今日价格"""
    collect_daily()


def cmd_search(keyword):
    """搜索材料"""
    results = search_materials(keyword)
    
    if not results:
        print(f"❌ 未找到包含 '{keyword}' 的材料")
        return
    
    print(f"\n🔍 搜索结果: '{keyword}'")
    print("=" * 40)
    
    for r in results:
        print(f"  • {r['material_name']}")


def print_help():
    """打印帮助信息"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║              工程材料价格跟踪系统                            ║
╚══════════════════════════════════════════════════════════════╝

用法: python main.py <命令> [参数]

命令:
  init              初始化数据库
  seed              生成示例数据（60天）
  list              列出所有材料分类
  latest [分类]     查看最新价格
  price <材料名>    查看特定材料价格及变化
  trend <材料名>    生成价格趋势图（需要matplotlib）
  compare <分类>    对比同类材料（需要matplotlib）
  report [材料名]   生成文字分析报告
  search <关键词>   搜索材料
  collect           采集今日价格（模拟或网络）

示例:
  python main.py init
  python main.py seed
  python main.py latest
  python main.py latest 钢筋
  python main.py price "HRB400 Φ18-25 螺纹钢"
  python main.py trend "HRB400 Φ18-25 螺纹钢"
  python main.py compare 钢筋
  python main.py report
  python main.py search 螺纹钢
  python main.py collect
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "init":
        cmd_init()
    
    elif cmd == "seed":
        cmd_seed()
    
    elif cmd == "list":
        cmd_list()
    
    elif cmd == "latest":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_latest(category)
    
    elif cmd == "price":
        if len(sys.argv) < 3:
            print("❌ 请指定材料名称")
            print("用法: python main.py price <材料名>")
            return
        cmd_price(sys.argv[2])
    
    elif cmd == "trend":
        if len(sys.argv) < 3:
            print("❌ 请指定材料名称")
            print("用法: python main.py trend <材料名> [天数]")
            return
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        cmd_trend(sys.argv[2], days)
    
    elif cmd == "compare":
        if len(sys.argv) < 3:
            print("❌ 请指定分类名称")
            print("用法: python main.py compare <分类> [天数]")
            return
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        cmd_compare(sys.argv[2], days)
    
    elif cmd == "report":
        material = sys.argv[2] if len(sys.argv) > 2 else None
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        cmd_report(material, days)
    
    elif cmd == "collect":
        cmd_collect()
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("❌ 请指定搜索关键词")
            return
        cmd_search(sys.argv[2])
    
    elif cmd in ["help", "-h", "--help"]:
        print_help()
    
    else:
        print(f"❌ 未知命令: {cmd}")
        print_help()


if __name__ == "__main__":
    main()
