# get_prompt - 获取 Prompt

获取并渲染指定 MCP prompt。支持 Store 全局视角与 Agent 分组视角，调用会通过 PyO3 进入 Rust core。

## SDK

同步：
- `store.for_store().get_prompt(prompt_name, arguments=None, service_name=None) -> dict`
- `store.for_agent(id).get_prompt(prompt_name, arguments=None, service_name=None) -> dict`

异步：
- `await store.for_store().get_prompt_async(prompt_name, arguments=None, service_name=None) -> dict`
- `await store.for_agent(id).get_prompt_async(prompt_name, arguments=None, service_name=None) -> dict`

## 参数

| 参数 | 类型 | 默认 | 说明 |
| ---- | ---- | ---- | ---- |
| `prompt_name` | `str` | 必填 | Prompt 名称。 |
| `arguments` | `Optional[dict]` | `None` | Prompt 参数；Python dict 会通过 PyO3 转入 Rust core。 |
| `service_name` | `Optional[str]` | `None` | 限定服务名；不传时由 Rust core 在当前视角解析。 |

## 示例

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

prompt = store.for_store().get_prompt(
    "summarize",
    {"topic": "Rust-backed Python SDK"},
)
print(prompt.get("messages", prompt))

agent_prompt = store.for_agent("agentA").get_prompt(
    "summarize",
    {"topic": "agent scope"},
)
```

`arguments` 使用 Python 字典，不需要先序列化为 JSON 字符串。
