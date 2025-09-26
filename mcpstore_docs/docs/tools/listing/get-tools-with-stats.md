# get_tools_with_stats()

获取工具列表及统计信息。

## 方法特性

- ✅ **异步版本**: `get_tools_with_stats_async()`
- ✅ **Store级别**: `store.for_store().get_tools_with_stats()`
- ✅ **Agent级别**: `store.for_agent("agent1").get_tools_with_stats()`
- 📁 **文件位置**: `tool_operations.py`
- 🏷️ **所属类**: `ToolOperationsMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| 无参数 | - | - | - | 该方法不需要参数 |

## 返回值

返回包含工具列表和统计信息的字典：

```python
{
    "tools": [
        {
            "name": "tool_name",
            "description": "工具描述",
            "service": "service_name",
            "input_schema": {...}
        }
    ],
    "statistics": {
        "total_tools": 15,
        "tools_by_service": {
            "filesystem": 8,
            "weather": 4,
            "database": 3
        },
        "services_count": 3,
        "healthy_services": 3,
        "last_updated": "2025-01-01T12:00:00Z"
    }
}
```

## 使用示例

### Store级别获取工具统计

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取工具列表及统计信息
result = store.for_store().get_tools_with_stats()

print(f"工具统计信息:")
print(f"  总工具数: {result['statistics']['total_tools']}")
print(f"  服务数量: {result['statistics']['services_count']}")
print(f"  健康服务: {result['statistics']['healthy_services']}")

# 按服务分组显示工具
print(f"\n按服务分组:")
for service_name, tool_count in result['statistics']['tools_by_service'].items():
    print(f"  {service_name}: {tool_count} 个工具")

# 显示工具列表
print(f"\n工具列表:")
for tool in result['tools']:
    print(f"  🛠️ {tool['name']} ({tool['service']})")
    print(f"     {tool['description']}")
```

### Agent级别获取工具统计

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式获取工具统计
agent_result = store.for_agent("agent1").get_tools_with_stats()

print(f"Agent工具统计:")
print(f"  Agent可用工具: {agent_result['statistics']['total_tools']}")
print(f"  Agent服务数: {agent_result['statistics']['services_count']}")

