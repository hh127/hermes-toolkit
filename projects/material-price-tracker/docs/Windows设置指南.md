# Windows端自动化设置指南

## 文件说明

| 文件 | 说明 |
|------|------|
| `install_deps.bat` | 安装依赖（首次运行） |
| `test_windows_env.py` | 测试环境配置 |
| `windows_auto_collector.py` | 采集脚本 |
| `run_collector.bat` | 运行采集（手动） |
| `setup_task.bat` | 创建定时任务（管理员） |
| `mysteel_cookies.json` | Cookie文件 |

## 快速开始

### 1. 复制文件到Windows

将以下文件复制到Windows目录（如 `D:\mysteel\`）：

```
install_deps.bat
test_windows_env.py
windows_auto_collector.py
run_collector.bat
setup_task.bat
mysteel_cookies.json
```

或在Windows中访问WSL目录：
```
\\wsl$\Ubuntu\home\hh127\material-price-tracker
```

### 2. 安装依赖

双击运行 `install_deps.bat`

或手动执行：
```cmd
pip install selenium webdriver-manager
```

### 3. 测试环境

```cmd
python test_windows_env.py
```

确保所有测试项都显示 ✅

### 4. 测试采集

```cmd
python windows_auto_collector.py
```

或双击 `run_collector.bat`

### 5. 设置定时任务

**以管理员身份运行** `setup_task.bat`

或手动创建：
1. 打开任务计划程序（Win+R → taskschd.msc）
2. 创建基本任务
3. 名称：`MysteelPriceCollector`
4. 触发器：每天 08:00
5. 操作：启动程序
   - 程序：`D:\mysteel\run_collector.bat`

## 定时任务管理

```cmd
# 查看任务
schtasks /query /tn "MysteelPriceCollector"

# 手动运行
schtasks /run /tn "MysteelPriceCollector"

# 删除任务
schtasks /delete /tn "MysteelPriceCollector" /f
```

## 数据流程

```
Windows (08:00)
    ↓
run_collector.bat
    ↓
windows_auto_collector.py
    ↓
保存 JSON 到 \\wsl$\Ubuntu\...\price_data\
    ↓
WSL (08:30 cron)
    ↓
auto_import.py
    ↓
导入 SQLite 数据库
    ↓
Web界面展示 (http://localhost:5000)
```

## 故障排除

### Chrome启动失败
- 确保已安装Chrome浏览器
- 运行 `pip install webdriver-manager --upgrade`

### Cookie过期
- 在浏览器中重新登录我的钢铁网
- 更新 `mysteel_cookies.json`

### WSL目录不可访问
- 确保WSL正在运行
- 检查网络连接

## 添加更多城市

编辑 `windows_auto_collector.py`，在 `CONFIG['urls']` 中添加：

```python
'urls': {
    '西安': 'https://jiancai.mysteel.com/m/...',
    '北京': 'https://jiancai.mysteel.com/m/...',
    '上海': 'https://jiancai.mysteel.com/m/...',
}
```
