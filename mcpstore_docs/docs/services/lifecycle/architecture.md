# 生命周期管理架构

本文档详细介绍 MCPStore 生命周期管理的内部架构、组件设计和工作原理。

## 🏗️ 整体架构图

```mermaid
graph TB
    subgraph "用户接口层"
        UserAPI[用户API]
        Context[MCPStoreContext]
    end
    
    subgraph "生命周期管理层"
        LifecycleManager[ServiceLifecycleManager<br/>生命周期管理器]
        StateMachine[ServiceStateMachine<br/>状态机]
        HealthManager[HealthManager<br/>健康管理器]
        ReconnectionManager[SmartReconnectionManager<br/>智能重连管理器]
    end
    
    subgraph "状态处理器"
        InitProcessor[InitializingStateProcessor<br/>初始化处理器]
        EventProcessor[StateChangeEventProcessor<br/>事件处理器]
        ContentManager[ContentManager<br/>内容管理器]
    end
    
    subgraph "监控系统"
        HealthCheck[健康检查<br/>30秒间隔]
        ToolsUpdate[工具更新<br/>2小时间隔]
        StateMonitor[状态监控<br/>实时]
        PerformanceTracker[性能跟踪器]
    end
    
    subgraph "数据存储"
        Registry[ServiceRegistry<br/>状态存储]
        Metadata[ServiceStateMetadata<br/>元数据]
        Config[LifecycleConfig<br/>配置]
        HealthHistory[健康历史记录]
    end
    
    subgraph "外部接口"
        Orchestrator[MCPOrchestrator<br/>编排器]
        FastMCP[FastMCP Client<br/>MCP客户端]
        Services[MCP Services<br/>外部服务]
    end
    
    %% 核心流程
    UserAPI --> Context
    Context --> LifecycleManager
    
    LifecycleManager --> StateMachine
    LifecycleManager --> HealthManager
    LifecycleManager --> ReconnectionManager
    
    StateMachine --> InitProcessor
    StateMachine --> EventProcessor
    
    HealthManager --> HealthCheck
    HealthCheck --> StateMonitor
    ToolsUpdate --> ContentManager
    StateMonitor --> PerformanceTracker
    
    %% 数据流
    LifecycleManager --> Registry
    Registry --> Metadata
    Config --> StateMachine
    HealthManager --> HealthHistory
    
    %% 外部交互
    LifecycleManager --> Orchestrator
    Orchestrator --> FastMCP
    FastMCP --> Services
    
    %% 反馈循环
    Services -.->|健康状态| HealthCheck
    StateMonitor -.->|状态变化| StateMachine
    ReconnectionManager -.->|重连触发| Orchestrator
    PerformanceTracker -.->|性能数据| Registry
    
    %% 样式
    classDef user fill:#e3f2fd
    classDef lifecycle fill:#f3e5f5
    classDef processor fill:#e8f5e8
    classDef monitor fill:#fff3e0
    classDef storage fill:#fce4ec
    classDef external fill:#f1f8e9
    
    class UserAPI,Context user
    class LifecycleManager,StateMachine,HealthManager,ReconnectionManager lifecycle
    class InitProcessor,EventProcessor,ContentManager processor
    class HealthCheck,ToolsUpdate,StateMonitor,PerformanceTracker monitor
    class Registry,Metadata,Config,HealthHistory storage
    class Orchestrator,FastMCP,Services external
```

## 🔄 7状态生命周期状态机

```mermaid
stateDiagram-v2
    [*] --> INITIALIZING : 服务注册
    
    INITIALIZING --> HEALTHY : 连接成功<br/>工具获取完成
    INITIALIZING --> RECONNECTING : 初始化失败<br/>连接超时
    
    HEALTHY --> WARNING : 偶发失败<br/>响应变慢
    HEALTHY --> RECONNECTING : 连续失败<br/>达到重连阈值
    HEALTHY --> DISCONNECTING : 手动停止<br/>用户操作
    
    WARNING --> HEALTHY : 恢复正常<br/>响应时间改善
    WARNING --> RECONNECTING : 持续失败<br/>达到重连阈值
    
    RECONNECTING --> HEALTHY : 重连成功<br/>服务恢复
    RECONNECTING --> UNREACHABLE : 重连失败<br/>超过最大重试次数
    
    UNREACHABLE --> RECONNECTING : 重试重连<br/>定期尝试
    UNREACHABLE --> DISCONNECTED : 放弃重连<br/>手动停止
    
    DISCONNECTING --> DISCONNECTED : 断开完成<br/>资源清理
    
    DISCONNECTED --> [*] : 服务删除<br/>完全移除
    DISCONNECTED --> INITIALIZING : 服务重启<br/>重新注册
    
    note right of INITIALIZING
        • 配置验证完成
        • 执行首次连接
        • 获取工具列表
        • 设置初始状态
    end note
    
    note right of HEALTHY
        • 连接正常稳定
        • 心跳检查成功
        • 工具调用可用
        • 响应时间正常
    end note
    
    note right of WARNING
        • 偶发心跳失败
        • 响应时间变慢
        • 未达到重连阈值
        • 仍可提供服务
    end note
    
    note right of RECONNECTING
        • 连续失败达到阈值
        • 正在执行重连
        • 服务暂时不可用
        • 自动恢复中
    end note
    
    note right of UNREACHABLE
        • 重连失败
        • 进入长周期重试
        • 服务完全不可用
        • 需要人工干预
    end note
    
    note right of DISCONNECTING
        • 执行优雅关闭
        • 清理连接资源
        • 保存状态信息
        • 准备完全停止
    end note
    
    note right of DISCONNECTED
        • 服务完全终止
        • 等待手动删除
        • 或准备重新启动
        • 状态信息保留
    end note
```

