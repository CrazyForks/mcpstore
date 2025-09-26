# get_usage_stats()

获取使用统计。

## 方法特性

- ✅ **异步版本**: `get_usage_stats_async()`
- ✅ **Store级别**: `store.for_store().get_usage_stats()`
- ✅ **Agent级别**: `store.for_agent("agent1").get_usage_stats()`
- 📁 **文件位置**: `advanced_features.py`
- 🏷️ **所属类**: `AdvancedFeaturesMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| 无参数 | - | - | - | 该方法不需要参数 |

## 返回值

返回使用统计信息字典：

```python
{
    "period": {
        "start_time": "2025-01-01T00:00:00Z",
        "end_time": "2025-01-01T12:00:00Z",
        "duration_hours": 12.0
    },
    "tool_usage": {
        "total_calls": 250,
        "unique_tools_used": 15,
        "most_used_tools": [
            {"name": "read_file", "calls": 45, "percentage": 18.0},
            {"name": "weather_get", "calls": 38, "percentage": 15.2},
            {"name": "db_query", "calls": 32, "percentage": 12.8}
        ],
        "least_used_tools": [
            {"name": "rare_tool", "calls": 1, "percentage": 0.4}
        ],
        "unused_tools": ["backup_tool", "debug_helper"]
    },
    "service_usage": {
        "calls_by_service": {
            "filesystem": 85,
            "weather": 78,
            "database": 87
        },
        "most_active_service": "database",
        "service_usage_distribution": {
            "filesystem": 34.0,
            "weather": 31.2,
            "database": 34.8
        }
    },
    "temporal_patterns": {
        "calls_by_hour": {
            "09": 25, "10": 45, "11": 38, "12": 42
        },
        "peak_hour": "10",
        "avg_calls_per_hour": 20.8
    },
    "performance_metrics": {
        "avg_response_time": 1.45,
        "fastest_tool": {"name": "simple_calc", "avg_time": 0.12},
        "slowest_tool": {"name": "heavy_process", "avg_time": 8.34},
        "success_rate": 0.964,
        "error_rate": 0.036
    },
    "user_patterns": {
        "agent_usage": {
            "agent1": 120,
            "agent2": 80,
            "store_direct": 50
        },
        "most_active_agent": "agent1"
    }
}
```

## 使用示例

### Store级别获取使用统计

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取使用统计
stats = store.for_store().get_usage_stats()

print("=== MCPStore 使用统计 ===")

# 时间周期
period = stats['period']
print(f"📅 统计周期:")
print(f"  开始时间: {period['start_time']}")
print(f"  结束时间: {period['end_time']}")
print(f"  统计时长: {period['duration_hours']:.1f} 小时")

# 工具使用统计
tool_usage = stats['tool_usage']
print(f"\n🛠️ 工具使用:")
print(f"  总调用次数: {tool_usage['total_calls']}")
print(f"  使用的工具数: {tool_usage['unique_tools_used']}")
print(f"  未使用工具: {len(tool_usage['unused_tools'])} 个")

# 最常用工具
print(f"\n🏆 最常用工具:")
for tool in tool_usage['most_used_tools'][:5]:
    print(f"  {tool['name']}: {tool['calls']} 次 ({tool['percentage']:.1f}%)")

# 服务使用分布
service_usage = stats['service_usage']
print(f"\n🏢 服务使用分布:")
for service, calls in service_usage['calls_by_service'].items():
    percentage = service_usage['service_usage_distribution'][service]
    print(f"  {service}: {calls} 次 ({percentage:.1f}%)")

# 性能指标
performance = stats['performance_metrics']
print(f"\n⚡ 性能指标:")
print(f"  平均响应时间: {performance['avg_response_time']:.2f}秒")
print(f"  成功率: {performance['success_rate']:.1%}")
print(f"  最快工具: {performance['fastest_tool']['name']} ({performance['fastest_tool']['avg_time']:.2f}秒)")
print(f"  最慢工具: {performance['slowest_tool']['name']} ({performance['slowest_tool']['avg_time']:.2f}秒)")
```

### Agent级别获取使用统计

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式获取使用统计
agent_stats = store.for_agent("agent1").get_usage_stats()

print("=== Agent 使用统计 ===")

tool_usage = agent_stats['tool_usage']
print(f"🤖 Agent工具使用:")
print(f"  Agent总调用: {tool_usage['total_calls']}")
print(f"  Agent使用工具数: {tool_usage['unique_tools_used']}")

