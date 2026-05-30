#!/usr/bin/env python3
"""
工程材料价格跟踪系统 - Web API 服务
提供 RESTful API 接口给前端页面
"""
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from datetime import datetime, date, timedelta
import json
import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import (
    init_db, get_connection, get_categories, get_latest_prices,
    get_price_trend, search_materials,
    delete_price, delete_prices_batch, delete_prices_by_source,
    delete_prices_by_date, get_price_by_id
)
from analyzer import (
    get_material_list, get_category_summary, calculate_price_change,
    get_price_data, generate_text_report
)
from collector import collect_daily
from alert_manager import (
    load_alerts, save_alerts, add_alert, delete_alert, toggle_alert,
    check_alerts, load_alert_history, get_alert_stats, load_settings, save_settings
)
from report_engine import (
    generate_daily_report, generate_weekly_report, generate_monthly_report,
    get_report_html_data
)
from source_manager import (
    load_sources, save_sources, add_source, update_source, delete_source,
    toggle_source, get_source_stats, get_materials_by_source, get_prices_by_source,
    get_cities, get_city_price_summary
)
from mysteel_collector import MysteelCollector, collect_mysteel
from mysteel_auto_collect import extract_prices_from_homepage, save_to_database
from mysteel_smart_collector import MysteelSmartCollector, collect_mysteel_smart, PRICE_SOURCES

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 初始化数据库
init_db()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/test')
def test_page():
    """测试页面"""
    return render_template('test.html')


@app.route('/api/categories')
def api_categories():
    """获取所有材料分类"""
    categories = get_categories()
    return jsonify({
        'success': True,
        'data': categories
    })


@app.route('/api/latest')
def api_latest_prices():
    """获取最新价格（支持来源、分类、城市筛选）"""
    category = request.args.get('category')
    city = request.args.get('city')
    source = request.args.get('source')
    
    prices = get_prices_by_source(source, category, city)
    
    return jsonify({
        'success': True,
        'data': prices,
        'count': len(prices)
    })


@app.route('/api/cities')
def api_cities():
    """获取所有城市列表"""
    cities = get_cities()
    
    # 添加"全国"选项
    city_list = ['全国'] + cities
    
    return jsonify({
        'success': True,
        'data': city_list
    })


@app.route('/api/price/<material_name>')
def api_price_analysis(material_name):
    """获取材料价格分析"""
    days = int(request.args.get('days', 30))
    
    change7 = calculate_price_change(material_name, 7)
    change30 = calculate_price_change(material_name, days)
    data = get_price_data(material_name, days)
    
    return jsonify({
        'success': True,
        'data': {
            'material': material_name,
            'change_7d': change7,
            'change_30d': change30,
            'history': data
        }
    })


@app.route('/api/trend/<material_name>')
def api_price_trend(material_name):
    """获取价格趋势数据"""
    days = int(request.args.get('days', 30))
    
    data = get_price_data(material_name, days)
    
    if not data:
        return jsonify({
            'success': False,
            'message': f'未找到 {material_name} 的价格数据'
        }), 404
    
    dates = [d['collect_date'] for d in data]
    prices = [d['price'] for d in data]
    
    # 计算统计信息
    stats = {
        'min': min(prices),
        'max': max(prices),
        'avg': sum(prices) / len(prices),
        'current': prices[-1] if prices else 0,
        'change': prices[-1] - prices[0] if len(prices) > 1 else 0,
        'change_pct': ((prices[-1] - prices[0]) / prices[0] * 100) if len(prices) > 1 and prices[0] > 0 else 0
    }
    
    return jsonify({
        'success': True,
        'data': {
            'dates': dates,
            'prices': prices,
            'stats': stats
        }
    })


@app.route('/api/compare/<category>')
def api_compare(category):
    """同类材料对比"""
    days = int(request.args.get('days', 30))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取该分类下所有材料
    cursor.execute("""
        SELECT DISTINCT p.material_name
        FROM material_prices p
        JOIN material_categories c ON p.category_id = c.id
        WHERE c.name = ?
        AND p.collect_date >= date('now', ?)
        ORDER BY p.material_name
    """, (category, f"-{days} days"))
    
    materials = [row['material_name'] for row in cursor.fetchall()]
    conn.close()
    
    result = {}
    for material in materials:
        data = get_price_data(material, days)
        if data:
            result[material] = {
                'dates': [d['collect_date'] for d in data],
                'prices': [d['price'] for d in data]
            }
    
    return jsonify({
        'success': True,
        'data': result
    })


