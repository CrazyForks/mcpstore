# get_performance_report()

获取性能报告。

## 方法特性

- ✅ **异步版本**: `get_performance_report_async()`
- ✅ **Store级别**: `store.for_store().get_performance_report()`
- ✅ **Agent级别**: `store.for_agent("agent1").get_performance_report()`
- 📁 **文件位置**: `advanced_features.py`
- 🏷️ **所属类**: `AdvancedFeaturesMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| 无参数 | - | - | - | 该方法不需要参数 |

## 返回值

返回详细的性能报告字典：

```python
{
    "report_info": {
        "generated_at": "2025-01-01T12:00:00Z",
        "report_period": "last_24_hours",
        "mcpstore_version": "1.0.0"
    },
    "overall_performance": {
        "total_requests": 1250,
        "successful_requests": 1198,
        "failed_requests": 52,
        "success_rate": 0.9584,
        "avg_response_time": 1.45,
        "median_response_time": 0.89,
        "p95_response_time": 4.23,
        "p99_response_time": 8.67
    },
    "tool_performance": {
        "fastest_tools": [
            {"name": "simple_calc", "avg_time": 0.12, "calls": 45},
            {"name": "get_time", "avg_time": 0.15, "calls": 32}
        ],
        "slowest_tools": [
            {"name": "heavy_analysis", "avg_time": 8.34, "calls": 12},
            {"name": "file_backup", "avg_time": 6.78, "calls": 8}
        ],
        "most_reliable_tools": [
            {"name": "read_config", "success_rate": 1.0, "calls": 67},
            {"name": "list_files", "success_rate": 0.99, "calls": 89}
        ],
        "least_reliable_tools": [
            {"name": "network_check", "success_rate": 0.85, "calls": 23},
            {"name": "external_api", "success_rate": 0.78, "calls": 15}
        ]
    },
    "service_performance": {
        "service_metrics": {
            "filesystem": {
                "avg_response_time": 0.89,
                "success_rate": 0.97,
                "total_calls": 456,
                "health_score": 0.95
            },
            "weather": {
                "avg_response_time": 2.34,
                "success_rate": 0.92,
                "total_calls": 234,
                "health_score": 0.88
            }
        },
        "best_performing_service": "filesystem",
        "worst_performing_service": "weather"
    },
    "error_analysis": {
        "error_types": {
            "timeout": 23,
            "connection_failed": 15,
            "invalid_params": 8,
            "service_unavailable": 6
        },
        "most_common_error": "timeout",
        "error_rate_by_service": {
            "filesystem": 0.03,
            "weather": 0.08,
            "database": 0.05
        }
    },
    "performance_trends": {
        "response_time_trend": "improving",
        "success_rate_trend": "stable",
        "load_trend": "increasing",
        "recommendations": [
            "优化weather服务响应时间",
            "增加timeout错误的重试机制",
            "考虑扩容以应对增长的负载"
        ]
    },
    "resource_usage": {
        "memory_usage_mb": 45.6,
        "cpu_usage_percent": 12.3,
        "network_io_mb": 234.5,
        "cache_hit_rate": 0.78
    }
}
```

## 使用示例

### Store级别获取性能报告

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取性能报告
report = store.for_store().get_performance_report()

print("=== MCPStore 性能报告 ===")

# 报告基本信息
report_info = report['report_info']
print(f"📋 报告信息:")
print(f"  生成时间: {report_info['generated_at']}")
print(f"  报告周期: {report_info['report_period']}")
print(f"  MCPStore版本: {report_info['mcpstore_version']}")

# 整体性能
overall = report['overall_performance']
print(f"\n📊 整体性能:")
print(f"  总请求数: {overall['total_requests']:,}")
print(f"  成功率: {overall['success_rate']:.1%}")
print(f"  平均响应时间: {overall['avg_response_time']:.2f}秒")
print(f"  P95响应时间: {overall['p95_response_time']:.2f}秒")
print(f"  P99响应时间: {overall['p99_response_time']:.2f}秒")

# 工具性能
tool_perf = report['tool_performance']
print(f"\n🛠️ 工具性能:")
print(f"  最快工具:")
for tool in tool_perf['fastest_tools'][:3]:
    print(f"    {tool['name']}: {tool['avg_time']:.2f}秒 ({tool['calls']} 次调用)")

print(f"  最慢工具:")
for tool in tool_perf['slowest_tools'][:3]:
    print(f"    {tool['name']}: {tool['avg_time']:.2f}秒 ({tool['calls']} 次调用)")

# 服务性能
service_perf = report['service_performance']
print(f"\n🏢 服务性能:")
print(f"  最佳服务: {service_perf['best_performing_service']}")
print(f"  待优化服务: {service_perf['worst_performing_service']}")

for service, metrics in service_perf['service_metrics'].items():
    print(f"  {service}:")
    print(f"    响应时间: {metrics['avg_response_time']:.2f}秒")
    print(f"    成功率: {metrics['success_rate']:.1%}")
    print(f"    健康评分: {metrics['health_score']:.1%}")

# 错误分析
error_analysis = report['error_analysis']
print(f"\n❌ 错误分析:")
print(f"  最常见错误: {error_analysis['most_common_error']}")
print(f"  错误类型分布:")
for error_type, count in error_analysis['error_types'].items():
    print(f"    {error_type}: {count} 次")

# 性能建议
trends = report['performance_trends']
print(f"\n💡 性能建议:")
for recommendation in trends['recommendations']:
    print(f"  - {recommendation}")
```

