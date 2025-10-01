# tool_info()

获取工具的详细信息。

## 方法特性

- ✅ **调用方式**: ToolProxy 方法
- ✅ **异步版本**: 支持异步调用
- ✅ **Store级别**: `tool_proxy = store.for_store().find_tool("name")` 后调用
- ✅ **Agent级别**: `tool_proxy = store.for_agent("agent1").find_tool("name")` 后调用
- 📁 **文件位置**: `tool_proxy.py`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回包含工具详细信息的字典：

```python
{
    "name": str,                    # 工具名称
    "description": str,             # 工具描述
    "service_name": str,            # 所属服务名
    "client_id": str,               # 客户端ID
    "inputSchema": dict             # 输入模式（JSON Schema）
}
```

## 使用示例

### Store级别获取工具信息

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

# 获取工具详情
info = tool_proxy.tool_info()
print(f"工具名称: {info['name']}")
print(f"工具描述: {info['description']}")
print(f"所属服务: {info['service_name']}")
print(f"输入模式: {info['inputSchema']}")
```

### Agent级别获取工具信息

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

# 获取工具详情
info = tool_proxy.tool_info()
print(f"Agent工具信息: {info}")
```

### 查看输入模式（Schema）

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
tool_proxy = store.for_store().find_tool("get_current_weather")

# 获取详情
info = tool_proxy.tool_info()

# 查看输入模式
schema = info['inputSchema']
print(f"输入类型: {schema.get('type')}")
print(f"必需参数: {schema.get('required', [])}")
print(f"参数定义:")
for param_name, param_def in schema.get('properties', {}).items():
    print(f"  - {param_name}:")
    print(f"      类型: {param_def.get('type')}")
    print(f"      描述: {param_def.get('description')}")
```

### 批量查看工具信息

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

# 列出所有工具
tools = store.for_store().list_tools()

print("📊 所有工具详情:")
print("=" * 50)

for tool in tools:
    # 获取每个工具的详细信息
    tool_proxy = store.for_store().find_tool(tool.name)
    info = tool_proxy.tool_info()
    
    print(f"\n工具: {info['name']}")
    print(f"  描述: {info['description']}")
    print(f"  服务: {info['service_name']}")
    
    # 显示参数
    schema = info.get('inputSchema', {})
    required = schema.get('required', [])
    properties = schema.get('properties', {})
    
    if properties:
        print(f"  参数:")
        for param in properties:
            is_required = "必需" if param in required else "可选"
            print(f"    - {param} ({is_required})")
```

## 相关方法

- [tool_tags()](tool-tags.md) - 获取工具标签
- [tool_schema()](tool-schema.md) - 获取工具输入模式
- [find_tool()](../finding/find-tool.md) - 查找工具
- [list_tools()](../finding/list-tools.md) - 列出所有工具

## 注意事项

1. **调用前提**: 必须先通过 `find_tool()` 获取 ToolProxy 对象
2. **信息完整性**: 返回的信息来自服务注册时的工具定义
3. **Agent隔离**: Agent级别只能看到该Agent的工具信息
4. **Schema格式**: inputSchema 遵循 JSON Schema 标准

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

