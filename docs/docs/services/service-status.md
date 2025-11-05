## service_status - 服务状态

获取服务的当前状态。

### SDK

调用方式：ServiceProxy 方法

获取方式：
  - `svc = store.for_store().find_service(name)`
  - `svc = store.for_agent(id).find_service(name)`

同步：
  - `svc.service_status() -> str`

异步：
  - `await svc.service_status_async() -> str`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回服务的当前状态字符串，可能的值：

| 状态值 | 描述 | 含义 |
|--------|------|------|
| `INITIALIZING` | 初始化中 | 服务正在进行首次连接和初始化 |
| `HEALTHY` | 健康 | 服务运行正常，连接稳定 |
| `WARNING` | 警告 | 服务有偶发问题，但仍可用 |
| `RECONNECTING` | 重连中 | 服务连接失败，正在尝试重连 |
| `UNREACHABLE` | 不可达 | 服务无法连接，已进入长周期重试 |
| `DISCONNECTING` | 断开中 | 服务正在执行断开操作 |
| `DISCONNECTED` | 已断开 | 服务已完全断开 |

## 使用示例

### Store级别获取服务状态

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

# 获取服务状态
status = svc.service_status()
print(f"服务状态: {status}")

# 根据状态做判断
if status == "HEALTHY":
    print("服务运行正常")
elif status == "WARNING":
    print("服务有警告")
elif status == "RECONNECTING":
    print("服务正在重连")
else:
    print(f"服务状态异常: {status}")
```

### Agent级别获取服务状态

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

# 获取服务状态
status = svc.service_status()
print(f"Agent服务状态: {status}")
```

### 监控服务状态变化

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

# 获取服务代理
svc = store.for_store().find_service("weather")

# 持续监控状态
print("开始监控服务状态...")
for i in range(10):
    status = svc.service_status()
    print(f"[{i+1}] 当前状态: {status}")
    time.sleep(2)
```

### 批量检查多个服务状态

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

# 检查所有服务状态
service_names = ["weather", "calculator"]
status_report = {}

for name in service_names:
    svc = store.for_store().find_service(name)
    status = svc.service_status()
    status_report[name] = status
    
print(f"{name}: {status}")

print(f"\n状态报告: {status_report}")
```

### 结合健康检查使用

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

# 获取状态
status = svc.service_status()
print(f"服务状态: {status}")

# 如果状态异常，获取详细健康信息
if status not in ["HEALTHY", "INITIALIZING"]:
    health = svc.health_details()
    print(f"健康详情: {health}")
```

## 状态说明

### 正常状态
- **INITIALIZING**: 服务刚添加，正在初始化
- **HEALTHY**: 服务完全正常，可以使用

### 警告状态
- **WARNING**: 服务有偶发问题，但仍在正常工作范围内

### 异常状态
- **RECONNECTING**: 连接失败，正在重连
- **UNREACHABLE**: 服务不可达，重连失败
- **DISCONNECTING**: 正在断开连接
- **DISCONNECTED**: 已完全断开

## 相关方法

- [service_info()](service-info.md) - 获取服务详细信息
- [check_health()](../health/check-health.md) - 检查服务健康摘要
- [health_details()](../health/health-details.md) - 获取健康详情
- [find_service()](../listing/find-service.md) - 查找服务

## 注意事项

- 调用前提: 必须先通过 `find_service()` 获取 ServiceProxy 对象
- 状态实时性: 返回的是当前的服务状态
- 状态转换: 状态会根据服务健康检查自动转换
- Agent 隔离: Agent 级别只能看到该 Agent 的服务状态

