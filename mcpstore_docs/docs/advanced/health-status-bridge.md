# 健康状态桥梁机制

本页详细说明 MCPStore 中 `HealthStatusBridge` 的设计和实现，该机制负责将健康检查结果映射到服务生命周期状态。

## 🎯 设计目标

- **状态统一**：将不同层次的状态枚举统一映射
- **错误安全**：确保所有健康状态都有明确的生命周期状态对应
- **可扩展性**：易于添加新的状态映射关系

## 🏗️ 架构设计

```mermaid
graph LR
    subgraph 健康检查层
        HC[健康检查]
        HR[HealthCheckResult]
        HS[HealthStatus]
    end
    
    subgraph 状态桥梁层
        HB[HealthStatusBridge]
        MAP[状态映射表]
    end
    
    subgraph 生命周期层
        SCS[ServiceConnectionState]
        LC[LifecycleManager]
    end
    
    HC --> HR
    HR --> HS
    HS --> HB
    HB --> MAP
    MAP --> SCS
    SCS --> LC
    
    style HB fill:#f9f,stroke:#333,stroke-width:2px
    style MAP fill:#bbf,stroke:#333,stroke-width:2px
```

## 🔄 状态映射关系

### 核心映射表

| HealthStatus | ServiceConnectionState | 说明 |
|--------------|------------------------|------|
| `HEALTHY` | `HEALTHY` | 直接映射，服务正常 |
| `WARNING` | `WARNING` | 直接映射，响应慢但可用 |
| `SLOW` | `WARNING` | 合并映射，慢响应归类为警告 |
| `UNHEALTHY` | `RECONNECTING` | 转换映射，触发重连流程 |
| `DISCONNECTED` | `DISCONNECTED` | 直接映射，连接断开 |
| `RECONNECTING` | `RECONNECTING` | 直接映射，重连中 |
| `FAILED` | `UNREACHABLE` | 转换映射，重连失败 |
| `UNKNOWN` | `DISCONNECTED` | 安全映射，未知状态视为断开 |

### 映射逻辑说明

```python
class HealthStatusBridge:
    STATUS_MAPPING = {
        HealthStatus.HEALTHY: ServiceConnectionState.HEALTHY,
        HealthStatus.WARNING: ServiceConnectionState.WARNING,
        HealthStatus.SLOW: ServiceConnectionState.WARNING,      # 慢响应归类为警告
        HealthStatus.UNHEALTHY: ServiceConnectionState.RECONNECTING,  # 触发重连
        HealthStatus.DISCONNECTED: ServiceConnectionState.DISCONNECTED,
        HealthStatus.RECONNECTING: ServiceConnectionState.RECONNECTING,
        HealthStatus.FAILED: ServiceConnectionState.UNREACHABLE,      # 重连失败
        HealthStatus.UNKNOWN: ServiceConnectionState.DISCONNECTED,    # 安全回退
    }
```

## 🔧 关键实现特性

### 1. 严格验证机制

```python
@classmethod
def map_health_to_lifecycle(cls, health_status: HealthStatus) -> ServiceConnectionState:
    if health_status not in cls.STATUS_MAPPING:
        error_msg = f"未知的健康状态，无法映射: {health_status}"
        logger.error(f"❌ [HEALTH_BRIDGE] {error_msg}")
        raise ValueError(error_msg)
    
    lifecycle_state = cls.STATUS_MAPPING[health_status]
    logger.debug(f"🔄 [HEALTH_BRIDGE] 状态映射: {health_status.value} → {lifecycle_state.value}")
    
    return lifecycle_state
```

**特性**：
- ✅ 抛出异常而非静默回退，确保所有状态都被正确处理
- ✅ 详细的日志记录，便于调试
- ✅ 类型安全的枚举映射

### 2. 正面状态判断

```python
@classmethod
def is_health_status_positive(cls, health_status: HealthStatus) -> bool:
    # 保持与原有逻辑一致：只有 UNHEALTHY 返回 False
    return health_status != HealthStatus.UNHEALTHY
```

**兼容性设计**：保持与原有布尔判断逻辑一致，确保平滑迁移。

### 3. 便利方法

```python
@classmethod
def map_health_result_to_lifecycle(cls, health_result: HealthCheckResult) -> ServiceConnectionState:
    return cls.map_health_to_lifecycle(health_result.status)

@classmethod
def get_mapping_summary(cls) -> dict:
    return {
        "mappings": {health.value: lifecycle.value for health, lifecycle in cls.STATUS_MAPPING.items()},
        "total_mappings": len(cls.STATUS_MAPPING),
        "positive_statuses": [status.value for status in HealthStatus if cls.is_health_status_positive(status)]
    }
```

