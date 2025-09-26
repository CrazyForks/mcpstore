# 完整示例集合

## 📋 概述

本文档提供了 MCPStore 的完整使用示例，涵盖从基础操作到高级功能的各种场景。这些示例可以帮助您快速上手并掌握 MCPStore 的各种功能。

## 🚀 基础示例

### 示例1: 快速开始

```python
from mcpstore import MCPStore

# 1. 初始化 MCPStore
store = MCPStore()

# 2. 添加文件系统服务
store.add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
    }
})

# 3. 列出可用工具
tools = store.list_tools()
print(f"📋 可用工具: {len(tools)} 个")
for tool in tools[:3]:  # 显示前3个
    print(f"  - {tool['name']}: {tool.get('description', '无描述')}")

# 4. 调用工具
result = store.call_tool("list_directory", {"path": "/tmp"})
print(f"📁 目录内容: {result}")

# 5. 使用便捷方法
content = store.use_tool("read_file", path="/tmp/test.txt")
print(f"📄 文件内容: {content}")
```

### 示例2: 多服务管理

```python
from mcpstore import MCPStore

# 初始化 MCPStore
store = MCPStore()

# 添加多个服务
services_config = {
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        },
        "web_search": {
            "command": "python",
            "args": ["-m", "web_search_server"]
        },
        "database": {
            "command": "python",
            "args": ["-m", "database_server", "--port", "5432"]
        }
    }
}

store.add_service(services_config)

# 检查所有服务状态
services = store.list_services()
print("🔍 服务状态检查:")
for service in services:
    try:
        status = store.get_service_status(service['name'])
        tools_count = len(store.list_tools(service_name=service['name']))
        print(f"  ✅ {service['name']}: {status} ({tools_count} 个工具)")
    except Exception as e:
        print(f"  ❌ {service['name']}: 错误 - {e}")

# 按服务调用工具
print("\n🛠️ 工具调用示例:")

# 文件操作
file_result = store.call_tool("filesystem_write_file", {
    "path": "/tmp/example.txt",
    "content": "Hello MCPStore!"
})
print(f"📝 文件写入: {file_result.get('success', False)}")

# Web搜索
search_result = store.call_tool("web_search_search", {
    "query": "MCPStore documentation"
})
print(f"🔍 搜索结果: {len(search_result.get('results', []))} 条")

# 数据库查询
db_result = store.call_tool("database_query", {
    "sql": "SELECT COUNT(*) FROM users"
})
print(f"💾 数据库查询: {db_result}")
```

## 🔄 批量操作示例

### 示例3: 批量文件处理

```python
from mcpstore import MCPStore
import time

store = MCPStore()
store.add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
    }
})

# 批量创建文件
def batch_file_creation_example():
    """批量文件创建示例"""
    print("📁 批量文件创建示例")
    
    # 准备批量调用
    batch_calls = []
    for i in range(10):
        batch_calls.append({
            "tool_name": "write_file",
            "arguments": {
                "path": f"/tmp/batch_file_{i}.txt",
                "content": f"这是批量创建的文件 {i}"
            }
        })
    
    # 执行批量调用
    start_time = time.time()
    results = store.batch_call(batch_calls)
    execution_time = time.time() - start_time
    
    # 统计结果
    successful = sum(1 for r in results if r.get('success'))
    print(f"✅ 批量创建完成: {successful}/{len(results)} 成功")
    print(f"⏱️ 执行时间: {execution_time:.2f}s")
    
    return results

# 批量读取和处理
def batch_file_processing_example():
    """批量文件处理示例"""
    print("\n📖 批量文件处理示例")
    
    # 首先列出所有文件
    dir_result = store.call_tool("list_directory", {"path": "/tmp"})
    files = [f for f in dir_result.get('files', []) if f.startswith('batch_file_')]
    
    # 批量读取文件
    read_calls = []
    for filename in files[:5]:  # 只处理前5个文件
        read_calls.append({
            "tool_name": "read_file",
            "arguments": {"path": f"/tmp/{filename}"}
        })
    
    # 执行批量读取
    read_results = store.batch_call(read_calls)
    
    # 处理读取结果
    total_content_length = 0
    for i, result in enumerate(read_results):
        if result.get('success'):
            content = result.get('content', '')
            total_content_length += len(content)
            print(f"  📄 文件 {i+1}: {len(content)} 字符")
    
    print(f"📊 总内容长度: {total_content_length} 字符")

# 执行示例
batch_file_creation_example()
batch_file_processing_example()
```

### 示例4: 混合服务批量调用

