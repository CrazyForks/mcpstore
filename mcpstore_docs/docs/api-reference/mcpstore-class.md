# MCPStore 类

MCPStore 是 MCPStore 库的核心类，提供智能体工具服务存储和上下文切换功能。

## 类定义

```python
class MCPStore:
    """
    MCPStore - Intelligent Agent Tool Service Store
    Provides context switching entry points and common operations
    """
    def __init__(self, orchestrator: MCPOrchestrator, config: MCPConfig,
                 tool_record_max_file_size: int = 30, tool_record_retention_days: int = 7):
        """
        初始化 MCPStore 实例

        Args:
            orchestrator: MCP编排器实例
            config: MCP配置实例
            tool_record_max_file_size: 工具记录文件最大大小(MB)，默认30MB
            tool_record_retention_days: 工具记录保留天数，默认7天
        """
```

## 静态工厂方法

### setup_store()

推荐的初始化方法，使用静态工厂模式创建 MCPStore 实例。

```python
@staticmethod
def setup_store(mcp_config_file: str = None, debug: bool = False, standalone_config=None,
               tool_record_max_file_size: int = 30, tool_record_retention_days: int = 7,
               monitoring: dict = None) -> MCPStore
```

#### 参数详解

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `mcp_config_file` | str | None | 自定义 mcp.json 配置文件路径，支持数据空间隔离 |
| `debug` | bool | False | 是否启用调试日志 |
| `standalone_config` | Any | None | 独立配置对象，不依赖环境变量 |
| `tool_record_max_file_size` | int | 30 | 工具记录文件最大大小(MB)，-1表示无限制 |
| `tool_record_retention_days` | int | 7 | 工具记录保留天数，-1表示不删除 |
| `monitoring` | dict | None | 监控配置字典 |

#### 监控配置参数

```python
monitoring = {
    "health_check_seconds": 30,        # 健康检查间隔(秒)
    "tools_update_hours": 2,           # 工具更新间隔(小时)
    "reconnection_seconds": 60,        # 重连间隔(秒)
    "cleanup_hours": 24,               # 清理间隔(小时)
    "enable_tools_update": True,       # 是否启用工具更新
    "enable_reconnection": True,       # 是否启用重连
    "update_tools_on_reconnection": True  # 重连时是否更新工具
}
```

## 核心属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `orchestrator` | MCPOrchestrator | MCP编排器，处理连接和调用 |
| `config` | MCPConfig | MCP配置管理器 |
| `registry` | ServiceRegistry | 服务注册表，管理服务和工具状态 |
| `client_manager` | ClientManager | 客户端管理器，处理Agent-Client映射 |
| `local_service_manager` | LocalServiceManager | 本地服务管理器 |
| `session_manager` | SessionManager | 会话管理器 |
| `cache_manager` | ServiceCacheManager | 缓存管理器 |
| `transaction_manager` | CacheTransactionManager | 缓存事务管理器 |
| `query` | SmartCacheQuery | 智能查询接口 |

## 上下文切换方法

### for_store()

获取 Store 级别的操作上下文，用于全局服务管理。

```python
def for_store() -> MCPStoreContext
```

**返回**: Store 级别的 MCPStoreContext 实例

### for_agent()

获取 Agent 级别的操作上下文，用于独立的 Agent 服务管理。

```python
def for_agent(agent_id: str) -> MCPStoreContext
```

**参数**:
- `agent_id` (str): Agent 标识符

**返回**: Agent 级别的 MCPStoreContext 实例

## 使用示例

### 基本初始化

```python
from mcpstore import MCPStore

# 使用默认配置初始化
store = MCPStore.setup_store()

# 启用调试模式
store = MCPStore.setup_store(debug=True)

# 使用自定义配置文件
store = MCPStore.setup_store(mcp_config_file="custom_mcp.json")
```

### 数据空间隔离

```python
from mcpstore import MCPStore

# 项目A的独立数据空间
project_a_store = MCPStore.setup_store(mcp_config_file="project_a/mcp.json")

# 项目B的独立数据空间
project_b_store = MCPStore.setup_store(mcp_config_file="project_b/mcp.json")

# 两个项目完全隔离，互不影响
project_a_store.for_store().add_service({"name": "service1", "url": "http://api1.com/mcp"})
project_b_store.for_store().add_service({"name": "service1", "url": "http://api2.com/mcp"})
```

### 上下文切换

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# Store 级别操作 - 全局服务管理
store_context = store.for_store()
store_context.add_service({"name": "global-service", "url": "http://api.com/mcp"})
store_services = store_context.list_services()

# Agent 级别操作 - 独立服务空间
agent_context = store.for_agent("my_agent")
agent_context.add_service({"name": "agent-service", "url": "http://agent-api.com/mcp"})
agent_services = agent_context.list_services()

print(f"Store 服务数: {len(store_services)}")
print(f"Agent 服务数: {len(agent_services)}")
```

### 链式调用

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# Store 级别链式调用
tools = (store.for_store()
         .add_service({"name": "weather", "url": "https://weather.com/mcp"})
         .add_service({"name": "calculator", "command": "npx", "args": ["-y", "calc-mcp"]})
         .list_tools())

print(f"链式调用获得 {len(tools)} 个工具")

# Agent 级别链式调用
agent_tools = (store.for_agent("my_agent")
               .add_service({"name": "agent-tool", "url": "https://agent.com/mcp"})
               .list_tools())

print(f"Agent 链式调用获得 {len(agent_tools)} 个工具")
```

