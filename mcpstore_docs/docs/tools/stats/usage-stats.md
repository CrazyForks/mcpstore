# usage_stats()

获取工具的使用统计信息。

## 方法特性

- ✅ **调用方式**: ToolProxy 方法
- ✅ **Store级别**: `tool_proxy = store.for_store().find_tool("name")` 后调用
- ✅ **Agent级别**: `tool_proxy = store.for_agent("agent1").find_tool("name")` 后调用
- 📁 **文件位置**: `tool_proxy.py`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回工具使用统计信息的字典：

```python
{
    "call_count": int,          # 总调用次数
    "success_count": int,       # 成功次数
    "error_count": int,         # 失败次数
    "avg_duration": float,      # 平均耗时（秒）
    "total_duration": float,    # 总耗时（秒）
    "last_called_at": str,      # 最后调用时间
    "first_called_at": str      # 首次调用时间
}
```

## 使用示例

### Store级别获取统计

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
for i in range(5):
    result = tool_proxy.call_tool({"query": f"城市{i+1}"})
    print(f"调用{i+1}: {result.text_output[:30]}...")

# 获取使用统计
stats = tool_proxy.usage_stats()
print(f"\n📊 使用统计:")
print(f"  总调用次数: {stats['call_count']}")
print(f"  成功次数: {stats['success_count']}")
print(f"  失败次数: {stats['error_count']}")
print(f"  平均耗时: {stats['avg_duration']:.3f}秒")
print(f"  总耗时: {stats['total_duration']:.3f}秒")
print(f"  最后调用: {stats['last_called_at']}")
```

### Agent级别获取统计

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

# 获取统计
stats = tool_proxy.usage_stats()
print(f"Agent工具统计: {stats}")
```

### 性能监控

```python
from mcpstore import MCPStore
import time

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

print("📊 工具性能监控")
print("=" * 50)

# 初始统计
initial_stats = tool_proxy.usage_stats()
print(f"初始调用次数: {initial_stats['call_count']}")

# 执行多次调用
test_count = 10
for i in range(test_count):
    start = time.time()
    result = tool_proxy.call_tool({"query": "测试"})
    duration = time.time() - start
    
    print(f"调用 {i+1}: {duration:.3f}秒")

# 最终统计
final_stats = tool_proxy.usage_stats()
print(f"\n📈 统计结果:")
print(f"  新增调用: {final_stats['call_count'] - initial_stats['call_count']}")
print(f"  平均耗时: {final_stats['avg_duration']:.3f}秒")
print(f"  成功率: {final_stats['success_count'] / final_stats['call_count'] * 100:.1f}%")
```

### 批量工具统计对比

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

# 获取所有工具
tools = store.for_store().list_tools()

print("📊 所有工具使用统计")
print("=" * 70)

for tool in tools:
    tool_proxy = store.for_store().find_tool(tool.name)
    stats = tool_proxy.usage_stats()
    
    if stats['call_count'] > 0:
        print(f"\n工具: {tool.name}")
        print(f"  调用次数: {stats['call_count']}")
        print(f"  成功率: {stats['success_count'] / stats['call_count'] * 100:.1f}%")
        print(f"  平均耗时: {stats['avg_duration']:.3f}秒")
```

## 相关方法

- [call_history()](call-history.md) - 获取调用历史
- [tools_stats()](tools-stats.md) - 服务工具统计
- [find_tool()](../finding/find-tool.md) - 查找工具
- [call_tool()](../usage/call-tool.md) - 调用工具

## 注意事项

1. **调用前提**: 必须先通过 `find_tool()` 获取 ToolProxy 对象
2. **统计范围**: 统计当前会话中的工具调用
3. **实时更新**: 每次调用后自动更新统计
4. **Agent隔离**: Agent级别只统计该Agent的调用

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