```python
def mixed_service_batch_example():
    """混合服务批量调用示例"""
    print("🔀 混合服务批量调用示例")
    
    # 准备混合调用
    mixed_calls = [
        # 文件操作
        {
            "tool_name": "write_file",
            "arguments": {
                "path": "/tmp/report.txt",
                "content": "Daily Report\n============\n"
            }
        },
        # Web搜索
        {
            "tool_name": "web_search",
            "arguments": {"query": "MCPStore latest news"}
        },
        # 数据库查询
        {
            "tool_name": "database_query",
            "arguments": {"sql": "SELECT COUNT(*) as user_count FROM users"}
        },
        # 文件读取
        {
            "tool_name": "read_file",
            "arguments": {"path": "/tmp/report.txt"}
        }
    ]
    
    # 执行混合批量调用
    start_time = time.time()
    results = store.batch_call(mixed_calls, parallel=True)
    execution_time = time.time() - start_time
    
    # 处理结果
    print(f"⚡ 混合调用完成，耗时: {execution_time:.2f}s")
    
    for i, result in enumerate(results):
        call = mixed_calls[i]
        if result.get('success'):
            print(f"  ✅ {call['tool_name']}: 成功")
        else:
            print(f"  ❌ {call['tool_name']}: 失败 - {result.get('error')}")

# 执行混合服务示例
mixed_service_batch_example()
```

## 🔗 链式调用示例

### 示例5: 文件处理工作流

```python
from mcpstore.chaining import ToolChain

def file_workflow_example():
    """文件处理工作流示例"""
    print("🔄 文件处理工作流示例")
    
    # 创建工具链
    chain = ToolChain(store)
    
    # 构建工作流
    chain.add_step(
        "create_directory",
        arguments={"path": "/tmp/workflow_demo"}
    ).add_step(
        "write_file",
        arguments=lambda ctx: {
            "path": "/tmp/workflow_demo/input.txt",
            "content": "Original content for processing"
        }
    ).add_step(
        "read_file",
        arguments={"path": "/tmp/workflow_demo/input.txt"},
        transform=lambda result, ctx: {
            **result,
            "processed_content": result.get('content', '').upper()
        }
    ).add_step(
        "write_file",
        arguments=lambda ctx: {
            "path": "/tmp/workflow_demo/output.txt", 
            "content": ctx['last_result']['processed_content']
        }
    ).add_step(
        "list_directory",
        arguments={"path": "/tmp/workflow_demo"}
    )
    
    # 执行工作流
    try:
        results = chain.execute()
        print(f"✅ 工作流完成，共 {len(results)} 个步骤")
        
        # 显示最终结果
        final_result = results[-1]
        if final_result.get('success'):
            files = final_result.get('files', [])
            print(f"📁 生成的文件: {files}")
        
    except Exception as e:
        print(f"❌ 工作流失败: {e}")

file_workflow_example()
```

### 示例6: 数据处理管道

```python
from mcpstore.chaining import Pipeline

def data_processing_pipeline_example():
    """数据处理管道示例"""
    print("\n🔧 数据处理管道示例")
    
    # 定义处理器函数
    def fetch_data(store, context):
        """获取数据"""
        result = store.call_tool("database_query", {
            "sql": "SELECT name, email FROM users LIMIT 10"
        })
        
        return {
            **context,
            "raw_data": result.get('rows', []),
            "record_count": len(result.get('rows', []))
        }
    
    def validate_data(store, context):
        """验证数据"""
        raw_data = context['raw_data']
        valid_records = []
        
        for record in raw_data:
            if record.get('email') and '@' in record['email']:
                valid_records.append(record)
        
        return {
            **context,
            "valid_data": valid_records,
            "validation_rate": len(valid_records) / len(raw_data) * 100
        }
    
    def save_processed_data(store, context):
        """保存处理后的数据"""
        valid_data = context['valid_data']
        
        # 转换为CSV格式
        csv_content = "name,email\n"
        for record in valid_data:
            csv_content += f"{record['name']},{record['email']}\n"
        
        # 保存到文件
        result = store.call_tool("write_file", {
            "path": "/tmp/processed_users.csv",
            "content": csv_content
        })
        
        return {
            **context,
            "output_file": "/tmp/processed_users.csv",
            "save_success": result.get('success', False)
        }
    
    # 创建管道
    pipeline = Pipeline(store)
    pipeline.add_processor(fetch_data) \
            .add_processor(validate_data) \
            .add_processor(save_processed_data)
    
    # 执行管道
    try:
        initial_context = {"pipeline_id": "data_processing_001"}
        final_result = pipeline.process(initial_context)
        
        print(f"📊 数据处理完成:")
        print(f"  原始记录: {final_result['record_count']}")
        print(f"  有效记录: {len(final_result['valid_data'])}")
        print(f"  验证率: {final_result['validation_rate']:.1f}%")
        print(f"  输出文件: {final_result['output_file']}")
        
    except Exception as e:
        print(f"❌ 数据处理失败: {e}")

data_processing_pipeline_example()
```

