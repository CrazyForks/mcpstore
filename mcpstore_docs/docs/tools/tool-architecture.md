# 工具管理架构

MCPStore 的工具管理系统采用**分层架构设计**，提供完整的工具发现、调用和管理功能，支持 Store/Agent 双模式和智能名称解析机制。

## 🏗️ 整体架构图

```mermaid
graph TB
    subgraph "用户接口层"
        UserAPI[用户API]
        StoreContext[Store上下文]
        AgentContext[Agent上下文]
    end
    
    subgraph "工具管理层"
        ToolManager[工具管理器]
        ToolDiscovery[工具发现器]
        ToolExecutor[工具执行器]
        NameResolver[名称解析器]
    end
    
    subgraph "智能等待系统"
        WaitManager[等待管理器]
        ServiceMonitor[服务监控器]
        TimeoutHandler[超时处理器]
        StateTracker[状态跟踪器]
    end
    
    subgraph "缓存系统"
        ToolCache[工具缓存]
        SchemaCache[Schema缓存]
        NameCache[名称缓存]
        ResultCache[结果缓存]
    end
    
    subgraph "名称映射系统"
        ServiceMapper[服务映射器]
        ToolNameMapper[工具名映射器]
        AgentNamespace[Agent命名空间]
        GlobalNamespace[全局命名空间]
    end
    
    subgraph "执行引擎"
        ParameterProcessor[参数处理器]
        SchemaValidator[Schema验证器]
        ErrorHandler[错误处理器]
        ResultProcessor[结果处理器]
    end
    
    subgraph "底层服务"
        FastMCP[FastMCP客户端]
        MCPServices[MCP服务]
        ServiceRegistry[服务注册表]
    end
    
    %% 用户接口流
    UserAPI --> StoreContext
    UserAPI --> AgentContext
    
    %% 工具管理流
    StoreContext --> ToolManager
    AgentContext --> ToolManager
    
    ToolManager --> ToolDiscovery
    ToolManager --> ToolExecutor
    ToolManager --> NameResolver
    
    %% 智能等待流
    ToolDiscovery --> WaitManager
    WaitManager --> ServiceMonitor
    WaitManager --> TimeoutHandler
    WaitManager --> StateTracker
    
    %% 缓存流
    ToolDiscovery --> ToolCache
    NameResolver --> NameCache
    ToolExecutor --> ResultCache
    
    %% 名称映射流
    NameResolver --> ServiceMapper
    NameResolver --> ToolNameMapper
    AgentContext --> AgentNamespace
    StoreContext --> GlobalNamespace
    
    %% 执行流
    ToolExecutor --> ParameterProcessor
    ToolExecutor --> SchemaValidator
    ToolExecutor --> ErrorHandler
    ToolExecutor --> ResultProcessor
    
    %% 底层服务流
    ToolExecutor --> FastMCP
    ToolDiscovery --> ServiceRegistry
    FastMCP --> MCPServices
    
    %% 样式
    classDef user fill:#e3f2fd
    classDef manager fill:#f3e5f5
    classDef wait fill:#e8f5e8
    classDef cache fill:#fff3e0
    classDef mapper fill:#fce4ec
    classDef executor fill:#f1f8e9
    classDef service fill:#fafafa
    
    class UserAPI,StoreContext,AgentContext user
    class ToolManager,ToolDiscovery,ToolExecutor,NameResolver manager
    class WaitManager,ServiceMonitor,TimeoutHandler,StateTracker wait
    class ToolCache,SchemaCache,NameCache,ResultCache cache
    class ServiceMapper,ToolNameMapper,AgentNamespace,GlobalNamespace mapper
    class ParameterProcessor,SchemaValidator,ErrorHandler,ResultProcessor executor
    class FastMCP,MCPServices,ServiceRegistry service
```

## 🔍 工具发现架构

### 智能等待机制