@app.route('/api/search')
def api_search():
    """搜索材料"""
    keyword = request.args.get('q', '')
    
    if not keyword:
        return jsonify({
            'success': False,
            'message': '请提供搜索关键词'
        }), 400
    
    results = search_materials(keyword)
    
    return jsonify({
        'success': True,
        'data': results,
        'count': len(results)
    })


@app.route('/api/report')
def api_report():
    """生成分析报告"""
    material = request.args.get('material')
    days = int(request.args.get('days', 30))
    report_type = request.args.get('type', 'daily')
    
    # 根据类型生成报告
    if report_type == 'weekly':
        report = generate_weekly_report()
    elif report_type == 'monthly':
        report = generate_monthly_report()
    else:
        report = generate_daily_report(material, days)
    
    return jsonify({
        'success': True,
        'data': report
    })


@app.route('/api/report/data')
def api_report_data():
    """获取报告数据（JSON格式，用于前端图表）"""
    material = request.args.get('material')
    days = int(request.args.get('days', 30))
    
    data = get_report_html_data(material, days)
    
    return jsonify({
        'success': True,
        'data': data
    })


@app.route('/api/report/types')
def api_report_types():
    """获取报告类型列表"""
    types = [
        {'id': 'daily', 'name': '每日报告', 'description': '近7天数据，适合日常监控'},
        {'id': 'weekly', 'name': '周报', 'description': '近7天数据，每周汇总'},
        {'id': 'monthly', 'name': '月报', 'description': '近30天数据，月度分析'},
        {'id': 'custom', 'name': '自定义报告', 'description': '自定义时间范围'}
    ]
    
    return jsonify({
        'success': True,
        'data': types
    })