## 🔧 高级功能示例

### 示例7: 监控和性能分析

```python
from mcpstore.monitoring import MonitoringDashboard
from mcpstore.performance import PerformanceBenchmark

def monitoring_example():
    """监控和性能分析示例"""
    print("📊 监控和性能分析示例")
    
    # 启动监控
    dashboard = MonitoringDashboard(store)
    dashboard.start_monitoring(interval=5)
    
    # 执行一些操作来生成监控数据
    print("🔄 执行操作生成监控数据...")
    
    for i in range(20):
        try:
            # 随机选择操作
            import random
            operations = [
                lambda: store.call_tool("list_directory", {"path": "/tmp"}),
                lambda: store.call_tool("read_file", {"path": "/tmp/test.txt"}),
                lambda: store.call_tool("write_file", {
                    "path": f"/tmp/monitor_test_{i}.txt",
                    "content": f"Monitor test {i}"
                })
            ]
            
            operation = random.choice(operations)
            operation()
            
            time.sleep(0.5)  # 短暂延迟
            
        except Exception as e:
            print(f"⚠️ 操作 {i} 失败: {e}")
    
    # 等待一段时间收集数据
    time.sleep(10)
    
    # 显示监控仪表板
    dashboard.print_dashboard()
    
    # 停止监控
    dashboard.stop_monitoring()
    
    # 性能基准测试
    print("\n🏃 性能基准测试:")
    benchmark = PerformanceBenchmark(store)
    
    # 测试简单调用
    def simple_call_test():
        store.call_tool("list_directory", {"path": "/tmp"})
    
    # 测试批量调用
    def batch_call_test():
        calls = [
            {"tool_name": "list_directory", "arguments": {"path": "/tmp"}}
            for _ in range(3)
        ]
        store.batch_call(calls)
    
    # 运行基准测试
    benchmark.run_benchmark("简单调用", simple_call_test, iterations=30)
    benchmark.run_benchmark("批量调用", batch_call_test, iterations=10)
    
    # 显示结果
    benchmark.print_results()

monitoring_example()
```

### 示例8: 错误处理和恢复

```python
from mcpstore.error_handling import RetryManager, RetryConfig, FallbackManager

def error_handling_example():
    """错误处理和恢复示例"""
    print("\n🛡️ 错误处理和恢复示例")
    
    # 配置重试机制
    retry_config = RetryConfig(
        max_attempts=3,
        strategy=RetryStrategy.EXPONENTIAL,
        base_delay=1.0,
        exceptions=(Exception,)
    )
    
    retry_manager = RetryManager(retry_config)
    
    # 模拟可能失败的操作
    def unreliable_operation():
        """不可靠的操作（有时会失败）"""
        import random
        if random.random() < 0.7:  # 70% 失败率
            raise Exception("模拟的网络错误")
        
        return store.call_tool("list_directory", {"path": "/tmp"})
    
    # 使用重试机制
    try:
        print("🔄 尝试不可靠操作（带重试）...")
        result = retry_manager.execute(unreliable_operation)
        print(f"✅ 操作成功: {len(result.get('files', []))} 个文件")
    except Exception as e:
        print(f"❌ 操作最终失败: {e}")
    
    # 配置降级机制
    fallback_manager = FallbackManager()
    
    # 添加缓存降级策略
    from mcpstore.error_handling import CacheFallback, DefaultValueFallback
    
    fallback_manager.add_strategy(CacheFallback(cache_duration=300))
    fallback_manager.add_strategy(DefaultValueFallback({"files": [], "fallback": True}))
    
    # 使用降级机制
    def get_directory_listing():
        """获取目录列表（可能失败）"""
        # 模拟服务不可用
        raise Exception("服务暂时不可用")
    
    try:
        print("\n🔄 尝试获取目录列表（带降级）...")
        result = fallback_manager.execute_with_fallback(get_directory_listing)
        
        if result.get('fallback'):
            print("📦 使用了降级策略")
        else:
            print(f"✅ 正常获取: {len(result.get('files', []))} 个文件")
            
    except Exception as e:
        print(f"❌ 所有策略都失败: {e}")

error_handling_example()
```

## 🎯 实际应用场景

### 示例9: 自动化报告生成

