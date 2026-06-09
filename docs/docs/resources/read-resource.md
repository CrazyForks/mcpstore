# read_resource - 读取资源

读取指定 MCP resource 的内容。支持 Store 全局视角与 Agent 分组视角，调用会通过 PyO3 进入 Rust core。

## SDK

同步：
- `store.for_store().read_resource(uri, service_name=None) -> dict`
- `store.for_agent(id).read_resource(uri, service_name=None) -> dict`

异步：
- `await store.for_store().read_resource_async(uri, service_name=None) -> dict`
- `await store.for_agent(id).read_resource_async(uri, service_name=None) -> dict`

## 参数

| 参数 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |
| `uri` | `str` | 是 | Resource URI。 |
| `service_name` | `Optional[str]` | 否 | 限定服务名；不传时由 Rust core 在当前视角解析。 |

## 示例

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

resource = store.for_store().read_resource("memory://docs/readme")
print(resource.get("contents", resource))

agent_resource = store.for_agent("agentA").read_resource(
    "memory://docs/readme",
    service_name="docs",
)
```

非文本 resource 内容会保留在返回对象中，不会被 Python façade 强制降级为纯文本。
