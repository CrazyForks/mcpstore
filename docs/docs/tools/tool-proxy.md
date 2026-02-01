## ToolProxy - 工具代理

ToolProxy 是 MCPStore 中的工具代理对象，提供工具级别的操作方法。

### 概述

ToolProxy 类似于 ServiceProxy，是通过 `find_tool()` 返回的代理对象，封装了对单个工具的所有操作。

### 获取 ToolProxy

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_store().wait_service("weather")

# 获取 ToolProxy
tool_proxy = store.for_store().find_tool("get_current_weather")
```

### ToolProxy 提供的方法

#### 工具详情查询

```python
# 获取工具详细信息
info = tool_proxy.tool_info()
print(f"工具名称: {info['name']}")
print(f"工具描述: {info['description']}")
print(f"所属服务: {info['service_name']}")

# 获取工具标签
tags = tool_proxy.tool_tags()
print(f"工具标签: {tags}")
```

#### 工具调用

```python
# 调用工具
result = tool_proxy.call_tool({"query": "北京天气"})
print(f"调用结果: {result.text_output}")
print(f"是否出错: {result.is_error}")
```

### Store vs Agent 模式

#### Store 模式
```python
# Store 级别的 ToolProxy
tool_proxy = store.for_store().find_tool("get_weather")

# 适用于全局共享的工具操作
info = tool_proxy.tool_info()
```

#### Agent 模式
```python
# Agent 级别的 ToolProxy
tool_proxy = store.for_agent("agent1").find_tool("get_weather")

# 适用于 Agent 独立的工具操作
info = tool_proxy.tool_info()
```

### 完整示例

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

# 获取 ToolProxy
tool_proxy = store.for_store().find_tool("get_current_weather")

print("=== 工具信息 ===")
info = tool_proxy.tool_info()
print(f"名称: {info['name']}")
print(f"描述: {info['description']}")

print("\n=== 工具标签 ===")
tags = tool_proxy.tool_tags()
print(f"标签: {tags}")

print("\n=== 调用工具 ===")
result = tool_proxy.call_tool({"query": "北京"})
print(f"结果: {result.text_output}")
```

### 相关文档

- [find_tool()](find-tool.md) - 查找工具获取 ToolProxy
- [tool_info()](tool-info.md) - 工具详情方法
- [call_tool()](call-tool.md) - 工具调用方法

### 设计理念

ToolProxy 的设计理念与 ServiceProxy 一致：

- 封装性: 将工具相关的所有操作封装在一个对象中
- 便捷性: 提供链式调用和简洁的 API
- 一致性: 与 ServiceProxy 保持相同的设计模式
- 隔离性: 支持 Store/Agent 双模式的工具管理