## 🧩 核心组件架构

### ServiceLifecycleManager

```mermaid
graph TB
    subgraph "ServiceLifecycleManager"
        Core[核心管理器]
        TaskScheduler[任务调度器]
        EventDispatcher[事件分发器]
    end
    
    subgraph "管理的组件"
        StateMachine[状态机]
        HealthManager[健康管理器]
        ReconnectionManager[重连管理器]
        ContentManager[内容管理器]
    end
    
    subgraph "定时任务"
        HealthCheckTask[健康检查任务<br/>30秒间隔]
        ToolsUpdateTask[工具更新任务<br/>2小时间隔]
        CleanupTask[清理任务<br/>24小时间隔]
        ReconnectionTask[重连任务<br/>动态间隔]
    end
    
    subgraph "事件处理"
        StateChangeEvent[状态变化事件]
        HealthChangeEvent[健康变化事件]
        ReconnectionEvent[重连事件]
        ToolsUpdateEvent[工具更新事件]
    end
    
    Core --> TaskScheduler
    Core --> EventDispatcher
    
    TaskScheduler --> HealthCheckTask
    TaskScheduler --> ToolsUpdateTask
    TaskScheduler --> CleanupTask
    TaskScheduler --> ReconnectionTask
    
    EventDispatcher --> StateChangeEvent
    EventDispatcher --> HealthChangeEvent
    EventDispatcher --> ReconnectionEvent
    EventDispatcher --> ToolsUpdateEvent
    
    Core --> StateMachine
    Core --> HealthManager
    Core --> ReconnectionManager
    Core --> ContentManager
    
    HealthCheckTask --> HealthManager
    ToolsUpdateTask --> ContentManager
    ReconnectionTask --> ReconnectionManager
    
    StateMachine --> StateChangeEvent
    HealthManager --> HealthChangeEvent
    ReconnectionManager --> ReconnectionEvent
    ContentManager --> ToolsUpdateEvent
```

### ServiceStateMachine

```mermaid
graph TB
    subgraph "状态转换引擎"
        TransitionEngine[转换引擎]
        RuleValidator[规则验证器]
        ThresholdManager[阈值管理器]
    end
    
    subgraph "转换规则"
        SuccessRules[成功转换规则]
        FailureRules[失败转换规则]
        TimeoutRules[超时转换规则]
        ManualRules[手动转换规则]
    end
    
    subgraph "状态处理器"
        InitializingHandler[初始化处理器]
        HealthyHandler[健康处理器]
        WarningHandler[警告处理器]
        ReconnectingHandler[重连处理器]
        UnreachableHandler[不可达处理器]
        DisconnectingHandler[断开处理器]
        DisconnectedHandler[已断开处理器]
    end
    
    TransitionEngine --> RuleValidator
    TransitionEngine --> ThresholdManager
    
    RuleValidator --> SuccessRules
    RuleValidator --> FailureRules
    RuleValidator --> TimeoutRules
    RuleValidator --> ManualRules
    
    TransitionEngine --> InitializingHandler
    TransitionEngine --> HealthyHandler
    TransitionEngine --> WarningHandler
    TransitionEngine --> ReconnectingHandler
    TransitionEngine --> UnreachableHandler
    TransitionEngine --> DisconnectingHandler
    TransitionEngine --> DisconnectedHandler
    
    ThresholdManager -.-> WarningHandler
    ThresholdManager -.-> ReconnectingHandler
    ThresholdManager -.-> UnreachableHandler
```

### HealthManager

