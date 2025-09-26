# MCPStoreContext 类

MCPStoreContext 是 MCPStore 的核心操作上下文类，提供所有服务和工具管理功能。

## 类定义

```python
class MCPStoreContext:
    """
    MCPStore 操作上下文
    提供服务管理、工具操作、LangChain集成等功能
    """
    def __init__(self, store: MCPStore, context_type: ContextType = ContextType.STORE, agent_id: str = None):
        """
        初始化上下文
        
        Args:
            store: MCPStore 实例
            context_type: 上下文类型 (STORE 或 AGENT)
            agent_id: Agent ID (仅在 AGENT 模式下使用)
        """
```

## 上下文类型

### ContextType 枚举

```python
from enum import Enum

class ContextType(Enum):
    STORE = "store"    # Store 级别上下文
    AGENT = "agent"    # Agent 级别上下文
```

### 上下文差异

| 特性 | Store 模式 | Agent 透明代理模式 |
|------|------------|------------|
| 服务范围 | 全局所有服务 | 仅该 Agent 的服务 |
| 服务命名 | 完整名称（含后缀） | 本地名称（隐藏后缀） |
| 数据隔离 | 全局共享 | Agent 级别隔离 |
| 配置文件 | 影响 mcp.json | 同时影响多个配置文件 |
| 工具解析 | 直接匹配 | 智能解析（精确→前缀→模糊） |
| 服务映射 | 无映射 | 本地服务名→全局服务名 |
| 客户端管理 | 直接使用 Agent ID | 使用 global_agent_store_id |

## 核心属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `context_type` | ContextType | 上下文类型 |
| `agent_id` | str | Agent ID（Agent 模式下） |
| `_store` | MCPStore | 关联的 MCPStore 实例 |
| `_service_mapper` | ServiceNameMapper | 服务名称映射器 |
| `_sync_helper` | AsyncSyncHelper | 同步/异步转换助手 |

## 服务操作方法

### add_service()

添加 MCP 服务，支持多种配置格式。

```python
def add_service(self, config: Union[ServiceConfigUnion, List[str], None] = None,
               json_file: str = None) -> 'MCPStoreContext'
```

**参数**:
- `config`: 服务配置（字典、列表或None）
- `json_file`: JSON配置文件路径

**返回**: 当前上下文实例（支持链式调用）

### list_services()

获取服务列表。

```python
def list_services() -> List[ServiceInfo]
```

**返回**: ServiceInfo 对象列表

### get_service_info()

获取指定服务的详细信息。

```python
def get_service_info(name: str) -> Any
```

**参数**:
- `name`: 服务名称

**返回**: 服务详细信息字典

### restart_service()

重启指定服务。

```python
def restart_service(name: str) -> bool
```

**参数**:
- `name`: 服务名称

**返回**: 重启是否成功

### check_services()

执行服务健康检查。

```python
def check_services() -> Dict[str, Any]
```

**返回**: 健康检查结果字典

### wait_service()

等待服务达到指定状态。

```python
def wait_service(client_id_or_service_name: str,
                status: Union[str, List[str]] = 'healthy',
                timeout: float = 10.0,
                raise_on_timeout: bool = False) -> bool
```

**参数**:
- `client_id_or_service_name`: 服务的 client_id 或服务名（智能识别）
- `status`: 目标状态，可以是单个状态或状态列表，默认 'healthy'
- `timeout`: 超时时间（秒），默认 10.0
- `raise_on_timeout`: 超时时是否抛出异常，默认 False

**返回**: 成功达到目标状态返回 True，超时返回 False

**异常**:
- `TimeoutError`: 当 `raise_on_timeout=True` 且超时时抛出
- `ValueError`: 当参数无法解析时抛出

### delete_service()

删除指定服务。

```python
def delete_service(name: str) -> bool
```

**参数**:
- `name`: 服务名称

**返回**: 删除是否成功

### update_service()

更新服务配置。

```python
def update_service(name: str, config: Dict[str, Any]) -> bool
```

**参数**:
- `name`: 服务名称
- `config`: 新的服务配置

**返回**: 更新是否成功

### patch_service()

部分更新服务配置。

```python
def patch_service(name: str, updates: Dict[str, Any]) -> bool
```

**参数**:
- `name`: 服务名称
- `updates`: 要更新的配置项

**返回**: 更新是否成功

