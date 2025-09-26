# list_services() - 服务列表查询

MCPStore 的 `list_services()` 方法提供完整的服务列表查询功能，支持 **Store/Agent 双模式**，返回详细的 `ServiceInfo` 对象，包含服务状态、生命周期信息和配置详情。

## 🎯 方法签名

### 同步版本

```python
def list_services(self) -> List[ServiceInfo]
```

### 异步版本

```python
async def list_services_async(self) -> List[ServiceInfo]
```

## 📊 ServiceInfo 完整模型

基于真实代码分析，`ServiceInfo` 包含以下完整属性：

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

### ServiceStateMetadata 详细信息

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

## 🤖 Agent 模式支持

### 支持状态
- ✅ **完全支持** - `list_services()` 在 Agent 模式下完全可用

### Agent 模式调用
```python
# Agent 模式调用
agent_services = store.for_agent("research_agent").list_services()

# 对比 Store 模式调用
store_services = store.for_store().list_services()
```

### 模式差异说明
- **Store 模式**: 返回所有全局注册的服务，包括带后缀的 Agent 服务（如 `weather-apibyagent1`）
- **Agent 模式**: 只返回当前 Agent 的服务，自动转换为本地名称（隐藏后缀）
- **主要区别**: Agent 模式提供完全隔离的服务视图，Agent 只看到原始服务名

### 返回值对比

#### Store 模式返回示例
```python
[
    ServiceInfo(name="weather-api", status="healthy", client_id="global_agent_store:weather-api"),
    ServiceInfo(name="maps-apibyagent1", status="healthy", client_id="agent1:maps-api"),
    ServiceInfo(name="calculator-apibyagent2", status="warning", client_id="agent2:calculator-api")
]
```

#### Agent 模式返回示例
```python
# Agent "agent1" 的视图
[
    ServiceInfo(name="weather-api", status="healthy", client_id="agent1:weather-api"),  # 本地名称
    ServiceInfo(name="maps-api", status="healthy", client_id="agent1:maps-api")        # 本地名称
]
```

### 使用建议
- **Agent 开发**: 推荐使用 Agent 模式，获得干净的服务视图
- **系统管理**: 使用 Store 模式，查看所有服务的全局状态
- **服务隔离**: Agent 模式确保不同 Agent 之间的服务完全隔离

## 🎭 上下文模式详解

### 🏪 Store 模式特点

```python
store.for_store().list_services()
```

**核心特点**:
- ✅ 返回所有全局注册的服务
- ✅ 包括带后缀的 Agent 服务
- ✅ 显示完整的服务名称和客户端ID
- ✅ 跨上下文的服务管理视图

### 🤖 Agent 模式特点

```python
store.for_agent(agent_id).list_services()
```

**核心特点**:
- ✅ 只返回当前 Agent 的服务
- ✅ 自动转换为本地名称
- ✅ 完全隔离的服务视图
- ✅ 透明的名称映射机制

## 🚀 使用示例

### 基础服务列表查询

```python
from mcpstore import MCPStore

def basic_service_listing():
    """基础服务列表查询"""
    store = MCPStore.setup_store()
    
    # 获取 Store 级别的服务列表
    services = store.for_store().list_services()
    
    print(f"📋 总共有 {len(services)} 个服务:")
    for service in services:
        status_icon = {
            "healthy": "✅",
            "warning": "⚠️",
            "reconnecting": "🔄",
            "unreachable": "❌",
            "initializing": "🔧"
        }.get(service.status, "❓")
        
        print(f"  {status_icon} {service.name}")
        print(f"     状态: {service.status}")
        print(f"     类型: {'远程' if service.url else '本地'}")
        print(f"     工具: {service.tool_count} 个")
        print()

# 使用
basic_service_listing()
```

### Agent 级别服务列表