## 🚀 使用示例

### 基本状态映射

```python
from mcpstore.core.lifecycle.health_bridge import HealthStatusBridge
from mcpstore.core.lifecycle.health_manager import HealthStatus

# 单个状态映射
health_status = HealthStatus.WARNING
lifecycle_state = HealthStatusBridge.map_health_to_lifecycle(health_status)
print(f"映射结果: {health_status.value} → {lifecycle_state.value}")

# 判断是否为正面状态
is_positive = HealthStatusBridge.is_health_status_positive(health_status)
print(f"正面状态: {is_positive}")
```

### 健康检查结果映射

```python
from mcpstore.core.lifecycle.health_manager import HealthCheckResult

# 创建健康检查结果
health_result = HealthCheckResult(
    status=HealthStatus.SLOW,
    response_time=5.0,
    timestamp=1642784400.0,
    error_message=None
)

# 映射到生命周期状态
lifecycle_state = HealthStatusBridge.map_health_result_to_lifecycle(health_result)
print(f"健康结果映射: {health_result.status.value} → {lifecycle_state.value}")
```

### 获取映射摘要

```python
# 获取完整映射关系
summary = HealthStatusBridge.get_mapping_summary()
print(f"映射关系数量: {summary['total_mappings']}")
print(f"正面状态列表: {summary['positive_statuses']}")

for health, lifecycle in summary['mappings'].items():
    print(f"  {health:12} → {lifecycle}")
```

## 🔄 与生命周期管理的集成

### 监控任务集成

```python
# 在 MonitoringTasksMixin._check_single_service_health 中
health_result = await self.check_service_health_detailed(name, client_id)

# 使用桥梁映射状态
suggested_state = HealthStatusBridge.map_health_to_lifecycle(health_result.status)

# 传递给增强版生命周期处理器
await self.lifecycle_manager.handle_health_check_result_enhanced(
    agent_id=client_id,
    service_name=name,
    suggested_state=suggested_state,
    response_time=health_result.response_time,
    error_message=health_result.error_message
)
```

### 生命周期管理器集成

```python
# 在 ServiceLifecycleManager.handle_health_check_result_enhanced 中
if suggested_state:
    success_states = [ServiceConnectionState.HEALTHY, ServiceConnectionState.WARNING]
    is_success = suggested_state in success_states
    
    if is_success:
        metadata.consecutive_failures = 0
        await self._transition_to_state(agent_id, service_name, suggested_state)
    else:
        metadata.consecutive_failures += 1
        await self._transition_to_state(agent_id, service_name, suggested_state)
```

## ⚡ 性能和安全特性

### 1. 性能优化
- **静态映射表**：映射关系在类级别定义，无运行时开销
- **简单查找**：O(1) 字典查找，高效映射
- **日志级别**：debug级别日志，生产环境无性能影响

### 2. 错误处理
- **严格验证**：未映射状态立即抛出异常
- **详细错误信息**：包含具体的未映射状态值
- **日志记录**：所有映射操作都有日志记录

### 3. 向后兼容
- **布尔判断兼容**：保持与原有 `is_healthy` 逻辑一致
- **便利函数**：提供兼容性包装函数

## 🔮 扩展点

### 添加新的状态映射

```python
# 如果 HealthStatus 添加了新的状态
class HealthStatusBridge:
    STATUS_MAPPING = {
        # ... 现有映射 ...
        HealthStatus.NEW_STATUS: ServiceConnectionState.APPROPRIATE_STATE,
    }
```

### 自定义映射逻辑

```python
# 可以继承并重写映射逻辑
class CustomHealthStatusBridge(HealthStatusBridge):
    @classmethod
    def map_health_to_lifecycle(cls, health_status: HealthStatus) -> ServiceConnectionState:
        # 自定义映射逻辑
        if health_status == HealthStatus.SPECIAL_CASE:
            return ServiceConnectionState.CUSTOM_STATE
        
        return super().map_health_to_lifecycle(health_status)
```

## 📝 最佳实践

1. **使用桥梁映射**：始终通过 `HealthStatusBridge` 进行状态转换
2. **处理异常**：捕获 `ValueError` 并提供合适的回退逻辑
3. **日志记录**：在关键路径上记录状态映射信息
4. **测试覆盖**：确保所有健康状态都有对应的测试用例

## 相关文档

- [生命周期管理](lifecycle.md) - 完整的7状态生命周期
- [统一状态管理器](unified-state-manager.md) - 状态管理接口
- [健康监控](../services/health/check-services.md) - 健康检查方法

更新时间：2025-01-15