```mermaid
graph TB
    subgraph "健康检查引擎"
        CheckEngine[检查引擎]
        StatusEvaluator[状态评估器]
        TimeoutManager[超时管理器]
    end
    
    subgraph "检查策略"
        PingCheck[Ping检查]
        ToolsCheck[工具检查]
        ResponseTimeCheck[响应时间检查]
        AvailabilityCheck[可用性检查]
    end
    
    subgraph "健康等级"
        HealthyLevel[HEALTHY<br/>< 1秒, >95%]
        WarningLevel[WARNING<br/>1-3秒, 90-95%]
        SlowLevel[SLOW<br/>3-10秒, 80-90%]
        UnhealthyLevel[UNHEALTHY<br/>>10秒, <80%]
    end
    
    subgraph "数据收集"
        ResponseTracker[响应跟踪器]
        FailureTracker[失败跟踪器]
        PerformanceTracker[性能跟踪器]
        HistoryTracker[历史跟踪器]
    end
    
    CheckEngine --> StatusEvaluator
    CheckEngine --> TimeoutManager
    
    CheckEngine --> PingCheck
    CheckEngine --> ToolsCheck
    CheckEngine --> ResponseTimeCheck
    CheckEngine --> AvailabilityCheck
    
    StatusEvaluator --> HealthyLevel
    StatusEvaluator --> WarningLevel
    StatusEvaluator --> SlowLevel
    StatusEvaluator --> UnhealthyLevel
    
    CheckEngine --> ResponseTracker
    CheckEngine --> FailureTracker
    CheckEngine --> PerformanceTracker
    CheckEngine --> HistoryTracker
    
    ResponseTracker --> StatusEvaluator
    FailureTracker --> StatusEvaluator
    PerformanceTracker --> StatusEvaluator
```

### SmartReconnectionManager

```mermaid
graph TB
    subgraph "重连策略引擎"
        StrategyEngine[策略引擎]
        BackoffCalculator[退避计算器]
        PriorityManager[优先级管理器]
    end
    
    subgraph "重连队列"
        CriticalQueue[关键服务队列<br/>0.5x延迟]
        HighQueue[高优先级队列<br/>0.7x延迟]
        NormalQueue[普通队列<br/>1.0x延迟]
        LowQueue[低优先级队列<br/>1.5x延迟]
    end
    
    subgraph "重连策略"
        ExponentialBackoff[指数退避<br/>60s → 600s]
        MaxAttempts[最大尝试次数<br/>10次]
        CircuitBreaker[熔断器<br/>失败保护]
        HealthyReset[健康重置<br/>成功后清零]
    end
    
    subgraph "监控指标"
        AttemptCounter[尝试计数器]
        SuccessRate[成功率统计]
        AverageDelay[平均延迟]
        QueueLength[队列长度]
    end
    
    StrategyEngine --> BackoffCalculator
    StrategyEngine --> PriorityManager
    
    PriorityManager --> CriticalQueue
    PriorityManager --> HighQueue
    PriorityManager --> NormalQueue
    PriorityManager --> LowQueue
    
    BackoffCalculator --> ExponentialBackoff
    BackoffCalculator --> MaxAttempts
    BackoffCalculator --> CircuitBreaker
    BackoffCalculator --> HealthyReset
    
    StrategyEngine --> AttemptCounter
    StrategyEngine --> SuccessRate
    StrategyEngine --> AverageDelay
    StrategyEngine --> QueueLength
```

## 📊 数据流架构

### 健康检查数据流

```mermaid
sequenceDiagram
    participant Timer as 定时器
    participant HealthManager as 健康管理器
    participant FastMCP as FastMCP客户端
    participant Service as MCP服务
    participant StateMachine as 状态机
    participant Registry as 注册表
    
    Timer->>HealthManager: 触发健康检查
    HealthManager->>FastMCP: ping_service()
    
    FastMCP->>Service: MCP Ping
    Service-->>FastMCP: Pong + 响应时间
    
    FastMCP-->>HealthManager: 检查结果
    HealthManager->>HealthManager: 评估健康状态
    
    alt 状态需要变化
        HealthManager->>StateMachine: 触发状态转换
        StateMachine->>Registry: 更新服务状态
        StateMachine->>HealthManager: 状态变化确认
    end
    
    HealthManager->>Registry: 更新健康元数据
    Registry-->>HealthManager: 更新完成
```

### 重连流程数据流

