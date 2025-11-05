## service_info - 服务详情


如何通过 MCPStore 的 ServiceProxy 获取单个服务的详细信息。

### SDK

同步：
  - `svc.service_info() -> ServiceInfo`

异步：
  - `await svc.service_info_async() -> ServiceInfo`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 无     | -    | 该方法不需要参数。 |

### 返回值

- 类型：`ServiceInfo`
- 说明：服务信息对象，包含标识、连接配置、状态、环境、生命周期元数据与完整配置。

字段概览：

| 字段              | 类型                     | 说明 |
|-------------------|--------------------------|------|
| `name`            | str                      | 服务名称 |
| `client_id`       | str                      | 客户端标识 |
| `status`          | ServiceConnectionState   | 连接状态 |
| `tool_count`      | int                      | 工具数量 |
| `transport_type`  | TransportType            | 传输类型 |
| `url`             | Optional[str]            | 远程服务 URL |
| `command`         | Optional[str]            | 本地服务命令 |
| `args`            | Optional[List[str]]      | 命令参数 |
| `working_dir`     | Optional[str]            | 工作目录 |
| `env`             | Optional[Dict[str, str]] | 环境变量 |
| `keep_alive`      | bool                     | 是否保持连接 |
| `state_metadata`  | ServiceStateMetadata     | 状态元数据（可为空） |
| `config`          | Dict[str, Any]           | 完整原始配置 |


### 视角
在通过 `find_service()` 获取的 `ServiceProxy` 上调用。支持 Store 级与 Agent 级：
`svc = store.for_store().find_service(name)` 或 `svc = store.for_agent(agent_id).find_service(name)`。


### 使用示例

Store 级获取服务详情：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

info = svc.service_info()
print(f"服务名称: {info.name}")
print(f"服务状态: {info.status}")
print(f"工具数量: {info.tool_count}")
print(f"传输类型: {info.transport_type}")
if info.url:
    print(f"服务URL: {info.url}")
```

Agent 级获取服务详情：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_agent("agent1").wait_service("weather")
svc = store.for_agent("agent1").find_service("weather")

info = svc.service_info()
print(f"名称: {info.name}")
print(f"状态: {info.status}")
print(f"客户端ID: {info.client_id}")
```

检查服务配置信息：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "calculator": {
            "command": "python",
            "args": ["calculator.py"],
            "env": {"DEBUG": "true"},
            "working_dir": "/workspace"
        }
    }
})

store.for_store().wait_service("calculator")
svc = store.for_store().find_service("calculator")

info = svc.service_info()
print(f"命令: {info.command}")
print(f"参数: {info.args}")
print(f"环境变量: {info.env}")
print(f"工作目录: {info.working_dir}")
```

查看状态元数据：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

info = svc.service_info()
if info.state_metadata:
    metadata = info.state_metadata
    print(f"响应时间: {metadata.response_time}")
    print(f"连续成功: {metadata.consecutive_successes}")
    print(f"连续失败: {metadata.consecutive_failures}")
    print(f"最后成功时间: {metadata.last_success_time}")
    print(f"最后失败时间: {metadata.last_failure_time}")
```


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 获取服务状态     | `svc.service_status()` |
| 刷新内容         | `svc.refresh_content()` |
| 列出工具         | `svc.list_tools()` |
| 重启服务         | `svc.restart_service()` |
| Store 获取详情   | `store.for_store().get_service_info(name)` |
| 查找服务         | `store.for_store().find_service(name)` |


### 使用场景

- 在调用前快速了解服务的当前配置与状态。
- 在更新或重启之后核验服务是否达成目标状态与配置。
- 展示层需要渲染服务详情页或调试信息时使用。


### 注意事项

- 调用前提：请先通过 `find_service()` 获取 `ServiceProxy` 对象。
- 信息实时性：返回的是当前已知信息，必要时结合状态刷新能力。
- Agent 隔离：Agent 级别只能看到该 Agent 的服务信息。
- 判空处理：`state_metadata` 可能为空，使用前请判断。

