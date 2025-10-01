# call_history()

获取工具的调用历史记录。

## 方法特性

- ✅ **调用方式**: ToolProxy 方法
- ✅ **Store级别**: `tool_proxy = store.for_store().find_tool("name")` 后调用
- ✅ **Agent级别**: `tool_proxy = store.for_agent("agent1").find_tool("name")` 后调用
- 📁 **文件位置**: `tool_proxy.py`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `limit` | `int` | ❌ | `10` | 返回的历史记录数量 |

## 返回值

返回调用历史记录列表（List[Dict]），每条记录包含：

```python
{
    "tool_name": str,           # 工具名称
    "arguments": dict,          # 调用参数
    "result": dict,             # 调用结果
    "is_error": bool,           # 是否出错
    "duration": float,          # 耗时（秒）
    "called_at": str            # 调用时间
}
```

## 使用示例

### Store级别获取历史

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 查找工具
tool_proxy = store.for_store().find_tool("get_current_weather")

# 多次调用工具
cities = ["北京", "上海", "广州", "深圳", "杭州"]
for city in cities:
    result = tool_proxy.call_tool({"query": city})
    print(f"{city}: {result.text_output[:30]}...")

# 获取调用历史（最近5条）
history = tool_proxy.call_history(limit=5)

print(f"\n📜 调用历史（共{len(history)}条）:")
for i, record in enumerate(history):
    print(f"\n记录 {i+1}:")
    print(f"  时间: {record['called_at']}")
    print(f"  参数: {record['arguments']}")
    print(f"  耗时: {record['duration']:.3f}秒")
    print(f"  是否出错: {record['is_error']}")
```

### Agent级别获取历史

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# Agent级别添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_agent("agent1").wait_service("weather")

# 查找工具并调用
tool_proxy = store.for_agent("agent1").find_tool("get_current_weather")
tool_proxy.call_tool({"query": "北京"})

# 获取历史
history = tool_proxy.call_history()
print(f"Agent调用历史: {history}")
```

### 详细历史分析

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 查找工具
tool_proxy = store.for_store().find_tool("get_current_weather")

# 多次调用
for i in range(10):
    tool_proxy.call_tool({"query": f"测试{i+1}"})

# 获取全部历史
history = tool_proxy.call_history(limit=100)

print("📊 调用历史分析")
print("=" * 50)

# 统计分析
total_calls = len(history)
error_calls = sum(1 for r in history if r['is_error'])
success_calls = total_calls - error_calls

durations = [r['duration'] for r in history]
avg_duration = sum(durations) / len(durations) if durations else 0
max_duration = max(durations) if durations else 0
min_duration = min(durations) if durations else 0

print(f"总调用次数: {total_calls}")
print(f"成功次数: {success_calls}")
print(f"失败次数: {error_calls}")
print(f"成功率: {success_calls / total_calls * 100:.1f}%")
print(f"\n性能指标:")
print(f"  平均耗时: {avg_duration:.3f}秒")
print(f"  最快: {min_duration:.3f}秒")
print(f"  最慢: {max_duration:.3f}秒")

# 显示最近5次调用
print(f"\n最近5次调用:")
for i, record in enumerate(history[:5]):
    status = "❌" if record['is_error'] else "✅"
    print(f"{status} {i+1}. {record['called_at']} - {record['duration']:.3f}秒")
```

### 查找特定参数的调用

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 查找工具并多次调用
tool_proxy = store.for_store().find_tool("get_current_weather")

test_queries = ["北京", "上海", "北京", "广州", "北京"]
for query in test_queries:
    tool_proxy.call_tool({"query": query})

# 获取历史
history = tool_proxy.call_history(limit=50)

# 查找所有北京的查询
beijing_calls = [
    r for r in history 
    if r['arguments'].get('query') == "北京"
]

print(f"查询'北京'的次数: {len(beijing_calls)}")
for i, record in enumerate(beijing_calls):
    print(f"{i+1}. {record['called_at']} - {record['duration']:.3f}秒")
```

### 错误调用分析

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 查找工具
tool_proxy = store.for_store().find_tool("get_current_weather")

# 执行一些调用
tool_proxy.call_tool({"query": "北京"})
tool_proxy.call_tool({"query": "上海"})

# 获取历史
history = tool_proxy.call_history()

# 分析错误
errors = [r for r in history if r['is_error']]

if errors:
    print("❌ 错误调用分析:")
    for i, error in enumerate(errors):
        print(f"\n错误 {i+1}:")
        print(f"  时间: {error['called_at']}")
        print(f"  参数: {error['arguments']}")
        print(f"  错误信息: {error['result']}")
else:
    print("✅ 所有调用都成功")
```

## 相关方法

- [usage_stats()](usage-stats.md) - 获取使用统计
- [tools_stats()](tools-stats.md) - 服务工具统计
- [find_tool()](../finding/find-tool.md) - 查找工具
- [call_tool()](../usage/call-tool.md) - 调用工具

## 注意事项

1. **调用前提**: 必须先通过 `find_tool()` 获取 ToolProxy 对象
2. **历史范围**: 返回当前会话中的调用历史
3. **数量限制**: 通过 `limit` 参数控制返回数量
4. **时间顺序**: 按时间倒序排列（最新的在前）
5. **Agent隔离**: Agent级别只返回该Agent的历史

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