# Agent模式下工具名称是本地化的
for tool in agent_result['tools']:
    print(f"  📱 {tool['name']} - {tool['description']}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_get_tools_stats():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步获取工具统计
    result = await store.for_store().get_tools_with_stats_async()
    
    print(f"异步获取工具统计:")
    stats = result['statistics']
    print(f"  总工具数: {stats['total_tools']}")
    print(f"  最后更新: {stats['last_updated']}")
    
    # 分析工具分布
    tools_by_service = stats['tools_by_service']
    if tools_by_service:
        max_tools_service = max(tools_by_service, key=tools_by_service.get)
        print(f"  工具最多的服务: {max_tools_service} ({tools_by_service[max_tools_service]} 个)")
    
    return result

# 运行异步获取
result = asyncio.run(async_get_tools_stats())
```

### 工具统计分析

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def analyze_tools_stats():
    """分析工具统计信息"""
    
    result = store.for_store().get_tools_with_stats()
    stats = result['statistics']
    tools = result['tools']
    
    print("=== 工具统计分析 ===")
    
    # 基础统计
    print(f"📊 基础统计:")
    print(f"  总工具数: {stats['total_tools']}")
    print(f"  服务数量: {stats['services_count']}")
    print(f"  健康服务: {stats['healthy_services']}")
    
    # 服务健康率
    if stats['services_count'] > 0:
        health_rate = stats['healthy_services'] / stats['services_count']
        print(f"  服务健康率: {health_rate:.1%}")
    
    # 工具分布分析
    tools_by_service = stats['tools_by_service']
    if tools_by_service:
        print(f"\n📈 工具分布分析:")
        
        # 平均每服务工具数
        avg_tools = stats['total_tools'] / stats['services_count']
        print(f"  平均每服务工具数: {avg_tools:.1f}")
        
        # 工具最多和最少的服务
        max_service = max(tools_by_service, key=tools_by_service.get)
        min_service = min(tools_by_service, key=tools_by_service.get)
        print(f"  工具最多: {max_service} ({tools_by_service[max_service]} 个)")
        print(f"  工具最少: {min_service} ({tools_by_service[min_service]} 个)")
    
    # 工具名称分析
    if tools:
        print(f"\n🔍 工具名称分析:")
        tool_names = [tool['name'] for tool in tools]
        
        # 最长和最短工具名
        longest_name = max(tool_names, key=len)
        shortest_name = min(tool_names, key=len)
        print(f"  最长工具名: {longest_name} ({len(longest_name)} 字符)")
        print(f"  最短工具名: {shortest_name} ({len(shortest_name)} 字符)")
        
        # 平均工具名长度
        avg_name_length = sum(len(name) for name in tool_names) / len(tool_names)
        print(f"  平均名称长度: {avg_name_length:.1f} 字符")
    
    return result

# 执行工具统计分析
analyze_tools_stats()
```

### 工具对比分析

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def compare_store_agent_tools():
    """对比Store和Agent的工具差异"""
    
    # 获取Store级别工具统计
    store_result = store.for_store().get_tools_with_stats()
    
    # 获取Agent级别工具统计
    agent_result = store.for_agent("agent1").get_tools_with_stats()
    
    print("=== Store vs Agent 工具对比 ===")
    
    store_stats = store_result['statistics']
    agent_stats = agent_result['statistics']
    
    print(f"📊 数量对比:")
    print(f"  Store工具数: {store_stats['total_tools']}")
    print(f"  Agent工具数: {agent_stats['total_tools']}")
    print(f"  差异: {store_stats['total_tools'] - agent_stats['total_tools']}")
    
    print(f"\n🏢 服务对比:")
    print(f"  Store服务数: {store_stats['services_count']}")
    print(f"  Agent服务数: {agent_stats['services_count']}")
    
    # 工具名称对比
    store_tools = {tool['name'] for tool in store_result['tools']}
    agent_tools = {tool['name'] for tool in agent_result['tools']}
    
    print(f"\n🔍 工具名称对比:")
    print(f"  Store独有工具: {len(store_tools - agent_tools)} 个")
    print(f"  Agent独有工具: {len(agent_tools - store_tools)} 个")
    print(f"  共同工具: {len(store_tools & agent_tools)} 个")
    
    # 显示差异详情
    if store_tools - agent_tools:
        print(f"\n  Store独有工具列表:")
        for tool_name in sorted(store_tools - agent_tools):
            print(f"    - {tool_name}")
    
    if agent_tools - store_tools:
        print(f"\n  Agent独有工具列表:")
        for tool_name in sorted(agent_tools - store_tools):
            print(f"    - {tool_name}")
    
    return {
        "store": store_result,
        "agent": agent_result
    }

# 执行对比分析
compare_store_agent_tools()
```

### 定期统计监控

```python
from mcpstore import MCPStore
import time
import json

# 初始化
store = MCPStore.setup_store()

def monitor_tools_stats(interval_seconds=60, max_iterations=5):
    """定期监控工具统计变化"""
    
    print(f"开始监控工具统计，间隔: {interval_seconds}秒")
    
    previous_stats = None
    
    for i in range(max_iterations):
        print(f"\n=== 监控轮次 {i + 1} ===")
        
        # 获取当前统计
        result = store.for_store().get_tools_with_stats()
        current_stats = result['statistics']
        
        print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总工具数: {current_stats['total_tools']}")
        print(f"服务数量: {current_stats['services_count']}")
        print(f"健康服务: {current_stats['healthy_services']}")
        
        # 与上次对比
        if previous_stats:
            tools_change = current_stats['total_tools'] - previous_stats['total_tools']
            services_change = current_stats['services_count'] - previous_stats['services_count']
            
            if tools_change != 0 or services_change != 0:
                print(f"📈 变化检测:")
                print(f"  工具数变化: {tools_change:+d}")
                print(f"  服务数变化: {services_change:+d}")
            else:
                print(f"📊 无变化")
        
        previous_stats = current_stats.copy()
        
        # 等待下次监控
        if i < max_iterations - 1:
            time.sleep(interval_seconds)
    
    print(f"\n监控完成")

# 执行定期监控（示例：每60秒监控一次，共5次）
# monitor_tools_stats(60, 5)
```

## 统计字段说明

### 工具信息 (tools)
- `name`: 工具名称
- `description`: 工具描述
- `service`: 所属服务名称
- `input_schema`: 输入参数模式

### 统计信息 (statistics)
- `total_tools`: 总工具数量
- `tools_by_service`: 按服务分组的工具数量
- `services_count`: 服务总数
- `healthy_services`: 健康服务数量
- `last_updated`: 最后更新时间

## 相关方法

- [list_tools()](list-tools.md) - 获取简单的工具列表
- [get_system_stats()](../stats/get-system-stats.md) - 获取系统级统计信息
- [call_tool()](../usage/call-tool.md) - 调用具体工具

## 注意事项

1. **实时统计**: 返回实时的工具统计信息，不是缓存数据
2. **Agent透明**: Agent模式下工具名称会转换为本地名称
3. **健康状态**: 统计信息包含服务健康状态
4. **性能考虑**: 大量工具时统计计算可能需要时间
5. **时间戳**: 包含最后更新时间，便于监控变化
