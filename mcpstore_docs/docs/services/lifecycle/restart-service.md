# restart_service()

重启指定的服务。这是一个组合操作，相当于先停止服务，然后重新启动。

## 语法

```python
store.for_store().restart_service(name: str) -> bool
store.for_agent(agent_id).restart_service(name: str) -> bool
```

## 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `name` | str | ✅ | 要重启的服务名称 |

## 返回值

- **类型**: `bool`
- **说明**: 重启成功返回 `True`，失败返回 `False`

## 上下文模式差异

### 🏪 Store 模式
- 直接调用 `orchestrator.restart_service(name)`
- 使用完整的服务名称

### 🤖 Agent 模式  
- 自动进行服务名称映射：`local_name → global_name`
- 调用 `orchestrator.restart_service(global_name, agent_id)`

## 使用示例

### 基本重启

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 重启服务
success = store.for_store().restart_service("weather-api")

if success:
    print("✅ 服务重启成功")
else:
    print("❌ 服务重启失败")
```

### Agent 级别重启

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

agent_id = "my_agent"
service_name = "weather-api"  # 使用原始名称，会自动映射

# Agent 级别重启服务
success = store.for_agent(agent_id).restart_service(service_name)

if success:
    print(f"✅ Agent {agent_id} 的服务 {service_name} 重启成功")
else:
    print(f"❌ Agent {agent_id} 的服务 {service_name} 重启失败")
```

### 带状态检查的重启

```python
from mcpstore import MCPStore
import time

store = MCPStore.setup_store()

service_name = "weather-api"

print(f"正在重启服务: {service_name}")

# 重启前检查状态
services = store.for_store().list_services()
for service in services:
    if service.name == service_name:
        print(f"重启前状态: {service.status}")
        break

# 执行重启
success = store.for_store().restart_service(service_name)

if success:
    print("✅ 重启命令执行成功")
    
    # 等待重启完成
    time.sleep(3)
    
    # 检查重启后状态
    services = store.for_store().list_services()
    for service in services:
        if service.name == service_name:
            print(f"重启后状态: {service.status}")
            break
else:
    print("❌ 重启失败")
```

### 批量重启服务

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 需要重启的服务列表
services_to_restart = ["weather-api", "filesystem", "calculator"]

print("开始批量重启服务...")
results = {}

for service_name in services_to_restart:
    print(f"重启服务: {service_name}")
    results[service_name] = store.for_store().restart_service(service_name)

# 显示结果
print("\n重启结果:")
for service, success in results.items():
    status = "✅ 成功" if success else "❌ 失败"
    print(f"  {service}: {status}")
```

## 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def restart_service_async_example():
    store = MCPStore.setup_store()
    
    # 异步重启服务
    success = await store.for_store().restart_service_async("weather-api")
    
    if success:
        print("✅ 异步重启成功")
    else:
        print("❌ 异步重启失败")

# 运行异步示例
asyncio.run(restart_service_async_example())
```

### 异步批量重启

```python
import asyncio
from mcpstore import MCPStore

async def batch_restart_async():
    store = MCPStore.setup_store()
    
    services = ["weather-api", "filesystem", "calculator"]
    
    # 并发重启多个服务
    tasks = [
        store.for_store().restart_service_async(service)
        for service in services
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 显示结果
    for service, result in zip(services, results):
        if isinstance(result, Exception):
            print(f"❌ {service}: 重启异常 - {result}")
        elif result:
            print(f"✅ {service}: 重启成功")
        else:
            print(f"❌ {service}: 重启失败")

# 运行异步批量重启
asyncio.run(batch_restart_async())
```

## 故障恢复重启

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

service_name = "weather-api"

# 检查服务健康状态
service_info = store.for_store().get_service_info(service_name)

if service_info and service_info.get('status') == 'error':
    print(f"检测到服务 {service_name} 出现故障，尝试重启...")
    
    success = store.for_store().restart_service(service_name)
    
    if success:
        print("✅ 故障恢复重启成功")
    else:
        print("❌ 重启失败，需要手动检查")
```

## 错误处理

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

try:
    success = store.for_store().restart_service("my-service")
    
    if not success:
        print("重启失败，可能的原因:")
        print("- 服务配置有误")
        print("- 服务依赖不满足")
        print("- 网络连接问题")
        
except Exception as e:
    print(f"❌ 重启服务时发生错误: {e}")
```

## 注意事项

1. **Agent 名称映射**: Agent 模式下会自动将本地名称转换为全局名称
2. **异常处理**: 方法内部会捕获异常并记录日志，返回 False 表示失败
3. **orchestrator 依赖**: 实际重启操作由 orchestrator 执行
4. **同步/异步**: 提供同步和异步两个版本

## 相关方法

- [list_services()](../listing/list-services.md) - 列出所有服务
- [get_service_info()](../listing/get-service-info.md) - 获取服务详细信息
- [add_service()](../registration/register-service.md) - 注册服务
- [check_services()](check-services.md) - 健康检查

## 下一步

- 了解 [服务健康检查](check-services.md)
- 学习 [服务注册方法](../registration/register-service.md)
- 查看 [工具使用方法](../../tools/usage/call-tool.md)
