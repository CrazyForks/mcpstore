# tool_tags()

获取工具的标签信息。

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

返回工具的标签列表（List[str]）。

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

# 获取工具标签
tags = tool_proxy.tool_tags()
print(f"工具标签: {tags}")
```

## 相关方法

- [tool_info()](tool-info.md) - 获取工具详细信息
- [tool_schema()](tool-schema.md) - 获取工具输入模式

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

