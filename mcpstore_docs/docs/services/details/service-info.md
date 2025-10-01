# service_info()

获取服务的详细信息。

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

返回 `ServiceInfo` 对象，包含以下信息：

```python
ServiceInfo:
    # 标识信息
    name: str                           # 服务名称
    client_id: str                      # 客户端ID
    
    # 连接配置
    url: Optional[str]                  # 远程服务URL
    command: Optional[str]              # 本地服务命令
    args: Optional[List[str]]           # 命令参数
    transport_type: TransportType       # 传输类型
    
    # 状态信息
    status: ServiceConnectionState      # 连接状态
    tool_count: int                     # 工具数量
    keep_alive: bool                    # 保持连接
    
    # 环境配置
    working_dir: Optional[str]          # 工作目录
    env: Optional[Dict[str, str]]       # 环境变量
    package_name: Optional[str]         # 包名
    
    # 生命周期数据
    state_metadata: ServiceStateMetadata # 状态元数据
    
    # 原始配置
    config: Dict[str, Any]              # 完整配置
```

## 使用示例

### Store级别获取服务详情

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

# 获取服务详情
info = svc.service_info()
print(f"服务名称: {info.name}")
print(f"服务状态: {info.status}")
print(f"工具数量: {info.tool_count}")
print(f"传输类型: {info.transport_type}")
print(f"服务URL: {info.url}")
```

### Agent级别获取服务详情

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

# 获取服务详情
info = svc.service_info()
print(f"Agent ID: {info.state_metadata.agent_id}")
print(f"服务详情: {info}")
```

### 检查服务配置信息

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "calculator": {
            "command": "python",
            "args": ["calculator.py"],
            "env": {"DEBUG": "true"},
            "working_dir": "/workspace"
        }
    }
})

# 等待并获取服务
store.for_store().wait_service("calculator")
svc = store.for_store().find_service("calculator")

# 获取详细配置
info = svc.service_info()
print(f"命令: {info.command}")
print(f"参数: {info.args}")
print(f"环境变量: {info.env}")
print(f"工作目录: {info.working_dir}")
```

### 查看服务元数据

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 获取详情
info = svc.service_info()

# 查看状态元数据
if info.state_metadata:
    metadata = info.state_metadata
    print(f"响应时间: {metadata.response_time}")
    print(f"连续成功次数: {metadata.consecutive_successes}")
    print(f"连续失败次数: {metadata.consecutive_failures}")
    print(f"最后成功时间: {metadata.last_success_time}")
    print(f"最后失败时间: {metadata.last_failure_time}")
```

## ServiceInfo 属性详解

### 基础属性
- `name`: 服务名称
- `client_id`: 唯一客户端标识
- `status`: 当前连接状态（HEALTHY/WARNING/RECONNECTING/UNREACHABLE等）
- `tool_count`: 服务提供的工具数量

### 连接配置
- `url`: 远程服务的 URL（HTTP/WebSocket）
- `command`: 本地服务的启动命令
- `args`: 命令行参数列表
- `transport_type`: 传输协议类型

### 环境配置
- `working_dir`: 服务的工作目录
- `env`: 环境变量字典
- `keep_alive`: 是否保持长连接

### 元数据
- `state_metadata`: 详细的状态元数据，包含性能指标、时间戳等

## 相关方法

- [service_status()](service-status.md) - 获取服务状态
- [find_service()](../listing/find-service.md) - 查找服务
- [list_services()](../listing/list-services.md) - 列出所有服务
- [check_health()](../health/check-health.md) - 检查服务健康

## 注意事项

1. **调用前提**: 必须先通过 `find_service()` 获取 ServiceProxy 对象
2. **信息实时性**: 返回的是当前缓存的服务信息
3. **Agent隔离**: Agent级别只能看到该Agent的服务信息
4. **元数据完整性**: state_metadata 可能为空，需要判空处理

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