```mermaid
stateDiagram-v2
    [*] --> CheckServices : 开始工具发现
    
    CheckServices --> HasInitializing : 检查服务状态
    
    HasInitializing --> SkipWait : 无初始化服务
    HasInitializing --> StartWait : 有初始化服务
    
    StartWait --> RemoteWait : 远程服务
    StartWait --> LocalWait : 本地服务
    
    RemoteWait --> StatusCheck : 最多1.5秒
    LocalWait --> StatusCheck : 最多5秒
    
    StatusCheck --> AllReady : 所有服务就绪
    StatusCheck --> Timeout : 等待超时
    StatusCheck --> StatusCheck : 继续等待
    
    AllReady --> GetTools : 获取工具列表
    Timeout --> GetTools : 获取当前可用工具
    SkipWait --> GetTools : 直接获取工具
    
    GetTools --> [*] : 返回工具列表
    
    note right of RemoteWait
        远程服务等待策略:
        - 最大等待时间: 1.5秒
        - 检查间隔: 0.1秒
        - 快速失败机制
    end note
    
    note right of LocalWait
        本地服务等待策略:
        - 最大等待时间: 5秒
        - 检查间隔: 0.1秒
        - 启动时间容忍
    end note
```

### 工具缓存策略

```mermaid
graph TB
    subgraph "缓存层次"
        L1Cache[L1: 内存缓存<br/>工具列表]
        L2Cache[L2: Schema缓存<br/>工具定义]
        L3Cache[L3: 名称缓存<br/>解析结果]
    end
    
    subgraph "缓存更新策略"
        ServiceChange[服务状态变化]
        ToolUpdate[工具列表更新]
        SchemaChange[Schema变化]
        NameMapping[名称映射变化]
    end
    
    subgraph "缓存失效策略"
        TTL[TTL过期<br/>30分钟]
        Manual[手动刷新]
        AutoRefresh[自动刷新<br/>2小时]
    end
    
    ServiceChange --> L1Cache
    ToolUpdate --> L1Cache
    SchemaChange --> L2Cache
    NameMapping --> L3Cache
    
    TTL --> L1Cache
    TTL --> L2Cache
    TTL --> L3Cache
    
    Manual --> L1Cache
    AutoRefresh --> L1Cache
    
    %% 样式
    classDef cache fill:#e3f2fd
    classDef update fill:#f3e5f5
    classDef invalidate fill:#e8f5e8
    
    class L1Cache,L2Cache,L3Cache cache
    class ServiceChange,ToolUpdate,SchemaChange,NameMapping update
    class TTL,Manual,AutoRefresh invalidate
```

## 🎯 工具调用架构

### 名称解析流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant Context as 上下文
    participant Resolver as 名称解析器
    participant Mapper as 映射器
    participant Cache as 缓存
    participant Registry as 注册表
    
    User->>Context: call_tool("tool_name", args)
    Context->>Resolver: 解析工具名称
    
    Resolver->>Cache: 检查名称缓存
    alt 缓存命中
        Cache-->>Resolver: 返回解析结果
    else 缓存未命中
        Resolver->>Mapper: 执行名称映射
        Mapper->>Registry: 查询工具注册表
        Registry-->>Mapper: 返回匹配结果
        Mapper-->>Resolver: 返回映射结果
        Resolver->>Cache: 更新缓存
    end
    
    Resolver-->>Context: 返回解析后的工具名
    Context->>Context: 执行工具调用
    Context-->>User: 返回执行结果
```

### 参数处理流程

```mermaid
graph TB
    subgraph "参数输入"
        DictArgs[字典参数]
        JSONArgs[JSON字符串]
        NoArgs[无参数]
        KwargsArgs[关键字参数]
    end
    
    subgraph "参数处理器"
        TypeDetector[类型检测器]
        JSONParser[JSON解析器]
        Validator[参数验证器]
        Normalizer[参数标准化器]
    end
    
    subgraph "Schema验证"
        SchemaLoader[Schema加载器]
        TypeChecker[类型检查器]
        RequiredChecker[必需参数检查器]
        FormatValidator[格式验证器]
    end
    
    subgraph "输出"
        ValidatedArgs[验证后参数]
        ErrorReport[错误报告]
    end
    
    DictArgs --> TypeDetector
    JSONArgs --> JSONParser
    NoArgs --> TypeDetector
    KwargsArgs --> TypeDetector
    
    TypeDetector --> Validator
    JSONParser --> Validator
    
    Validator --> SchemaLoader
    Validator --> Normalizer
    
    SchemaLoader --> TypeChecker
    SchemaLoader --> RequiredChecker
    SchemaLoader --> FormatValidator
    
    TypeChecker --> ValidatedArgs
    RequiredChecker --> ValidatedArgs
    FormatValidator --> ValidatedArgs
    
    TypeChecker --> ErrorReport
    RequiredChecker --> ErrorReport
    FormatValidator --> ErrorReport
    
    Normalizer --> ValidatedArgs
    
    %% 样式
    classDef input fill:#e3f2fd
    classDef processor fill:#f3e5f5
    classDef validator fill:#e8f5e8
    classDef output fill:#fff3e0
    
    class DictArgs,JSONArgs,NoArgs,KwargsArgs input
    class TypeDetector,JSONParser,Validator,Normalizer processor
    class SchemaLoader,TypeChecker,RequiredChecker,FormatValidator validator
    class ValidatedArgs,ErrorReport output
