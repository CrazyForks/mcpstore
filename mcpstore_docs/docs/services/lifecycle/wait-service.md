# 等待服务状态 (wait_service)

MCPStore 提供了强大的 `wait_service` 功能，允许您等待服务达到指定状态后再继续执行后续操作。这对于确保服务就绪、自动化流程和错误处理非常有用。

## 🎯 功能概述

`wait_service` 方法会持续监控指定服务的状态，直到达到目标状态或超时。支持：

- ✅ **智能参数识别**: 自动识别 `client_id` 或 `service_name`
- ✅ **多状态支持**: 可等待单个状态或多个状态中的任意一个
- ✅ **精确超时控制**: 可配置超时时间和异常处理
- ✅ **Store/Agent 双级别**: 支持 Store 和 Agent 两种上下文
- ✅ **同步/异步**: 提供同步和异步两个版本
- ✅ **API 支持**: 完整的 REST API 接口

## 📋 方法签名

### SDK 方法

```python
# 同步版本
def wait_service(
    client_id_or_service_name: str,
    status: Union[str, List[str]] = 'healthy',
    timeout: float = 10.0,
    raise_on_timeout: bool = False
) -> bool

# 异步版本
async def wait_service_async(
    client_id_or_service_name: str,
    status: Union[str, List[str]] = 'healthy',
    timeout: float = 10.0,
    raise_on_timeout: bool = False
) -> bool
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `client_id_or_service_name` | `str` | - | 服务的 client_id 或服务名（智能识别） |
| `status` | `str` \| `List[str]` | `'healthy'` | 目标状态，可以是单个状态或状态列表 |
| `timeout` | `float` | `10.0` | 超时时间（秒） |
| `raise_on_timeout` | `bool` | `False` | 超时时是否抛出异常 |

### 返回值

- `True`: 成功达到目标状态
- `False`: 超时未达到目标状态（当 `raise_on_timeout=False` 时）
- 抛出 `TimeoutError`: 超时异常（当 `raise_on_timeout=True` 时）

## 🔄 支持的状态

MCPStore 支持以下服务状态：

| 状态 | 描述 | 可用性 |
|------|------|--------|
| `initializing` | 初始化中 | ❌ 不可用 |
| `healthy` | 健康 | ✅ 完全可用 |
| `warning` | 警告 | ⚠️ 部分可用 |
| `reconnecting` | 重连中 | ❌ 不可用 |
| `unreachable` | 不可达 | ❌ 不可用 |
| `disconnecting` | 断开中 | ❌ 不可用 |
| `disconnected` | 已断开 | ❌ 不可用 |

## 🚀 使用示例

### 基础用法

```python
from mcpstore import MCPStore

# 初始化 MCPStore
store = MCPStore.setup_store()

# Store 级别等待
store_context = store.for_store()

# 等待服务达到健康状态
result = store_context.wait_service("my-service", "healthy", timeout=30.0)
if result:
    print("✅ 服务已就绪")
else:
    print("⏰ 等待超时")
```

### 等待多个状态

```python
# 等待服务达到健康或警告状态（任意一个即可）
result = store_context.wait_service(
    "my-service", 
    ["healthy", "warning"],  # 接受多个状态
    timeout=15.0
)
```

### Agent 级别使用

```python
# Agent 级别等待（支持本地服务名）
agent_context = store.for_agent("agent1")

# 添加服务
agent_context.add_service({
    "mcpServers": {
        "local-service": {
            "command": "npx",
            "args": ["-y", "howtocook-mcp"]
        }
    }
})

# 等待本地服务就绪
result = agent_context.wait_service("local-service", "healthy")
```

### 异步使用

```python
import asyncio

async def wait_for_services():
    store = MCPStore.setup_store()
    context = store.for_store()
    
    # 并发等待多个服务
    tasks = [
        context.wait_service_async("service1", "healthy", timeout=20.0),
        context.wait_service_async("service2", "healthy", timeout=20.0),
        context.wait_service_async("service3", ["healthy", "warning"], timeout=20.0)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"❌ 服务{i} 等待失败: {result}")
        elif result:
            print(f"✅ 服务{i} 已就绪")
        else:
            print(f"⏰ 服务{i} 等待超时")