```python
def agent_service_listing():
    """Agent 级别服务列表查询"""
    store = MCPStore.setup_store()
    
    agent_id = "research_agent"
    
    # 获取特定 Agent 的服务列表
    agent_services = store.for_agent(agent_id).list_services()
    
    print(f"🤖 Agent '{agent_id}' 有 {len(agent_services)} 个服务:")
    for service in agent_services:
        print(f"  📦 {service.name}")
        print(f"     状态: {service.status}")
        print(f"     客户端ID: {service.client_id}")
        
        # 显示生命周期信息
        if service.state_metadata:
            metadata = service.state_metadata
            print(f"     连续成功: {metadata.consecutive_successes}")
            print(f"     连续失败: {metadata.consecutive_failures}")
            if metadata.last_ping_time:
                print(f"     最后检查: {metadata.last_ping_time}")
        print()

# 使用
agent_service_listing()
```

### 详细服务信息展示

```python
def detailed_service_info():
    """详细服务信息展示"""
    store = MCPStore.setup_store()
    
    services = store.for_store().list_services()
    
    print("📊 详细服务信息报告")
    print("=" * 50)
    
    for service in services:
        print(f"🔸 服务名称: {service.name}")
        print(f"   状态: {service.status}")
        print(f"   传输类型: {service.transport_type}")
        print(f"   工具数量: {service.tool_count}")
        
        # 连接信息
        if service.url:
            print(f"   服务URL: {service.url}")
        elif service.command:
            print(f"   启动命令: {service.command}")
            if service.args:
                print(f"   命令参数: {' '.join(service.args)}")
        
        # 环境配置
        if service.working_dir:
            print(f"   工作目录: {service.working_dir}")
        if service.env:
            print(f"   环境变量: {len(service.env)} 个")
        
        # 生命周期信息
        if service.state_metadata:
            metadata = service.state_metadata
            print(f"   响应时间: {metadata.response_time}ms")
            print(f"   重连次数: {metadata.reconnect_attempts}")
            if metadata.error_message:
                print(f"   错误信息: {metadata.error_message}")
        
        print(f"   客户端ID: {service.client_id}")
        print("-" * 30)

# 使用
detailed_service_info()
```

### 服务状态统计

```python
def service_statistics():
    """服务状态统计"""
    store = MCPStore.setup_store()
    
    services = store.for_store().list_services()
    
    # 统计各种状态
    status_counts = {}
    transport_counts = {}
    total_tools = 0
    
    for service in services:
        # 状态统计
        status = service.status
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # 传输类型统计
        transport = service.transport_type
        transport_counts[transport] = transport_counts.get(transport, 0) + 1
        
        # 工具总数
        total_tools += service.tool_count
    
    print("📈 服务统计报告")
    print("=" * 30)
    print(f"总服务数: {len(services)}")
    print(f"总工具数: {total_tools}")
    print()
    
    print("状态分布:")
    for status, count in status_counts.items():
        percentage = count / len(services) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")
    print()
    
    print("传输类型分布:")
    for transport, count in transport_counts.items():
        percentage = count / len(services) * 100
        print(f"  {transport}: {count} ({percentage:.1f}%)")

# 使用
service_statistics()
```

### 异步服务列表查询

```python
import asyncio

async def async_service_listing():
    """异步服务列表查询"""
    store = MCPStore.setup_store()
    
    # 异步获取服务列表
    services = await store.for_store().list_services_async()
    
    print(f"🔄 异步获取到 {len(services)} 个服务")
    
    # 并发获取多个 Agent 的服务
    agent_ids = ["agent1", "agent2", "agent3"]
    
    tasks = [
        store.for_agent(agent_id).list_services_async()
        for agent_id in agent_ids
    ]
    
    agent_services_list = await asyncio.gather(*tasks)
    
    for i, agent_services in enumerate(agent_services_list):
        agent_id = agent_ids[i]
        print(f"🤖 Agent {agent_id}: {len(agent_services)} 个服务")

# 使用
# asyncio.run(async_service_listing())
```

## 🔍 高级查询功能

### 按状态筛选服务

