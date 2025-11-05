## get_service_info - 服务信息查询


如何通过 MCPStore 获取单个服务的详细信息（配置、状态、工具列表、连接信息等）。

### SDK

同步：
  - `store.for_store().get_service_info(name) -> Optional[ServiceInfo]`
  - `store.for_agent(id).get_service_info(name) -> Optional[ServiceInfo]`

异步：
  - `await store.for_store().get_service_info_async(name) -> Optional[ServiceInfo]`
  - `await store.for_agent(id).get_service_info_async(name) -> Optional[ServiceInfo]`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `name` | str  | 服务名称。Store 使用完整名称；Agent 使用本地名称。 |

### 返回值

- 类型：`ServiceInfo | None`
- 说明：返回服务信息对象；不存在时返回 `None`。


### 视角
通过 `for_store()` 可查询任意服务（使用完整服务名，如 `weather-apibyagent1`）。
通过 `for_agent(id)` 查询当前 Agent 的服务（使用本地名，如 `weather-api`），名称映射自动处理。


### 使用示例

基础服务信息查询：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

service_name = "weather-api"
service_info = store.for_store().get_service_info(service_name)

if service_info:
    print(f"名称: {service_info.name}")
    print(f"状态: {service_info.status}")
    print(f"工具数: {service_info.tool_count}")
    print(f"客户端ID: {service_info.client_id}")
    if service_info.url:
        print(f"URL: {service_info.url}")
    elif service_info.command:
        print(f"命令: {service_info.command}")
else:
    print("服务不存在")
```

Agent 模式查询：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

agent_id = "agent1"
service_info = store.for_agent(agent_id).get_service_info("weather-api")

if service_info:
    print(f"名称: {service_info.name}")
    print(f"客户端ID: {service_info.client_id}")
    print(f"状态: {service_info.status}")
```

异步版本：
```python
import asyncio
from mcpstore import MCPStore

async def main():
    store = MCPStore.setup_store()
    info = await store.for_store().get_service_info_async("weather-api")
    if info:
        print(info.name, info.status, info.tool_count)

asyncio.run(main())
```

批量查询：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

services = store.for_store().list_services()
for s in services:
    info = store.for_store().get_service_info(s.name)
    if info:
        print(info.name, info.status, info.tool_count)
```


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 列出服务         | `store.for_store().list_services()` |
| 获取服务状态     | `store.for_store().get_service_status(name)` |
| 注册服务         | `store.for_store().add_service(config=..., ...)` |
| 更新服务         | `store.for_store().update_service(name, config)` |
| 增量更新         | `store.for_store().patch_service(name, patch)` |
| 删除服务         | `store.for_store().delete_service(name)` |


### 使用场景

- 检索单个服务的详细信息用于展示或诊断。
- 在更新或重启后验证服务是否达到期望状态。
- 批量巡检时抽取关键指标（状态、工具数、响应信息等）。
- Agent 侧开发时通过本地名称读取服务视图。


### 注意事项

- 名称规则：Store 使用完整名；Agent 使用本地名，系统自动映射。
- 空值检查：返回值可能为 `None`，请做好空值判断。
- 字段可选：URL/命令等字段按服务类型可空，请做条件判断。
- 性能：查询可能触发轻量数据装配，建议批量场景复用 `store` 实例。
- 一致性：若需最新运行态信息，结合 `get_service_status()` 或刷新相关能力使用。
