# 服务列表（list_services）

列出当前上下文可见的服务，支持 Store 全局视角与 Agent 分组视角，返回 `ServiceInfo` 列表。

## 概念与前置
- Store：全局服务仓库，`for_store()` 返回全部已注册服务（参见 [服务管理概览](overview.md)）。
- Agent：逻辑分组，`for_agent(agent_id)` 仅返回该分组的服务，并将带后缀的全局名映射为本地名。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化 Store。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局列表 | `store.for_store().list_services()` | `List[ServiceInfo]` | 同步列出全局服务 |
| Agent 列表 | `store.for_agent("agentA").list_services()` | `List[ServiceInfo]` | 仅列出该 Agent 的服务 |
| 异步形式 | `await store.for_store().list_services_async()` | `List[ServiceInfo]` | 异步列出全局服务 |

## 返回值
- 类型：`List[ServiceInfo]`，每项包含名称、传输/连接信息、状态、工具数、配置等字段。

## 视角
- Store 视角：返回全局注册的所有服务。
- Agent 视角：仅返回该 Agent 名下服务，并映射为本地名。

```python
# Store 视角
store_services = store.for_store().list_services()

# Agent 视角
agent_services = store.for_agent("agent1").list_services()
```

## 标准使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 全局服务列表
services = store.for_store().list_services()
print(f"总服务数: {len(services)}")
for s in services:
    print(f"- {s.name} | 状态: {s.status} | 工具: {s.tool_count}")
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

agent_services = store.for_agent(agent_id).list_services()
print(f"Agent {agent_id} 服务数: {len(agent_services)}")
for s in agent_services:
    print(f"- {s.name} | 状态: {s.status}")
```