### get_service_status()

获取单个服务的状态信息。

```python
def get_service_status(name: str) -> dict
```

**参数**:
- `name`: 服务名称

**返回**: 服务状态信息字典

### show_config()

显示配置信息。

```python
def show_config(scope: str = "all") -> Dict[str, Any]
```

**参数**:
- `scope`: 配置范围 ("all", "mcp", "agent", "client")

**返回**: 配置信息字典

### reset_config()

重置配置。

```python
def reset_config(scope: str = "all") -> bool
```

**参数**:
- `scope`: 重置范围 ("all", "mcp", "agent", "client")

**返回**: 重置是否成功

### show_mcpconfig()

显示 MCP 配置。

```python
def show_mcpconfig() -> Dict[str, Any]
```

**返回**: MCP 配置字典

## 工具操作方法

### list_tools()

获取工具列表。

```python
def list_tools() -> List[ToolInfo]
```

**返回**: ToolInfo 对象列表

### call_tool()

调用指定工具，支持 Agent 透明代理。

```python
def call_tool(tool_name: str, args: Union[Dict[str, Any], str] = None, **kwargs) -> Any
```

**参数**:
- `tool_name`: 工具名称（Agent 模式下支持智能解析）
- `args`: 工具参数
- `**kwargs`: 额外参数

**返回**: 工具执行结果

**Agent 透明代理特性**:
- **智能工具解析**: 支持精确匹配、前缀匹配、模糊匹配
- **自动服务映射**: 本地服务名自动映射到全局服务名
- **透明执行**: Agent 无需关心底层服务名称映射

### use_tool()

调用工具的向后兼容别名。

```python
def use_tool(tool_name: str, args: Union[Dict[str, Any], str] = None, **kwargs) -> Any
```

**说明**: 与 `call_tool()` 功能完全相同，保持向后兼容性。

### get_tools_with_stats()

获取工具列表及统计信息。

```python
def get_tools_with_stats() -> Dict[str, Any]
```

**返回**: 包含工具列表和统计信息的字典

### batch_add_services()

批量添加服务。

```python
def batch_add_services(services: List[Union[str, Dict[str, Any]]]) -> Dict[str, Any]
```

**参数**:
- `services`: 服务配置列表

**返回**: 批量添加结果字典

### get_system_stats()

获取系统统计信息。

```python
def get_system_stats() -> Dict[str, Any]
```

**返回**: 系统统计信息字典，包含服务数量、工具数量、性能指标等

## FastMCP 核心功能

### list_resources()

列出可用的资源。

```python
def list_resources(
    self,
    service_name: Optional[str] = None
) -> Dict[str, Any]
```

**参数**:
- `service_name`: 指定服务名称（可选）

**返回**: 资源列表字典

**示例**:
```python
# 列出所有资源
resources = context.list_resources()

# 列出特定服务的资源
weather_resources = context.list_resources("weather")
```

### list_resource_templates()

列出可用的资源模板。

```python
def list_resource_templates(
    self,
    service_name: Optional[str] = None
) -> Dict[str, Any]
```

**参数**:
- `service_name`: 指定服务名称（可选）

**返回**: 资源模板列表字典

### read_resource()

读取资源内容。

```python
def read_resource(
    self,
    uri: str,
    service_name: Optional[str] = None
) -> Dict[str, Any]
```

**参数**:
- `uri`: 资源URI
- `service_name`: 指定服务名称（可选）

**返回**: 资源内容字典

**示例**:
```python
# 读取文件资源
content = context.read_resource("file://config.json")

# 从特定服务读取资源
data = context.read_resource("weather://current", "weather")
```

### list_prompts()

列出可用的提示词。

```python
def list_prompts(
    self,
    service_name: Optional[str] = None
) -> Dict[str, Any]
```

**参数**:
- `service_name`: 指定服务名称（可选）

**返回**: 提示词列表字典

**示例**:
```python
# 列出所有提示词
prompts = context.list_prompts()

# 列出特定服务的提示词
weather_prompts = context.list_prompts("weather")
```

### get_prompt()

获取提示词内容。

```python
def get_prompt(
    self,
    name: str,
    arguments: Optional[Dict[str, Any]] = None,
    service_name: Optional[str] = None
) -> Dict[str, Any]
```