```

## 🎭 双模式架构

### Store 模式架构

```mermaid
graph TB
    subgraph "Store模式"
        StoreAPI[Store API]
        GlobalNamespace[全局命名空间]
        AllServices[所有服务]
        AllTools[所有工具]
    end
    
    subgraph "工具访问"
        FullToolNames[完整工具名称<br/>service_tool]
        ServicePrefixes[服务前缀<br/>service-name_tool]
        CrossService[跨服务调用]
    end
    
    subgraph "权限控制"
        GlobalAccess[全局访问权限]
        AdminOperations[管理员操作]
        SystemTools[系统工具]
    end
    
    StoreAPI --> GlobalNamespace
    GlobalNamespace --> AllServices
    AllServices --> AllTools
    
    AllTools --> FullToolNames
    AllTools --> ServicePrefixes
    AllTools --> CrossService
    
    GlobalNamespace --> GlobalAccess
    GlobalAccess --> AdminOperations
    GlobalAccess --> SystemTools
    
    %% 样式
    classDef store fill:#e3f2fd
    classDef access fill:#f3e5f5
    classDef permission fill:#e8f5e8
    
    class StoreAPI,GlobalNamespace,AllServices,AllTools store
    class FullToolNames,ServicePrefixes,CrossService access
    class GlobalAccess,AdminOperations,SystemTools permission
```

### Agent 模式架构

```mermaid
graph TB
    subgraph "Agent模式"
        AgentAPI[Agent API]
        AgentNamespace[Agent命名空间]
        AgentServices[Agent服务]
        AgentTools[Agent工具]
    end
    
    subgraph "名称映射"
        LocalNames[本地名称<br/>原始工具名]
        NameTranslation[名称转换]
        GlobalMapping[全局映射]
    end
    
    subgraph "隔离机制"
        ServiceIsolation[服务隔离]
        ToolIsolation[工具隔离]
        DataIsolation[数据隔离]
    end
    
    AgentAPI --> AgentNamespace
    AgentNamespace --> AgentServices
    AgentServices --> AgentTools
    
    AgentTools --> LocalNames
    LocalNames --> NameTranslation
    NameTranslation --> GlobalMapping
    
    AgentNamespace --> ServiceIsolation
    ServiceIsolation --> ToolIsolation
    ToolIsolation --> DataIsolation
    
    %% 样式
    classDef agent fill:#f3e5f5
    classDef mapping fill:#e8f5e8
    classDef isolation fill:#fff3e0
    
    class AgentAPI,AgentNamespace,AgentServices,AgentTools agent
    class LocalNames,NameTranslation,GlobalMapping mapping
    class ServiceIsolation,ToolIsolation,DataIsolation isolation
```

## 🔧 错误处理架构

### 错误分类和处理

```mermaid
graph TB
    subgraph "错误类型"
        ToolNotFound[ToolNotFoundError<br/>工具不存在]
        ServiceNotFound[ServiceNotFoundError<br/>服务不存在]
        ParamValidation[ParameterValidationError<br/>参数验证失败]
        Timeout[TimeoutError<br/>执行超时]
        Connection[ConnectionError<br/>连接错误]
        Execution[ExecutionError<br/>执行错误]
    end
    
    subgraph "错误处理策略"
        Retry[重试机制]
        Fallback[降级处理]
        Circuit[熔断器]
        Logging[错误日志]
    end
    
    subgraph "用户反馈"
        ErrorMessage[错误消息]
        Suggestions[修复建议]
        Documentation[文档链接]
        Support[支持信息]
    end
    
    ToolNotFound --> Suggestions
    ServiceNotFound --> Retry
    ParamValidation --> ErrorMessage
    Timeout --> Retry
    Connection --> Circuit
    Execution --> Fallback
    
    Retry --> Logging
    Fallback --> Logging
    Circuit --> Logging
    
    ErrorMessage --> Documentation
    Suggestions --> Documentation
    Documentation --> Support
    
    %% 样式
    classDef error fill:#ffebee
    classDef strategy fill:#e8f5e8
    classDef feedback fill:#e3f2fd
    
    class ToolNotFound,ServiceNotFound,ParamValidation,Timeout,Connection,Execution error
    class Retry,Fallback,Circuit,Logging strategy
    class ErrorMessage,Suggestions,Documentation,Support feedback