```python
def filter_services_by_status():
    """按状态筛选服务"""
    store = MCPStore.setup_store()

    services = store.for_store().list_services()

    # 筛选健康的服务
    healthy_services = [s for s in services if s.status == "healthy"]
    print(f"✅ 健康服务: {len(healthy_services)} 个")

    # 筛选有问题的服务
    problem_services = [s for s in services if s.status in ["warning", "reconnecting", "unreachable"]]
    print(f"⚠️ 问题服务: {len(problem_services)} 个")

    for service in problem_services:
        print(f"  - {service.name}: {service.status}")
        if service.state_metadata and service.state_metadata.error_message:
            print(f"    错误: {service.state_metadata.error_message}")

# 使用
filter_services_by_status()
```

### 按传输类型分组

```python
def group_services_by_transport():
    """按传输类型分组服务"""
    store = MCPStore.setup_store()

    services = store.for_store().list_services()

    # 按传输类型分组
    transport_groups = {}
    for service in services:
        transport = service.transport_type
        if transport not in transport_groups:
            transport_groups[transport] = []
        transport_groups[transport].append(service)

    print("📡 按传输类型分组:")
    for transport, group_services in transport_groups.items():
        print(f"\n{transport} ({len(group_services)} 个服务):")
        for service in group_services:
            print(f"  - {service.name}: {service.status}")

# 使用
group_services_by_transport()
```

### 服务性能分析

```python
def analyze_service_performance():
    """服务性能分析"""
    store = MCPStore.setup_store()

    services = store.for_store().list_services()

    performance_data = []

    for service in services:
        if service.state_metadata:
            metadata = service.state_metadata
            performance_data.append({
                'name': service.name,
                'response_time': metadata.response_time or 0,
                'success_rate': metadata.consecutive_successes /
                               (metadata.consecutive_successes + metadata.consecutive_failures + 1) * 100,
                'reconnect_attempts': metadata.reconnect_attempts
            })

    # 按响应时间排序
    performance_data.sort(key=lambda x: x['response_time'])

    print("⚡ 服务性能分析:")
    print(f"{'服务名称':<20} {'响应时间':<10} {'成功率':<10} {'重连次数':<10}")
    print("-" * 60)

    for data in performance_data:
        print(f"{data['name']:<20} {data['response_time']:<10.2f} {data['success_rate']:<10.1f}% {data['reconnect_attempts']:<10}")

# 使用
analyze_service_performance()
```

### 服务对比分析

```python
def compare_store_vs_agent_services():
    """对比 Store 和 Agent 服务"""
    store = MCPStore.setup_store()

    # Store 级别服务
    store_services = store.for_store().list_services()

    # Agent 级别服务
    agent_id = "test_agent"
    agent_services = store.for_agent(agent_id).list_services()

    print("🔍 Store vs Agent 服务对比")
    print("=" * 40)

    print(f"🏪 Store 级别服务 ({len(store_services)} 个):")
    for service in store_services:
        print(f"  - {service.name} ({service.status})")

    print(f"\n🤖 Agent '{agent_id}' 服务 ({len(agent_services)} 个):")
    for service in agent_services:
        print(f"  - {service.name} ({service.status})")

    # 分析隔离效果
    store_names = {s.name for s in store_services}
    agent_names = {s.name for s in agent_services}

    print(f"\n📊 隔离分析:")
    print(f"  Store 独有服务: {store_names - agent_names}")
    print(f"  Agent 独有服务: {agent_names - store_names}")
    print(f"  共同服务: {store_names & agent_names}")

# 使用
compare_store_vs_agent_services()
```

## 📊 API 响应格式

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

## 🎯 性能特点

- **平均耗时**: 0.002秒
- **缓存机制**: 内存缓存，实时更新
- **并发支持**: 支持异步并发查询
- **数据一致性**: 实时反映服务状态

## 🔗 相关文档

- [get_service_info()](get-service-info.md) - 获取单个服务详细信息
- [服务注册](../registration/add-service.md) - 了解服务注册
- [服务生命周期](../lifecycle/service-lifecycle.md) - 理解服务状态
- [工具列表查询](../../tools/listing/list-tools.md) - 获取工具列表

## 🎯 下一步

- 学习 [服务详细信息获取](get-service-info.md)
- 了解 [服务健康检查](../lifecycle/check-services.md)
- 掌握 [工具列表查询](../../tools/listing/list-tools.md)
- 查看 [服务管理操作](../management/service-management.md)
```
