# find_tool()

查找工具并返回 ToolProxy 对象。

## 方法特性

- ✅ **调用方式**: Context 方法
- ✅ **异步版本**: 支持异步调用
- ✅ **Store级别**: `store.for_store().find_tool("tool_name")`
- ✅ **Agent级别**: `store.for_agent("agent1").find_tool("tool_name")`
- 📁 **文件位置**: `tool_operations.py`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `tool_name` | `str` | ✅ | - | 工具名称（支持多种格式） |
| `service_name` | `str` | ❌ | `None` | 指定服务名称（可选） |

## 返回值

返回 `ToolProxy` 对象，提供工具级别的操作方法。

## 使用示例

### Store级别查找工具

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

# 等待服务就绪
store.for_store().wait_service("weather")

# 查找工具
tool_proxy = store.for_store().find_tool("get_current_weather")

# 使用 ToolProxy
info = tool_proxy.tool_info()
print(f"工具信息: {info}")

result = tool_proxy.call_tool({"query": "北京"})
print(f"调用结果: {result.text_output}")
```

### Agent级别查找工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent级别添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_agent("agent1").wait_service("weather")

# 查找工具
tool_proxy = store.for_agent("agent1").find_tool("get_current_weather")

# 使用 ToolProxy
result = tool_proxy.call_tool({"query": "上海"})
print(f"Agent工具调用: {result.text_output}")
```

### 指定服务查找

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加多个服务
store.for_store().add_service({
    "mcpServers": {
        "weather1": {"url": "https://api1.example.com/mcp"},
        "weather2": {"url": "https://api2.example.com/mcp"}
    }
})

# 等待服务
store.for_store().wait_service("weather1")
store.for_store().wait_service("weather2")

# 指定服务查找工具
tool_proxy = store.for_store().find_tool(
    tool_name="get_weather",
    service_name="weather1"
)

print(f"找到工具: {tool_proxy.tool_info()}")
```

### 支持的工具名称格式

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "my-service": {"url": "https://example.com/mcp"}
    }
})

store.for_store().wait_service("my-service")

# 1. 简短名称
tool1 = store.for_store().find_tool("get_weather")

# 2. 服务前缀格式（双下划线）
tool2 = store.for_store().find_tool("my-service__get_weather")

# 3. 服务前缀格式（单下划线）
tool3 = store.for_store().find_tool("my-service_get_weather")

# 所有格式都能找到同一个工具
print(f"工具1: {tool1.tool_info()['name']}")
print(f"工具2: {tool2.tool_info()['name']}")
print(f"工具3: {tool3.tool_info()['name']}")
```

## ToolProxy 提供的方法

```python
tool_proxy = store.for_store().find_tool("tool_name")

# 工具详情
tool_proxy.tool_info()          # 获取工具详细信息
tool_proxy.tool_tags()          # 获取工具标签
tool_proxy.tool_schema()        # 获取工具输入模式

# 工具配置
tool_proxy.set_redirect(True)   # 设置重定向标记（return_direct）

# 工具调用
tool_proxy.call_tool(args)      # 调用工具

# 工具统计
tool_proxy.usage_stats()        # 获取使用统计
tool_proxy.call_history()       # 获取调用历史
```

## 相关方法

- [list_tools()](list-tools.md) - 列出所有工具
- [tool_info()](../details/tool-info.md) - 获取工具详情
- [call_tool()](../usage/call-tool.md) - 调用工具
- [ToolProxy 概念](tool-proxy.md) - 了解 ToolProxy

## 注意事项

1. **工具名称格式**: 支持简短名称、带服务前缀的名称
2. **服务范围**: 可以指定 `service_name` 限定查找范围
3. **ToolProxy对象**: 返回的对象提供工具级别的操作方法
4. **Agent隔离**: Agent级别只能查找该Agent的工具

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

