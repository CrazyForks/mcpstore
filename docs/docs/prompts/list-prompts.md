# list_prompts - Prompt 列表

列出当前上下文可见的 MCP prompts。支持 Store 全局视角与 Agent 分组视角，调用会通过 PyO3 进入 Rust core。

## SDK

同步：
- `store.for_store().list_prompts(service_name=None) -> List[dict]`
- `store.for_agent(id).list_prompts(service_name=None) -> List[dict]`

异步：
- `await store.for_store().list_prompts_async(service_name=None) -> List[dict]`
- `await store.for_agent(id).list_prompts_async(service_name=None) -> List[dict]`

## 参数

| 参数 | 类型 | 默认 | 说明 |
| ---- | ---- | ---- | ---- |
| `service_name` | `Optional[str]` | `None` | 限定某个服务；不传则列出当前视角全部 prompts。 |

## 示例

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

prompts = store.for_store().list_prompts()
for prompt in prompts:
    print(prompt.get("name"), prompt.get("description"))

agent_prompts = store.for_agent("agentA").list_prompts()
```

返回值保持 Rust-backed SDK record 形态，既可以按 dict 读取，也支持常见字段的属性访问。