# Agent最常用工具
print(f"\n🏆 Agent最常用工具:")
for tool in tool_usage['most_used_tools'][:3]:
    print(f"  {tool['name']}: {tool['calls']} 次")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_get_usage_stats():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步获取使用统计
    stats = await store.for_store().get_usage_stats_async()
    
    print(f"异步获取使用统计:")
    
    tool_usage = stats['tool_usage']
    performance = stats['performance_metrics']
    
    print(f"  总调用: {tool_usage['total_calls']}")
    print(f"  成功率: {performance['success_rate']:.1%}")
    print(f"  平均响应: {performance['avg_response_time']:.2f}秒")
    
    return stats

# 运行异步获取
result = asyncio.run(async_get_usage_stats())
```

### 使用模式分析

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def analyze_usage_patterns():
    """分析使用模式"""
    
    stats = store.for_store().get_usage_stats()
    
    print("=== 使用模式分析 ===")
    
    # 工具使用模式分析
    tool_usage = stats['tool_usage']
    
    print(f"📊 工具使用模式:")
    total_calls = tool_usage['total_calls']
    unique_tools = tool_usage['unique_tools_used']
    
    if total_calls > 0 and unique_tools > 0:
        avg_calls_per_tool = total_calls / unique_tools
        print(f"  平均每工具调用: {avg_calls_per_tool:.1f} 次")
        
        # 分析使用集中度
        most_used = tool_usage['most_used_tools']
        if most_used:
            top_3_percentage = sum(tool['percentage'] for tool in most_used[:3])
            print(f"  前3工具占比: {top_3_percentage:.1f}%")
            
            if top_3_percentage > 60:
                print("  📈 使用高度集中，少数工具承担主要工作")
            elif top_3_percentage > 40:
                print("  📊 使用相对集中，有明显的热门工具")
            else:
                print("  📉 使用较为分散，工具使用均匀")
    
    # 时间模式分析
    temporal = stats['temporal_patterns']
    print(f"\n⏰ 时间模式:")
    print(f"  峰值时段: {temporal['peak_hour']}:00")
    print(f"  平均每小时调用: {temporal['avg_calls_per_hour']:.1f} 次")
    
    # 分析活跃时段
    calls_by_hour = temporal['calls_by_hour']
    if calls_by_hour:
        max_calls = max(calls_by_hour.values())
        min_calls = min(calls_by_hour.values())
        peak_ratio = max_calls / min_calls if min_calls > 0 else float('inf')
        
        print(f"  峰谷比: {peak_ratio:.1f}")
        if peak_ratio > 3:
            print("  📈 使用时间高度集中")
        elif peak_ratio > 2:
            print("  📊 使用时间相对集中")
        else:
            print("  📉 使用时间较为均匀")
    
    # 性能模式分析
    performance = stats['performance_metrics']
    print(f"\n⚡ 性能模式:")
    
    fastest = performance['fastest_tool']
    slowest = performance['slowest_tool']
    
    if fastest and slowest:
        speed_ratio = slowest['avg_time'] / fastest['avg_time']
        print(f"  性能差异倍数: {speed_ratio:.1f}x")
        
        if speed_ratio > 50:
            print("  ⚠️ 工具性能差异极大，建议优化慢工具")
        elif speed_ratio > 10:
            print("  📊 工具性能差异较大")
        else:
            print("  ✅ 工具性能相对均衡")
    
    return stats

# 执行使用模式分析
analyze_usage_patterns()
```

### 使用趋势报告

