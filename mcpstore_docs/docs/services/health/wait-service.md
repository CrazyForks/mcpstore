# wait_service()

等待服务达到指定状态。

## 方法特性

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

### 基本等待服务健康

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 等待服务变为健康状态
success = store.for_store().wait_service("weather", "healthy", timeout=30.0)
if success:
    print("Weather服务已就绪")
else:
    print("Weather服务启动超时")
```

### 等待多种状态

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 等待服务达到健康或警告状态（任一即可）
success = store.for_store().wait_service(
    "weather",
    ["healthy", "warning"],
    timeout=60.0
)
if success:
    print("Weather服务可用")
```

### Agent级别等待

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式等待服务
success = store.for_agent("agent1").wait_service(
    "weather-local",  # 本地服务名
    "healthy",
    timeout=20.0
)
if success:
    print("Agent Weather服务已就绪")
```

### 等待模式（status 参数）

- `"change"` 模式（功能A）
  - 语义：只要状态与调用瞬间的“初始状态”不同就返回 True
  - 适合：快速确认是否进入下一阶段（如从 initializing → reconnecting/healthy）
  - 用法示例：
    ```python
    store.for_store().wait_service("weather", status="change", timeout=5)
    ```

- 指定状态（功能B）
  - 语义：直到达到给定状态（或状态列表）才返回 True
  - 例如等待进入重连：
    ```python
    store.for_store().wait_service("weather", status="reconnecting", timeout=20)
    ```


### 超时异常处理

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

try:
    # 等待服务，超时时抛出异常
    store.for_store().wait_service(
        "weather",
        "healthy",
        timeout=10.0,
        raise_on_timeout=True
    )
    print("服务已就绪")
except TimeoutError:
    print("服务启动超时，请检查服务配置")
except ValueError as e:
    print(f"参数错误: {e}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_wait_service():
    # 初始化
    store = MCPStore.setup_store()

    # 异步等待服务
    success = await store.for_store().wait_service_async(
        "weather",
        "healthy",
        timeout=30.0
    )

    if success:
        print("服务异步等待成功")
        return True
    else:
        print("服务异步等待超时")
        return False

# 运行异步等待
result = asyncio.run(async_wait_service())
```

### 服务启动流程

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://api.weather.com/mcp"}
    }
})

# 等待服务启动完成
print("等待Weather服务启动...")
success = store.for_store().wait_service("weather", "healthy", timeout=60.0)

if success:
    print("✅ Weather服务启动成功")
    # 继续后续操作
    tools = store.for_store().list_tools()
    print(f"可用工具: {len(tools)} 个")
else:
    print("❌ Weather服务启动失败")
```

## 支持的状态值（7 状态体系）

| 状态值 | 描述 |
|--------|------|
| `initializing` | 初始化中（首次连接窗口） |
| `healthy` | 健康 |
| `warning` | 警告（响应慢但正常） |
| `reconnecting` | 重连中（初次失败或连续失败后进入） |
| `unreachable` | 不可达（进入长周期重试） |
| `disconnecting` | 断开连接中 |
| `disconnected` | 已断开 |

## 相关方法

- [get_service_status()](get-service-status.md) - 获取当前服务状态
- [check_services()](check-services.md) - 检查所有服务状态
- [restart_service()](../management/restart-service.md) - 重启服务

## 注意事项

1. **智能识别**: 参数支持client_id或服务名，系统会自动识别
2. **轮询机制**: 内部使用轮询检查状态，间隔约200ms（高频，不会出现“隔很久才检查一次”）
3. **Agent映射**: Agent模式下自动处理服务名映射
4. **超时处理**: 合理设置超时时间，避免无限等待
5. **状态列表**: 支持等待多种状态中的任意一种
