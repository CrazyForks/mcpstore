## list_services - 服务列表查询

`list_services()` 提供服务列表查询，支持 Store/Agent 双模式，返回 `ServiceInfo` 列表，包含服务状态、生命周期与配置信息。

### SDK

同步：
  - `store.for_store().list_services() -> List[ServiceInfo]`
  - `store.for_agent(id).list_services() -> List[ServiceInfo]`

异步：
  - `await store.for_store().list_services_async() -> List[ServiceInfo]`
  - `await store.for_agent(id).list_services_async() -> List[ServiceInfo]`

### 返回值

返回 `List[ServiceInfo]`。

### ServiceInfo 模型

```python
class ServiceInfo:
    # 基础信息
    name: str                           # 服务名称
    url: Optional[str]                  # 服务URL（远程服务）
    command: Optional[str]              # 启动命令（本地服务）
    args: Optional[List[str]]           # 命令参数

    # 传输和连接
    transport_type: TransportType       # 传输类型
    client_id: Optional[str]            # 客户端ID
    keep_alive: bool                    # 是否保持连接

    # 状态信息
    status: ServiceConnectionState      # 服务连接状态
    tool_count: int                     # 工具数量

    # 环境配置
    working_dir: Optional[str]          # 工作目录
    env: Optional[Dict[str, str]]       # 环境变量
    package_name: Optional[str]         # 包名

    # 生命周期元数据
    state_metadata: Optional[ServiceStateMetadata]  # 状态元数据

    # 配置信息
    config: Optional[Dict[str, Any]]    # 原始配置
```

### ServiceStateMetadata 模型

```python
class ServiceStateMetadata:
    consecutive_failures: int = 0           # 连续失败次数
    consecutive_successes: int = 0          # 连续成功次数
    last_ping_time: Optional[datetime]      # 最后Ping时间
    last_success_time: Optional[datetime]   # 最后成功时间
    last_failure_time: Optional[datetime]   # 最后失败时间
    response_time: Optional[float]          # 响应时间
    error_message: Optional[str]            # 错误消息
    reconnect_attempts: int = 0             # 重连尝试次数
    next_retry_time: Optional[datetime]     # 下次重试时间
    state_entered_time: Optional[datetime]  # 状态进入时间
    disconnect_reason: Optional[str]        # 断开原因
    service_config: Dict[str, Any]          # 服务配置
    service_name: Optional[str]             # 服务名称
    agent_id: Optional[str]                 # Agent ID
    last_health_check: Optional[datetime]   # 最后健康检查
    last_response_time: Optional[float]     # 最后响应时间
```

### 视角

Store 视角返回全局注册的所有服务；Agent 视角仅返回该 Agent 的服务，并将带后缀的全局名映射为本地名。

```python
# Store 视角
store_services = store.for_store().list_services()

# Agent 视角
agent_services = store.for_agent("agent1").list_services()
```

### 示例

基础服务列表查询：
```python
from mcpstore import MCPStore

def basic_service_listing():
    store = MCPStore.setup_store()
    services = store.for_store().list_services()
    print(f"总服务数: {len(services)}")
    for service in services:
        print(f"- {service.name}")
        print(f"  状态: {service.status}")
        print(f"  类型: {'远程' if service.url else '本地'}")
        print(f"  工具: {service.tool_count}")

basic_service_listing()
```

Agent 级别服务列表：
```python
from mcpstore import MCPStore

def agent_service_listing():
    store = MCPStore.setup_store()
    agent_id = "research_agent"
    agent_services = store.for_agent(agent_id).list_services()
    print(f"Agent '{agent_id}' 服务数: {len(agent_services)}")
    for service in agent_services:
        print(f"- {service.name}")
        print(f"  状态: {service.status}")
        print(f"  客户端ID: {service.client_id}")
        if service.state_metadata:
            m = service.state_metadata
            print(f"  连续成功: {m.consecutive_successes}")
            print(f"  连续失败: {m.consecutive_failures}")

agent_service_listing()
```

详细服务信息展示：
```python
from mcpstore import MCPStore

def detailed_service_info():
    store = MCPStore.setup_store()
    services = store.for_store().list_services()
    print("详细服务信息")
    print("=" * 40)
    for service in services:
        print(f"服务: {service.name}")
        print(f"  状态: {service.status}")
        print(f"  传输: {service.transport_type}")
        print(f"  工具: {service.tool_count}")
        if service.url:
            print(f"  URL: {service.url}")
        elif service.command:
            print(f"  命令: {service.command}")
            if service.args:
                print(f"  参数: {' '.join(service.args)}")
        if service.working_dir:
            print(f"  工作目录: {service.working_dir}")
        if service.env:
            print(f"  环境变量: {len(service.env)}")
        if service.state_metadata:
            m = service.state_metadata
            print(f"  响应时间: {m.response_time}ms")
            print(f"  重连次数: {m.reconnect_attempts}")
            if m.error_message:
                print(f"  错误: {m.error_message}")
        print(f"  客户端ID: {service.client_id}")
        print("-" * 30)

detailed_service_info()
```

