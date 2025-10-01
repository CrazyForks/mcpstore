# tool_schema()

获取工具的输入模式（JSON Schema）。

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

返回工具的输入模式（JSON Schema 格式的字典）。

## 使用示例

### 基本使用

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

# 获取工具模式
schema = tool_proxy.tool_schema()
print(f"输入模式: {schema}")

# 查看参数定义
properties = schema.get('properties', {})
for param_name, param_def in properties.items():
    print(f"参数: {param_name}")
    print(f"  类型: {param_def.get('type')}")
    print(f"  描述: {param_def.get('description')}")
```

## 相关方法

- [tool_info()](tool-info.md) - 获取工具详细信息
- [tool_tags()](tool-tags.md) - 获取工具标签

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