**参数**:
- `name`: 提示词名称
- `arguments`: 提示词参数（可选）
- `service_name`: 指定服务名称（可选）

**返回**: 提示词内容字典

**示例**:
```python
# 获取提示词
prompt = context.get_prompt("weather_prompt", {
    "location": "Beijing",
    "format": "json"
})

# 从特定服务获取提示词
weather_prompt = context.get_prompt("current_weather", {"city": "Shanghai"}, "weather")
```

### list_changed_tools()

列出变化的工具。

```python
def list_changed_tools(
    self,
    service_name: Optional[str] = None,
    force_refresh: bool = False
) -> Dict[str, Any]
```

**参数**:
- `service_name`: 指定服务名称（可选）
- `force_refresh`: 强制刷新（默认False）

**返回**: 工具变化信息字典

**示例**:
```python
# 检查工具变化
changes = context.list_changed_tools()

# 强制刷新检查
force_changes = context.list_changed_tools(force_refresh=True)
```

## LangChain 集成

### for_langchain()

获取 LangChain 适配器。

```python
def for_langchain() -> 'LangChainAdapter'
```

**返回**: LangChainAdapter 实例

**使用示例**:
```python
# 获取 LangChain 工具
tools = store.for_store().for_langchain().list_tools()

# 链式调用
tools = (store.for_store()
         .add_service(config)
         .for_langchain()
         .list_tools())
```

## 高级功能方法

### create_simple_tool()

创建简化版本的工具。

```python
def create_simple_tool(
    self,
    original_tool: str,
    friendly_name: Optional[str] = None
) -> 'MCPStoreContext'
```

**参数**:
- `original_tool`: 原始工具名称
- `friendly_name`: 友好名称（可选）

**返回**: 返回自身，支持链式调用

**示例**:
```python
# 创建简化工具
context.create_simple_tool("complex_weather_api", "weather")

# 使用简化后的工具
result = context.call_tool("weather", {"city": "Beijing"})
```

### create_safe_tool()

创建安全版本的工具（带验证）。

```python
def create_safe_tool(
    self,
    original_tool: str,
    validation_rules: Dict[str, Any]
) -> 'MCPStoreContext'
```

**参数**:
- `original_tool`: 原始工具名称
- `validation_rules`: 验证规则字典

**返回**: 返回自身，支持链式调用

**示例**:
```python
# 创建安全工具
validation_rules = {
    "max_file_size": 1024,
    "allowed_extensions": [".txt", ".json"]
}
context.create_safe_tool("file_operation", validation_rules)
```

### switch_environment()

切换运行环境。

```python
def switch_environment(
    self,
    environment: str
) -> 'MCPStoreContext'
```

**参数**:
- `environment`: 环境名称

**返回**: 返回自身，支持链式调用

**示例**:
```python
# 切换到生产环境
context.switch_environment("production")

# 切换到开发环境
context.switch_environment("development")
```

### import_api()

导入OpenAPI服务。

```python
def import_api(
    self,
    api_url: str,
    api_name: Optional[str] = None
) -> 'MCPStoreContext'
```

**参数**:
- `api_url`: API URL
- `api_name`: API名称（可选）

**返回**: 返回自身，支持链式调用

**示例**:
```python
# 导入OpenAPI服务
context.import_api("https://api.example.com/openapi.json", "external_api")

# 使用导入的API
result = context.call_tool("external_api_get_data", {"id": 123})
```

### setup_auth()

设置认证。

```python
def setup_auth(
    self,
    auth_type: str = "bearer",
    enabled: bool = True
) -> 'MCPStoreContext'
```

**参数**:
- `auth_type`: 认证类型（默认"bearer"）
- `enabled`: 是否启用（默认True）

**返回**: 返回自身，支持链式调用

### get_performance_report()

获取性能报告。

```python
def get_performance_report(self) -> Dict[str, Any]
```

**返回**: 性能报告字典

### get_usage_stats()

获取使用统计。

```python
def get_usage_stats(self) -> Dict[str, Any]
```

**返回**: 使用统计字典

### enable_caching()

启用缓存。

```python
def enable_caching(
    self,
    patterns: Optional[Dict[str, int]] = None
) -> 'MCPStoreContext'
```

**参数**:
- `patterns`: 缓存模式字典（可选）

**返回**: 返回自身，支持链式调用

## 异步版本方法