### 监控配置

```python
from mcpstore import MCPStore

# 自定义监控配置
monitoring_config = {
    "health_check_seconds": 15,        # 更频繁的健康检查
    "tools_update_hours": 1,           # 每小时更新工具
    "reconnection_seconds": 30,        # 更快的重连
    "enable_tools_update": True,
    "enable_reconnection": True,
    "update_tools_on_reconnection": True
}

store = MCPStore.setup_store(
    debug=True,
    monitoring=monitoring_config,
    tool_record_max_file_size=50,      # 50MB 工具记录
    tool_record_retention_days=14      # 保留14天
)

print("✅ MCPStore 初始化完成，使用自定义监控配置")
```

## API 服务器集成

### start_api_server()

启动内置的 HTTP API 服务器。

```python
def start_api_server(self, host="0.0.0.0", port=18200, reload=False,
                    log_level="info", auto_open_browser=False, show_startup_info=True):
    """启动HTTP API服务器，提供RESTful接口访问当前store实例"""
```

#### 使用示例

```python
from mcpstore import MCPStore

# 初始化 MCPStore
store = MCPStore.setup_store()

# 添加一些服务
store.for_store().add_service({
    "name": "demo-service",
    "url": "https://demo.example.com/mcp"
})

# 启动 API 服务器
store.start_api_server(
    host="0.0.0.0",
    port=18200,
    show_startup_info=False  # 简洁输出
)

# 服务器启动后，可以通过 HTTP API 访问
# GET http://localhost:18200/for_store/list_services
# POST http://localhost:18200/for_store/call_tool
```

### 生产环境部署

```python
from mcpstore import MCPStore

# 生产环境配置
prod_store = MCPStore.setup_store(
    mcp_config_file="production/mcp.json",
    debug=False,  # 关闭调试日志
    tool_record_max_file_size=100,  # 100MB
    tool_record_retention_days=30,  # 保留30天
    monitoring={
        "health_check_seconds": 60,     # 生产环境较长的检查间隔
        "tools_update_hours": 4,        # 4小时更新一次
        "reconnection_seconds": 120,    # 2分钟重连间隔
        "enable_tools_update": True,
        "enable_reconnection": True
    }
)

# 启动生产 API 服务器
prod_store.start_api_server(
    host="0.0.0.0",
    port=18200,
    log_level="warning",  # 只显示警告和错误
    show_startup_info=False
)
```

## 内部组件访问

MCPStore 提供对内部组件的直接访问，用于高级操作：

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 访问编排器
orchestrator = store.orchestrator

# 访问注册表
registry = store.registry

# 访问客户端管理器
client_manager = store.client_manager

# 访问缓存管理器
cache_manager = store.cache_manager

# 访问智能查询接口
query = store.query

# 示例：直接查询缓存
cached_services = query.get_all_services()
print(f"缓存中的服务: {len(cached_services)} 个")
```

## 数据空间管理

### 多项目隔离

```python
from mcpstore import MCPStore

# 为不同项目创建完全隔离的 MCPStore 实例
projects = {
    "web_app": MCPStore.setup_store(mcp_config_file="projects/web_app/mcp.json"),
    "mobile_app": MCPStore.setup_store(mcp_config_file="projects/mobile_app/mcp.json"),
    "data_pipeline": MCPStore.setup_store(mcp_config_file="projects/data_pipeline/mcp.json")
}

# 每个项目独立配置服务
projects["web_app"].for_store().add_service({
    "name": "web-api",
    "url": "https://web-api.example.com/mcp"
})

projects["mobile_app"].for_store().add_service({
    "name": "mobile-api",
    "url": "https://mobile-api.example.com/mcp"
})

projects["data_pipeline"].for_store().add_service({
    "name": "data-processor",
    "command": "python",
    "args": ["data_processor.py"]
})

# 各项目的数据完全隔离
for project_name, project_store in projects.items():
    services = project_store.for_store().list_services()
    print(f"{project_name}: {len(services)} 个服务")
```

## 注意事项

1. **静态工厂模式**: 推荐使用 `setup_store()` 而非直接构造函数
2. **上下文切换**: 通过 `for_store()` 和 `for_agent()` 实现不同级别的操作
3. **数据空间隔离**: 每个 mcp_config_file 对应独立的数据空间
4. **延迟初始化**: 上下文实例按需创建和缓存
5. **API 服务器**: 内置 HTTP API 服务器，支持 RESTful 接口

## 相关文档

- [MCPStoreContext 类](context-class.md) - 上下文操作类
- [数据模型](data-models.md) - 数据结构定义
- [REST API](rest-api.md) - HTTP API 接口

## 下一步

- 了解 [上下文操作](context-class.md)
- 学习 [服务注册](../services/registration/register-service.md)
- 查看 [工具调用](../tools/usage/call-tool.md)
```
