# health_details()

获取单个服务的详细健康信息（ServiceProxy级别）。

## 方法特性

- ✅ **调用方式**: ServiceProxy 方法
- ✅ **异步版本**: 支持异步调用
- ✅ **Store级别**: `svc = store.for_store().find_service("name")` 后调用
- ✅ **Agent级别**: `svc = store.for_agent("agent1").find_service("name")` 后调用
- 📁 **文件位置**: `service_proxy.py`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回详细的健康信息字典：

```python
{
    "healthy": bool,                        # 是否健康
    "status": str,                          # 状态字符串
    "response_time": float,                 # 响应时间（秒）
    "last_check": str,                      # 最后检查时间
    "consecutive_failures": int,            # 连续失败次数
    "consecutive_successes": int,           # 连续成功次数
    "last_success_time": str,               # 最后成功时间
    "last_failure_time": str,               # 最后失败时间
    "reconnect_attempts": int,              # 重连尝试次数
    "error_message": str,                   # 错误消息（如有）
    "disconnect_reason": str,               # 断开原因（如有）
    "tool_count": int,                      # 工具数量
    "state_entered_time": str               # 进入当前状态的时间
}
```

## 使用示例

### Store级别获取详细健康信息

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_store().wait_service("weather")

# 查找服务
svc = store.for_store().find_service("weather")

# 获取详细健康信息
details = svc.health_details()
print("📊 详细健康信息:")
print(f"  健康状态: {'✅' if details['healthy'] else '❌'}")
print(f"  服务状态: {details['status']}")
print(f"  响应时间: {details['response_time']:.3f}秒")
print(f"  工具数量: {details['tool_count']}")
print(f"  连续成功: {details['consecutive_successes']} 次")
print(f"  连续失败: {details['consecutive_failures']} 次")
```

### Agent级别获取详细健康信息

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent级别添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_agent("agent1").wait_service("weather")

# 查找服务
svc = store.for_agent("agent1").find_service("weather")

# 获取详细健康信息
details = svc.health_details()
print(f"Agent服务健康详情: {details}")
```

### 故障诊断

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 获取详细健康信息
details = svc.health_details()

# 故障诊断
if not details["healthy"]:
    print("🔍 服务故障诊断:")
    print(f"  状态: {details['status']}")
    
    if details["error_message"]:
        print(f"  错误信息: {details['error_message']}")
    
    if details["disconnect_reason"]:
        print(f"  断开原因: {details['disconnect_reason']}")
    
    if details["consecutive_failures"] > 0:
        print(f"  连续失败: {details['consecutive_failures']} 次")
    
    if details["reconnect_attempts"] > 0:
        print(f"  重连尝试: {details['reconnect_attempts']} 次")
    
    if details["last_failure_time"]:
        print(f"  最后失败: {details['last_failure_time']}")
```

### 性能分析

```python
from mcpstore import MCPStore
import time

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 持续收集性能数据
print("📊 性能监控 (10次)")
print("=" * 50)

response_times = []
for i in range(10):
    details = svc.health_details()
    response_times.append(details['response_time'])
    
    print(f"[{i+1}] 响应时间: {details['response_time']:.3f}秒, "
          f"状态: {details['status']}")
    
    time.sleep(1)

# 统计
avg_response = sum(response_times) / len(response_times)
max_response = max(response_times)
min_response = min(response_times)

print("\n📈 性能统计:")
print(f"  平均响应: {avg_response:.3f}秒")
print(f"  最大响应: {max_response:.3f}秒")
print(f"  最小响应: {min_response:.3f}秒")
```

### 服务可靠性报告

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 获取详细信息
details = svc.health_details()

# 生成可靠性报告
print("📋 服务可靠性报告")
print("=" * 50)
print(f"服务名称: {svc.service_info().name}")
print(f"健康状态: {'✅ 健康' if details['healthy'] else '❌ 异常'}")
print(f"当前状态: {details['status']}")
print(f"进入状态时间: {details['state_entered_time']}")
print()

print("📊 性能指标:")
print(f"  响应时间: {details['response_time']:.3f}秒")
print(f"  工具数量: {details['tool_count']}")
print()

print("📈 成功率指标:")
print(f"  连续成功: {details['consecutive_successes']} 次")
print(f"  连续失败: {details['consecutive_failures']} 次")
print(f"  重连尝试: {details['reconnect_attempts']} 次")
print()

print("⏰ 时间记录:")
if details['last_success_time']:
    print(f"  最后成功: {details['last_success_time']}")
if details['last_failure_time']:
    print(f"  最后失败: {details['last_failure_time']}")
print(f"  最后检查: {details['last_check']}")
```

### 批量服务健康对比

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加多个服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"},
        "calculator": {"command": "python", "args": ["calc.py"]}
    }
})

# 等待所有服务
store.for_store().wait_service("weather")
store.for_store().wait_service("calculator")

# 对比服务健康
service_names = ["weather", "calculator"]

print("📊 服务健康对比")
print("=" * 70)

for name in service_names:
    svc = store.for_store().find_service(name)
    details = svc.health_details()
    
    icon = "✅" if details["healthy"] else "❌"
    print(f"\n{icon} {name}")
    print(f"  状态: {details['status']}")
    print(f"  响应时间: {details['response_time']:.3f}秒")
    print(f"  成功/失败: {details['consecutive_successes']}/{details['consecutive_failures']}")
    
    if details['error_message']:
        print(f"  错误: {details['error_message']}")
```

## 返回字段详解

### 基础健康指标
- `healthy`: 服务整体是否健康
- `status`: 当前服务状态
- `response_time`: 最近一次检查的响应时间

### 可靠性指标
- `consecutive_failures`: 连续失败次数，用于判断服务稳定性
- `consecutive_successes`: 连续成功次数，用于判断服务恢复
- `reconnect_attempts`: 重连尝试次数，用于故障分析

### 时间记录
- `last_check`: 最后一次健康检查时间
- `last_success_time`: 最后一次成功时间
- `last_failure_time`: 最后一次失败时间
- `state_entered_time`: 进入当前状态的时间

### 故障信息
- `error_message`: 最近的错误消息
- `disconnect_reason`: 服务断开的原因

### 服务信息
- `tool_count`: 服务提供的工具数量

## 与 check_health() 的区别

| 对比项 | check_health() | health_details() |
|--------|----------------|------------------|
| **信息量** | 简化摘要 | 详细完整 |
| **性能开销** | 较小 | 较大 |
| **使用场景** | 快速健康检查 | 故障诊断分析 |
| **返回字段** | 4个基础字段 | 12+个详细字段 |

## 相关方法

- [check_health()](check-health.md) - 简化健康检查
- [check_services()](check-services.md) - 检查所有服务
- [service_status()](../details/service-status.md) - 获取服务状态
- [service_info()](../details/service-info.md) - 获取服务信息

## 注意事项

1. **调用前提**: 必须先通过 `find_service()` 获取 ServiceProxy 对象
2. **性能考虑**: 返回字段较多，建议在需要详细信息时使用
3. **字段完整性**: 某些字段可能为空，需要判空处理
4. **实时性**: 返回的是最新的健康检查结果

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

