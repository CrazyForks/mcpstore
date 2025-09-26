# get_service_info() - 服务详细信息查询

MCPStore 的 `get_service_info()` 方法提供单个服务的详细信息查询，返回完整的服务配置、状态元数据、工具列表和连接信息。

## 🎯 方法签名

### 同步版本

```python
def get_service_info(self, name: str) -> Optional[ServiceInfo]
```

### 异步版本

```python
async def get_service_info_async(self, name: str) -> Optional[ServiceInfo]
```

#### 参数说明

- `name`: 服务名称
  - **Store 模式**: 使用完整服务名称（如 `weather-apibyagent1`）
  - **Agent 模式**: 使用本地服务名称（如 `weather-api`）

#### 返回值

- **类型**: `Optional[ServiceInfo]`
- **说明**: 服务信息对象，如果服务不存在则返回 `None`

## 🤖 Agent 模式支持

### 支持状态
- ✅ **完全支持** - `get_service_info()` 在 Agent 模式下完全可用

### Agent 模式调用
```python
# Agent 模式调用（使用本地服务名）
service_info = store.for_agent("research_agent").get_service_info("weather-api")

# 对比 Store 模式调用（使用完整服务名）
service_info = store.for_store().get_service_info("weather-apibyagent1")
```

### 模式差异说明
- **Store 模式**: 使用完整服务名称（如 `weather-apibyagent1`），可查询任何服务
- **Agent 模式**: 使用本地服务名称（如 `weather-api`），只能查询当前 Agent 的服务
- **主要区别**: Agent 模式自动进行名称映射，提供透明的本地视图

### 名称映射示例

#### Store 模式查询
```python
# 查询全局服务（需要完整名称）
service_info = store.for_store().get_service_info("weather-apibyagent1")
if service_info:
    print(f"服务名: {service_info.name}")           # weather-apibyagent1
    print(f"客户端ID: {service_info.client_id}")    # agent1:weather-api
```

#### Agent 模式查询
```python
# 查询 Agent 服务（使用本地名称）
service_info = store.for_agent("agent1").get_service_info("weather-api")
if service_info:
    print(f"服务名: {service_info.name}")           # weather-api (本地视图)
    print(f"客户端ID: {service_info.client_id}")    # agent1:weather-api (实际ID)
```

### 使用建议
- **Agent 开发**: 推荐使用 Agent 模式，使用简洁的本地服务名
- **系统管理**: 使用 Store 模式，通过完整名称管理所有服务
- **服务查询**: Agent 模式下无需关心服务名后缀，系统自动处理映射

## 📊 ServiceInfo 详细结构

```python
class ServiceInfo:
    # 基础标识
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

## 🚀 使用示例

### 基础服务信息查询

```python
from mcpstore import MCPStore

def basic_service_info():
    """基础服务信息查询"""
    store = MCPStore.setup_store()
    
    service_name = "weather-api"
    
    # 获取服务详细信息
    service_info = store.for_store().get_service_info(service_name)
    
    if service_info:
        print(f"📦 服务信息: {service_info.name}")
        print(f"   状态: {service_info.status}")
        print(f"   类型: {'远程' if service_info.url else '本地'}")
        print(f"   工具数: {service_info.tool_count}")
        print(f"   客户端ID: {service_info.client_id}")
        
        if service_info.url:
            print(f"   URL: {service_info.url}")
        elif service_info.command:
            print(f"   命令: {service_info.command}")
            if service_info.args:
                print(f"   参数: {' '.join(service_info.args)}")
    else:
        print(f"❌ 服务 '{service_name}' 不存在")

# 使用
basic_service_info()
```

### Agent 模式服务查询

```python
def agent_service_info():
    """Agent 模式服务信息查询"""
    store = MCPStore.setup_store()
    
    agent_id = "research_agent"
    service_name = "weather-api"  # 使用本地名称
    
    # Agent 使用本地名称查询
    service_info = store.for_agent(agent_id).get_service_info(service_name)
    
    if service_info:
        print(f"🤖 Agent '{agent_id}' 的服务信息:")
        print(f"   服务名: {service_info.name}")  # 显示本地名称
        print(f"   实际客户端ID: {service_info.client_id}")  # 显示全局ID
        print(f"   状态: {service_info.status}")
        
        # 显示生命周期信息
        if service_info.state_metadata:
            metadata = service_info.state_metadata
            print(f"   连续成功: {metadata.consecutive_successes}")
            print(f"   连续失败: {metadata.consecutive_failures}")
            print(f"   响应时间: {metadata.response_time}ms")
            if metadata.last_ping_time:
                print(f"   最后检查: {metadata.last_ping_time}")
    else:
        print(f"❌ Agent '{agent_id}' 没有服务 '{service_name}'")

