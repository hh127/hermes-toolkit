#!/usr/bin/env python3
"""
Cookie管理工具
用于更新我的钢铁网Cookie，获取真实价格数据
"""
import json
import os
import sys
import requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIES_FILE = os.path.join(BASE_DIR, 'mysteel_cookies.json')


def load_cookies():
    """加载当前Cookie"""
    if not os.path.exists(COOKIES_FILE):
        return {}
    
    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_cookies(cookies):
    """保存Cookie"""
    with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"✅ Cookie已保存到 {COOKIES_FILE}")


def test_cookies(cookies):
    """测试Cookie是否有效"""
    print("\n测试Cookie有效性...")
    
    session = requests.Session()
    session.cookies.update(cookies)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    # 测试访问西安价格页面
    url = 'https://jiancai.mysteel.com/m/26052910/892658956BF3E75C.html'
    
    try:
        response = session.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            # 检查是否有真实价格（不是***）
            if '***' in response.text and 'data-encrypt="true"' in response.text:
                print("⚠️ Cookie有效，但价格仍被加密（可能需要会员权限）")
                return False
            elif '元/吨' in response.text:
                # 检查是否有数字价格
                import re
                prices = re.findall(r'(\d{3,4}(?:\.\d+)?)\s*元/吨', response.text)
                if prices:
                    print(f"✅ Cookie有效！找到 {len(prices)} 个真实价格")
                    print(f"   示例: {prices[:3]}")
                    return True
            
            print("⚠️ Cookie可能有效，但未找到明确的价格数据")
            return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def import_from_browser():
    """从浏览器导入Cookie（手动方式）"""
    print("\n" + "="*60)
    print("从浏览器导入Cookie")
    print("="*60)
    print("""
请按以下步骤操作：

1. 打开浏览器，访问 https://www.mysteel.com
2. 登录你的账号
3. 按 F12 打开开发者工具
4. 切换到 Application（应用程序）标签
5. 在左侧找到 Cookies → https://www.mysteel.com
6. 复制所有Cookie值

Cookie格式示例：
{
  "_login_token": "xxxxx",
  "_MSPASS_SESSION": "xxxxx",
  ...
}
""")
    
    print("请粘贴Cookie JSON（直接从浏览器复制）:")
    print("（输入完成后按两次回车）")
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == '':
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
    
    if not lines:
        print("❌ 未输入Cookie")
        return None
    
    try:
        cookie_text = '\n'.join(lines)
        cookies = json.loads(cookie_text)
        
        if isinstance(cookies, dict):
            print(f"\n✅ 解析成功，共 {len(cookies)} 个Cookie")
            return cookies
        else:
            print("❌ Cookie格式错误，应该是JSON对象")
            return None
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print("\n尝试其他格式...")
        
        # 尝试解析 "key=value; key2=value2" 格式
        cookie_text = '\n'.join(lines)
        cookies = {}
        
        for pair in cookie_text.replace('\n', ';').split(';'):
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()
        
        if cookies:
            print(f"✅ 解析成功，共 {len(cookies)} 个Cookie")
            return cookies
        
        return None


def import_from_string(cookie_string):
    """从字符串导入Cookie"""
    cookies = {}
    
    # 解析 "key=value; key2=value2" 格式
    for pair in cookie_string.split(';'):
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    return cookies


def show_current_cookies():
    """显示当前Cookie信息"""
    cookies = load_cookies()
    
    if not cookies:
        print("❌ 没有找到Cookie文件")
        return
    
    print(f"\n当前Cookie: {len(cookies)} 个")
    print("\n主要Cookie:")
    
    important_keys = ['_login_token', '_MSPASS_SESSION', 'WM_NI', 'WM_NIKE', 'WM_TID']
    
    for key in important_keys:
        if key in cookies:
            value = cookies[key]
            if len(value) > 30:
                value = value[:30] + '...'
            print(f"  ✅ {key}: {value}")
        else:
            print(f"  ❌ {key}: 缺失")
    
    # 检查最后更新时间
    last_time = cookies.get('_last_ch_r_t', '')
    if last_time:
        try:
            timestamp = int(last_time) / 1000
            dt = datetime.fromtimestamp(timestamp)
            hours_ago = (datetime.now() - dt).total_seconds() / 3600
            
            if hours_ago < 24:
                print(f"\n✅ 最后活动: {dt.strftime('%Y-%m-%d %H:%M')} ({hours_ago:.1f}小时前)")
            else:
                print(f"\n⚠️ 最后活动: {dt.strftime('%Y-%m-%d %H:%M')} ({hours_ago/24:.1f}天前)")
                print("   Cookie可能已过期，建议更新")
        except:
            pass


def interactive_update():
    """交互式更新Cookie"""
    print("="*60)
    print("我的钢铁网Cookie管理工具")
    print("="*60)
    
    while True:
        print("\n请选择操作:")
        print("1. 查看当前Cookie")
        print("2. 测试Cookie有效性")
        print("3. 从浏览器导入Cookie")
        print("4. 手动输入Cookie字符串")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == '1':
            show_current_cookies()
            
        elif choice == '2':
            cookies = load_cookies()
            if cookies:
                test_cookies(cookies)
            else:
                print("❌ 没有Cookie，请先导入")
                
        elif choice == '3':
            cookies = import_from_browser()
            if cookies:
                save_cookies(cookies)
                test_cookies(cookies)
                
        elif choice == '4':
            print("\n请输入Cookie字符串 (格式: key1=value1; key2=value2; ...):")
            cookie_string = input().strip()
            
            if cookie_string:
                cookies = import_from_string(cookie_string)
                if cookies:
                    save_cookies(cookies)
                    test_cookies(cookies)
                    
        elif choice == '5':
            print("再见！")
            break
            
        else:
            print("无效选项，请重新输入")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == 'test':
            cookies = load_cookies()
            if cookies:
                test_cookies(cookies)
            else:
                print("❌ 没有Cookie")
                
        elif sys.argv[1] == 'show':
            show_current_cookies()
            
        elif sys.argv[1] == 'import' and len(sys.argv) > 2:
            # 从文件导入
            file_path = sys.argv[2]
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                save_cookies(cookies)
                test_cookies(cookies)
            else:
                print(f"❌ 文件不存在: {file_path}")
                
        elif sys.argv[1] == 'help':
            print("""
用法:
  python cookie_manager.py              # 交互式模式
  python cookie_manager.py test         # 测试Cookie
  python cookie_manager.py show         # 显示Cookie
  python cookie_manager.py import FILE  # 从文件导入
""")
        else:
            print("未知命令，使用 'help' 查看帮助")
    else:
        # 交互式模式
        interactive_update()