### Agent级别获取性能报告

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式获取性能报告
agent_report = store.for_agent("agent1").get_performance_report()

print("=== Agent 性能报告 ===")

overall = agent_report['overall_performance']
print(f"🤖 Agent性能:")
print(f"  Agent总请求: {overall['total_requests']}")
print(f"  Agent成功率: {overall['success_rate']:.1%}")
print(f"  Agent平均响应: {overall['avg_response_time']:.2f}秒")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_get_performance_report():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步获取性能报告
    report = await store.for_store().get_performance_report_async()
    
    print(f"异步获取性能报告:")
    
    overall = report['overall_performance']
    trends = report['performance_trends']
    
    print(f"  整体成功率: {overall['success_rate']:.1%}")
    print(f"  响应时间趋势: {trends['response_time_trend']}")
    print(f"  负载趋势: {trends['load_trend']}")
    
    return report

# 运行异步获取
result = asyncio.run(async_get_performance_report())
```

### 性能诊断分析

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def diagnose_performance():
    """性能诊断分析"""
    
    report = store.for_store().get_performance_report()
    
    print("=== 性能诊断分析 ===")
    
    overall = report['overall_performance']
    
    # 整体健康评估
    print(f"🏥 整体健康评估:")
    
    health_score = 0
    issues = []
    
    # 成功率评估
    if overall['success_rate'] >= 0.99:
        print(f"  ✅ 成功率优秀: {overall['success_rate']:.1%}")
        health_score += 25
    elif overall['success_rate'] >= 0.95:
        print(f"  👍 成功率良好: {overall['success_rate']:.1%}")
        health_score += 20
    elif overall['success_rate'] >= 0.90:
        print(f"  ⚠️ 成功率一般: {overall['success_rate']:.1%}")
        health_score += 15
        issues.append("成功率偏低")
    else:
        print(f"  ❌ 成功率较差: {overall['success_rate']:.1%}")
        health_score += 5
        issues.append("成功率严重偏低")
    
    # 响应时间评估
    avg_time = overall['avg_response_time']
    if avg_time <= 1.0:
        print(f"  ✅ 响应时间优秀: {avg_time:.2f}秒")
        health_score += 25
    elif avg_time <= 3.0:
        print(f"  👍 响应时间良好: {avg_time:.2f}秒")
        health_score += 20
    elif avg_time <= 5.0:
        print(f"  ⚠️ 响应时间一般: {avg_time:.2f}秒")
        health_score += 15
        issues.append("响应时间偏慢")
    else:
        print(f"  ❌ 响应时间较差: {avg_time:.2f}秒")
        health_score += 5
        issues.append("响应时间严重偏慢")
    
    # P99响应时间评估
    p99_time = overall['p99_response_time']
    if p99_time <= 5.0:
        print(f"  ✅ P99响应时间优秀: {p99_time:.2f}秒")
        health_score += 25
    elif p99_time <= 10.0:
        print(f"  👍 P99响应时间良好: {p99_time:.2f}秒")
        health_score += 20
    elif p99_time <= 20.0:
        print(f"  ⚠️ P99响应时间一般: {p99_time:.2f}秒")
        health_score += 15
        issues.append("长尾响应时间偏长")
    else:
        print(f"  ❌ P99响应时间较差: {p99_time:.2f}秒")
        health_score += 5
        issues.append("长尾响应时间严重偏长")
    
    # 资源使用评估
    if 'resource_usage' in report:
        resource = report['resource_usage']
        cache_hit_rate = resource.get('cache_hit_rate', 0)
        
        if cache_hit_rate >= 0.8:
            print(f"  ✅ 缓存命中率优秀: {cache_hit_rate:.1%}")
            health_score += 25
        elif cache_hit_rate >= 0.6:
            print(f"  👍 缓存命中率良好: {cache_hit_rate:.1%}")
            health_score += 20
        elif cache_hit_rate >= 0.4:
            print(f"  ⚠️ 缓存命中率一般: {cache_hit_rate:.1%}")
            health_score += 15
            issues.append("缓存命中率偏低")
        else:
            print(f"  ❌ 缓存命中率较差: {cache_hit_rate:.1%}")
            health_score += 5
            issues.append("缓存命中率严重偏低")
    
    # 综合评分
    print(f"\n🎯 综合健康评分: {health_score}/100")
    
    if health_score >= 90:
        print(f"  🏆 系统性能优秀")
    elif health_score >= 75:
        print(f"  👍 系统性能良好")
    elif health_score >= 60:
        print(f"  ⚠️ 系统性能一般")
    else:
        print(f"  ❌ 系统性能需要优化")
    
    # 问题汇总
    if issues:
        print(f"\n🔧 发现的问题:")
        for issue in issues:
            print(f"  - {issue}")
    
    # 优化建议
    trends = report['performance_trends']
    if 'recommendations' in trends:
        print(f"\n💡 优化建议:")
        for rec in trends['recommendations']:
            print(f"  - {rec}")
    
    return health_score, issues

# 执行性能诊断
health_score, issues = diagnose_performance()
```

