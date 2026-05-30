#!/usr/bin/env python3
"""
使用 Pyppeteer 浏览器模拟采集我的钢铁网价格数据
"""
import asyncio
from pyppeteer import launch
import json
import re
from datetime import date
from bs4 import BeautifulSoup


async def collect_with_browser():
    """使用浏览器采集价格"""
    
    print("="*60)
    print("Pyppeteer 浏览器采集测试")
    print("="*60)

    print("\n正在启动浏览器...")
    browser = await launch({
        'headless': True,
        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
        ]
    })
    
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    
    # 加载Cookie
    with open('mysteel_cookies.json', 'r') as f:
        cookies = json.load(f)
    
    for name, value in cookies.items():
        await page.setCookie({
            'name': name,
            'value': value,
            'domain': '.mysteel.com',
            'path': '/',
        })
    
    print(f"已设置 {len(cookies)} 个Cookie")
    
    # 测试页面
    test_pages = {
        '螺纹钢': 'https://list1.mysteel.com/market/p-221-----010101-0--------1.html',
        '水泥': 'https://list1.mysteel.com/market/p-219-----01011001-0--------1.html',
    }
    
    all_prices = []
    
    for name, url in test_pages.items():
        print(f"\n{'='*40}")
        print(f"采集 {name}: {url}")
        print('='*40)
        
        try:
            await page.goto(url, {
                'waitUntil': 'networkidle0',
                'timeout': 60000
            })
            
            # 等待JavaScript加载
            print("等待页面加载...")
            await asyncio.sleep(5)
            
            # 获取渲染后的HTML
            content = await page.content()
            print(f"页面大小: {len(content)} 字符")
            
            # 保存HTML
            safe_name = name.replace('/', '_')
            with open(f'rendered_{safe_name}.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 用BeautifulSoup解析
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找表格
            tables = soup.find_all('table')
            print(f"找到 {len(tables)} 个表格")
            
            for i, table in enumerate(tables):
                rows = table.find_all('tr')
                if len(rows) <= 1:
                    continue
                    
                # 检查表头
                header = rows[0]
                header_cells = header.find_all(['th', 'td'])
                header_text = [c.get_text(strip=True) for c in header_cells]
                header_str = ' '.join(header_text)
                
                # 是否是价格表格
                is_price_table = any(kw in header_str for kw in ['价格', '报价', '元', '涨跌', '品名', '规格'])
                
                if is_price_table:
                    print(f"\n✅ 价格表格 {i+1}: {len(rows)-1} 行数据")
                    print(f"  表头: {header_text[:8]}")
                    
                    # 提取数据
                    for row in rows[1:]:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 3:
                            cell_texts = [c.get_text(strip=True) for c in cells]
                            
                            # 查找价格（4位数字）
                            price = None
                            for text in cell_texts:
                                match = re.search(r'(\d{3,4}(?:\.\d+)?)\s*$', text)
                                if match:
                                    p = float(match.group(1))
                                    if 200 < p < 10000:
                                        price = p
                                        break
                            
                            if price:
                                all_prices.append({
                                    'name': name,
                                    'data': cell_texts,
                                    'price': price,
                                })
            
            # 也用正则从整个页面文本提取
            text = soup.get_text()
            
            # 查找 "材料名 规格 价格元/吨" 模式
            if name == '螺纹钢':
                patterns = [
                    r'(上海|北京|广州|天津|杭州|南京|武汉|成都|重庆|西安)\s+.*?(HRB400\s*\S+)\s+.*?(\d{4})\s',
                    r'(螺纹钢)\s+(\S+)\s+(\d{4})\s',
                ]
            elif name == '水泥':
                patterns = [
                    r'(上海|北京|广州|天津|杭州|南京|武汉|成都|重庆|西安)\s+.*?(P\.\w\s*\d+\.\d+\s*\S*)\s+.*?(\d{3,4})\s',
                ]
            else:
                patterns = []
            
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    print(f"\n正则匹配到 {len(matches)} 条:")
                    for m in matches[:5]:
                        print(f"  {m}")
                        
        except Exception as e:
            print(f"❌ 采集失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 汇总结果
    print("\n" + "="*60)
    print("采集结果汇总")
    print("="*60)
    
    if all_prices:
        print(f"\n共采集到 {len(all_prices)} 条价格数据:")
        for p in all_prices[:10]:
            print(f"  [{p['name']}] {p['data'][:3]} - ¥{p['price']}")
    else:
        print("\n⚠️ 未从表格中提取到价格数据")
    
    # 查看渲染后的HTML内容
    print("\n" + "="*60)
    print("分析渲染后页面")
    print("="*60)
    
    # 重新分析渲染后的HTML
    try:
        with open('rendered_螺纹钢.html', 'r', encoding='utf-8') as f:
            rendered = f.read()
        
        # 统计变化
        print(f"\n渲染后页面大小: {len(rendered)} 字符")
        
        # 查找价格相关元素
        price_patterns = [
            r'元/吨',
            r'元/立方米',
            r'HRB\d+',
            r'Φ\d+',
            r'报价',
        ]
        
        for pattern in price_patterns:
            count = len(re.findall(pattern, rendered))
            print(f"  '{pattern}': {count} 个匹配")
        
        # 查找数据表格
        soup = BeautifulSoup(rendered, 'html.parser')
        
        # 查找所有class包含data-table或price-table的元素
        data_tables = soup.find_all(class_=re.compile(r'data|price|table|list', re.I))
        print(f"\n找到 {len(data_tables)} 个数据相关元素")
        
        for elem in data_tables[:5]:
            tag = elem.name
            cls = elem.get('class', [])
            text = elem.get_text(strip=True)[:80]
            print(f"  <{tag} class={cls}>: {text}...")
            
    except Exception as e:
        print(f"分析失败: {e}")
    
    await browser.close()
    print("\n✅ 浏览器已关闭")


if __name__ == '__main__':
    asyncio.run(collect_with_browser())
