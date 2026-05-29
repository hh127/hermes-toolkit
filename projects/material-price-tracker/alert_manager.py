#!/usr/bin/env python3
"""
预警管理模块
支持定时检查、通知推送、历史记录
"""
import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional
from models import get_connection
from analyzer import calculate_price_change

ALERTS_FILE = os.path.join(os.path.dirname(__file__), 'alerts.json')
ALERT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'alert_history.json')
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'alert_settings.json')


def load_alerts() -> List[Dict]:
    """加载预警规则"""
    if not os.path.exists(ALERTS_FILE):
        return []
    
    with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_alerts(alerts: List[Dict]):
    """保存预警规则"""
    with open(ALERTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)


def add_alert(material: str, condition: str, threshold: float, 
              notify_method: str = 'browser', enabled: bool = True) -> Dict:
    """
    添加预警规则
    
    Args:
        material: 材料名称
        condition: 条件 ('above' 或 'below')
        threshold: 阈值价格
        notify_method: 通知方式 ('browser', 'email', 'wechat')
        enabled: 是否启用
    
    Returns:
        新添加的预警规则
    """
    alerts = load_alerts()
    
    alert = {
        'id': max([a.get('id', 0) for a in alerts], default=0) + 1,
        'material': material,
        'condition': condition,
        'threshold': threshold,
        'notify_method': notify_method,
        'enabled': enabled,
        'created_at': datetime.now().isoformat(),
        'last_triggered': None,
        'trigger_count': 0
    }
    
    alerts.append(alert)
    save_alerts(alerts)
    
    return alert


def delete_alert(alert_id: int) -> bool:
    """删除预警规则"""
    alerts = load_alerts()
    alerts = [a for a in alerts if a.get('id') != alert_id]
    save_alerts(alerts)
    return True


def toggle_alert(alert_id: int, enabled: bool) -> bool:
    """启用/禁用预警规则"""
    alerts = load_alerts()
    for alert in alerts:
        if alert.get('id') == alert_id:
            alert['enabled'] = enabled
            break
    save_alerts(alerts)
    return True


def check_alerts() -> List[Dict]:
    """
    检查所有预警规则，返回触发的预警
    
    Returns:
        触发的预警列表
    """
    alerts = load_alerts()
    triggered = []
    
    for alert in alerts:
        if not alert.get('enabled', True):
            continue
        
        material = alert.get('material')
        condition = alert.get('condition')
        threshold = alert.get('threshold')
        
        # 获取最新价格
        change = calculate_price_change(material, 1)
        if 'error' in change:
            continue
        
        current_price = change.get('current_price', 0)
        
        # 检查条件
        is_triggered = False
        if condition == 'above' and current_price > threshold:
            is_triggered = True
        elif condition == 'below' and current_price < threshold:
            is_triggered = True
        
        if is_triggered:
            # 更新触发次数
            alert['trigger_count'] = alert.get('trigger_count', 0) + 1
            alert['last_triggered'] = datetime.now().isoformat()
            
            triggered.append({
                **alert,
                'current_price': current_price,
                'message': f'{material} 当前价格 ¥{current_price:.2f} 已{"超过" if condition == "above" else "低于"}预警值 ¥{threshold:.2f}'
            })
    
    # 保存更新后的触发次数
    if triggered:
        save_alerts(alerts)
        # 记录历史
        save_alert_history(triggered)
    
    return triggered


def save_alert_history(triggered_alerts: List[Dict]):
    """保存预警触发历史"""
    history = load_alert_history()
    
    for alert in triggered_alerts:
        history.append({
            'alert_id': alert.get('id'),
            'material': alert.get('material'),
            'condition': alert.get('condition'),
            'threshold': alert.get('threshold'),
            'current_price': alert.get('current_price'),
            'message': alert.get('message'),
            'triggered_at': datetime.now().isoformat()
        })
    
    # 只保留最近1000条记录
    if len(history) > 1000:
        history = history[-1000:]
    
    with open(ALERT_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def load_alert_history() -> List[Dict]:
    """加载预警历史"""
    if not os.path.exists(ALERT_HISTORY_FILE):
        return []
    
    with open(ALERT_HISTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_alert_stats() -> Dict:
    """获取预警统计信息"""
    alerts = load_alerts()
    history = load_alert_history()
    
    return {
        'total_alerts': len(alerts),
        'enabled_alerts': len([a for a in alerts if a.get('enabled', True)]),
        'total_triggers': len(history),
        'today_triggers': len([h for h in history if h.get('triggered_at', '').startswith(date.today().isoformat())])
    }


def load_settings() -> Dict:
    """加载预警设置"""
    if not os.path.exists(SETTINGS_FILE):
        return {
            'check_interval': 3600,  # 检查间隔（秒）
            'enable_browser_notify': True,
            'enable_email_notify': False,
            'email_address': '',
            'enable_wechat_notify': False,
            'wechat_webhook': ''
        }
    
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_settings(settings: Dict):
    """保存预警设置"""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # 测试代码
    print("当前预警规则:")
    for alert in load_alerts():
        print(f"  - {alert['material']}: {alert['condition']} ¥{alert['threshold']}")
    
    print("\n检查预警...")
    triggered = check_alerts()
    if triggered:
        print("触发的预警:")
        for t in triggered:
            print(f"  ⚠️ {t['message']}")
    else:
        print("无触发的预警")
