# tools_stats()

获取服务的工具统计信息（ServiceProxy 方法）。

## 方法特性

- ✅ **调用方式**: ServiceProxy 方法
- ✅ **Store级别**: `svc = store.for_store().find_service("name")` 后调用
- ✅ **Agent级别**: `svc = store.for_agent("agent1").find_service("name")` 后调用
- 📁 **文件位置**: `service_proxy.py`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回服务所有工具的统计信息字典。

## 使用示例

### Store级别获取服务工具统计

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

# 查找服务
svc = store.for_store().find_service("weather")

# 获取工具统计
stats = svc.tools_stats()
print(f"📊 服务工具统计:")
print(f"  工具总数: {len(stats)}")
print(f"  统计信息: {stats}")
```

### Agent级别获取统计

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

# 查找服务
svc = store.for_agent("agent1").find_service("weather")

# 获取工具统计
stats = svc.tools_stats()
print(f"Agent服务工具统计: {stats}")
```

### 结合工具列表使用

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

# 查找服务
svc = store.for_store().find_service("weather")

# 获取工具列表
tools = svc.list_tools()
print(f"工具列表（{len(tools)}个）:")
for tool in tools:
    print(f"  - {tool.name}: {tool.description}")

# 获取工具统计
stats = svc.tools_stats()
print(f"\n工具统计:")
print(stats)
```

## 与 ToolProxy.usage_stats() 的区别

| 对比项 | tools_stats() | usage_stats() |
|--------|---------------|---------------|
| **调用方式** | ServiceProxy方法 | ToolProxy方法 |
| **统计范围** | 服务所有工具 | 单个工具 |
| **使用场景** | 服务级别统计 | 工具级别统计 |

```python
# tools_stats() - ServiceProxy级别（服务所有工具）
svc = store.for_store().find_service("weather")
service_stats = svc.tools_stats()  # 服务所有工具的统计

# usage_stats() - ToolProxy级别（单个工具）
tool = store.for_store().find_tool("get_weather")
tool_stats = tool.usage_stats()  # 单个工具的统计
```

## 相关方法

- [usage_stats()](usage-stats.md) - 单个工具使用统计
- [call_history()](call-history.md) - 工具调用历史
- [find_service()](../../services/listing/find-service.md) - 查找服务
- [list_tools()](../finding/list-tools.md) - 列出工具

## 注意事项

1. **调用前提**: 必须先通过 `find_service()` 获取 ServiceProxy 对象
2. **统计范围**: 统计当前服务的所有工具
3. **Agent隔离**: Agent级别只统计该Agent服务的工具

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

