# 故障排除指南

## 📋 概述

本文档提供了 MCPStore 常见问题的诊断和解决方案。如果您遇到问题，请按照本指南进行排查。

## 🔍 常见问题

### 服务启动问题

#### 问题：服务启动失败

**症状**：
- `start_service()` 返回 `False`
- 服务状态显示为 `error`
- 日志中出现启动错误

**可能原因和解决方案**：

```python
# 1. 检查命令和参数
def diagnose_service_startup(store, service_name):
    """诊断服务启动问题"""
    
    try:
        # 获取服务信息
        info = store.get_service_info(service_name)
        print(f"🔍 服务配置:")
        print(f"  命令: {info['command']}")
        print(f"  参数: {info['args']}")
        print(f"  环境变量: {info['env']}")
        
        # 检查命令是否存在
        import shutil
        if not shutil.which(info['command']):
            print(f"❌ 命令不存在: {info['command']}")
            print("💡 解决方案:")
            print("  - 检查命令是否已安装")
            print("  - 检查 PATH 环境变量")
            print("  - 使用完整路径")
            return False
        
        # 检查工作目录
        cwd = info.get('cwd')
        if cwd:
            import os
            if not os.path.exists(cwd):
                print(f"❌ 工作目录不存在: {cwd}")
                print("💡 解决方案: 创建工作目录或修改配置")
                return False
        
        # 检查端口占用（如果适用）
        if 'port' in info.get('env', {}):
            port = int(info['env']['port'])
            if is_port_in_use(port):
                print(f"❌ 端口 {port} 已被占用")
                print("💡 解决方案: 更改端口或停止占用进程")
                return False
        
        print("✅ 基础检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 诊断过程中发生错误: {e}")
        return False

def is_port_in_use(port):
    """检查端口是否被占用"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# 使用诊断工具
diagnose_service_startup(store, "filesystem")
```

#### 问题：服务启动超时

**解决方案**：

```python
# 增加启动超时时间
store.start_service("service_name", timeout=60.0)

# 或者在配置中设置
config = {
    "mcpServers": {
        "service_name": {
            "command": "your_command",
            "timeout": 60
        }
    }
}
```

### 工具调用问题

#### 问题：工具不存在

**症状**：
- `ToolNotFoundError` 异常
- `list_tools()` 中找不到工具

**解决方案**：

```python
def diagnose_tool_issues(store, tool_name):
    """诊断工具问题"""
    
    # 1. 检查工具是否存在
    all_tools = store.list_tools()
    tool_names = [tool['name'] for tool in all_tools]
    
    if tool_name not in tool_names:
        print(f"❌ 工具 '{tool_name}' 不存在")
        print("📋 可用工具:")
        for name in tool_names:
            print(f"  - {name}")
        
        # 模糊匹配建议
        import difflib
        suggestions = difflib.get_close_matches(tool_name, tool_names, n=3)
        if suggestions:
            print("💡 您是否想要:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        return False
    
    # 2. 检查工具所属服务状态
    tool_info = store.get_tool_info(tool_name)
    service_name = tool_info['service_name']
    service_status = store.get_service_status(service_name)
    
    if service_status != 'running':
        print(f"❌ 工具所属服务 '{service_name}' 未运行")
        print(f"   当前状态: {service_status}")
        print("💡 解决方案: 启动服务")
        print(f"   store.start_service('{service_name}')")
        return False
    
    print(f"✅ 工具 '{tool_name}' 可用")
    return True

# 使用工具诊断
diagnose_tool_issues(store, "read_file")
```

#### 问题：工具执行失败

**解决方案**：

```python
def safe_tool_call(store, tool_name, arguments, max_retries=3):
    """安全的工具调用"""
    
    for attempt in range(max_retries):
        try:
            # 验证参数
            tool_info = store.get_tool_info(tool_name)
            validate_tool_arguments(tool_info, arguments)
            
            # 执行工具调用
            result = store.call_tool(tool_name, arguments)
            return result
            
        except Exception as e:
            print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
            
            if attempt < max_retries - 1:
                import time
                time.sleep(1)  # 等待1秒后重试
            else:
                print("💥 所有重试都失败了")
                raise e

def validate_tool_arguments(tool_info, arguments):
    """验证工具参数"""
    required_params = tool_info.get('parameters', {}).get('required', [])
    
    for param in required_params:
        if param not in arguments:
            raise ValueError(f"缺少必需参数: {param}")
    
    print("✅ 参数验证通过")

# 使用安全调用
try:
    result = safe_tool_call(store, "read_file", {"path": "/tmp/test.txt"})
    print(f"✅ 调用成功: {result}")
except Exception as e:
    print(f"❌ 调用失败: {e}")
```