```python
def automated_report_example():
    """自动化报告生成示例"""
    print("📋 自动化报告生成示例")
    
    from datetime import datetime
    
    # 报告生成工作流
    def generate_daily_report():
        """生成日常报告"""
        
        # 1. 收集系统信息
        system_info = store.call_tool("get_system_info", {})
        
        # 2. 查询数据库统计
        db_stats = store.call_tool("database_query", {
            "sql": "SELECT COUNT(*) as total_users, MAX(created_at) as last_signup FROM users"
        })
        
        # 3. 检查文件系统使用情况
        disk_usage = store.call_tool("get_disk_usage", {"path": "/tmp"})
        
        # 4. 生成报告内容
        report_content = f"""
日常系统报告
=============
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

系统信息:
- CPU使用率: {system_info.get('cpu_percent', 'N/A')}%
- 内存使用率: {system_info.get('memory_percent', 'N/A')}%

数据库统计:
- 总用户数: {db_stats.get('total_users', 'N/A')}
- 最后注册: {db_stats.get('last_signup', 'N/A')}

磁盘使用:
- 已用空间: {disk_usage.get('used_gb', 'N/A')} GB
- 可用空间: {disk_usage.get('free_gb', 'N/A')} GB

报告生成完成。
"""
        
        # 5. 保存报告
        report_filename = f"/tmp/daily_report_{datetime.now().strftime('%Y%m%d')}.txt"
        save_result = store.call_tool("write_file", {
            "path": report_filename,
            "content": report_content
        })
        
        if save_result.get('success'):
            print(f"✅ 报告已保存到: {report_filename}")
            
            # 6. 可选：发送邮件通知
            # email_result = store.call_tool("send_email", {
            #     "to": "admin@example.com",
            #     "subject": "日常系统报告",
            #     "body": "请查看附件中的系统报告",
            #     "attachment": report_filename
            # })
            
        return report_filename
    
    # 执行报告生成
    try:
        report_file = generate_daily_report()
        print(f"📊 报告生成完成: {report_file}")
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")

automated_report_example()
```

### 示例10: 文件同步系统

```python
def file_sync_example():
    """文件同步系统示例"""
    print("\n🔄 文件同步系统示例")
    
    def sync_directories(source_dir, target_dir):
        """同步目录"""
        
        # 1. 获取源目录文件列表
        source_files = store.call_tool("list_directory", {"path": source_dir})
        
        # 2. 获取目标目录文件列表
        target_files = store.call_tool("list_directory", {"path": target_dir})
        
        source_file_names = set(source_files.get('files', []))
        target_file_names = set(target_files.get('files', []))
        
        # 3. 找出需要同步的文件
        files_to_copy = source_file_names - target_file_names
        files_to_delete = target_file_names - source_file_names
        
        print(f"📁 同步分析:")
        print(f"  需要复制: {len(files_to_copy)} 个文件")
        print(f"  需要删除: {len(files_to_delete)} 个文件")
        
        # 4. 批量复制文件
        if files_to_copy:
            copy_calls = []
            for filename in files_to_copy:
                # 读取源文件
                copy_calls.append({
                    "tool_name": "read_file",
                    "arguments": {"path": f"{source_dir}/{filename}"}
                })
            
            # 批量读取
            read_results = store.batch_call(copy_calls)
            
            # 批量写入
            write_calls = []
            for i, filename in enumerate(files_to_copy):
                read_result = read_results[i]
                if read_result.get('success'):
                    write_calls.append({
                        "tool_name": "write_file",
                        "arguments": {
                            "path": f"{target_dir}/{filename}",
                            "content": read_result.get('content', '')
                        }
                    })
            
            if write_calls:
                write_results = store.batch_call(write_calls)
                successful_copies = sum(1 for r in write_results if r.get('success'))
                print(f"✅ 成功复制: {successful_copies}/{len(write_calls)} 个文件")
        
        # 5. 批量删除文件
        if files_to_delete:
            delete_calls = []
            for filename in files_to_delete:
                delete_calls.append({
                    "tool_name": "delete_file",
                    "arguments": {"path": f"{target_dir}/{filename}"}
                })
            
            delete_results = store.batch_call(delete_calls)
            successful_deletes = sum(1 for r in delete_results if r.get('success'))
            print(f"🗑️ 成功删除: {successful_deletes}/{len(delete_calls)} 个文件")
        
        print("🎯 目录同步完成")
    
    # 执行同步
    try:
        sync_directories("/tmp/source", "/tmp/backup")
    except Exception as e:
        print(f"❌ 同步失败: {e}")

file_sync_example()
```

## 🔗 相关文档

- [快速开始](../getting-started/quick-demo.md)
- [服务管理](../services/management/service-management.md)
- [工具调用](../tools/usage/call-tool.md)
- [批量调用](../tools/usage/batch-call.md)
- [链式调用](../advanced/chaining.md)
- [监控系统](../advanced/monitoring.md)
- [错误处理](../advanced/error-handling.md)

## 📚 最佳实践总结

1. **服务管理**：合理配置服务，定期检查服务状态
2. **错误处理**：实现完善的错误处理和重试机制
3. **性能优化**：使用批量调用和链式调用提高效率
4. **监控分析**：建立监控体系，分析使用模式
5. **资源管理**：及时清理临时文件和资源
6. **安全考虑**：验证输入参数，控制访问权限

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0
