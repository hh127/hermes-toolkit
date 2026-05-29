        // Load Alerts
        async function loadAlerts() {
            try {
                // 加载预警规则
                const response = await fetch(`${API_BASE}/api/alerts`);
                const data = await response.json();
                
                if (data.success) {
                    const alerts = data.data;
                    const stats = data.stats;
                    
                    // 更新统计
                    document.getElementById('alert-total').textContent = stats.total_alerts;
                    document.getElementById('alert-enabled').textContent = stats.enabled_alerts;
                    document.getElementById('alert-today').textContent = stats.today_triggers;
                    document.getElementById('alert-total-triggers').textContent = stats.total_triggers;
                    document.getElementById('alert-count').textContent = alerts.length;
                    
                    // 更新预警列表
                    const html = alerts.map(alert => `
                        <tr>
                            <td>${alert.material}</td>
                            <td>
                                <span class="badge ${alert.condition === 'above' ? 'bg-danger' : 'bg-success'}">
                                    ${alert.condition === 'above' ? '高于' : '低于'}
                                </span>
                            </td>
                            <td>¥${alert.threshold.toFixed(2)}</td>
                            <td>${alert.trigger_count || 0} 次</td>
                            <td>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" 
                                        ${alert.enabled ? 'checked' : ''} 
                                        onchange="toggleAlertEnabled(${alert.id}, this.checked)">
                                </div>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-outline-danger" onclick="deleteAlert(${alert.id})">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                    
                    document.getElementById('alerts-table').innerHTML = html || 
                        '<tr><td colspan="6" class="text-center text-muted py-4">暂无预警规则</td></tr>';
                }
                
                // 加载触发的预警
                const triggeredResponse = await fetch(`${API_BASE}/api/check-alerts`);
                const triggeredData = await triggeredResponse.json();
                
                if (triggeredData.success && triggeredData.data.length > 0) {
                    const triggeredHtml = triggeredData.data.map(alert => `
                        <div class="alert alert-warning mb-2">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <i class="bi bi-exclamation-triangle"></i>
                                    <strong>${alert.material}</strong>
                                </div>
                                <small class="text-muted">${new Date().toLocaleTimeString()}</small>
                            </div>
                            <div class="mt-1">${alert.message}</div>
                        </div>
                    `).join('');
                    document.getElementById('triggered-alerts').innerHTML = triggeredHtml;
                } else {
                    document.getElementById('triggered-alerts').innerHTML = 
                        '<p class="text-muted text-center py-4">暂无触发的预警</p>';
                }
                
                // 加载预警历史
                loadAlertHistory();
                
            } catch (error) {
                console.error('Load alerts failed:', error);
            }
        }
        
        // Load Alert History
        async function loadAlertHistory() {
            try {
                const response = await fetch(`${API_BASE}/api/alert-history`);
                const data = await response.json();
                
                if (data.success && data.data.length > 0) {
                    const html = data.data.map(item => `
                        <tr>
                            <td><small>${item.triggered_at ? new Date(item.triggered_at).toLocaleString() : '-'}</small></td>
                            <td>${item.material}</td>
                            <td>${item.condition === 'above' ? '高于' : '低于'}</td>
                            <td>¥${item.threshold}</td>
                            <td>¥${item.current_price}</td>
                            <td><small>${item.message}</small></td>
                        </tr>
                    `).join('');
                    
                    document.getElementById('alert-history-table').innerHTML = html;
                }
            } catch (error) {
                console.error('Load alert history failed:', error);
            }
        }
        
        // Show Add Alert Modal
        function showAddAlert() {
            const modal = new bootstrap.Modal(document.getElementById('alertModal'));
            modal.show();
        }
        
        // Save Alert
        async function saveAlert() {
            const material = document.getElementById('alert-material').value;
            const condition = document.getElementById('alert-condition').value;
            const threshold = document.getElementById('alert-threshold').value;
            const notifyMethod = document.getElementById('alert-notify').value;
            
            if (!material || !threshold) {
                alert('请填写完整信息');
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE}/api/alerts`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        material,
                        condition,
                        threshold: parseFloat(threshold),
                        notify_method: notifyMethod
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('alertModal'));
                    modal.hide();
                    
                    // 清空表单
                    document.getElementById('alert-material').value = '';
                    document.getElementById('alert-threshold').value = '';
                    
                    // 重新加载
                    loadAlerts();
                    
                    alert('预警规则已添加');
                } else {
                    alert(data.message || '添加失败');
                }
            } catch (error) {
                console.error('Save alert failed:', error);
                alert('添加失败: ' + error.message);
            }
        }
        
        // Toggle Alert Enabled
        async function toggleAlertEnabled(id, enabled) {
            try {
                await fetch(`${API_BASE}/api/alerts/${id}/toggle`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ enabled })
                });
                
                loadAlerts();
            } catch (error) {
                console.error('Toggle alert failed:', error);
            }
        }
        
        // Delete Alert
        async function deleteAlert(id) {
            if (!confirm('确定删除此预警？')) {
                return;
            }
            
            try {
                await fetch(`${API_BASE}/api/alerts/${id}`, {
                    method: 'DELETE'
                });
                
                loadAlerts();
            } catch (error) {
                console.error('Delete alert failed:', error);
            }
        }
        
        // Check Alerts Now
        async function checkAlertsNow() {
            try {
                const response = await fetch(`${API_BASE}/api/check-alerts`);
                const data = await response.json();
                
                if (data.success) {
                    if (data.data.length > 0) {
                        alert(`发现 ${data.data.length} 个触发的预警！`);
                    } else {
                        alert('没有触发的预警');
                    }
                    
                    loadAlerts();
                }
            } catch (error) {
                console.error('Check alerts failed:', error);
            }
        }
