# get_info - Store 上下文信息

返回当前 Store/Agent 上下文的轻量摘要。该方法由 Python façade 组合 Rust core 返回的数据，不依赖旧 Python core。

## SDK

同步：
- `store.for_store().get_info() -> dict`
- `store.for_agent(id).get_info() -> dict`

异步：
- `await store.for_store().get_info_async() -> dict`
- `await store.for_agent(id).get_info_async() -> dict`

## 返回字段

| 字段 | 说明 |
| ---- | ---- |
| `context_type` | `store` 或 `agent`。 |
| `agent_id` | Agent 视角下的 ID；Store 视角为 `None`。 |
| `namespace` | 当前 Rust cache namespace。 |
| `backend` | 当前 Rust cache backend。 |
| `service_count` | 当前视角可见服务数量。 |
| `tool_count` | 当前视角可见工具数量。 |

## 示例

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

info = store.for_store().get_info()
print(info.context_type, info.backend, info.service_count)

agent_info = store.for_agent("agentA").get_info()
print(agent_info.agent_id, agent_info.tool_count)
```
