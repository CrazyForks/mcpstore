# check_services()

检查所有服务健康状态。

## 方法特性

- ✅ **异步版本**: `check_services_async()`
- ✅ **Store级别**: `store.for_store().check_services()`
- ✅ **Agent级别**: `store.for_agent("agent1").check_services()`
- 📁 **文件位置**: `service_management.py`
- 🏷️ **所属类**: `ServiceManagementMixin`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回包含所有服务健康状态的字典，格式如下：

```python
{
    "service_name": {
        "status": "healthy|warning|reconnecting|unreachable|disconnected|unknown",
        "response_time": 1.23,  # 响应时间（秒）
        "last_check": "2025-01-01T12:00:00Z",
        "error": None  # 错误信息（如果有）
    }
}
```

## 使用示例

### Store级别健康检查

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Store级别健康检查
health_status = store.for_store().check_services()
print(f"Store级别健康状态: {health_status}")

# 检查特定服务状态
for service_name, status in health_status.items():
    if status['status'] != 'healthy':
        print(f"服务 {service_name} 状态异常: {status}")
```

### Agent级别健康检查

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent级别健康检查
agent_health = store.for_agent("agent1").check_services()
print(f"Agent级别健康状态: {agent_health}")

# 统计健康状态
healthy_count = sum(1 for s in agent_health.values() if s['status'] == 'healthy')
total_count = len(agent_health)
print(f"健康服务: {healthy_count}/{total_count}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_health_check():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步健康检查
    health_status = await store.for_store().check_services_async()
    
    # 分析健康状态
    for service_name, status in health_status.items():
        print(f"服务 {service_name}: {status['status']} ({status['response_time']:.2f}s)")
    
    return health_status

# 运行异步检查
result = asyncio.run(async_health_check())
```

## 健康状态说明

| 状态 | 描述 | 条件 |
|------|------|------|
| `healthy` | 健康 | ping成功且响应时间正常 |
| `warning` | 警告 | ping成功但响应时间较慢，或偶发失败但未达重连阈值 |
| `reconnecting` | 重连中 | 连续失败达到阈值，正在执行重连 |
| `unreachable` | 不可达 | 重连失败，进入长周期重试 |
| `disconnected` | 已断开 | 服务终止或连接断开 |
| `unknown` | 未知 | 无法确定状态 |

> **📝 注意**：健康检查结果会通过 `HealthStatusBridge` 自动映射到对应的服务生命周期状态。详见 [生命周期管理](../../advanced/lifecycle.md)

## 相关方法

- [get_service_status()](get-service-status.md) - 获取单个服务状态
- [wait_service()](wait-service.md) - 等待服务达到指定状态
- [restart_service()](../management/restart-service.md) - 重启不健康的服务

## 注意事项

1. **性能考虑**: 健康检查会并发执行，但大量服务时可能需要时间
2. **网络依赖**: 远程服务的健康检查依赖网络连接
3. **缓存机制**: 健康状态有缓存，避免频繁检查
4. **Agent隔离**: Agent级别只检查该Agent的服务