### 性能对比分析

```python
from mcpstore import MCPStore
import time

# 初始化
store = MCPStore.setup_store()

def compare_performance_over_time():
    """对比不同时间的性能"""
    
    print("=== 性能对比分析 ===")
    
    # 获取当前性能报告
    current_report = store.for_store().get_performance_report()
    current_overall = current_report['overall_performance']
    
    print(f"📊 当前性能基线:")
    print(f"  成功率: {current_overall['success_rate']:.1%}")
    print(f"  平均响应时间: {current_overall['avg_response_time']:.2f}秒")
    print(f"  总请求数: {current_overall['total_requests']}")
    
    # 模拟等待一段时间后再次获取（实际使用中可能是定期任务）
    print(f"\n⏳ 等待性能数据更新...")
    time.sleep(2)  # 实际场景中可能是更长时间
    
    # 获取新的性能报告
    new_report = store.for_store().get_performance_report()
    new_overall = new_report['overall_performance']
    
    print(f"\n📈 性能变化分析:")
    
    # 成功率变化
    success_rate_change = new_overall['success_rate'] - current_overall['success_rate']
    print(f"  成功率变化: {success_rate_change:+.1%}")
    
    # 响应时间变化
    response_time_change = new_overall['avg_response_time'] - current_overall['avg_response_time']
    print(f"  响应时间变化: {response_time_change:+.2f}秒")
    
    # 请求量变化
    request_change = new_overall['total_requests'] - current_overall['total_requests']
    print(f"  请求量变化: {request_change:+d}")
    
    # 趋势分析
    trends = new_report['performance_trends']
    print(f"\n📊 趋势分析:")
    print(f"  响应时间趋势: {trends['response_time_trend']}")
    print(f"  成功率趋势: {trends['success_rate_trend']}")
    print(f"  负载趋势: {trends['load_trend']}")
    
    return {
        "current": current_report,
        "new": new_report,
        "changes": {
            "success_rate": success_rate_change,
            "response_time": response_time_change,
            "requests": request_change
        }
    }

# 执行性能对比分析
# comparison = compare_performance_over_time()
```

## 报告字段说明

### 报告信息 (report_info)
- `generated_at`: 报告生成时间
- `report_period`: 报告周期
- `mcpstore_version`: MCPStore版本

### 整体性能 (overall_performance)
- `total_requests`: 总请求数
- `successful_requests`: 成功请求数
- `failed_requests`: 失败请求数
- `success_rate`: 成功率
- `avg_response_time`: 平均响应时间
- `median_response_time`: 中位数响应时间
- `p95_response_time`: P95响应时间
- `p99_response_time`: P99响应时间

### 工具性能 (tool_performance)
- `fastest_tools`: 最快的工具列表
- `slowest_tools`: 最慢的工具列表
- `most_reliable_tools`: 最可靠的工具列表
- `least_reliable_tools`: 最不可靠的工具列表

### 服务性能 (service_performance)
- `service_metrics`: 各服务的性能指标
- `best_performing_service`: 性能最佳的服务
- `worst_performing_service`: 性能最差的服务

### 错误分析 (error_analysis)
- `error_types`: 错误类型统计
- `most_common_error`: 最常见的错误
- `error_rate_by_service`: 各服务的错误率

### 性能趋势 (performance_trends)
- `response_time_trend`: 响应时间趋势
- `success_rate_trend`: 成功率趋势
- `load_trend`: 负载趋势
- `recommendations`: 优化建议

### 资源使用 (resource_usage)
- `memory_usage_mb`: 内存使用量（MB）
- `cpu_usage_percent`: CPU使用率
- `network_io_mb`: 网络IO（MB）
- `cache_hit_rate`: 缓存命中率

## 相关方法

- [get_system_stats()](get-system-stats.md) - 获取系统统计信息
- [get_usage_stats()](get-usage-stats.md) - 获取使用统计
- [get_tools_with_stats()](../listing/get-tools-with-stats.md) - 获取工具统计

## 注意事项

1. **报告周期**: 性能报告基于特定时间周期的数据
2. **Agent视角**: Agent模式下只包含该Agent的性能数据
3. **实时性**: 报告数据可能有轻微延迟
4. **资源消耗**: 生成详细报告可能消耗一定资源
5. **趋势分析**: 趋势分析需要历史数据支持
