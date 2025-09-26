# 数据模型

MCPStore 使用 Pydantic 模型定义所有数据结构，确保类型安全和数据验证。

## 服务相关模型

### TransportType

传输类型枚举，定义服务的连接方式。

```python
from enum import Enum

class TransportType(str, Enum):
    STREAMABLE_HTTP = "streamable_http"    # HTTP 流式传输
    STDIO = "stdio"                        # 标准输入输出
    STDIO_PYTHON = "stdio_python"          # Python 标准输入输出
    STDIO_NODE = "stdio_node"              # Node.js 标准输入输出
    STDIO_SHELL = "stdio_shell"            # Shell 标准输入输出
```

### ServiceConnectionState

服务连接生命周期状态枚举。

```python
from enum import Enum

class ServiceConnectionState(str, Enum):
    INITIALIZING = "initializing"      # 初始化中：配置验证完成，执行首次连接
    HEALTHY = "healthy"                # 健康：连接正常，心跳成功
    WARNING = "warning"                # 警告：偶发心跳失败，但未达到重连阈值
    RECONNECTING = "reconnecting"      # 重连中：连续失败达到阈值，正在重连
    UNREACHABLE = "unreachable"        # 不可达：重连失败，进入长周期重试
    DISCONNECTING = "disconnecting"    # 断开中：执行优雅关闭
    DISCONNECTED = "disconnected"      # 已断开：服务终止，等待手动删除
```

### ServiceStateMetadata

服务状态元数据模型。

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ServiceStateMetadata(BaseModel):
    consecutive_failures: int = 0                    # 连续失败次数
    consecutive_successes: int = 0                   # 连续成功次数
    last_ping_time: Optional[datetime] = None       # 最后心跳时间
    last_success_time: Optional[datetime] = None    # 最后成功时间
    last_failure_time: Optional[datetime] = None    # 最后失败时间
    response_time: Optional[float] = None           # 响应时间(毫秒)
    error_message: Optional[str] = None             # 错误信息
    reconnect_attempts: int = 0                     # 重连尝试次数
    next_retry_time: Optional[datetime] = None      # 下次重试时间
    state_entered_time: Optional[datetime] = None   # 状态进入时间
    disconnect_reason: Optional[str] = None         # 断开原因
    service_config: Dict[str, Any] = {}             # 服务配置信息
    service_name: Optional[str] = None              # 服务名称
    agent_id: Optional[str] = None                  # Agent ID
    last_health_check: Optional[datetime] = None    # 最后健康检查时间
    last_response_time: Optional[float] = None      # 最后响应时间
```

### ServiceInfo

服务信息模型，包含服务的完整状态和配置。

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ServiceInfo(BaseModel):
    url: str = ""                                           # 服务URL
    name: str                                               # 服务名称
    transport_type: TransportType                           # 传输类型
    status: ServiceConnectionState                          # 连接状态
    tool_count: int                                         # 工具数量
    keep_alive: bool                                        # 是否保持连接
    working_dir: Optional[str] = None                       # 工作目录
    env: Optional[Dict[str, str]] = None                    # 环境变量
    last_heartbeat: Optional[datetime] = None               # 最后心跳时间
    command: Optional[str] = None                           # 启动命令
    args: Optional[List[str]] = None                        # 命令参数
    package_name: Optional[str] = None                      # 包名
    state_metadata: Optional[ServiceStateMetadata] = None  # 状态元数据
    last_state_change: Optional[datetime] = None            # 最后状态变更时间
    client_id: Optional[str] = None                         # 客户端ID
    config: Dict[str, Any] = Field(default_factory=dict)   # 完整配置信息
```

### ServiceInfoResponse

单个服务详细信息响应模型。

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ServiceInfoResponse(BaseModel):
    service: Optional[ServiceInfo] = Field(None, description="服务信息")
    tools: List[Dict[str, Any]] = Field(..., description="服务提供的工具列表")
    connected: bool = Field(..., description="服务连接状态")
    success: bool = Field(True, description="操作是否成功")
    message: Optional[str] = Field(None, description="响应消息")
```

### ServicesResponse

服务列表响应模型。

```python
from pydantic import BaseModel, Field
from typing import List

class ServicesResponse(BaseModel):
    services: List[ServiceInfo] = Field(..., description="服务列表")
    total_services: int = Field(..., description="服务总数")
    total_tools: int = Field(..., description="工具总数")
    success: bool = Field(True, description="操作是否成功")
```

## 工具相关模型

### ToolInfo

工具信息模型。

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ToolInfo(BaseModel):
    name: str                                      # 工具名称
    description: str                               # 工具描述
    service_name: str                              # 所属服务名
    client_id: Optional[str] = None                # 客户端ID
    inputSchema: Optional[Dict[str, Any]] = None   # 输入参数Schema
```

### ToolsResponse

工具列表响应模型。

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ToolsResponse(BaseModel):
    tools: List[ToolInfo] = Field(..., description="工具列表")
    total_tools: int = Field(..., description="工具总数")
    success: bool = Field(True, description="操作是否成功")
    message: Optional[str] = Field(None, description="响应消息")
