## tool_schema - 工具输入模式


获取工具的输入模式（JSON Schema）。

### SDK

同步：
  - `tool_proxy.tool_schema() -> Dict[str, Any]`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 无     | -    | 该方法不需要参数。 |

### 返回值

- 类型：`Dict[str, Any]`
- 说明：JSON Schema 格式的输入模式。

常见字段：

| 字段         | 类型 | 说明 |
|--------------|------|------|
| `type`       | str  | 输入类型（通常为 `object`）。 |
| `properties` | dict | 参数定义字典。 |
| `required`   | list | 必需参数名称列表。 |


### 视角
在通过 `find_tool()` 获取的 `ToolProxy` 上调用。支持 Store 与 Agent 视角。


### 使用示例

基本使用：
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

schema = tool_proxy.tool_schema()
print("输入模式:", schema)

properties = schema.get("properties", {})
for param_name, param_def in properties.items():
    print("参数:", param_name)
    print("  类型:", param_def.get("type"))
    print("  描述:", param_def.get("description"))
```


### 你可能想找的方法

| 场景/方法     | 同步方法 |
|----------------|----------|
| 获取工具信息   | `tool_proxy.tool_info()` |
| 获取工具标签   | `tool_proxy.tool_tags()` |
| 调用工具       | `tool_proxy.call_tool(args)` |


### 使用场景

- 生成前端表单或参数校验器。
- 调用前动态构建参数对象。
- 文档生成与工具能力对外说明。


### 注意事项

- Schema 兼容性：遵循 JSON Schema 约定，具体字段随服务实现而异。
- 判空处理：`properties`、`required` 等字段可能缺省。

