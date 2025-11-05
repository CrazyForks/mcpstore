## wait_service - 服务等待

如何在 MCPStore 等待服务达到指定状态。

### SDK

同步：
  - `store.for_store().wait_service(name, status="healthy", timeout=..., raise_on_timeout=False) -> bool`
  - `store.for_agent("agent_id").wait_service(name, status="healthy", timeout=..., raise_on_timeout=False) -> bool`

异步：
  - `await store.for_store().wait_service_async(name, status=..., timeout=..., raise_on_timeout=False) -> bool`
  - `await store.for_agent("agent_id").wait_service_async(name, status=..., timeout=..., raise_on_timeout=False) -> bool`

### 参数

| 参数名 | 类型 | 说明 | 默认值 |
|---|---|---|---|
| `client_id_or_service_name` | str | 服务的 client_id 或服务名（智能识别；Agent 视角支持本地服务名） | - |
| `status` | str/list[str] | 目标状态；也可为 `"change"` 表示任意状态变化即返回 | `"healthy"` |
| `timeout` | float | 超时时间（秒） | `10.0` |
| `raise_on_timeout` | bool | 超时时是否抛出异常 | `False` |

### 返回值

- 返回 `True`：达到目标状态
- 返回 `False`：未达目标且未抛异常
- 抛出 `TimeoutError`：当 `raise_on_timeout=True` 且超时

### 视角

- Store 视角：`store.for_store().wait_service("weather", "healthy", timeout=30)`
- Agent 视角：`store.for_agent("agent1").wait_service("weather", "healthy", timeout=30)`  （Agent 使用本地服务名，内部自动映射）

### 使用示例

基础等待（Store）：
```python
store.for_store().wait_service("weather")  # 默认为 healthy
```

指定状态列表：
```python
store.for_store().wait_service("weather", ["healthy", "warning"], timeout=60)
```

变化模式（任意状态变化即返回）：
```python
store.for_store().wait_service("weather", status="change", timeout=5)
```

异常模式（超时抛出）：
```python
store.for_store().wait_service("weather", "healthy", timeout=10, raise_on_timeout=True)
```

异步：
```python
await store.for_agent("agent1").wait_service_async("weather", "healthy", timeout=20)
```

### 状态值（7 状态体系）

| 状态值 | 描述 |
|---|---|
| `initializing` | 初始化中 |
| `healthy` | 健康（推荐等待目标） |
| `warning` | 警告（可用但偏慢） |
| `reconnecting` | 重连中 |
| `unreachable` | 不可达（长周期重试） |
| `disconnecting` | 断开中 |
| `disconnected` | 已断开 |

### 相关方法

| 场景/方法 | 同步方法 |
|---|---|
| 获取服务状态 | `store.for_store().get_service_status(name)` |
| 检查所有服务 | `store.for_store().check_services()` |
| 添加服务 | `store.for_store().add_service(config=...)` |
| 重启服务 | `store.for_store().restart_service(name)` |

### 注意事项

- 参数智能识别：支持传入 client_id 或服务名
- Agent 视角自动做本地名→全局名映射
- 合理设置 `timeout` 与 `raise_on_timeout`，避免阻塞
- 高并发/批量等待建议使用异步版本
- `status="change"` 返回条件为“与调用瞬间的初始状态不同”


