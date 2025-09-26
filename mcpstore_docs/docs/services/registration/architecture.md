# 服务注册架构

本文档详细介绍 MCPStore 服务注册的内部架构和工作原理。

## 🏗️ 整体架构图

```mermaid
graph TB
    subgraph "用户层"
        User[用户代码]
        Context[MCPStoreContext]
    end
    
    subgraph "业务逻辑层"
        ServiceOps[ServiceOperations]
        ConfigProcessor[ConfigProcessor]
        WaitStrategy[WaitStrategy]
    end
    
    subgraph "核心管理层"
        Registry[ServiceRegistry]
        Orchestrator[MCPOrchestrator]
        Lifecycle[LifecycleManager]
    end
    
    subgraph "配置管理层"
        MCPConfig[MCPConfig]
        AgentClients[agent_clients.json]
        ClientServices[client_services.json]
    end
    
    subgraph "协议层"
        FastMCP[FastMCP Client]
        MCPProtocol[MCP Protocol]
    end
    
    subgraph "外部服务"
        RemoteService[远程 MCP 服务]
        LocalService[本地 MCP 服务]
    end
    
    %% 数据流
    User --> Context
    Context --> ServiceOps
    ServiceOps --> ConfigProcessor
    ServiceOps --> Registry
    ServiceOps --> MCPConfig
    
    ConfigProcessor --> Orchestrator
    Registry --> Lifecycle
    Orchestrator --> FastMCP
    
    MCPConfig --> AgentClients
    MCPConfig --> ClientServices
    
    FastMCP --> MCPProtocol
    MCPProtocol --> RemoteService
    MCPProtocol --> LocalService
    
    Lifecycle --> Registry
    WaitStrategy --> ServiceOps
    
    %% 样式
    classDef user fill:#e3f2fd
    classDef business fill:#f3e5f5
    classDef core fill:#e8f5e8
    classDef config fill:#fff3e0
    classDef protocol fill:#fce4ec
    classDef external fill:#f1f8e9
    
    class User,Context user
    class ServiceOps,ConfigProcessor,WaitStrategy business
    class Registry,Orchestrator,Lifecycle core
    class MCPConfig,AgentClients,ClientServices config
    class FastMCP,MCPProtocol protocol
    class RemoteService,LocalService external
```

## 🔄 三阶段注册流程

### 阶段1: 立即缓存操作 (<100ms)

```mermaid
sequenceDiagram
    participant User as 用户
    participant ServiceOps as ServiceOperations
    participant ConfigProcessor as ConfigProcessor
    participant Registry as ServiceRegistry
    
    User->>ServiceOps: add_service(config)
    ServiceOps->>ConfigProcessor: preprocess_config(config)
    ConfigProcessor-->>ServiceOps: validated_config
    
    ServiceOps->>Registry: add_to_cache(service_info)
    ServiceOps->>Registry: update_agent_client_mapping()
    ServiceOps->>Registry: add_service_client_mapping()
    
    Registry-->>ServiceOps: cache_updated
    ServiceOps-->>User: MCPStoreContext (立即返回)
    
    Note over User: 用户可以立即进行链式调用
```

### 阶段2: 异步配置持久化

```mermaid
sequenceDiagram
    participant ServiceOps as ServiceOperations
    participant MCPConfig as MCPConfig
    participant AgentClients as agent_clients.json
    participant ClientServices as client_services.json
    
    Note over ServiceOps: 异步任务开始
    
    ServiceOps->>MCPConfig: save_config_async(config)
    MCPConfig->>AgentClients: update_agent_mapping()
    MCPConfig->>ClientServices: update_client_config()
    
    AgentClients-->>MCPConfig: mapping_updated
    ClientServices-->>MCPConfig: config_updated
    MCPConfig-->>ServiceOps: persistence_complete
    
    Note over ServiceOps: 配置持久化完成
```

### 阶段3: 异步连接建立

```mermaid
sequenceDiagram
    participant ServiceOps as ServiceOperations
    participant Orchestrator as MCPOrchestrator
    participant Lifecycle as LifecycleManager
    participant FastMCP as FastMCP Client
    participant Registry as ServiceRegistry
    participant Service as MCP Service
    
    Note over ServiceOps: 异步连接任务开始
    
    ServiceOps->>Orchestrator: create_client_async(config)
    Orchestrator->>FastMCP: create_mcp_client(config)
    FastMCP-->>Orchestrator: client_instance
    
    Orchestrator->>Lifecycle: initialize_service(service_name)
    Lifecycle->>Registry: set_service_state(INITIALIZING)
    
    Lifecycle->>FastMCP: connect_and_list_tools()
    FastMCP->>Service: MCP Connection Request
    Service-->>FastMCP: Connection + Tools List
    
    FastMCP-->>Lifecycle: tools_list
    Lifecycle->>Registry: update_tools_cache(tools)
    Lifecycle->>Registry: set_service_state(HEALTHY)
    
    Note over Registry: 服务完全就绪
```

## 🧩 核心组件详解

### ServiceOperations

**职责**: 服务操作的业务逻辑层
- 处理用户输入的各种配置格式
- 协调三阶段注册流程
- 管理等待策略
- 提供链式调用支持

**关键方法**:
- `add_service()` - 主要注册方法
- `_preprocess_service_config()` - 配置预处理
- `_add_service_cache_first()` - 缓存优先流程
- `_wait_for_services_ready()` - 等待服务就绪

### ConfigProcessor

**职责**: 配置格式转换和验证
- 将用户配置转换为 FastMCP 兼容格式
- 自动推断 transport 类型
- 验证配置完整性
- 清理非标准字段