服务状态统计：
```python
from mcpstore import MCPStore

def service_statistics():
    store = MCPStore.setup_store()
    services = store.for_store().list_services()
    status_counts = {}
    transport_counts = {}
    total_tools = 0
    for service in services:
        status_counts[service.status] = status_counts.get(service.status, 0) + 1
        transport_counts[service.transport_type] = transport_counts.get(service.transport_type, 0) + 1
        total_tools += service.tool_count
    print("服务统计")
    print(f"总服务数: {len(services)}")
    print(f"总工具数: {total_tools}")
    print("状态分布:")
    for k, v in status_counts.items():
        print(f"  {k}: {v}")
    print("传输类型分布:")
    for k, v in transport_counts.items():
        print(f"  {k}: {v}")

service_statistics()
```

异步服务列表查询：
```python
import asyncio
from mcpstore import MCPStore

async def async_service_listing():
    store = MCPStore.setup_store()
    services = await store.for_store().list_services_async()
    print(f"异步服务数: {len(services)}")
    agent_ids = ["agent1", "agent2", "agent3"]
    tasks = [store.for_agent(a).list_services_async() for a in agent_ids]
    agent_lists = await asyncio.gather(*tasks)
    for a, lst in zip(agent_ids, agent_lists):
        print(f"Agent {a}: {len(lst)}")

# asyncio.run(async_service_listing())
```

### 高级用法

按状态筛选：
```python
from mcpstore import MCPStore

def filter_services_by_status():
    store = MCPStore.setup_store()
    services = store.for_store().list_services()
    healthy = [s for s in services if s.status == "healthy"]
    problems = [s for s in services if s.status in ["warning", "reconnecting", "unreachable"]]
    print(f"健康: {len(healthy)}")
    print(f"异常: {len(problems)}")
    for s in problems:
        print(f"- {s.name}: {s.status}")
        if s.state_metadata and s.state_metadata.error_message:
            print(f"  错误: {s.state_metadata.error_message}")

filter_services_by_status()
```

按传输类型分组：
```python
from mcpstore import MCPStore

def group_services_by_transport():
    store = MCPStore.setup_store()
    services = store.for_store().list_services()
    groups = {}
    for s in services:
        groups.setdefault(s.transport_type, []).append(s)
    for transport, items in groups.items():
        print(f"{transport} ({len(items)})")
        for s in items:
            print(f"- {s.name}: {s.status}")

group_services_by_transport()
```

服务性能分析：
```python
from mcpstore import MCPStore

def analyze_service_performance():
    store = MCPStore.setup_store()
    services = store.for_store().list_services()
    data = []
    for s in services:
        if s.state_metadata:
            m = s.state_metadata
            total = m.consecutive_successes + m.consecutive_failures + 1
            data.append({
                "name": s.name,
                "response_time": m.response_time or 0,
                "success_rate": m.consecutive_successes / total * 100,
                "reconnect_attempts": m.reconnect_attempts,
            })
    data.sort(key=lambda x: x["response_time"])
    print("名称            响应时间    成功率      重连次数")
    print("-" * 50)
    for d in data:
        print(f"{d['name']:<16} {d['response_time']:<10.2f} {d['success_rate']:<10.1f} {d['reconnect_attempts']:<10}")

analyze_service_performance()
```

Store 与 Agent 对比：
```python
from mcpstore import MCPStore

def compare_store_vs_agent_services():
    store = MCPStore.setup_store()
    store_services = store.for_store().list_services()
    agent_id = "test_agent"
    agent_services = store.for_agent(agent_id).list_services()
    print("Store 级别服务")
    for s in store_services:
        print(f"- {s.name} ({s.status})")
    print(f"Agent {agent_id} 服务")
    for s in agent_services:
        print(f"- {s.name} ({s.status})")
    store_names = {s.name for s in store_services}
    agent_names = {s.name for s in agent_services}
    print(f"Store 独有: {store_names - agent_names}")
    print(f"Agent 独有: {agent_names - store_names}")
    print(f"共同: {store_names & agent_names}")

compare_store_vs_agent_services()
```

## API 响应格式

### Store API 响应

```json
{
  "success": true,
  "data": [
    {
      "name": "weather-api",
      "status": "healthy",
      "transport": "streamable-http",
      "config": {
        "url": "https://weather.example.com/mcp",
        "headers": {"Authorization": "Bearer token"}
      },
      "client_id": "global_agent_store:weather-api"
    }
  ],
  "message": "Retrieved 1 services for store"
}
```

### Agent API 响应

```json
{
  "success": true,
  "data": [
    {
      "name": "weather-api",
      "status": "healthy",
      "transport": "streamable-http",
      "config": {
        "url": "https://weather.example.com/mcp"
      },
      "client_id": "agent1:weather-api"
    }
  ],
  "message": "Retrieved 1 services for agent 'agent1'"
}
```

### 性能

- 平均耗时：约 0.002 秒
- 缓存机制：内存缓存，实时更新
- 并发支持：支持异步并发查询
- 数据一致性：实时反映服务状态

### 相关文档

- [get_service_info()](get-service-info.md)
- [服务注册](../registration/add-service.md)
- [服务生命周期](../lifecycle/service-lifecycle.md)
- [工具列表查询](../../tools/listing/list-tools.md)

### 你可能想找的方法

| 场景/方法           | 同步方法                                              |
|---------------------|-------------------------------------------------------|
| 获取服务信息        | `store.for_store().get_service_info(name)`            |
| 获取工具列表        | `store.for_store().list_tools(name)`                  |
| 等待服务就绪        | `store.for_store().wait_service(name, status=...)`    |
| 注册服务            | `store.for_store().add_service(config=..., ...)`      |
| 删除服务            | `store.for_store().delete_service(name)`              |
| 更新服务            | `store.for_store().update_service(name, config=...)`  |
