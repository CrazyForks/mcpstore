## tool_info - 工具信息


获取工具的详细信息。

### SDK

同步：
  - `tool_proxy.tool_info() -> Dict[str, Any]`

异步：
  - `await tool_proxy.tool_info_async() -> Dict[str, Any]`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 无     | -    | 该方法不需要参数。 |

### 返回值

- 类型：`Dict[str, Any]`
- 字段：

| 字段           | 类型 | 说明 |
|----------------|------|------|
| `name`         | str  | 工具名称 |
| `description`  | str  | 工具描述 |
| `service_name` | str  | 所属服务名 |
| `client_id`    | str  | 客户端标识 |
| `inputSchema`  | dict | 输入模式（JSON Schema） |


### 视角
在通过 `find_tool()` 获取的 `ToolProxy` 上调用。支持 Store 级与 Agent 级：`tool_proxy = store.for_store().find_tool(name)` 或 `store.for_agent(agent_id).find_tool(name)`。


### 使用示例

Store 级获取工具信息：
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
print("工具名称:", info["name"])
print("工具描述:", info["description"])
print("所属服务:", info["service_name"])
print("输入模式:", info["inputSchema"])
```

Agent 级获取工具信息：
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

info = tool_proxy.tool_info()
print("Agent 工具信息:", info)
```

查看输入模式（Schema）：
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
schema = info["inputSchema"]
print("输入类型:", schema.get("type"))
print("必需参数:", schema.get("required", []))
properties = schema.get("properties", {})
for param_name, param_def in properties.items():
    print(param_name, param_def.get("type"), param_def.get("description"))
```


### 你可能想找的方法

| 场景/方法     | 同步方法 |
|----------------|----------|
| 获取工具标签   | `tool_proxy.tool_tags()` |
| 获取输入模式   | `tool_proxy.tool_schema()` |
| 查找工具       | `store.for_store().find_tool(name)` |
| 列出工具       | `store.for_store().list_tools()` |


### 使用场景

- 展示层渲染工具详情与参数说明。
- 调用前读取 `inputSchema` 做参数校验与表单生成。
- Agent 开发时核对本地可见的工具元信息。


### 注意事项

- 调用前提：需先通过 `find_tool()` 获取 `ToolProxy`。
- 信息来源：数据来自服务注册的工具定义，可能与实时实现略有不同。
- Schema：`inputSchema` 符合 JSON Schema 约定，字段可能为空请做好判空。

