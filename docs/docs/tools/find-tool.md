## find_tool - 查找工具


查找工具并返回 `ToolProxy` 对象。

### SDK

同步：
  - `store.for_store().find_tool(tool_name, service_name=None) -> ToolProxy`
  - `store.for_agent(id).find_tool(tool_name, service_name=None) -> ToolProxy`

异步：
  - `await store.for_store().find_tool_async(tool_name, service_name=None) -> ToolProxy`
  - `await store.for_agent(id).find_tool_async(tool_name, service_name=None) -> ToolProxy`

### 参数

| 参数名         | 类型 | 说明 |
|----------------|------|------|
| `tool_name`    | str  | 工具名称，支持多种格式（见“工具名称格式”）。 |
| `service_name` | str  | 指定服务名称（可选）。 |

### 返回值

- 类型：`ToolProxy`
- 说明：工具代理对象，提供工具详情、配置与调用等操作。


### 视角
通过 `for_store()` 可在全局范围查找任意服务的工具；通过 `for_agent(id)` 仅查找当前 Agent 的工具，名称映射自动处理。


### 使用示例

Store 级别查找工具：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

tool_proxy = store.for_store().find_tool("get_current_weather")

info = tool_proxy.tool_info()
print("工具信息:", info)

result = tool_proxy.call_tool({"query": "北京"})
print("调用结果:", getattr(result, "text_output", result))
```

Agent 级别查找工具：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_agent("agent1").wait_service("weather")

tool_proxy = store.for_agent("agent1").find_tool("get_current_weather")
result = tool_proxy.call_tool({"query": "上海"})
print("Agent 工具调用:", getattr(result, "text_output", result))
```

指定服务查找：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather1": {"url": "https://api1.example.com/mcp"},
        "weather2": {"url": "https://api2.example.com/mcp"}
    }
})

store.for_store().wait_service("weather1")
store.for_store().wait_service("weather2")

tool_proxy = store.for_store().find_tool(
    tool_name="get_weather",
    service_name="weather1"
)
print("找到工具:", tool_proxy.tool_info())
```

工具名称格式：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "my-service": {"url": "https://example.com/mcp"}
    }
})

store.for_store().wait_service("my-service")

# 简短名称
tool1 = store.for_store().find_tool("get_weather")

# 服务前缀（双下划线）
tool2 = store.for_store().find_tool("my-service__get_weather")

# 服务前缀（单下划线）
tool3 = store.for_store().find_tool("my-service_get_weather")

print(tool1.tool_info()["name"])  # 一致
print(tool2.tool_info()["name"])  # 一致
print(tool3.tool_info()["name"])  # 一致
```


### 你可能想找的方法

| 场景/方法     | 同步方法 |
|----------------|----------|
| 列出工具       | `store.for_store().list_tools()` |
| 获取工具详情   | `tool_proxy.tool_info()` |
| 调用工具       | `tool_proxy.call_tool(args)` 或 `store.for_store().call_tool(...)` |
| 设置重定向     | `tool_proxy.set_redirect(True)` |
| ToolProxy 概念 | 见 `tool-proxy.md` |


### 使用场景

- 根据名称快速定位并获取某个工具的代理对象。
- 在多服务场景下通过 `service_name` 锁定查询范围。
- 在 Agent 模式下使用本地名称进行开发与调试。


### 注意事项

- 名称格式：支持简短名以及带服务前缀的名称（单/双下划线）。
- 查询范围：`service_name` 可用于限定服务，避免歧义。
- Agent 隔离：Agent 级别只能查找该 Agent 的工具。
- ToolProxy：返回对象提供工具详情、调用与配置相关操作。