```

### ToolExecutionRequest

工具执行请求模型。

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ToolExecutionRequest(BaseModel):
    tool_name: str = Field(..., description="工具名称（FastMCP原始名称）")
    service_name: str = Field(..., description="服务名称")
    args: Dict[str, Any] = Field(default_factory=dict, description="工具参数")
    agent_id: Optional[str] = Field(None, description="Agent ID")
    client_id: Optional[str] = Field(None, description="客户端ID")
    
    # FastMCP 标准参数
    timeout: Optional[float] = Field(None, description="超时时间（秒）")
    progress_handler: Optional[Any] = Field(None, description="进度处理器")
    raise_on_error: bool = Field(True, description="是否在错误时抛出异常")
```

## 通用响应模型

### BaseResponse

统一基础响应模型。

```python
from pydantic import BaseModel, Field
from typing import Optional

class BaseResponse(BaseModel):
    success: bool = Field(..., description="操作是否成功")
    message: Optional[str] = Field(None, description="响应消息")
```

### APIResponse

通用API响应模型。

```python
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class APIResponse(BaseResponse):
    data: Optional[Any] = Field(None, description="响应数据")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据信息")
    execution_info: Optional[Dict[str, Any]] = Field(None, description="执行信息")
```

### ListResponse

列表响应模型（泛型）。

```python
from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic

T = TypeVar('T')

class ListResponse(BaseResponse, Generic[T]):
    items: List[T] = Field(..., description="数据项列表")
    total: int = Field(..., description="总数量")
```

### DataResponse

单数据项响应模型（泛型）。

```python
from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar('T')

class DataResponse(BaseResponse, Generic[T]):
    data: T = Field(..., description="数据项")
```

### RegistrationResponse

注册操作响应模型。

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RegistrationResponse(BaseResponse):
    client_id: str = Field(..., description="客户端ID")
    service_names: List[str] = Field(..., description="服务名称列表")
    config: Dict[str, Any] = Field(..., description="配置信息")
```

### ExecutionResponse

执行操作响应模型。

```python
from pydantic import BaseModel, Field
from typing import Optional, Any

class ExecutionResponse(BaseResponse):
    result: Optional[Any] = Field(None, description="执行结果")
    error: Optional[str] = Field(None, description="错误信息")
```

### ConfigResponse

配置响应模型。

```python
from pydantic import BaseModel, Field
from typing import Dict, Any

class ConfigResponse(BaseResponse):
    client_id: str = Field(..., description="客户端ID")
    config: Dict[str, Any] = Field(..., description="配置信息")
```

### HealthResponse

健康检查响应模型。

```python
from pydantic import BaseModel, Field
from typing import Optional

class HealthResponse(BaseResponse):
    service_name: str = Field(..., description="服务名称")
    status: str = Field(..., description="健康状态")
    last_check: Optional[str] = Field(None, description="最后检查时间")
```

## 使用示例

### 创建服务信息

```python
from mcpstore.core.models.service import ServiceInfo, TransportType, ServiceConnectionState
from datetime import datetime

service_info = ServiceInfo(
    name="weather-api",
    url="https://weather.example.com/mcp",
    transport_type=TransportType.STREAMABLE_HTTP,
    status=ServiceConnectionState.HEALTHY,
    tool_count=5,
    keep_alive=True,
    last_heartbeat=datetime.now(),
    client_id="client_123"
)

print(f"服务: {service_info.name}, 状态: {service_info.status}")
```

### 创建工具信息

```python
from mcpstore.core.models.tool import ToolInfo

tool_info = ToolInfo(
    name="get_weather",
    description="获取天气信息",
    service_name="weather-api",
    client_id="client_123",
    inputSchema={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名称"}
        },
        "required": ["city"]
    }
)

print(f"工具: {tool_info.name}, 描述: {tool_info.description}")
```

### 处理响应数据

```python
from mcpstore.core.models.common import APIResponse, ExecutionResponse

# API 响应
api_response = APIResponse(
    success=True,
    message="操作成功",
    data={"result": "北京今天晴天"},
    metadata={"execution_time": 0.5}
)

# 执行响应
exec_response = ExecutionResponse(
    success=True,
    result={"temperature": 25, "weather": "晴天"},
    error=None
)

print(f"API响应: {api_response.success}, 数据: {api_response.data}")
print(f"执行结果: {exec_response.result}")
```

## 注意事项

1. **类型安全**: 所有模型使用 Pydantic 确保类型安全
2. **数据验证**: 自动验证输入数据的格式和类型
3. **序列化**: 支持 JSON 序列化和反序列化
4. **文档生成**: 自动生成 API 文档
5. **向后兼容**: 保持模型的向后兼容性

## 相关文档

- [MCPStore 类](mcpstore-class.md) - 主入口类
- [MCPStoreContext 类](context-class.md) - 上下文操作类
- [REST API](rest-api.md) - HTTP API 接口

## 下一步

- 了解 [REST API 接口](rest-api.md)
- 学习 [服务注册方法](../services/registration/register-service.md)
- 查看 [工具调用方法](../tools/usage/call-tool.md)