@app.route('/api/dashboard')
def api_dashboard():
    """仪表盘数据"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取最新日期
    cursor.execute("SELECT MAX(collect_date) as latest FROM material_prices")
    latest_date = cursor.fetchone()['latest']
    
    # 获取今日价格概览
    cursor.execute("""
        SELECT 
            c.name as category,
            c.unit,
            COUNT(DISTINCT p.material_name) as count,
            ROUND(AVG(p.price), 2) as avg_price,
            ROUND(MIN(p.price), 2) as min_price,
            ROUND(MAX(p.price), 2) as max_price
        FROM material_prices p
        JOIN material_categories c ON p.category_id = c.id
        WHERE p.collect_date = ?
        GROUP BY c.name, c.unit
        ORDER BY c.name
    """, (latest_date,))
    
    categories = [dict(row) for row in cursor.fetchall()]
    
    # 获取涨跌幅排行
    materials = get_material_list()
    changes = []
    
    for m in materials:
        change = calculate_price_change(m, 7)
        if 'error' not in change and change.get('change_pct') is not None:
            changes.append({
                'material': m,
                'current_price': change['current_price'],
                'change': change.get('change', 0),
                'change_pct': change.get('change_pct', 0)
            })
    
    # 排序
    changes.sort(key=lambda x: x['change_pct'], reverse=True)
    
    # 获取总数据量
    cursor.execute("SELECT COUNT(*) as total FROM material_prices")
    total_records = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(DISTINCT material_name) as total FROM material_prices")
    total_materials = cursor.fetchone()['total']
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': {
            'latest_date': latest_date,
            'categories': categories,
            'top_gainers': changes[:5],
            'top_losers': changes[-5:] if len(changes) > 5 else [],
            'total_records': total_records,
            'total_materials': total_materials
        }
    })


@app.route('/api/export/<format_type>')
def api_export(format_type):
    """导出数据"""
    category = request.args.get('category')
    days = int(request.args.get('days', 30))
    
    prices = get_latest_prices(category)
    
    if format_type == 'csv':
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow(['材料名称', '规格', '品牌', '价格', '单位', '城市', '日期'])
        
        # 写入数据
        for p in prices:
            writer.writerow([
                p['material_name'],
                p.get('specification', ''),
                p.get('brand', ''),
                p['price'],
                p.get('unit', ''),
                p.get('city', ''),
                p.get('collect_date', '')
            ])
        
        from flask import Response
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=material_prices_{date.today().isoformat()}.csv'
            }
        )
    
    elif format_type == 'json':
        return jsonify({
            'success': True,
            'data': prices,
            'export_date': datetime.now().isoformat()
        })
    
    else:
        return jsonify({
            'success': False,
            'message': f'不支持的格式: {format_type}'
        }), 400


@app.route('/api/collect', methods=['POST'])
def api_collect():
    """手动触发采集"""
    try:
        collect_daily()
        return jsonify({
            'success': True,
            'message': '采集完成'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/alerts', methods=['GET'])
def api_get_alerts():
    """获取所有预警规则"""
    alerts = load_alerts()
    stats = get_alert_stats()
    
    return jsonify({
        'success': True,
        'data': alerts,
        'stats': stats
    })


@app.route('/api/alerts', methods=['POST'])
def api_set_alert():
    """添加预警规则"""
    data = request.json
    
    material = data.get('material')
    condition = data.get('condition', 'above')
    threshold = data.get('threshold')
    notify_method = data.get('notify_method', 'browser')
    
    if not material or not threshold:
        return jsonify({
            'success': False,
            'message': '请填写完整信息'
        }), 400
    
    alert = add_alert(material, condition, float(threshold), notify_method)
    
    return jsonify({
        'success': True,
        'data': alert,
        'message': '预警规则已添加'
    })


@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def api_delete_alert(alert_id):
    """删除预警规则"""
    delete_alert(alert_id)
    
    return jsonify({
        'success': True,
        'message': '预警规则已删除'
    })


@app.route('/api/alerts/<int:alert_id>/toggle', methods=['POST'])
def api_toggle_alert(alert_id):
    """启用/禁用预警规则"""
    data = request.json
    enabled = data.get('enabled', True)
    
    toggle_alert(alert_id, enabled)
    
    return jsonify({
        'success': True,
        'message': f'预警规则已{"启用" if enabled else "禁用"}'
    })


@app.route('/api/check-alerts')
def api_check_alerts():
    """检查预警触发"""
    triggered = check_alerts()
    
    return jsonify({
        'success': True,
        'data': triggered,
        'count': len(triggered)
    })


@app.route('/api/alert-history')
def api_alert_history():
    """获取预警历史"""
    history = load_alert_history()
    
    # 按时间倒序
    history.sort(key=lambda x: x.get('triggered_at', ''), reverse=True)
    
    return jsonify({
        'success': True,
        'data': history[:100],  # 只返回最近100条
        'total': len(history)
    })


@app.route('/api/alert-settings', methods=['GET'])
def api_get_alert_settings():
    """获取预警设置"""
    settings = load_settings()
    
    return jsonify({
        'success': True,
        'data': settings
    })


@app.route('/api/alert-settings', methods=['POST'])
def api_save_alert_settings():
    """保存预警设置"""
    data = request.json
    save_settings(data)
    
    return jsonify({
        'success': True,
        'message': '设置已保存'
    })

@app.route('/api/sources')
def api_get_sources():
    """获取所有数据来源"""
    sources = load_sources()
    stats = get_source_stats()
    
    # 合并配置和统计
    result = []
    for source in sources:
        # 查找对应的统计
        stat = next((s for s in stats if s['source_id'] == source['id']), None)
        
        result.append({
            **source,
            'total_records': stat['total_records'] if stat else 0,
            'material_count': stat['material_count'] if stat else 0,
            'latest_date': stat['latest_date'] if stat else None
        })
    
    return jsonify({
        'success': True,
        'data': result,
        'stats': stats
    })


@app.route('/api/sources', methods=['POST'])
def api_add_source():
    """添加数据来源"""
    data = request.json
    
    if not data.get('name'):
        return jsonify({'success': False, 'message': '请填写来源名称'}), 400
    
    source = add_source(data)
    
    return jsonify({
        'success': True,
        'data': source,
        'message': '数据来源已添加'
    })


@app.route('/api/sources/<source_id>', methods=['PUT'])
def api_update_source(source_id):
    """更新数据来源"""
    data = request.json
    update_source(source_id, data)
    
    return jsonify({
        'success': True,
        'message': '数据来源已更新'
    })


@app.route('/api/sources/<source_id>', methods=['DELETE'])
def api_delete_source(source_id):
    """删除数据来源"""
    delete_source(source_id)
    
    return jsonify({
        'success': True,
        'message': '数据来源已删除'
    })


@app.route('/api/sources/<source_id>/toggle', methods=['POST'])
def api_toggle_source(source_id):
    """启用/禁用数据来源"""
    data = request.json
    enabled = data.get('enabled', True)
    toggle_source(source_id, enabled)
    
    return jsonify({
        'success': True,
        'message': f'数据来源已{"启用" if enabled else "禁用"}'
    })


@app.route('/api/sources/stats')
def api_source_stats():
    """获取数据来源统计"""
    stats = get_source_stats()
    
    return jsonify({
        'success': True,
        'data': stats
    })


@app.route('/api/sources/<source_name>/materials')
def api_source_materials(source_name):
    """获取指定来源的材料列表"""
    materials = get_materials_by_source(source_name)
    
    return jsonify({
        'success': True,
        'data': materials
    })


@app.route('/api/sources/<source_name>/prices')
def api_source_prices(source_name):
    """获取指定来源的价格列表"""
    category = request.args.get('category')
    prices = get_prices_by_source(source_name, category)
    
    return jsonify({
        'success': True,
        'data': prices,
        'count': len(prices)
    })






@app.route('/api/mysteel/login', methods=['POST'])
def api_mysteel_login():
    """登录我的钢铁网"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    collector = MysteelCollector(username, password)
    success = collector.login()
    
    return jsonify({
        'success': success,
        'message': '登录成功' if success else '登录失败'
    })