所有同步方法都有对应的异步版本，方法名后缀为 `_async`：

```python
# 异步服务操作
async def add_service_async(config, json_file=None) -> 'MCPStoreContext'
async def list_services_async() -> List[ServiceInfo]
async def get_service_info_async(name: str) -> Any
async def restart_service_async(name: str) -> bool
async def check_services_async() -> Dict[str, Any]
async def wait_service_async(client_id_or_service_name: str, status='healthy', timeout=10.0, raise_on_timeout=False) -> bool

# 异步工具操作
async def list_tools_async() -> List[ToolInfo]
async def call_tool_async(tool_name: str, args=None, **kwargs) -> Any
async def use_tool_async(tool_name: str, args=None, **kwargs) -> Any
async def get_tools_with_stats_async() -> Dict[str, Any]
async def batch_add_services_async(services) -> Dict[str, Any]
```

## 使用示例

### Store 级别操作

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 获取 Store 上下文
store_context = store.for_store()

# 添加服务
store_context.add_service({
    "name": "weather-api",
    "url": "https://weather.example.com/mcp"
})

# 列出服务和工具
services = store_context.list_services()
tools = store_context.list_tools()

# 调用工具
result = store_context.call_tool("get_weather", {"city": "北京"})

print(f"Store 级别: {len(services)} 服务, {len(tools)} 工具")
```

### Agent 透明代理操作

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 获取 Agent 上下文（透明代理模式）
agent_context = store.for_agent("my_agent")

# Agent 级别操作（透明代理）
agent_context.add_service({
    "name": "weather-api",  # 本地服务名
    "url": "https://weather.example.com/mcp"
})
# 实际注册为: "weather-apibyagent_my_agent"

# Agent 只能看到自己的服务（隐藏后缀）
agent_services = agent_context.list_services()
agent_tools = agent_context.list_tools()

# 透明代理工具调用
result = agent_context.call_tool("get_weather", {"city": "北京"})
# 自动解析工具名称，映射服务名称，透明执行

print(f"Agent 透明代理: {len(agent_services)} 服务, {len(agent_tools)} 工具")
print(f"工具调用结果: {result}")
```

### 链式调用

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# Store 级别链式调用
result = (store.for_store()
          .add_service({"name": "service1", "url": "https://api1.com/mcp"})
          .add_service({"name": "service2", "url": "https://api2.com/mcp"})
          .list_tools())

print(f"链式调用获得 {len(result)} 个工具")

# Agent 透明代理链式调用
agent_result = (store.for_agent("test_agent")
                .add_service({"name": "agent_service", "url": "https://agent.com/mcp"})
                .call_tool("some_tool", {"param": "value"}))  # 透明代理执行

print(f"Agent 透明代理工具调用结果: {agent_result}")
```

### 异步操作

```python
import asyncio
from mcpstore import MCPStore

async def async_operations():
    store = MCPStore.setup_store()
    
    # 异步添加服务
    context = await store.for_store().add_service_async({
        "name": "async-service",
        "url": "https://async.example.com/mcp"
    })
    
    # 异步获取工具列表
    tools = await context.list_tools_async()
    
    # 异步调用工具
    result = await context.call_tool_async("async_tool", {"data": "test"})
    
    print(f"异步操作: {len(tools)} 工具, 结果: {result}")

# 运行异步示例
asyncio.run(async_operations())
```

## 注意事项

1. **上下文隔离**: Store 和 Agent 上下文完全隔离
2. **链式调用**: 大部分方法返回上下文实例，支持链式操作
3. **异步支持**: 所有方法都有异步版本
4. **Agent 透明代理**: Agent 模式下自动处理服务名称映射和工具解析
5. **智能工具解析**: 支持精确匹配、前缀匹配、模糊匹配三种解析策略
6. **客户端管理**: Agent 透明代理自动管理客户端注册和映射
7. **向后兼容**: 保留 `use_tool()` 等向后兼容方法

## 相关文档

- [MCPStore 类](mcpstore-class.md) - 主入口类
- [数据模型](data-models.md) - 数据结构定义
- [服务注册](../services/registration/add-service.md) - 服务注册方法

## 下一步

- 了解 [数据模型定义](data-models.md)
- 学习 [服务注册方法](../services/registration/add-service.md)
- 查看 [工具调用方法](../tools/usage/call-tool.md)
