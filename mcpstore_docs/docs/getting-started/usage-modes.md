# 两种使用模式

MCPStore 提供两种不同的使用模式，以适应不同的应用场景。

## Store 模式（全局共享）

### 概述
Store 模式下，所有服务在全局范围内共享，适合单一应用场景。

### 使用方式

```python
from mcpstore import MCPStore
# 实例化一个store
store = MCPStore.setup_store()
# 为你的store添加服务
store.for_store().add_service({"name":"mcpstore-wiki","url":"https://mcpstore.wiki/mcp"})
```

## Agent 模式（独立隔离）

### 概述
Agent 模式下，每个 Agent 拥有独立的服务空间，适合多智能体场景。

### 使用方式

```python
# 初始化Store
store = MCPStore.setup_store()

# 为“知识管理Agent”分配专用的Wiki工具
# 该操作在"knowledge" agent的私有上下文中进行
agent_id1 = "my-knowledge-agent"
knowledge_agent_context = store.for_agent(agent_id1).add_service(
    {"name": "mcpstore-wiki", "url": "http://mcpstore.wiki/mcp"}
)

# 为“开发支持Agent”分配专用的开发工具
# 该操作在"development" agent的私有上下文中进行
agent_id2 = "my-development-agent"
dev_agent_context = store.for_agent(agent_id2).add_service(
    {"name": "mcpstore-demo", "url": "http://mcpstore.wiki/mcp"}
)

# 各Agent的工具集完全隔离，互不影响
knowledge_tools = store.for_agent(agent_id1).list_tools()
dev_tools = store.for_agent(agent_id2).list_tools()
```


## 下一步

现在你已经了解了基本概念，让我们深入学习 [服务管理](../services/overview.md)。