```python
from mcpstore import MCPStore
import json

# 初始化
store = MCPStore.setup_store()

def generate_usage_report():
    """生成使用趋势报告"""
    
    stats = store.for_store().get_usage_stats()
    
    print("=== MCPStore 使用趋势报告 ===")
    
    # 报告头部
    period = stats['period']
    print(f"📋 报告周期: {period['start_time']} 至 {period['end_time']}")
    print(f"📊 统计时长: {period['duration_hours']:.1f} 小时")
    
    # 核心指标
    tool_usage = stats['tool_usage']
    performance = stats['performance_metrics']
    
    print(f"\n🎯 核心指标:")
    print(f"  总调用次数: {tool_usage['total_calls']:,}")
    print(f"  工具使用率: {tool_usage['unique_tools_used']}/{tool_usage['unique_tools_used'] + len(tool_usage['unused_tools'])} ({tool_usage['unique_tools_used']/(tool_usage['unique_tools_used'] + len(tool_usage['unused_tools'])):.1%})")
    print(f"  平均响应时间: {performance['avg_response_time']:.2f}秒")
    print(f"  调用成功率: {performance['success_rate']:.1%}")
    
    # 热门工具排行
    print(f"\n🏆 热门工具排行:")
    for i, tool in enumerate(tool_usage['most_used_tools'][:5], 1):
        print(f"  {i}. {tool['name']}: {tool['calls']} 次 ({tool['percentage']:.1f}%)")
    
    # 服务活跃度
    service_usage = stats['service_usage']
    print(f"\n🏢 服务活跃度:")
    sorted_services = sorted(
        service_usage['calls_by_service'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    for service, calls in sorted_services:
        percentage = service_usage['service_usage_distribution'][service]
        print(f"  {service}: {calls} 次 ({percentage:.1f}%)")
    
    # 性能洞察
    print(f"\n⚡ 性能洞察:")
    fastest = performance['fastest_tool']
    slowest = performance['slowest_tool']
    print(f"  最快工具: {fastest['name']} ({fastest['avg_time']:.2f}秒)")
    print(f"  最慢工具: {slowest['name']} ({slowest['avg_time']:.2f}秒)")
    
    # 优化建议
    print(f"\n💡 优化建议:")
    
    if len(tool_usage['unused_tools']) > 0:
        print(f"  - 有 {len(tool_usage['unused_tools'])} 个工具未被使用，考虑清理或推广")
    
    if performance['error_rate'] > 0.05:
        print(f"  - 错误率 {performance['error_rate']:.1%} 偏高，建议检查服务稳定性")
    
    if performance['avg_response_time'] > 3.0:
        print(f"  - 平均响应时间 {performance['avg_response_time']:.2f}秒 较慢，建议优化")
    
    # 用户活跃度
    if 'user_patterns' in stats:
        user_patterns = stats['user_patterns']
        print(f"\n👥 用户活跃度:")
        agent_usage = user_patterns['agent_usage']
        for agent, calls in sorted(agent_usage.items(), key=lambda x: x[1], reverse=True):
            print(f"  {agent}: {calls} 次调用")
    
    return stats

# 生成使用趋势报告
generate_usage_report()
```

### 导出使用统计

```python
from mcpstore import MCPStore
import json
from datetime import datetime

# 初始化
store = MCPStore.setup_store()

def export_usage_stats(filename=None):
    """导出使用统计到文件"""
    
    stats = store.for_store().get_usage_stats()
    
    # 生成文件名
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcpstore_usage_stats_{timestamp}.json"
    
    # 导出统计数据
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"使用统计已导出到: {filename}")
        
        # 显示导出摘要
        tool_usage = stats['tool_usage']
        print(f"导出摘要:")
        print(f"  总调用次数: {tool_usage['total_calls']}")
        print(f"  统计周期: {stats['period']['duration_hours']:.1f} 小时")
        print(f"  文件大小: {len(json.dumps(stats))} 字符")
        
        return filename
        
    except Exception as e:
        print(f"导出失败: {e}")
        return None

# 导出使用统计
export_usage_stats()
```

## 统计字段说明

### 时间周期 (period)
- `start_time`: 统计开始时间
- `end_time`: 统计结束时间
- `duration_hours`: 统计时长（小时）

### 工具使用 (tool_usage)
- `total_calls`: 总调用次数
- `unique_tools_used`: 使用的工具数量
- `most_used_tools`: 最常用工具列表
- `least_used_tools`: 最少用工具列表
- `unused_tools`: 未使用工具列表

### 服务使用 (service_usage)
- `calls_by_service`: 按服务分组的调用次数
- `most_active_service`: 最活跃的服务
- `service_usage_distribution`: 服务使用分布百分比

### 时间模式 (temporal_patterns)
- `calls_by_hour`: 按小时分组的调用次数
- `peak_hour`: 峰值时段
- `avg_calls_per_hour`: 平均每小时调用次数

### 性能指标 (performance_metrics)
- `avg_response_time`: 平均响应时间
- `fastest_tool`: 最快的工具
- `slowest_tool`: 最慢的工具
- `success_rate`: 成功率
- `error_rate`: 错误率

### 用户模式 (user_patterns)
- `agent_usage`: 按Agent分组的使用情况
- `most_active_agent`: 最活跃的Agent

## 相关方法

- [get_system_stats()](get-system-stats.md) - 获取系统统计信息
- [get_performance_report()](get-performance-report.md) - 获取性能报告
- [get_tools_with_stats()](../listing/get-tools-with-stats.md) - 获取工具统计

## 注意事项

1. **统计周期**: 统计数据基于特定时间周期，可能不包含历史数据
2. **Agent视角**: Agent模式下只统计该Agent的使用情况
3. **实时性**: 统计数据可能有轻微延迟
4. **隐私保护**: 不包含具体的调用参数和返回值
5. **性能影响**: 统计计算对性能影响很小