# 运行
asyncio.run(wait_for_services())
```

### 异常处理

```python
try:
    # 设置 raise_on_timeout=True 来抛出异常
    result = store_context.wait_service(
        "critical-service",
        "healthy",
        timeout=30.0,
        raise_on_timeout=True
    )
    print("✅ 关键服务已就绪")
    
except TimeoutError as e:
    print(f"⏰ 关键服务等待超时: {e}")
    # 执行紧急处理逻辑
    
except ValueError as e:
    print(f"❌ 参数错误: {e}")
```

## 🌐 API 接口

### Store 级别 API

```bash
POST /for_store/wait_service
Content-Type: application/json

{
    "client_id_or_service_name": "my-service",
    "status": "healthy",
    "timeout": 10.0,
    "raise_on_timeout": false
}
```

### Agent 级别 API

```bash
POST /for_agent/{agent_id}/wait_service
Content-Type: application/json

{
    "client_id_or_service_name": "local-service",
    "status": ["healthy", "warning"],
    "timeout": 15.0,
    "raise_on_timeout": false
}
```

### API 响应格式

**成功响应**:
```json
{
    "success": true,
    "message": "Service wait completed: success",
    "data": {
        "client_id_or_service_name": "my-service",
        "target_status": "healthy",
        "timeout": 10.0,
        "result": true,
        "context": "store"
    }
}
```

**超时响应**:
```json
{
    "success": false,
    "message": "Service wait completed: timeout",
    "data": {
        "client_id_or_service_name": "my-service",
        "target_status": "healthy",
        "timeout": 10.0,
        "result": false,
        "context": "store"
    }
}
```

### cURL 示例

```bash
# Store 级别等待
curl -X POST http://localhost:18200/for_store/wait_service \
  -H "Content-Type: application/json" \
  -d '{
    "client_id_or_service_name": "weather-api",
    "status": ["healthy", "warning"],
    "timeout": 20.0
  }'

# Agent 级别等待
curl -X POST http://localhost:18200/for_agent/my-agent/wait_service \
  -H "Content-Type: application/json" \
  -d '{
    "client_id_or_service_name": "local-tool",
    "status": "healthy",
    "timeout": 30.0,
    "raise_on_timeout": false
  }'
```

## 🔧 高级用法

### 服务启动流程

```python
def deploy_service_with_wait():
    """部署服务并等待就绪"""
    store = MCPStore.setup_store()
    context = store.for_store()
    
    # 1. 注册服务
    print("📝 注册服务...")
    context.add_service({
        "mcpServers": {
            "new-service": {
                "url": "https://api.example.com/mcp",
                "transport": "sse"
            }
        }
    })
    
    # 2. 等待服务初始化完成
    print("⏳ 等待服务初始化...")
    try:
        result = context.wait_service(
            "new-service",
            ["healthy", "warning"],  # 接受健康或警告状态
            timeout=60.0,           # 给足够的启动时间
            raise_on_timeout=True   # 启动失败时抛出异常
        )
        
        if result:
            print("✅ 服务部署成功并已就绪")
            
            # 3. 验证服务功能
            tools = context.list_tools("new-service")
            print(f"🔧 服务提供 {len(tools)} 个工具")
            
            return True
            
    except TimeoutError:
        print("❌ 服务启动超时，回滚部署")
        context.delete_config("new-service")
        return False
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

# 使用
success = deploy_service_with_wait()
```

### 健康检查流程

```python
def health_check_workflow():
    """健康检查工作流"""
    store = MCPStore.setup_store()
    context = store.for_store()
    
    services = context.list_services()
    unhealthy_services = []
    
    for service in services:
        print(f"🔍 检查服务: {service.name}")
        
        # 等待服务达到健康状态（短超时）
        is_healthy = context.wait_service(
            service.name,
            "healthy",
            timeout=5.0,  # 短超时快速检查
            raise_on_timeout=False
        )
        
        if not is_healthy:
            print(f"⚠️ 服务 {service.name} 不健康")
            unhealthy_services.append(service.name)
            
            # 尝试等待恢复
            print(f"⏳ 等待 {service.name} 恢复...")
            recovered = context.wait_service(
                service.name,
                ["healthy", "warning"],
                timeout=30.0,
                raise_on_timeout=False
            )
            
            if recovered:
                print(f"✅ 服务 {service.name} 已恢复")
                unhealthy_services.remove(service.name)
            else:
                print(f"❌ 服务 {service.name} 恢复失败")
    
    return unhealthy_services

