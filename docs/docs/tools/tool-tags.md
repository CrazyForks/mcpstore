## tool_tags - 工具标签


获取工具的标签列表。

### SDK

同步：
  - `tool_proxy.tool_tags() -> List[str]`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 无     | -    | 该方法不需要参数。 |

### 返回值

- 类型：`List[str]`
- 说明：工具标签名称列表。


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

tags = tool_proxy.tool_tags()
print("工具标签:", tags)
```


### 你可能想找的方法

| 场景/方法     | 同步方法 |
|----------------|----------|
| 获取工具信息   | `tool_proxy.tool_info()` |
| 获取输入模式   | `tool_proxy.tool_schema()` |
| 查找工具       | `store.for_store().find_tool(name)` |
| 列出工具       | `store.for_store().list_tools()` |


### 使用场景

- 在 UI 中展示工具分类或筛选条件。
- 基于标签做工具启用、排序或权限配置。
- 生成文档索引或搜索提示。


### 注意事项

- 标签可能为空列表，请做好判空处理。
- 标签来源于服务注册时的工具元数据，可能因服务实现而异。