```

## 📊 性能优化架构

### 并发处理架构

```mermaid
graph TB
    subgraph "并发层"
        AsyncAPI[异步API]
        ThreadPool[线程池]
        TaskQueue[任务队列]
        ResultAggregator[结果聚合器]
    end
    
    subgraph "负载均衡"
        LoadBalancer[负载均衡器]
        ServicePool[服务池]
        ConnectionPool[连接池]
        ResourceManager[资源管理器]
    end
    
    subgraph "性能监控"
        MetricsCollector[指标收集器]
        PerformanceTracker[性能跟踪器]
        BottleneckDetector[瓶颈检测器]
        OptimizationEngine[优化引擎]
    end
    
    AsyncAPI --> ThreadPool
    ThreadPool --> TaskQueue
    TaskQueue --> ResultAggregator
    
    ThreadPool --> LoadBalancer
    LoadBalancer --> ServicePool
    ServicePool --> ConnectionPool
    ConnectionPool --> ResourceManager
    
    TaskQueue --> MetricsCollector
    MetricsCollector --> PerformanceTracker
    PerformanceTracker --> BottleneckDetector
    BottleneckDetector --> OptimizationEngine
    
    %% 样式
    classDef concurrent fill:#e3f2fd
    classDef balance fill:#f3e5f5
    classDef monitor fill:#e8f5e8
    
    class AsyncAPI,ThreadPool,TaskQueue,ResultAggregator concurrent
    class LoadBalancer,ServicePool,ConnectionPool,ResourceManager balance
    class MetricsCollector,PerformanceTracker,BottleneckDetector,OptimizationEngine monitor
```

## 🔄 数据流架构

### 完整数据流

```mermaid
sequenceDiagram
    participant User as 用户
    participant Context as 上下文
    participant Manager as 工具管理器
    participant Cache as 缓存系统
    participant Resolver as 名称解析器
    participant Executor as 执行器
    participant FastMCP as FastMCP
    participant Service as MCP服务
    
    User->>Context: 调用工具
    Context->>Manager: 处理请求
    
    Manager->>Cache: 检查工具缓存
    alt 缓存命中
        Cache-->>Manager: 返回工具信息
    else 缓存未命中
        Manager->>Resolver: 发现工具
        Resolver-->>Manager: 返回工具列表
        Manager->>Cache: 更新缓存
    end
    
    Manager->>Resolver: 解析工具名称
    Resolver-->>Manager: 返回解析结果
    
    Manager->>Executor: 执行工具
    Executor->>FastMCP: 调用MCP客户端
    FastMCP->>Service: 发送工具请求
    Service-->>FastMCP: 返回执行结果
    FastMCP-->>Executor: 返回结果
    Executor-->>Manager: 处理结果
    Manager-->>Context: 返回最终结果
    Context-->>User: 返回给用户
```

## 🎯 架构特点

### 核心优势

1. **分层设计**: 清晰的架构层次，职责分离
2. **智能等待**: 自动等待服务初始化，确保工具完整性
3. **双模式支持**: Store/Agent 模式完全隔离
4. **名称解析**: 智能的工具名称解析和映射
5. **缓存优化**: 多层缓存机制，提升性能
6. **错误处理**: 完整的错误分类和处理策略
7. **并发支持**: 异步并发执行，提高吞吐量
8. **性能监控**: 实时性能监控和优化

### 扩展性

- **插件化架构**: 支持自定义工具处理器
- **中间件支持**: 可插入自定义中间件
- **协议扩展**: 支持多种MCP协议版本
- **存储后端**: 可配置不同的缓存存储

## 🔗 相关文档

- [工具列表概览](listing/tool-listing-overview.md) - 工具发现机制
- [工具使用概览](usage/tool-usage-overview.md) - 工具调用机制
- [服务生命周期](../services/lifecycle/service-lifecycle.md) - 服务管理
- [最佳实践](../advanced/best-practices.md) - 架构最佳实践

## 🎯 下一步

- 深入了解 [工具列表概览](listing/tool-listing-overview.md)
- 学习 [工具使用概览](usage/tool-usage-overview.md)
- 掌握 [服务管理架构](../services/architecture.md)
- 查看 [性能优化指南](../advanced/performance-optimization.md)