@app.route('/api/mysteel/collect', methods=['POST'])
def api_mysteel_collect():
    """采集我的钢铁网数据（从首页提取）"""
    try:
        # 从首页提取价格
        prices = extract_prices_from_homepage()
        
        if prices:
            # 保存到数据库
            saved = save_to_database(prices)
            return jsonify({
                'success': True,
                'message': f'采集完成，共 {saved} 条数据',
                'data': {
                    'total': len(prices),
                    'saved': saved,
                    'prices': prices
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': '未提取到价格数据，可能 Cookie 已过期'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'采集失败: {str(e)}'
        }), 500


@app.route('/api/mysteel/status')
def api_mysteel_status():
    """检查我的钢铁网登录状态"""
    collector = MysteelCollector()
    logged_in = collector._load_cookies()
    
    return jsonify({
        'success': True,
        'logged_in': logged_in,
        'username': collector.username
    })




@app.route('/api/mysteel/smart-collect', methods=['POST'])
def api_mysteel_smart_collect():
    """智能采集（支持选择模式和品种）"""
    data = request.json or {}
    mode = data.get('mode', 'homepage')  # homepage / all / custom
    material_types = data.get('material_types', [])
    
    try:
        if mode == 'homepage':
            # 首页快速采集
            saved = collect_mysteel_smart(use_homepage=True)
        elif mode == 'all':
            # 全品种采集
            saved = collect_mysteel_smart(use_homepage=False)
        elif mode == 'custom' and material_types:
            # 自定义品种
            saved = collect_mysteel_smart(material_types=material_types, use_homepage=False)
        else:
            return jsonify({
                'success': False,
                'message': '无效的采集模式'
            }), 400
        
        return jsonify({
            'success': True,
            'message': f'采集完成，共 {saved} 条数据',
            'data': {'saved': saved}
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'采集失败: {str(e)}'
        }), 500


@app.route('/api/mysteel/sources')
def api_mysteel_sources():
    """获取可采集的品种列表"""
    sources = []
    for name, info in PRICE_SOURCES.items():
        sources.append({
            'name': name,
            'category': info['category'],
            'unit': info['unit'],
            'url': info['url']
        })
    
    return jsonify({
        'success': True,
        'data': sources,
        'total': len(sources)
    })




@app.route('/api/prices/<int:price_id>', methods=['DELETE'])
def api_delete_price(price_id):
    """删除单条价格记录"""
    # 先检查记录是否存在
    price = get_price_by_id(price_id)
    if not price:
        return jsonify({
            'success': False,
            'message': '记录不存在'
        }), 404
    
    success = delete_price(price_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': f'已删除: {price["material_name"]}'
        })
    else:
        return jsonify({
            'success': False,
            'message': '删除失败'
        }), 500


@app.route('/api/prices/batch-delete', methods=['POST'])
def api_delete_prices_batch():
    """批量删除价格记录"""
    data = request.json
    price_ids = data.get('ids', [])
    
    if not price_ids:
        return jsonify({
            'success': False,
            'message': '请选择要删除的记录'
        }), 400
    
    deleted = delete_prices_batch(price_ids)
    
    return jsonify({
        'success': True,
        'message': f'已删除 {deleted} 条记录',
        'data': {'deleted': deleted}
    })


@app.route('/api/prices/by-source/<source>', methods=['DELETE'])
def api_delete_by_source(source):
    """按来源删除价格记录"""
    deleted = delete_prices_by_source(source)
    
    return jsonify({
        'success': True,
        'message': f'已删除 {deleted} 条来自 {source} 的记录',
        'data': {'deleted': deleted}
    })


@app.route('/api/prices/by-date/<date>', methods=['DELETE'])
def api_delete_by_date(date):
    """按日期删除价格记录"""
    deleted = delete_prices_by_date(date)
    
    return jsonify({
        'success': True,
        'message': f'已删除 {deleted} 条 {date} 的记录',
        'data': {'deleted': deleted}
    })

if __name__ == '__main__':
    print("=" * 50)
    print("工程材料价格跟踪系统 - Web 服务")
    print("=" * 50)
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
