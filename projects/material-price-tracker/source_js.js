        // Source Charts
        let sourceDistributionChart;
        
        // Load Sources
        async function loadSources() {
            try {
                const response = await fetch(`${API_BASE}/api/sources`);
                const data = await response.json();
                
                if (data.success) {
                    const sources = data.data;
                    const stats = data.stats;
                    
                    // 更新统计
                    document.getElementById('source-total').textContent = sources.length;
                    document.getElementById('source-enabled').textContent = sources.filter(s => s.enabled).length;
                    
                    const totalRecords = stats.reduce((sum, s) => sum + s.total_records, 0);
                    const totalMaterials = Math.max(...stats.map(s => s.material_count), 0);
                    
                    document.getElementById('source-records').textContent = totalRecords.toLocaleString();
                    document.getElementById('source-materials').textContent = totalMaterials;
                    
                    // 更新表格
                    const html = sources.map(source => `
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    <i class="bi ${source.icon || 'bi-link'} me-2 text-primary"></i>
                                    <div>
                                        <div class="fw-bold">${source.name}</div>
                                        <small class="text-muted">${source.url || '-'}</small>
                                    </div>
                                </div>
                            </td>
                            <td><span class="badge bg-info">${source.category}</span></td>
                            <td>${(source.total_records || 0).toLocaleString()}</td>
                            <td>${source.material_count || 0}</td>
                            <td>${source.latest_date || '-'}</td>
                            <td>
                                <div class="form-check form-switch">
                                    <input class="form-check-input" type="checkbox" 
                                        ${source.enabled ? 'checked' : ''} 
                                        onchange="toggleSource('${source.id}', this.checked)">
                                </div>
                            </td>
                            <td>
                                <div class="btn-group btn-group-sm">
                                    <button class="btn btn-outline-primary" onclick="viewSourceDetail('${source.name}')">
                                        <i class="bi bi-eye"></i>
                                    </button>
                                    <button class="btn btn-outline-danger" onclick="deleteSource('${source.id}')">
                                        <i class="bi bi-trash"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `).join('');
                    
                    document.getElementById('sources-table').innerHTML = html || 
                        '<tr><td colspan="7" class="text-center text-muted py-4">暂无数据来源</td></tr>';
                    
                    // 更新图表
                    updateSourceChart(stats);
                    
                    // 更新价格页面的来源筛选
                    updateSourceFilter(sources);
                }
            } catch (error) {
                console.error('Load sources failed:', error);
            }
        }
        
        // Update Source Chart
        function updateSourceChart(stats) {
            const ctx = document.getElementById('source-distribution-chart').getContext('2d');
            
            if (sourceDistributionChart) {
                sourceDistributionChart.destroy();
            }
            
            const colors = [
                '#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#6366f1'
            ];
            
            sourceDistributionChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: stats.map(s => s.source_name),
                    datasets: [{
                        data: stats.map(s => s.total_records),
                        backgroundColor: colors.slice(0, stats.length)
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                font: { size: 10 },
                                padding: 10
                            }
                        }
                    }
                }
            });
        }
        
        // Update Source Filter (for prices page)
        function updateSourceFilter(sources) {
            const select = document.getElementById('source-filter');
            if (select) {
                const html = sources
                    .filter(s => s.enabled)
                    .map(s => `<option value="${s.name}">${s.name}</option>`)
                    .join('');
                select.innerHTML = '<option value="">全部来源</option>' + html;
            }
        }
        
        // View Source Detail
        async function viewSourceDetail(sourceName) {
            try {
                const response = await fetch(`${API_BASE}/api/sources/${encodeURIComponent(sourceName)}/prices`);
                const data = await response.json();
                
                if (data.success) {
                    const prices = data.data;
                    
                    const html = `
                        <h6 class="mb-3">${sourceName} - 数据详情</h6>
                        <p class="text-muted">共 ${prices.length} 条数据</p>
                        <div class="table-responsive" style="max-height: 300px; overflow-y: auto;">
                            <table class="table table-sm table-hover">
                                <thead>
                                    <tr>
                                        <th>材料</th>
                                        <th>规格</th>
                                        <th>价格</th>
                                        <th>日期</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${prices.slice(0, 50).map(p => `
                                        <tr>
                                            <td>${p.material_name}</td>
                                            <td>${p.specification || '-'}</td>
                                            <td>¥${p.price.toFixed(2)}</td>
                                            <td>${p.collect_date}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                    
                    document.getElementById('source-details').innerHTML = html;
                }
            } catch (error) {
                console.error('View source detail failed:', error);
            }
        }
        
        // Show Add Source Modal
        function showAddSource() {
            const modal = new bootstrap.Modal(document.getElementById('sourceModal'));
            modal.show();
        }
        
        // Save Source
        async function saveSource() {
            const id = document.getElementById('source-id').value;
            const name = document.getElementById('source-name').value;
            const url = document.getElementById('source-url').value;
            const category = document.getElementById('source-category').value;
            const description = document.getElementById('source-description').value;
            
            if (!name) {
                alert('请填写来源名称');
                return;
            }
            
            try {
                const response = await fetch(`${API_BASE}/api/sources`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: id || name.toLowerCase().replace(/\s+/g, '_'),
                        name,
                        url,
                        category,
                        description
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('sourceModal'));
                    modal.hide();
                    
                    // 清空表单
                    document.getElementById('source-id').value = '';
                    document.getElementById('source-name').value = '';
                    document.getElementById('source-url').value = '';
                    document.getElementById('source-description').value = '';
                    
                    loadSources();
                    alert('数据来源已添加');
                }
            } catch (error) {
                console.error('Save source failed:', error);
            }
        }
        
        // Toggle Source
        async function toggleSource(sourceId, enabled) {
            try {
                await fetch(`${API_BASE}/api/sources/${sourceId}/toggle`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ enabled })
                });
                
                loadSources();
            } catch (error) {
                console.error('Toggle source failed:', error);
            }
        }
        
        // Delete Source
        async function deleteSource(sourceId) {
            if (!confirm('确定删除此数据来源？')) return;
            
            try {
                await fetch(`${API_BASE}/api/sources/${sourceId}`, {
                    method: 'DELETE'
                });
                
                loadSources();
            } catch (error) {
                console.error('Delete source failed:', error);
            }
        }