```mermaid
sequenceDiagram
    participant StateMachine as 状态机
    participant ReconnectionManager as 重连管理器
    participant Orchestrator as 编排器
    participant FastMCP as FastMCP客户端
    participant Service as MCP服务
    participant Registry as 注册表
    
    StateMachine->>ReconnectionManager: 添加重连任务
    ReconnectionManager->>ReconnectionManager: 计算重连延迟
    
    loop 重连循环
        ReconnectionManager->>Orchestrator: 触发重连
        Orchestrator->>FastMCP: 断开旧连接
        Orchestrator->>FastMCP: 创建新连接
        
        FastMCP->>Service: 建立连接
        
        alt 连接成功
            Service-->>FastMCP: 连接确认
            FastMCP->>Service: 获取工具列表
            Service-->>FastMCP: 工具列表
            FastMCP-->>Orchestrator: 重连成功
            Orchestrator-->>ReconnectionManager: 成功通知
            ReconnectionManager->>StateMachine: 触发成功转换
            StateMachine->>Registry: 更新为HEALTHY
        else 连接失败
            Service-->>FastMCP: 连接失败
            FastMCP-->>Orchestrator: 重连失败
            Orchestrator-->>ReconnectionManager: 失败通知
            ReconnectionManager->>ReconnectionManager: 增加失败计数
            ReconnectionManager->>ReconnectionManager: 计算下次重连时间
        end
    end
```

## 🔧 配置架构

### 生命周期配置层次

```mermaid
graph TB
    subgraph "全局配置"
        GlobalConfig[全局生命周期配置]
        DefaultThresholds[默认阈值配置]
        DefaultTimeouts[默认超时配置]
    end
    
    subgraph "服务类型配置"
        CriticalConfig[关键服务配置]
        NormalConfig[普通服务配置]
        BackgroundConfig[后台服务配置]
    end
    
    subgraph "运行时配置"
        DynamicThresholds[动态阈值调整]
        AdaptiveTimeouts[自适应超时]
        LoadBasedConfig[负载基础配置]
    end
    
    subgraph "服务特定配置"
        ServiceOverrides[服务特定覆盖]
        CustomHealthChecks[自定义健康检查]
        SpecialHandling[特殊处理规则]
    end
    
    GlobalConfig --> DefaultThresholds
    GlobalConfig --> DefaultTimeouts
    
    GlobalConfig --> CriticalConfig
    GlobalConfig --> NormalConfig
    GlobalConfig --> BackgroundConfig
    
    CriticalConfig --> DynamicThresholds
    NormalConfig --> AdaptiveTimeouts
    BackgroundConfig --> LoadBasedConfig
    
    DynamicThresholds --> ServiceOverrides
    AdaptiveTimeouts --> CustomHealthChecks
    LoadBasedConfig --> SpecialHandling
```

## 📈 性能优化架构

### 并发处理架构

```mermaid
graph TB
    subgraph "任务调度器"
        MainScheduler[主调度器]
        HealthScheduler[健康检查调度器]
        ReconnectionScheduler[重连调度器]
        CleanupScheduler[清理调度器]
    end
    
    subgraph "工作线程池"
        HealthWorkers[健康检查工作线程<br/>并发执行]
        ReconnectionWorkers[重连工作线程<br/>优先级队列]
        CleanupWorkers[清理工作线程<br/>后台执行]
    end
    
    subgraph "缓存层"
        StateCache[状态缓存<br/>快速访问]
        HealthCache[健康缓存<br/>减少检查]
        MetadataCache[元数据缓存<br/>性能优化]
    end
    
    subgraph "批处理优化"
        BatchHealthCheck[批量健康检查]
        BatchStateUpdate[批量状态更新]
        BatchNotification[批量通知]
    end
    
    MainScheduler --> HealthScheduler
    MainScheduler --> ReconnectionScheduler
    MainScheduler --> CleanupScheduler
    
    HealthScheduler --> HealthWorkers
    ReconnectionScheduler --> ReconnectionWorkers
    CleanupScheduler --> CleanupWorkers
    
    HealthWorkers --> StateCache
    ReconnectionWorkers --> HealthCache
    CleanupWorkers --> MetadataCache
    
    HealthWorkers --> BatchHealthCheck
    HealthWorkers --> BatchStateUpdate
    HealthWorkers --> BatchNotification
```

## 🔗 相关文档

- [服务生命周期概览](service-lifecycle.md) - 了解生命周期管理
- [健康检查机制](health-check.md) - 深入了解健康检查
- [完整示例集合](examples.md) - 实际使用示例
- [服务注册架构](../registration/architecture.md) - 注册架构详解

## 🎯 下一步

- 深入了解 [健康检查机制](health-check.md)
- 学习 [实际使用示例](examples.md)
- 掌握 [监控和调试](../../advanced/monitoring.md)
- 查看 [最佳实践](../../advanced/best-practices.md)
