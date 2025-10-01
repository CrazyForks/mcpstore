# wait_service()

等待服务达到指定状态。

## 方法特性

- ✅ **调用方式**: Context 方法
- ✅ **异步版本**: `wait_service_async()`
- ✅ **Store级别**: `store.for_store().wait_service()`
- ✅ **Agent级别**: `store.for_agent("agent1").wait_service()`
- 📁 **文件位置**: `service_management.py`
- 🏷️ **所属类**: `ServiceManagementMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `client_id_or_service_name` | `str` | ✅ | - | 服务的client_id或服务名（智能识别） |
| `status` | `str` \| `List[str]` | ❌ | `'healthy'` | 目标状态，可以是单个状态或状态列表 |
| `timeout` | `float` | ❌ | `10.0` | 超时时间（秒） |
| `raise_on_timeout` | `bool` | ❌ | `False` | 超时时是否抛出异常 |

## 返回值

- **成功**: 返回 `True`，表示服务达到目标状态
- **超时**: 返回 `False`（当 `raise_on_timeout=False` 时）
- **异常**: 抛出 `TimeoutError`（当 `raise_on_timeout=True` 时）

## 使用示例

### Store级别基本等待

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

# 等待服务变为健康状态
success = store.for_store().wait_service("weather", "healthy", timeout=30.0)

if success:
    print("✅ Weather服务已就绪")
else:
    print("❌ Weather服务启动超时")
```

### Agent级别等待

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

# Agent模式等待服务
success = store.for_agent("agent1").wait_service(
    "weather",  # 本地服务名
    "healthy",
    timeout=20.0
)

if success:
    print("✅ Agent Weather服务已就绪")
else:
    print("❌ Agent Weather服务启动超时")
```

### 等待多种状态

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

# 等待服务达到健康或警告状态（任一即可）
success = store.for_store().wait_service(
    "weather",
    ["healthy", "warning"],  # 状态列表
    timeout=60.0
)

if success:
    print("✅ Weather服务可用")
```

### 等待状态变化（change模式）

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

# 等待状态发生任何变化
# 只要状态与调用瞬间的"初始状态"不同就返回 True
success = store.for_store().wait_service(
    "weather",
    status="change",  # 特殊模式
    timeout=5.0
)

if success:
    print("✅ 服务状态已变化")
```

### 超时异常处理

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

try:
    # 等待服务，超时时抛出异常
    store.for_store().wait_service(
        "weather",
        "healthy",
        timeout=10.0,
        raise_on_timeout=True
    )
    print("✅ 服务已就绪")
    
except TimeoutError:
    print("❌ 服务启动超时，请检查服务配置")
    
except ValueError as e:
    print(f"❌ 参数错误: {e}")
```

### 完整的服务启动流程

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 1. 添加服务
print("📝 添加服务...")
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 2. 等待服务启动完成
print("⏳ 等待服务启动...")
success = store.for_store().wait_service("weather", "healthy", timeout=60.0)

if success:
    print("✅ 服务启动成功")
    
    # 3. 验证服务可用性
    svc = store.for_store().find_service("weather")
    tools = svc.list_tools()
    print(f"🛠️ 可用工具: {len(tools)} 个")
    
    # 4. 获取服务状态
    status = svc.service_status()
    print(f"📊 服务状态: {status}")
else:
    print("❌ 服务启动失败")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_wait_service():
    # 初始化
    store = MCPStore.setup_store()
    
    # 添加服务
    store.for_store().add_service({
        "mcpServers": {
            "weather": {"url": "https://mcpstore.wiki/mcp"}
        }
    })
    
    # 异步等待服务
    success = await store.for_store().wait_service_async(
        "weather",
        "healthy",
        timeout=30.0
    )
    
    if success:
        print("✅ 服务异步等待成功")
        return True
    else:
        print("❌ 服务异步等待超时")
        return False

# 运行异步等待
result = asyncio.run(async_wait_service())
```

### 批量等待多个服务

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

# 批量等待
service_names = ["weather", "calculator"]
results = {}

print("⏳ 批量等待服务启动...")
for name in service_names:
    success = store.for_store().wait_service(name, "healthy", timeout=30.0)
    results[name] = success
    
    icon = "✅" if success else "❌"
    print(f"{icon} {name}: {'就绪' if success else '超时'}")

# 统计
success_count = sum(1 for v in results.values() if v)
print(f"\n📊 成功: {success_count}/{len(service_names)}")
```

### 监控等待过程

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

# 监控等待过程
print("⏳ 开始等待服务...")
start_time = time.time()

success = store.for_store().wait_service("weather", "healthy", timeout=30.0)

elapsed_time = time.time() - start_time

if success:
    print(f"✅ 服务就绪 (耗时: {elapsed_time:.2f}秒)")
else:
    print(f"❌ 服务超时 (等待时间: {elapsed_time:.2f}秒)")
```

## 等待模式说明

### 1. 默认模式（等待健康）
```python
store.for_store().wait_service("weather")  # 默认等待 healthy 状态
```

### 2. 指定状态模式
```python
# 等待单个状态
store.for_store().wait_service("weather", "reconnecting")

# 等待多个状态之一
store.for_store().wait_service("weather", ["healthy", "warning"])
```

### 3. 变化模式（change）
```python
# 只要状态与初始状态不同就返回
store.for_store().wait_service("weather", status="change", timeout=5)
```

## 支持的状态值（7 状态体系）

| 状态值 | 描述 | 常用场景 |
|--------|------|----------|
| `initializing` | 初始化中 | 服务首次连接 |
| `healthy` | 健康 | 服务正常运行 ⭐️ |
| `warning` | 警告 | 响应慢但仍可用 |
| `reconnecting` | 重连中 | 连接失败后重连 |
| `unreachable` | 不可达 | 进入长周期重试 |
| `disconnecting` | 断开中 | 正在断开连接 |
| `disconnected` | 已断开 | 连接已断开 |

> ⭐️ 最常用的是等待 `healthy` 状态

## 使用场景

### 1. 服务启动后立即使用
添加服务后等待就绪，确保服务可用再进行操作。

### 2. 服务重启后等待恢复
重启服务后等待服务重新健康。

### 3. 批量服务初始化
批量添加多个服务后，等待所有服务就绪。

### 4. 状态转换确认
等待服务从某个状态转换到另一个状态。

## 相关方法

- [service_status()](../details/service-status.md) - 获取当前服务状态
- [check_services()](../health/check-services.md) - 检查所有服务状态
- [add_service()](../registration/add-service.md) - 添加服务
- [restart_service()](../management/restart-service.md) - 重启服务

## 注意事项

1. **智能识别**: 参数支持client_id或服务名，系统会自动识别
2. **轮询机制**: 内部使用轮询检查状态，间隔约200ms（高频检查）
3. **Agent映射**: Agent模式下自动处理服务名映射
4. **超时设置**: 合理设置超时时间，避免无限等待
5. **状态列表**: 支持等待多种状态中的任意一种
6. **异步支持**: 提供异步版本适配异步应用场景

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

