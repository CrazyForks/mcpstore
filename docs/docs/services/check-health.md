## check_health - 健康检查（ServiceProxy）

检查单个服务的健康状态（ServiceProxy 级别）。

### SDK

调用方式：ServiceProxy 方法

获取方式：
  - `svc = store.for_store().find_service(name)`
  - `svc = store.for_agent(id).find_service(name)`

同步：
  - `svc.check_health() -> Dict[str, Any]`

异步：
  - `await svc.check_health_async() -> Dict[str, Any]`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回简化的健康状态摘要字典：

```python
{
    "healthy": bool,                    # 是否健康
    "status": str,                      # 状态字符串
    "response_time": float,             # 响应时间（秒）
    "last_check": str                   # 最后检查时间（ISO格式）
}
```

## 使用示例

### Store级别健康检查

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

# 检查健康状态
health = svc.check_health()
print(f"健康状态: {health}")

if health["healthy"]:
    print(f"服务健康 (响应时间: {health['response_time']:.3f}秒)")
else:
    print(f"服务异常: {health['status']}")
```

### Agent级别健康检查

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

# 检查健康状态
health = svc.check_health()
print(f"Agent服务健康: {health}")
```

### 持续健康监控

```python
import time
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

# 持续监控健康状态
print("开始健康监控...")
for i in range(5):
    health = svc.check_health()
    print(f"[检查 {i+1}] 状态: {health['status']}, 响应时间: {health['response_time']:.3f}秒")
    time.sleep(3)
```

### 批量健康检查

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

# 批量健康检查
service_names = ["weather", "calculator"]
health_report = {}

print("服务健康报告")
print("=" * 50)

for name in service_names:
    svc = store.for_store().find_service(name)
    health = svc.check_health()
    health_report[name] = health
    
    print(f"{name}:")
    print(f"   状态: {health['status']}")
    print(f"   响应时间: {health['response_time']:.3f}秒")
    print(f"   最后检查: {health['last_check']}")
    print()

# 统计
healthy_count = sum(1 for h in health_report.values() if h["healthy"])
print(f"健康服务: {healthy_count}/{len(service_names)}")
```

### 响应时间分析

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

# 多次检查，计算平均响应时间
response_times = []

for _ in range(10):
    health = svc.check_health()
    response_times.append(health['response_time'])

avg_response = sum(response_times) / len(response_times)
max_response = max(response_times)
min_response = min(response_times)

print(f"响应时间分析 (10次检查)")
print(f"  平均响应时间: {avg_response:.3f}秒")
print(f"  最大响应时间: {max_response:.3f}秒")
print(f"  最小响应时间: {min_response:.3f}秒")
```

### 异常处理示例

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

try:
    health = svc.check_health()
    
    if not health["healthy"]:
        print(f"服务不健康: {health['status']}")
        
        # 尝试重启
        print("尝试重启服务...")
        svc.restart_service()
        
        # 再次检查
        import time
        time.sleep(2)
        health = svc.check_health()
        
        if health["healthy"]:
            print("服务已恢复健康")
        else:
            print("服务仍然异常")
            
except Exception as e:
    print(f"健康检查失败: {e}")
```

## 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `healthy` | bool | 服务是否健康，true表示健康 |
| `status` | str | 服务状态（HEALTHY/WARNING/RECONNECTING等）|
| `response_time` | float | 最近一次健康检查的响应时间（秒）|
| `last_check` | str | 最后一次检查的时间戳（ISO 8601格式）|

## 与 check_services() 的区别

| 对比项 | check_health() | check_services() |
|--------|----------------|------------------|
| **调用方式** | ServiceProxy方法 | Context方法 |
| **检查范围** | 单个服务 | 所有服务 |
| **返回格式** | 简化摘要 | 详细字典 |
| **使用场景** | 针对性检查 | 全局健康检查 |

```python
# check_health() - ServiceProxy级别
svc = store.for_store().find_service("weather")
health = svc.check_health()  # 只检查weather服务

# check_services() - Context级别
health_all = store.for_store().check_services()  # 检查所有服务
```

## 相关方法

- [health_details()](health-details.md) - 获取详细健康信息
- [check_services()](check-services.md) - 检查所有服务健康状态
- [service_status()](../details/service-status.md) - 获取服务状态
- [wait_service()](../waiting/wait-service.md) - 等待服务就绪

## 注意事项

- 调用前提: 必须先通过 `find_service()` 获取 ServiceProxy 对象
- 性能影响: 健康检查会执行实际的 ping 操作
- 缓存机制: 结果有短暂缓存，避免频繁检查
- 网络依赖: 远程服务依赖网络连接