# 使用
agent_service_info()
```

### 完整配置信息展示

```python
def detailed_service_config():
    """详细服务配置信息"""
    store = MCPStore.setup_store()
    
    service_name = "weather-api"
    service_info = store.for_store().get_service_info(service_name)
    
    if not service_info:
        print(f"❌ 服务 '{service_name}' 不存在")
        return
    
    print(f"🔍 服务 '{service_name}' 详细配置")
    print("=" * 50)
    
    # 基础信息
    print("📋 基础信息:")
    print(f"   名称: {service_info.name}")
    print(f"   客户端ID: {service_info.client_id}")
    print(f"   状态: {service_info.status}")
    print(f"   传输类型: {service_info.transport_type}")
    print(f"   工具数量: {service_info.tool_count}")
    print(f"   保持连接: {service_info.keep_alive}")
    print()
    
    # 连接配置
    print("🔗 连接配置:")
    if service_info.url:
        print(f"   URL: {service_info.url}")
    elif service_info.command:
        print(f"   命令: {service_info.command}")
        if service_info.args:
            print(f"   参数: {service_info.args}")
        if service_info.working_dir:
            print(f"   工作目录: {service_info.working_dir}")
        if service_info.env:
            print(f"   环境变量:")
            for key, value in service_info.env.items():
                print(f"     {key}: {value}")
    print()
    
    # 状态元数据
    if service_info.state_metadata:
        metadata = service_info.state_metadata
        print("📊 状态元数据:")
        print(f"   连续成功: {metadata.consecutive_successes}")
        print(f"   连续失败: {metadata.consecutive_failures}")
        print(f"   重连次数: {metadata.reconnect_attempts}")
        print(f"   响应时间: {metadata.response_time}ms")
        
        if metadata.last_success_time:
            print(f"   最后成功: {metadata.last_success_time}")
        if metadata.last_failure_time:
            print(f"   最后失败: {metadata.last_failure_time}")
        if metadata.error_message:
            print(f"   错误信息: {metadata.error_message}")
        if metadata.next_retry_time:
            print(f"   下次重试: {metadata.next_retry_time}")
        print()
    
    # 原始配置
    print("⚙️ 原始配置:")
    import json
    print(json.dumps(service_info.config, indent=2, ensure_ascii=False))

# 使用
detailed_service_config()
```

### 服务健康状态检查

```python
def check_service_health():
    """检查服务健康状态"""
    store = MCPStore.setup_store()
    
    service_name = "weather-api"
    service_info = store.for_store().get_service_info(service_name)
    
    if not service_info:
        print(f"❌ 服务 '{service_name}' 不存在")
        return
    
    print(f"🏥 服务 '{service_name}' 健康检查")
    print("=" * 40)
    
    # 基础状态
    status_icon = {
        "healthy": "✅",
        "warning": "⚠️",
        "reconnecting": "🔄",
        "unreachable": "❌",
        "initializing": "🔧",
        "disconnecting": "⏹️",
        "disconnected": "💤"
    }.get(service_info.status, "❓")
    
    print(f"状态: {status_icon} {service_info.status}")
    
    if service_info.state_metadata:
        metadata = service_info.state_metadata
        
        # 性能指标
        print(f"响应时间: {metadata.response_time or 'N/A'}ms")
        
        # 可靠性指标
        total_attempts = metadata.consecutive_successes + metadata.consecutive_failures
        if total_attempts > 0:
            success_rate = metadata.consecutive_successes / total_attempts * 100
            print(f"成功率: {success_rate:.1f}%")
        
        # 故障信息
        if metadata.consecutive_failures > 0:
            print(f"⚠️ 连续失败: {metadata.consecutive_failures} 次")
        
        if metadata.reconnect_attempts > 0:
            print(f"🔄 重连次数: {metadata.reconnect_attempts}")
        
        if metadata.error_message:
            print(f"❌ 最后错误: {metadata.error_message}")
        
        # 时间信息
        if metadata.last_ping_time:
            from datetime import datetime
            time_diff = datetime.now() - metadata.last_ping_time
            print(f"⏰ 最后检查: {time_diff.total_seconds():.1f} 秒前")

