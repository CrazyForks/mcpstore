## get_service_status - 获取服务状态

获取单个服务状态信息。

### SDK

同步：
  - `store.for_store().get_service_status(name) -> Dict[str, Any]`
  - `store.for_agent(id).get_service_status(name) -> Dict[str, Any]`

异步：
  - `await store.for_store().get_service_status_async(name) -> Dict[str, Any]`
  - `await store.for_agent(id).get_service_status_async(name) -> Dict[str, Any]`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `name` | `str` | ✅ | - | 服务名称 |

## 返回值

返回指定服务的状态信息字典：

```python
{
    "name": "service_name",
    "status": "initializing|healthy|warning|reconnecting|unreachable|disconnecting|disconnected",
    "connection_state": "connected|connecting|disconnected",
    "response_time": 1.23,  # 响应时间（秒）
    "last_check": "2025-01-01T12:00:00Z",
    "uptime": 3600,  # 运行时间（秒）
    "error": None,   # 错误信息（如果有）
    "metadata": {    # 额外元数据
        "version": "1.0.0",
        "capabilities": ["tools", "resources"]
    }
}
```

## 使用示例

### Store级别获取服务状态

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取单个服务状态
status = store.for_store().get_service_status("weather")
print(f"Weather服务状态: {status}")

# 检查服务是否健康
if status['status'] == 'healthy':
    print(f"服务运行正常，响应时间: {status['response_time']:.2f}秒")
else:
    print(f"服务状态异常: {status['error']}")
```

### Agent级别获取服务状态

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式获取服务状态
agent_status = store.for_agent("agent1").get_service_status("weather-local")
print(f"Agent Weather服务状态: {agent_status}")

# 检查连接状态
if agent_status['connection_state'] == 'connected':
    print("服务已连接")
else:
    print(f"服务连接状态: {agent_status['connection_state']}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_get_status():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步获取服务状态
    status = await store.for_store().get_service_status_async("weather")
    
    # 分析状态信息
    print(f"服务名称: {status['name']}")
    print(f"健康状态: {status['status']}")
    print(f"连接状态: {status['connection_state']}")
    print(f"运行时间: {status['uptime']}秒")
    
    return status

# 运行异步获取
result = asyncio.run(async_get_status())
```

### 批量状态检查

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取所有服务列表
services = store.for_store().list_services()

# 逐个检查状态
for service in services:
    status = store.for_store().get_service_status(service.name)
    print(f"{service.name}: {status['status']} ({status['response_time']:.2f}s)")
```

## 状态字段说明

### 服务状态 (status) - 7状态生命周期
- `initializing`: 初始化中，配置验证完成，执行首次连接
- `healthy`: 服务正常运行，连接正常，心跳成功
- `warning`: 服务运行但有警告（响应慢或偶发心跳失败）
- `reconnecting`: 重连中，连续失败达到阈值，正在重连
- `unreachable`: 不可达，重连失败，进入长周期重试
- `disconnecting`: 断开中，执行优雅关闭
- `disconnected`: 已断开，服务终止，等待手动删除

### 连接状态 (connection_state) - 兼容性字段
- `connected`: 已连接并可通信
- `connecting`: 正在连接中  
- `disconnected`: 连接断开

> 注意：`status` 字段使用完整的 7 状态生命周期模型，而 `connection_state` 是简化的兼容性字段。建议使用 `status` 字段获得更精确的状态信息。

## 相关方法

- [check_services()](check-services.md) - 检查所有服务健康状态
- [wait_service()](wait-service.md) - 等待服务达到指定状态
- [get_service_info()](../listing/get-service-info.md) - 获取服务详细信息

## 注意事项

- 实时状态: 该方法返回实时状态，可能触发网络请求
- Agent 映射: Agent 模式下会自动处理服务名映射
- 错误处理: 服务不存在时会抛出异常
- 缓存策略: 状态信息可能有短暂缓存以提高性能
