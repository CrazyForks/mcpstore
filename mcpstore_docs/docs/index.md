# 欢迎使用 MCP-Store

## 什么是 MCPStore？

MCPStore 是一个轻量级的 MCP（Model Context Protocol）工具管理库，旨在简化智能体（agents）和链（chains）使用 MCP 工具的配置和管理过程。

## 快速体验



```python
from mcpstore import MCPStore

# 创建 Store 实例
store = MCPStore.setup_store()

# 注册服务
store.for_store().add_service({"name":"mcpstore-wiki","url":"https://mcpstore.wiki/mcp"})

# 调用工具
tools = store.for_store().list_tools()
result = store.for_store().use_tool(tools[0].name,{"query":'hi!'})
print(result)
```

## 两种使用模式

### Store 模式（全局共享）
所有服务在全局范围内共享，适合单一应用场景。

### Agent 模式（独立隔离）
每个 Agent 拥有独立的服务空间，适合多智能体场景。

## 下一步

- [快速上手](getting-started/quickstart.md) - 30秒快速上手 MCPStore
- [服务管理](services/overview.md) - 了解如何管理 MCP 服务
- [工具管理](tools/overview.md) - 学习如何使用工具

---

**准备好开始了吗？** 让我们从 [快速上手指南](getting-started/quickstart.md) 开始吧！ 🚀