**处理流程**:
```mermaid
graph LR
    A[用户配置] --> B[格式检测]
    B --> C[字段验证]
    C --> D[Transport推断]
    D --> E[字段清理]
    E --> F[FastMCP配置]
```

### ServiceRegistry

**职责**: 服务状态和缓存管理
- 维护服务注册表
- 管理 Agent-Client 映射
- 缓存工具列表
- 跟踪服务状态

**数据结构**:
```python
{
    "sessions": {
        "agent_id": {
            "service_name": session_object
        }
    },
    "tool_cache": {
        "agent_id": {
            "tool_name": tool_definition
        }
    },
    "service_states": {
        "agent_id": {
            "service_name": ServiceConnectionState
        }
    }
}
```

### LifecycleManager

**职责**: 服务生命周期管理
- 管理服务状态转换
- 执行健康检查
- 处理重连逻辑
- 监控服务健康

**状态机**:
```mermaid
stateDiagram-v2
    [*] --> INITIALIZING
    INITIALIZING --> HEALTHY : 连接成功
    INITIALIZING --> UNREACHABLE : 连接失败
    HEALTHY --> WARNING : 偶发失败
    HEALTHY --> RECONNECTING : 连续失败
    WARNING --> HEALTHY : 恢复正常
    WARNING --> RECONNECTING : 持续失败
    RECONNECTING --> HEALTHY : 重连成功
    RECONNECTING --> UNREACHABLE : 重连失败
    UNREACHABLE --> RECONNECTING : 重试重连
```

## 🔧 配置处理流程

### 输入格式识别

```mermaid
graph TD
    A[用户输入] --> B{输入类型?}
    B -->|None| C[Store全量注册]
    B -->|Dict| D{包含mcpServers?}
    B -->|List| E{元素类型?}
    B -->|String| F[JSON文件路径]
    
    D -->|Yes| G[MCPConfig格式]
    D -->|No| H[单服务格式]
    
    E -->|String| I[服务名称列表]
    E -->|Dict| J[批量服务配置]
    
    C --> K[处理流程]
    G --> K
    H --> K
    I --> K
    J --> K
    F --> K
```

### 配置验证流程

```mermaid
graph TD
    A[原始配置] --> B[必需字段检查]
    B --> C{name字段存在?}
    C -->|No| D[抛出错误]
    C -->|Yes| E[连接方式检查]
    
    E --> F{url和command?}
    F -->|Both| G[抛出冲突错误]
    F -->|Neither| H[抛出缺失错误]
    F -->|One| I[Transport推断]
    
    I --> J[字段清理]
    J --> K[生成FastMCP配置]
```

## 📊 性能优化策略

### 缓存优先架构

**优势**:
- 用户操作响应时间 <100ms
- 支持立即链式调用
- 异步处理不阻塞用户

**实现**:
```python
async def _add_service_cache_first(self, config, agent_id, wait):
    # 第1阶段：立即缓存 (<100ms)
    cache_results = await self._add_to_cache_immediately(config)
    
    # 立即返回，支持链式调用
    context = self._return_context()
    
    # 第2阶段：异步持久化
    asyncio.create_task(self._persist_config_async(config))
    
    # 第3阶段：异步连接
    asyncio.create_task(self._connect_service_async(config))
    
    return context
```

### 并发处理

**批量注册优化**:
```python
# 并发处理多个服务
tasks = []
for service_config in services:
    task = asyncio.create_task(
        self._process_single_service(service_config)
    )
    tasks.append(task)

results = await asyncio.gather(*tasks, return_exceptions=True)
```

**连接等待优化**:
```python
# 并发等待多个服务就绪
async def wait_for_services(service_names, timeout):
    tasks = [
        wait_single_service(name, timeout) 
        for name in service_names
    ]
    return await asyncio.gather(*tasks)
```

## 🛡️ 错误处理机制

### 分层错误处理

```mermaid
graph TD
    A[用户调用] --> B[配置验证层]
    B --> C[业务逻辑层]
    C --> D[协议层]
    D --> E[网络层]
    
    B --> F[InvalidConfigError]
    C --> G[ServiceNotFoundError]
    D --> H[ProtocolError]
    E --> I[ConnectionError]
    
    F --> J[用户友好错误]
    G --> J
    H --> J
    I --> J
```

### 错误恢复策略

**配置错误**:
- 提供详细的错误信息
- 建议正确的配置格式
- 支持配置验证预检

**连接错误**:
- 自动重试机制
- 智能退避策略
- 状态降级处理

**部分失败处理**:
- 批量操作中的部分成功
- 详细的失败报告
- 支持重试失败的服务

## 📈 监控和观测

### 关键指标

- **注册延迟**: 第1阶段响应时间
- **连接成功率**: 服务连接成功比例
- **状态转换**: 服务状态变化统计
- **错误率**: 各类错误的发生频率

### 日志记录

```python
# 结构化日志
logger.info("🔄 [ADD_SERVICE] 开始注册服务", extra={
    "source": source,
    "config_type": type(config).__name__,
    "context_type": self._context_type.name,
    "agent_id": agent_id
})
```

## 🔗 相关文档

- [add_service() 完整指南](add-service.md) - 详细使用文档
- [配置格式速查表](config-formats.md) - 配置格式参考
- [服务生命周期](../lifecycle/service-lifecycle.md) - 生命周期管理
- [错误处理指南](../../advanced/error-handling.md) - 错误处理最佳实践

## 🎯 下一步

- 深入了解 [服务生命周期管理](../lifecycle/service-lifecycle.md)
- 学习 [监控和调试](../../advanced/monitoring.md)
- 掌握 [性能优化](../../advanced/performance.md)
