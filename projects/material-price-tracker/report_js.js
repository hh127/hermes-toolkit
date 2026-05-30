        // Report Charts
        let reportCategoryChart, reportGainersChart, reportLosersChart;
        
        // Generate Report
        async function generateReport() {
            const material = document.getElementById('report-material').value;
            const days = document.getElementById('report-days').value;
            const reportType = document.getElementById('report-type').value;
            
            try {
                // 生成文字报告
                let url = `${API_BASE}/api/report?type=${reportType}&days=${days}`;
                if (material) {
                    url += `&material=${encodeURIComponent(material)}`;
                }
                
                const response = await fetch(url);
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('report-content').textContent = data.data;
                }
                
                // 获取图表数据
                const dataUrl = `${API_BASE}/api/report/data?days=${days}${material ? `&material=${encodeURIComponent(material)}` : ''}`;
                const dataResponse = await fetch(dataUrl);
                const reportData = await dataResponse.json();
                
                if (reportData.success) {
                    // 更新统计
                    const summary = reportData.data.summary;
                    document.getElementById('report-total-materials').textContent = summary.total_materials;
                    document.getElementById('report-avg-change').textContent = summary.avg_change.toFixed(2) + '%';
                    document.getElementById('report-up-count').textContent = summary.up_count;
                    document.getElementById('report-down-count').textContent = summary.down_count;
                    
                    // 更新图表
                    updateReportCharts(reportData.data.chart_data);
                }
                
            } catch (error) {
                console.error('Generate report failed:', error);
            }
        }
        
        // Update Report Charts
        function updateReportCharts(chartData) {
            // 材料分类饼图
            if (chartData.category_pie) {
                const ctx1 = document.getElementById('report-category-chart').getContext('2d');
                if (reportCategoryChart) reportCategoryChart.destroy();
                
                reportCategoryChart = new Chart(ctx1, {
                    type: 'doughnut',
                    data: {
                        labels: chartData.category_pie.labels,
                        datasets: [{
                            data: chartData.category_pie.values,
                            backgroundColor: [
                                '#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                                '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#6366f1'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { font: { size: 10 } }
                            }
                        }
                    }
                });
            }
            
            // 涨幅柱状图
            if (chartData.gainers_bar) {
                const ctx2 = document.getElementById('report-gainers-chart').getContext('2d');
                if (reportGainersChart) reportGainersChart.destroy();
                
                reportGainersChart = new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: chartData.gainers_bar.labels,
                        datasets: [{
                            label: '涨幅 %',
                            data: chartData.gainers_bar.values,
                            backgroundColor: '#ef4444'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: {
                                ticks: {
                                    callback: function(value) {
                                        return value + '%';
                                    }
                                }
                            }
                        }
                    }
                });
            }
            
            // 跌幅柱状图
            if (chartData.losers_bar) {
                const ctx3 = document.getElementById('report-losers-chart').getContext('2d');
                if (reportLosersChart) reportLosersChart.destroy();
                
                reportLosersChart = new Chart(ctx3, {
                    type: 'bar',
                    data: {
                        labels: chartData.losers_bar.labels,
                        datasets: [{
                            label: '跌幅 %',
                            data: chartData.losers_bar.values,
                            backgroundColor: '#10b981'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            y: {
                                ticks: {
                                    callback: function(value) {
                                        return value + '%';
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
        
        // Copy Report
        function copyReport() {
            const content = document.getElementById('report-content').textContent;
            navigator.clipboard.writeText(content).then(() => {
                alert('报告已复制到剪贴板');
            }).catch(err => {
                console.error('Copy failed:', err);
                alert('复制失败');
            });
        }
