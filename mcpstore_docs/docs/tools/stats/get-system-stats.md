# get_system_stats()

获取系统统计信息。

## 方法特性

- ✅ **异步版本**: `get_system_stats_async()`
- ✅ **Store级别**: `store.for_store().get_system_stats()`
- ✅ **Agent级别**: `store.for_agent("agent1").get_system_stats()`
- 📁 **文件位置**: `tool_operations.py`
- 🏷️ **所属类**: `ToolOperationsMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| 无参数 | - | - | - | 该方法不需要参数 |

## 返回值

返回系统统计信息字典：

```python
{
    "system_info": {
        "mcpstore_version": "1.0.0",
        "python_version": "3.11.0",
        "platform": "Windows-10",
        "uptime_seconds": 3600
    },
    "services": {
        "total_services": 5,
        "healthy_services": 4,
        "warning_services": 1,
        "unhealthy_services": 0,
        "services_by_status": {
            "healthy": ["weather", "database", "filesystem"],
            "warning": ["slow-api"],
            "unhealthy": []
        }
    },
    "tools": {
        "total_tools": 25,
        "tools_by_service": {
            "weather": 8,
            "database": 10,
            "filesystem": 7
        },
        "avg_tools_per_service": 5.0
    },
    "performance": {
        "avg_response_time": 1.23,
        "total_calls": 150,
        "successful_calls": 145,
        "failed_calls": 5,
        "success_rate": 0.967
    },
    "memory": {
        "cache_size_mb": 12.5,
        "active_connections": 5,
        "connection_pool_size": 10
    },
    "timestamp": "2025-01-01T12:00:00Z"
}
```

## 使用示例

### Store级别获取系统统计

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取系统统计信息
stats = store.for_store().get_system_stats()

print("=== MCPStore 系统统计 ===")

# 系统信息
system_info = stats['system_info']
print(f"📊 系统信息:")
print(f"  MCPStore版本: {system_info['mcpstore_version']}")
print(f"  Python版本: {system_info['python_version']}")
print(f"  运行平台: {system_info['platform']}")
print(f"  运行时间: {system_info['uptime_seconds']} 秒")

# 服务统计
services = stats['services']
print(f"\n🏢 服务统计:")
print(f"  总服务数: {services['total_services']}")
print(f"  健康服务: {services['healthy_services']}")
print(f"  警告服务: {services['warning_services']}")
print(f"  异常服务: {services['unhealthy_services']}")

# 工具统计
tools = stats['tools']
print(f"\n🛠️ 工具统计:")
print(f"  总工具数: {tools['total_tools']}")
print(f"  平均每服务工具数: {tools['avg_tools_per_service']:.1f}")

# 性能统计
performance = stats['performance']
print(f"\n⚡ 性能统计:")
print(f"  平均响应时间: {performance['avg_response_time']:.2f}秒")
print(f"  总调用次数: {performance['total_calls']}")
print(f"  成功率: {performance['success_rate']:.1%}")
```

### Agent级别获取系统统计

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式获取系统统计
agent_stats = store.for_agent("agent1").get_system_stats()

print("=== Agent 系统统计 ===")

# Agent特定的统计信息
services = agent_stats['services']
tools = agent_stats['tools']

print(f"🤖 Agent统计:")
print(f"  Agent可见服务: {services['total_services']}")
print(f"  Agent可用工具: {tools['total_tools']}")

