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