# 使用
unhealthy = health_check_workflow()
if unhealthy:
    print(f"🚨 发现 {len(unhealthy)} 个不健康的服务: {unhealthy}")
```

### 批量服务管理

```python
async def batch_service_management():
    """批量服务管理"""
    store = MCPStore.setup_store()
    context = store.for_store()
    
    # 要管理的服务列表
    services_config = [
        {"name": "auth-service", "url": "https://auth.example.com/mcp"},
        {"name": "data-service", "url": "https://data.example.com/mcp"},
        {"name": "ai-service", "url": "https://ai.example.com/mcp"}
    ]
    
    # 1. 批量注册服务
    print("📝 批量注册服务...")
    for config in services_config:
        context.add_service({
            "mcpServers": {
                config["name"]: {
                    "url": config["url"],
                    "transport": "sse"
                }
            }
        })
    
    # 2. 并发等待所有服务就绪
    print("⏳ 等待所有服务就绪...")
    wait_tasks = [
        context.wait_service_async(
            config["name"],
            ["healthy", "warning"],
            timeout=45.0,
            raise_on_timeout=False
        )
        for config in services_config
    ]
    
    results = await asyncio.gather(*wait_tasks)
    
    # 3. 检查结果
    ready_services = []
    failed_services = []
    
    for i, (config, result) in enumerate(zip(services_config, results)):
        if result:
            ready_services.append(config["name"])
            print(f"✅ {config['name']} 已就绪")
        else:
            failed_services.append(config["name"])
            print(f"❌ {config['name']} 启动失败")
    
    print(f"\n📊 批量启动结果:")
    print(f"   成功: {len(ready_services)}/{len(services_config)}")
    print(f"   失败: {len(failed_services)}/{len(services_config)}")
    
    return ready_services, failed_services

# 使用
ready, failed = asyncio.run(batch_service_management())
```

## ⚙️ 配置和优化

### 轮询配置

`wait_service` 使用 200ms 的轮询间隔来检查服务状态，这个间隔在响应速度和系统负载之间取得了良好的平衡。

### 超时建议

根据不同场景建议的超时时间：

| 场景 | 建议超时 | 说明 |
|------|----------|------|
| 快速健康检查 | 3-5秒 | 检查服务当前状态 |
| 服务启动等待 | 30-60秒 | 等待服务完全启动 |
| 网络服务连接 | 15-30秒 | 考虑网络延迟 |
| 本地服务启动 | 10-20秒 | 本地进程启动时间 |
| 批量操作 | 60-120秒 | 多个服务并发启动 |

### 性能优化

```python
# 对于频繁的状态检查，使用较短的超时
quick_check = context.wait_service("service", "healthy", timeout=3.0)

# 对于关键流程，使用较长的超时和异常处理
critical_wait = context.wait_service(
    "critical-service", 
    "healthy", 
    timeout=60.0, 
    raise_on_timeout=True
)

# 对于非关键服务，接受多种状态
flexible_wait = context.wait_service(
    "optional-service",
    ["healthy", "warning", "initializing"],
    timeout=20.0
)
```

## 🔗 相关文档

- [服务生命周期](service-lifecycle.md) - 了解服务状态详情
- [健康检查](check-services.md) - 学习健康检查机制
- [服务重启](restart-service.md) - 掌握服务重启方法
- [服务管理](../management/service-management.md) - 完整的服务管理指南

## 🎯 最佳实践

1. **合理设置超时**: 根据服务类型和网络环境设置合适的超时时间
2. **使用多状态等待**: 对于非关键场景，接受 `["healthy", "warning"]` 等多种状态
3. **异常处理**: 在关键流程中使用 `raise_on_timeout=True` 并妥善处理异常
4. **并发等待**: 使用异步版本并发等待多个服务，提高效率
5. **状态验证**: 等待成功后，可以进一步验证服务功能（如列出工具）

通过 `wait_service` 功能，您可以构建更可靠的自动化流程，确保服务在使用前已经完全就绪。