### 连接问题

#### 问题：连接超时

**解决方案**：

```python
# 1. 增加超时时间
store = MCPStore(config={
    "timeout": 60,
    "connection_timeout": 30
})

# 2. 检查网络连接
def check_network_connectivity():
    """检查网络连接"""
    import socket
    
    try:
        # 测试本地连接
        socket.create_connection(("127.0.0.1", 80), timeout=5)
        print("✅ 本地网络正常")
        return True
    except Exception as e:
        print(f"❌ 网络连接问题: {e}")
        return False

# 3. 检查防火墙设置
def check_firewall_settings():
    """检查防火墙设置"""
    print("🔥 防火墙检查清单:")
    print("  - 检查本地防火墙是否阻止连接")
    print("  - 检查企业防火墙设置")
    print("  - 确认端口是否开放")
```

### 性能问题

#### 问题：响应速度慢

**解决方案**：

```python
def optimize_performance(store):
    """性能优化建议"""
    
    print("🚀 性能优化建议:")
    
    # 1. 启用缓存
    print("1. 启用缓存:")
    print("   store = MCPStore(config={'enable_cache': True, 'cache_size': 1000})")
    
    # 2. 使用批量调用
    print("2. 使用批量调用:")
    print("   results = store.batch_call(calls, parallel=True)")
    
    # 3. 调整连接池
    print("3. 调整连接池:")
    print("   store = MCPStore(config={'max_connections': 20})")
    
    # 4. 监控性能
    print("4. 监控性能:")
    print("   health = store.check_services()")

def performance_benchmark(store):
    """性能基准测试"""
    import time
    
    # 测试单次调用
    start_time = time.time()
    store.call_tool("list_directory", {"path": "/tmp"})
    single_call_time = time.time() - start_time
    
    # 测试批量调用
    calls = [{"tool_name": "list_directory", "arguments": {"path": "/tmp"}} for _ in range(10)]
    start_time = time.time()
    store.batch_call(calls)
    batch_call_time = time.time() - start_time
    
    print(f"📊 性能测试结果:")
    print(f"  单次调用: {single_call_time:.3f}s")
    print(f"  批量调用(10次): {batch_call_time:.3f}s")
    print(f"  平均每次: {batch_call_time/10:.3f}s")

# 运行性能测试
performance_benchmark(store)
```

## 🛠️ 诊断工具

### 系统诊断

```python
class MCPStoreDiagnostics:
    """MCPStore 诊断工具"""
    
    def __init__(self, store):
        self.store = store
    
    def run_full_diagnosis(self):
        """运行完整诊断"""
        print("🔍 MCPStore 系统诊断")
        print("=" * 50)
        
        # 1. 基础环境检查
        self.check_environment()
        
        # 2. 服务状态检查
        self.check_services()
        
        # 3. 工具可用性检查
        self.check_tools()
        
        # 4. 连接健康检查
        self.check_connections()
        
        # 5. 性能检查
        self.check_performance()
        
        print("\n✅ 诊断完成")
    
    def check_environment(self):
        """检查环境"""
        print("\n🌍 环境检查:")
        
        import sys
        import platform
        
        print(f"  Python版本: {sys.version}")
        print(f"  操作系统: {platform.system()} {platform.release()}")
        print(f"  架构: {platform.machine()}")
        
        # 检查依赖包
        try:
            import mcpstore
            print(f"  MCPStore版本: {mcpstore.__version__}")
        except:
            print("  ❌ MCPStore未正确安装")
    
    def check_services(self):
        """检查服务"""
        print("\n🔧 服务检查:")
        
        services = self.store.list_services()
        if not services:
            print("  ⚠️ 没有注册的服务")
            return
        
        for service in services:
            name = service['name']
            status = service['status']
            
            if status == 'running':
                print(f"  ✅ {name}: {status}")
            else:
                print(f"  ❌ {name}: {status}")
    
    def check_tools(self):
        """检查工具"""
        print("\n🛠️ 工具检查:")
        
        tools = self.store.list_tools()
        if not tools:
            print("  ⚠️ 没有可用的工具")
            return
        
        print(f"  📋 总计 {len(tools)} 个工具")
        
        # 按服务分组
        by_service = {}
        for tool in tools:
            service = tool.get('service_name', 'unknown')
            if service not in by_service:
                by_service[service] = []
            by_service[service].append(tool['name'])
        
        for service, tool_names in by_service.items():
            print(f"  🔧 {service}: {len(tool_names)} 个工具")
    
    def check_connections(self):
        """检查连接"""
        print("\n🔗 连接检查:")
        
        health = self.store.check_services()
        for service_name, health_info in health.items():
            if health_info['healthy']:
                response_time = health_info.get('response_time', 0)
                print(f"  ✅ {service_name}: 健康 ({response_time:.3f}s)")
            else:
                error = health_info.get('error', 'Unknown error')
                print(f"  ❌ {service_name}: 不健康 - {error}")
    
    def check_performance(self):
        """检查性能"""
        print("\n⚡ 性能检查:")
        
        import time
        
        # 简单性能测试
        try:
            start_time = time.time()
            tools = self.store.list_tools()
            list_time = time.time() - start_time
            
            print(f"  📋 工具列表查询: {list_time:.3f}s")
            
            if tools:
                # 测试工具调用
                test_tool = tools[0]
                try:
                    start_time = time.time()
                    # 这里需要根据实际工具调整参数
                    # result = self.store.call_tool(test_tool['name'], {})
                    # call_time = time.time() - start_time
                    # print(f"  🔧 工具调用测试: {call_time:.3f}s")
                    print(f"  🔧 工具调用测试: 跳过（需要具体参数）")
                except Exception as e:
                    print(f"  ⚠️ 工具调用测试失败: {e}")
        
        except Exception as e:
            print(f"  ❌ 性能检查失败: {e}")

# 使用诊断工具
diagnostics = MCPStoreDiagnostics(store)
diagnostics.run_full_diagnosis()
```