# 使用
check_service_health()
```

### 批量服务信息查询

```python
def batch_service_info():
    """批量服务信息查询"""
    store = MCPStore.setup_store()
    
    # 获取所有服务名称
    services = store.for_store().list_services()
    service_names = [s.name for s in services]
    
    print(f"📊 批量查询 {len(service_names)} 个服务的详细信息")
    print("=" * 60)
    
    for service_name in service_names:
        service_info = store.for_store().get_service_info(service_name)
        
        if service_info:
            print(f"🔸 {service_info.name}")
            print(f"   状态: {service_info.status}")
            print(f"   工具: {service_info.tool_count} 个")
            
            if service_info.state_metadata:
                metadata = service_info.state_metadata
                print(f"   响应: {metadata.response_time or 'N/A'}ms")
                print(f"   失败: {metadata.consecutive_failures} 次")
            
            print(f"   ID: {service_info.client_id}")
            print()

# 使用
batch_service_info()
```

### 异步服务信息查询

```python
import asyncio

async def async_service_info():
    """异步服务信息查询"""
    store = MCPStore.setup_store()
    
    service_name = "weather-api"
    
    # 异步获取服务信息
    service_info = await store.for_store().get_service_info_async(service_name)
    
    if service_info:
        print(f"🔄 异步获取服务信息: {service_info.name}")
        print(f"   状态: {service_info.status}")
        print(f"   工具数: {service_info.tool_count}")
    else:
        print(f"❌ 异步查询失败: 服务 '{service_name}' 不存在")

# 使用
# asyncio.run(async_service_info())
```

### 服务配置对比

```python
def compare_service_configs():
    """对比不同上下文中的服务配置"""
    store = MCPStore.setup_store()
    
    service_name = "weather-api"
    agent_id = "test_agent"
    
    # Store 级别查询
    store_service = store.for_store().get_service_info(service_name)
    
    # Agent 级别查询
    agent_service = store.for_agent(agent_id).get_service_info(service_name)
    
    print("🔍 服务配置对比")
    print("=" * 40)
    
    if store_service:
        print(f"🏪 Store 级别:")
        print(f"   名称: {store_service.name}")
        print(f"   客户端ID: {store_service.client_id}")
        print(f"   状态: {store_service.status}")
    else:
        print("🏪 Store 级别: 服务不存在")
    
    print()
    
    if agent_service:
        print(f"🤖 Agent '{agent_id}' 级别:")
        print(f"   名称: {agent_service.name}")
        print(f"   客户端ID: {agent_service.client_id}")
        print(f"   状态: {agent_service.status}")
    else:
        print(f"🤖 Agent '{agent_id}' 级别: 服务不存在")
    
    # 分析差异
    if store_service and agent_service:
        print(f"\n📊 差异分析:")
        print(f"   名称相同: {store_service.name == agent_service.name}")
        print(f"   客户端ID相同: {store_service.client_id == agent_service.client_id}")
        print(f"   状态相同: {store_service.status == agent_service.status}")

# 使用
compare_service_configs()
```

## 📊 API 响应格式

### 成功响应

```json
{
  "success": true,
  "data": {
    "name": "weather-api",
    "status": "healthy",
    "transport": "streamable-http",
    "tool_count": 5,
    "client_id": "global_agent_store:weather-api",
    "config": {
      "url": "https://weather.example.com/mcp",
      "headers": {"Authorization": "Bearer token"}
    },
    "state_metadata": {
      "consecutive_successes": 10,
      "consecutive_failures": 0,
      "response_time": 150.5,
      "last_ping_time": "2024-01-15T10:30:00Z"
    }
  },
  "message": "Service info retrieved successfully"
}
```

### 服务不存在响应

```json
{
  "success": false,
  "data": null,
  "message": "Service 'non-existent-service' not found"
}
```

## 🎯 性能特点

- **平均耗时**: 0.001秒
- **缓存机制**: 内存缓存，实时数据
- **数据完整性**: 包含完整的配置和状态信息
- **上下文感知**: 自动处理 Store/Agent 名称映射

## 🔗 相关文档

- [list_services()](list-services.md) - 获取服务列表
- [服务注册](../registration/add-service.md) - 了解服务注册
- [服务生命周期](../lifecycle/service-lifecycle.md) - 理解服务状态
- [服务管理](../management/service-management.md) - 服务管理操作

## 🎯 下一步

- 学习 [服务列表查询](list-services.md)
- 了解 [服务健康检查](../lifecycle/check-services.md)
- 掌握 [服务管理操作](../management/service-management.md)
- 查看 [工具列表查询](../../tools/listing/list-tools.md)