# Agent性能统计
performance = agent_stats['performance']
print(f"  Agent调用成功率: {performance['success_rate']:.1%}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_get_system_stats():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步获取系统统计
    stats = await store.for_store().get_system_stats_async()
    
    print(f"异步获取系统统计:")
    
    # 快速概览
    services = stats['services']
    tools = stats['tools']
    performance = stats['performance']
    
    print(f"  服务: {services['healthy_services']}/{services['total_services']} 健康")
    print(f"  工具: {tools['total_tools']} 个可用")
    print(f"  性能: {performance['success_rate']:.1%} 成功率")
    print(f"  响应: {performance['avg_response_time']:.2f}秒 平均")
    
    return stats

# 运行异步获取
result = asyncio.run(async_get_system_stats())
```

### 系统健康检查

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def system_health_check():
    """基于系统统计进行健康检查"""
    
    stats = store.for_store().get_system_stats()
    
    print("=== 系统健康检查 ===")
    
    health_issues = []
    
    # 检查服务健康状态
    services = stats['services']
    if services['unhealthy_services'] > 0:
        health_issues.append(f"发现 {services['unhealthy_services']} 个异常服务")
    
    service_health_rate = services['healthy_services'] / services['total_services']
    if service_health_rate < 0.8:
        health_issues.append(f"服务健康率过低: {service_health_rate:.1%}")
    
    # 检查性能指标
    performance = stats['performance']
    if performance['success_rate'] < 0.9:
        health_issues.append(f"调用成功率过低: {performance['success_rate']:.1%}")
    
    if performance['avg_response_time'] > 5.0:
        health_issues.append(f"平均响应时间过长: {performance['avg_response_time']:.2f}秒")
    
    # 检查内存使用
    memory = stats['memory']
    if memory['cache_size_mb'] > 100:
        health_issues.append(f"缓存占用过大: {memory['cache_size_mb']:.1f}MB")
    
    # 输出检查结果
    if health_issues:
        print("❌ 发现健康问题:")
        for issue in health_issues:
            print(f"  - {issue}")
        
        # 提供建议
        print("\n💡 建议:")
        if services['unhealthy_services'] > 0:
            print("  - 检查并重启异常服务")
        if performance['success_rate'] < 0.9:
            print("  - 检查网络连接和服务配置")
        if performance['avg_response_time'] > 5.0:
            print("  - 优化服务性能或增加超时时间")
        if memory['cache_size_mb'] > 100:
            print("  - 清理缓存或调整缓存策略")
    else:
        print("✅ 系统健康状态良好")
    
    return len(health_issues) == 0

# 执行健康检查
is_healthy = system_health_check()
```

### 性能趋势分析

```python
from mcpstore import MCPStore
import time
import json

# 初始化
store = MCPStore.setup_store()

def performance_trend_analysis(samples=5, interval=30):
    """性能趋势分析"""
    
    print(f"开始性能趋势分析，采样 {samples} 次，间隔 {interval} 秒")
    
    performance_history = []
    
    for i in range(samples):
        print(f"\n采样 {i + 1}/{samples}")
        
        stats = store.for_store().get_system_stats()
        performance = stats['performance']
        
        # 记录关键性能指标
        sample = {
            "timestamp": time.time(),
            "response_time": performance['avg_response_time'],
            "success_rate": performance['success_rate'],
            "total_calls": performance['total_calls'],
            "cache_size": stats['memory']['cache_size_mb']
        }
        
        performance_history.append(sample)
        
        print(f"  响应时间: {sample['response_time']:.2f}秒")
        print(f"  成功率: {sample['success_rate']:.1%}")
        print(f"  总调用: {sample['total_calls']}")
        
        if i < samples - 1:
            time.sleep(interval)
    
    # 分析趋势
    print(f"\n=== 趋势分析 ===")
    
    if len(performance_history) >= 2:
        first = performance_history[0]
        last = performance_history[-1]
        
        # 响应时间趋势
        response_trend = last['response_time'] - first['response_time']
        print(f"📈 响应时间趋势: {response_trend:+.2f}秒")
        
        # 调用量趋势
        calls_trend = last['total_calls'] - first['total_calls']
        print(f"📊 调用量变化: {calls_trend:+d}")
        
        # 缓存趋势
        cache_trend = last['cache_size'] - first['cache_size']
        print(f"💾 缓存变化: {cache_trend:+.1f}MB")
        
        # 成功率趋势
        success_trend = last['success_rate'] - first['success_rate']
        print(f"✅ 成功率变化: {success_trend:+.1%}")
    
    return performance_history

# 执行性能趋势分析（示例：5次采样，间隔30秒）
# trend_data = performance_trend_analysis(5, 30)
```

### 系统资源监控

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def monitor_system_resources():
    """监控系统资源使用情况"""
    
    stats = store.for_store().get_system_stats()
    
    print("=== 系统资源监控 ===")
    
    # 内存使用情况
    memory = stats['memory']
    print(f"💾 内存使用:")
    print(f"  缓存大小: {memory['cache_size_mb']:.1f} MB")
    print(f"  活跃连接: {memory['active_connections']}")
    print(f"  连接池大小: {memory['connection_pool_size']}")
    
    # 连接池使用率
    if memory['connection_pool_size'] > 0:
        pool_usage = memory['active_connections'] / memory['connection_pool_size']
        print(f"  连接池使用率: {pool_usage:.1%}")
        
        if pool_usage > 0.8:
            print("  ⚠️ 连接池使用率较高，考虑扩容")
    
    # 服务负载分析
    services = stats['services']
    tools = stats['tools']
    
    print(f"\n🏢 服务负载:")
    print(f"  服务总数: {services['total_services']}")
    print(f"  工具总数: {tools['total_tools']}")
    
    if services['total_services'] > 0:
        avg_tools = tools['total_tools'] / services['total_services']
        print(f"  平均每服务工具数: {avg_tools:.1f}")
        
        if avg_tools > 10:
            print("  💡 建议: 考虑拆分工具较多的服务")
    
    # 性能指标
    performance = stats['performance']
    print(f"\n⚡ 性能指标:")
    print(f"  平均响应时间: {performance['avg_response_time']:.2f}秒")
    print(f"  调用成功率: {performance['success_rate']:.1%}")
    
    # 性能评级
    if performance['avg_response_time'] < 1.0 and performance['success_rate'] > 0.95:
        print("  🏆 性能评级: 优秀")
    elif performance['avg_response_time'] < 3.0 and performance['success_rate'] > 0.9:
        print("  👍 性能评级: 良好")
    elif performance['avg_response_time'] < 5.0 and performance['success_rate'] > 0.8:
        print("  ⚠️ 性能评级: 一般")
    else:
        print("  ❌ 性能评级: 需要优化")
    
    return stats

# 执行系统资源监控
monitor_system_resources()
```

## 统计字段说明

### 系统信息 (system_info)
- `mcpstore_version`: MCPStore版本
- `python_version`: Python版本
- `platform`: 运行平台
- `uptime_seconds`: 运行时间（秒）

### 服务统计 (services)
- `total_services`: 总服务数
- `healthy_services`: 健康服务数
- `warning_services`: 警告服务数
- `unhealthy_services`: 异常服务数
- `services_by_status`: 按状态分组的服务列表

### 工具统计 (tools)
- `total_tools`: 总工具数
- `tools_by_service`: 按服务分组的工具数
- `avg_tools_per_service`: 平均每服务工具数

### 性能统计 (performance)
- `avg_response_time`: 平均响应时间
- `total_calls`: 总调用次数
- `successful_calls`: 成功调用次数
- `failed_calls`: 失败调用次数
- `success_rate`: 成功率

### 内存统计 (memory)
- `cache_size_mb`: 缓存大小（MB）
- `active_connections`: 活跃连接数
- `connection_pool_size`: 连接池大小

## 相关方法

- [get_tools_with_stats()](../listing/get-tools-with-stats.md) - 获取工具统计
- [get_usage_stats()](get-usage-stats.md) - 获取使用统计
- [get_performance_report()](get-performance-report.md) - 获取性能报告

## 注意事项

1. **实时数据**: 返回实时的系统统计信息
2. **Agent视角**: Agent模式下统计信息限于该Agent可见的资源
3. **性能影响**: 统计计算可能对性能有轻微影响
4. **时间戳**: 包含统计生成时间，便于趋势分析
5. **内存监控**: 包含内存和连接池使用情况