### 日志分析

```python
def analyze_logs(log_file_path):
    """分析日志文件"""
    import re
    from collections import Counter
    
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            logs = f.readlines()
        
        print(f"📄 日志分析: {log_file_path}")
        print(f"📊 总行数: {len(logs)}")
        
        # 统计日志级别
        levels = Counter()
        errors = []
        
        for line in logs:
            # 提取日志级别
            level_match = re.search(r'\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b', line)
            if level_match:
                levels[level_match.group(1)] += 1
            
            # 收集错误信息
            if 'ERROR' in line or 'Exception' in line:
                errors.append(line.strip())
        
        print("\n📊 日志级别统计:")
        for level, count in levels.items():
            print(f"  {level}: {count}")
        
        if errors:
            print(f"\n❌ 发现 {len(errors)} 个错误:")
            for error in errors[-5:]:  # 显示最近5个错误
                print(f"  {error}")
        else:
            print("\n✅ 没有发现错误")
    
    except FileNotFoundError:
        print(f"❌ 日志文件不存在: {log_file_path}")
    except Exception as e:
        print(f"❌ 日志分析失败: {e}")

# 分析日志
analyze_logs("/path/to/mcpstore.log")
```

## 📞 获取帮助

### 收集诊断信息

```python
def collect_diagnostic_info(store):
    """收集诊断信息"""
    import json
    import platform
    import sys
    from datetime import datetime
    
    diagnostic_info = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "platform": platform.platform(),
            "python_version": sys.version,
            "architecture": platform.machine()
        },
        "mcpstore": {
            "version": getattr(store, '__version__', 'unknown'),
            "config": store.get_config() if hasattr(store, 'get_config') else {}
        },
        "services": [],
        "tools": [],
        "health": {}
    }
    
    try:
        # 收集服务信息
        services = store.list_services()
        for service in services:
            diagnostic_info["services"].append({
                "name": service['name'],
                "status": service['status'],
                "command": service.get('command'),
                "uptime": service.get('uptime', 0)
            })
        
        # 收集工具信息
        tools = store.list_tools()
        diagnostic_info["tools"] = [
            {"name": tool['name'], "service": tool.get('service_name')}
            for tool in tools
        ]
        
        # 收集健康信息
        health = store.check_services()
        diagnostic_info["health"] = health
        
    except Exception as e:
        diagnostic_info["error"] = str(e)
    
    # 保存诊断信息
    filename = f"mcpstore_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(diagnostic_info, f, indent=2, ensure_ascii=False)
    
    print(f"📋 诊断信息已保存到: {filename}")
    return filename

# 收集诊断信息
diagnostic_file = collect_diagnostic_info(store)
```

### 联系支持

如果问题仍然无法解决，请：

1. **收集诊断信息**：运行上述诊断工具
2. **查看日志**：检查错误日志和异常信息
3. **准备复现步骤**：详细描述问题复现步骤
4. **提供环境信息**：操作系统、Python版本、MCPStore版本

## 🔗 相关文档

- [配置指南](configuration.md)
- [API 参考](api/reference.md)
- [快速开始](getting-started/quick-demo.md)
- [迁移指南](advanced/migration-guide.md)

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0
