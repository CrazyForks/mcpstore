# API 参考文档

## 📋 概述

本文档提供了 MCPStore 的完整 API 参考，包括所有类、方法、参数和返回值的详细说明。

## 🏗️ 核心类

### MCPStore

MCPStore 的主要类，提供所有核心功能。

```python
class MCPStore:
    """MCPStore 主类"""
    
    def __init__(self, config: Optional[Dict] = None, config_file: Optional[str] = None):
        """
        初始化 MCPStore
        
        Args:
            config: 配置字典
            config_file: 配置文件路径
        """
```

#### 服务管理方法

##### add_service()

```python
def add_service(self, config: Union[Dict, str, Path]) -> bool:
    """
    添加 MCP 服务
    
    Args:
        config: 服务配置，支持以下格式：
            - 字典格式：{"mcpServers": {"service_name": {...}}}
            - JSON 文件路径
            - 配置字典
    
    Returns:
        bool: 添加是否成功
    
    Raises:
        ConfigurationError: 配置格式错误
        ServiceRegistrationError: 服务注册失败
    
    Example:
        >>> store.add_service({
        ...     "mcpServers": {
        ...         "filesystem": {
        ...             "command": "npx",
        ...             "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        ...         }
        ...     }
        ... })
        True
    """
```

##### list_services()

```python
def list_services(self) -> List[Dict[str, Any]]:
    """
    列出所有已注册的服务
    
    Returns:
        List[Dict]: 服务列表，每个服务包含以下字段：
            - name (str): 服务名称
            - status (str): 服务状态
            - command (str): 启动命令
            - args (List[str]): 命令参数
            - pid (Optional[int]): 进程ID
            - uptime (float): 运行时间（秒）
    
    Example:
        >>> services = store.list_services()
        >>> print(services[0]['name'])
        'filesystem'
    """
```

##### start_service()

```python
def start_service(self, service_name: str, timeout: Optional[float] = 30.0) -> bool:
    """
    启动指定服务
    
    Args:
        service_name: 服务名称
        timeout: 启动超时时间（秒）
    
    Returns:
        bool: 启动是否成功
    
    Raises:
        ServiceNotFoundError: 服务不存在
        ServiceStartError: 服务启动失败
        ServiceTimeoutError: 启动超时
    
    Example:
        >>> store.start_service("filesystem")
        True
    """
```

##### stop_service()

```python
def stop_service(self, service_name: str, timeout: Optional[float] = 30.0, force: bool = False) -> bool:
    """
    停止指定服务
    
    Args:
        service_name: 服务名称
        timeout: 停止超时时间（秒）
        force: 是否强制停止
    
    Returns:
        bool: 停止是否成功
    
    Raises:
        ServiceNotFoundError: 服务不存在
        ServiceStopError: 服务停止失败
    
    Example:
        >>> store.stop_service("filesystem")
        True
    """
```

##### restart_service()

```python
def restart_service(self, service_name: str, timeout: Optional[float] = 60.0) -> bool:
    """
    重启指定服务
    
    Args:
        service_name: 服务名称
        timeout: 重启超时时间（秒）
    
    Returns:
        bool: 重启是否成功
    
    Raises:
        ServiceNotFoundError: 服务不存在
        ServiceRestartError: 服务重启失败
    
    Example:
        >>> store.restart_service("filesystem")
        True
    """
```

##### get_service_status()

```python
def get_service_status(self, service_name: str) -> str:
    """
    获取服务状态
    
    Args:
        service_name: 服务名称
    
    Returns:
        str: 服务状态，可能的值：
            - "not_started": 未启动
            - "starting": 启动中
            - "running": 运行中
            - "stopping": 停止中
            - "stopped": 已停止
            - "error": 错误状态
    
    Raises:
        ServiceNotFoundError: 服务不存在
    
    Example:
        >>> status = store.get_service_status("filesystem")
        >>> print(status)
        'running'
    """
```

##### get_service_info()

```python
def get_service_info(self, service_name: str) -> Dict[str, Any]:
    """
    获取服务详细信息
    
    Args:
        service_name: 服务名称
    
    Returns:
        Dict: 服务信息，包含以下字段：
            - name (str): 服务名称
            - status (str): 服务状态
            - command (str): 启动命令
            - args (List[str]): 命令参数
            - env (Dict[str, str]): 环境变量
            - pid (Optional[int]): 进程ID
            - uptime (float): 运行时间
            - tools (List[Dict]): 可用工具列表
            - last_error (Optional[str]): 最后错误信息
    
    Raises:
        ServiceNotFoundError: 服务不存在
    
    Example:
        >>> info = store.get_service_info("filesystem")
        >>> print(f"工具数量: {len(info['tools'])}")
    """
```

#### 工具管理方法

##### list_tools()

```python
def list_tools(self, service_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    列出可用工具
    
    Args:
        service_name: 可选，指定服务名称以过滤工具
    
    Returns:
        List[Dict]: 工具列表，每个工具包含以下字段：
            - name (str): 工具名称
            - description (str): 工具描述
            - service_name (str): 所属服务
            - parameters (Dict): 参数定义
            - returns (Dict): 返回值定义
    
    Example:
        >>> tools = store.list_tools()
        >>> filesystem_tools = store.list_tools(service_name="filesystem")
    """
```

##### get_tool_info()

```python
def get_tool_info(self, tool_name: str, service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    获取工具详细信息
    
    Args:
        tool_name: 工具名称
        service_name: 可选，服务名称
    
    Returns:
        Dict: 工具信息，包含以下字段：
            - name (str): 工具名称
            - description (str): 工具描述
            - service_name (str): 所属服务
            - parameters (Dict): 参数定义
            - returns (Dict): 返回值定义
            - examples (List[Dict]): 使用示例
    
    Raises:
        ToolNotFoundError: 工具不存在
    
    Example:
        >>> info = store.get_tool_info("read_file")
        >>> print(info['description'])
    """
```

##### call_tool()

```python
def call_tool(self, tool_name: str, arguments: Dict[str, Any], **options) -> Any:
    """
    调用指定工具
    
    Args:
        tool_name: 工具名称
        arguments: 工具参数
        **options: 额外选项
            - timeout (float): 调用超时时间
            - retry_count (int): 重试次数
            - service_name (str): 指定服务名称
    
    Returns:
        Any: 工具执行结果
    
    Raises:
        ToolNotFoundError: 工具不存在
        ToolExecutionError: 工具执行失败
        ToolTimeoutError: 工具执行超时
    
    Example:
        >>> result = store.call_tool("read_file", {"path": "/tmp/test.txt"})
        >>> print(result)
    """
```

##### use_tool()

```python
def use_tool(self, tool_name: str, **kwargs) -> Any:
    """
    便捷的工具调用方法
    
    Args:
        tool_name: 工具名称
        **kwargs: 工具参数（作为关键字参数）
    
    Returns:
        Any: 工具执行结果
    
    Example:
        >>> content = store.use_tool("read_file", path="/tmp/test.txt")
        >>> store.use_tool("write_file", path="/tmp/output.txt", content="Hello")
    """
```

##### batch_call()

```python
def batch_call(self, calls: List[Dict[str, Any]], parallel: bool = True, max_workers: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    批量调用工具
    
    Args:
        calls: 调用列表，每个调用包含：
            - tool_name (str): 工具名称
            - arguments (Dict): 工具参数
        parallel: 是否并行执行
        max_workers: 最大工作线程数
    
    Returns:
        List[Dict]: 执行结果列表，每个结果包含：
            - success (bool): 是否成功
            - result (Any): 执行结果
            - error (Optional[str]): 错误信息
            - execution_time (float): 执行时间
    
    Example:
        >>> calls = [
        ...     {"tool_name": "read_file", "arguments": {"path": "/tmp/file1.txt"}},
        ...     {"tool_name": "read_file", "arguments": {"path": "/tmp/file2.txt"}}
        ... ]
        >>> results = store.batch_call(calls)
    """
```

#### 健康检查方法

##### check_services()

```python
def check_services(self, service_names: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """
    检查服务健康状态
    
    Args:
        service_names: 可选，指定要检查的服务名称列表
    
    Returns:
        Dict: 健康检查结果，格式为：
            {
                "service_name": {
                    "healthy": bool,
                    "status": str,
                    "response_time": float,
                    "last_check": float,
                    "error": Optional[str]
                }
            }
    
    Example:
        >>> health = store.check_services()
        >>> print(health["filesystem"]["healthy"])
        True
    """
```

## 🔧 配置类

### MCPStoreConfig

```python
class MCPStoreConfig:
    """MCPStore 配置类"""
    
    def __init__(self, **kwargs):
        """
        初始化配置
        
        Args:
            data_dir (str): 数据目录
            log_level (str): 日志级别
            timeout (float): 默认超时时间
            max_connections (int): 最大连接数
            retry_count (int): 重试次数
            cache_size (int): 缓存大小
            enable_monitoring (bool): 启用监控
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'MCPStoreConfig':
        """从字典创建配置"""
    
    @classmethod
    def from_file(cls, config_file: str) -> 'MCPStoreConfig':
        """从文件加载配置"""
```

## ⚠️ 异常类

### 基础异常

```python
class MCPStoreError(Exception):
    """MCPStore 基础异常"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
```

### 服务相关异常

```python
class ServiceError(MCPStoreError):
    """服务相关异常基类"""

class ServiceNotFoundError(ServiceError):
    """服务不存在异常"""

class ServiceStartError(ServiceError):
    """服务启动异常"""

class ServiceStopError(ServiceError):
    """服务停止异常"""

class ServiceTimeoutError(ServiceError):
    """服务超时异常"""

class ServiceRegistrationError(ServiceError):
    """服务注册异常"""
```

### 工具相关异常

```python
class ToolError(MCPStoreError):
    """工具相关异常基类"""

class ToolNotFoundError(ToolError):
    """工具不存在异常"""

class ToolExecutionError(ToolError):
    """工具执行异常"""

class ToolTimeoutError(ToolError):
    """工具超时异常"""
```

### 配置相关异常

```python
class ConfigurationError(MCPStoreError):
    """配置异常"""

class InvalidConfigError(ConfigurationError):
    """无效配置异常"""

class ConfigFileNotFoundError(ConfigurationError):
    """配置文件不存在异常"""
```

## 📊 数据类型

### 服务状态枚举

```python
from enum import Enum

class ServiceStatus(Enum):
    NOT_STARTED = "not_started"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    UNKNOWN = "unknown"
```

### 工具调用结果

```python
from typing import TypedDict, Optional, Any

class ToolCallResult(TypedDict):
    success: bool
    result: Optional[Any]
    error: Optional[str]
    execution_time: float
    tool_name: str
    arguments: Dict[str, Any]
```

### 服务信息

```python
class ServiceInfo(TypedDict):
    name: str
    status: str
    command: str
    args: List[str]
    env: Dict[str, str]
    pid: Optional[int]
    uptime: float
    tools: List[Dict[str, Any]]
    last_error: Optional[str]
```

## 🔗 常量

```python
# 默认配置
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRY_COUNT = 3
DEFAULT_MAX_CONNECTIONS = 10
DEFAULT_CACHE_SIZE = 1000

# 状态常量
SERVICE_STATUS_RUNNING = "running"
SERVICE_STATUS_STOPPED = "stopped"
SERVICE_STATUS_ERROR = "error"

# 错误代码
ERROR_SERVICE_NOT_FOUND = "SERVICE_NOT_FOUND"
ERROR_TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
ERROR_EXECUTION_FAILED = "EXECUTION_FAILED"
ERROR_TIMEOUT = "TIMEOUT"
ERROR_CONFIGURATION = "CONFIGURATION_ERROR"
```

## 📚 使用示例

### 完整 API 使用示例

```python
from mcpstore import MCPStore
from mcpstore.exceptions import ServiceError, ToolError

# 初始化
store = MCPStore(config={
    "timeout": 60,
    "max_connections": 15,
    "log_level": "INFO"
})

try:
    # 添加服务
    store.add_service({
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        }
    })
    
    # 启动服务
    store.start_service("filesystem")
    
    # 检查状态
    status = store.get_service_status("filesystem")
    print(f"服务状态: {status}")
    
    # 列出工具
    tools = store.list_tools()
    print(f"可用工具: {[t['name'] for t in tools]}")
    
    # 调用工具
    result = store.call_tool("read_file", {"path": "/tmp/test.txt"})
    print(f"文件内容: {result}")
    
    # 批量调用
    calls = [
        {"tool_name": "list_directory", "arguments": {"path": "/tmp"}},
        {"tool_name": "get_file_info", "arguments": {"path": "/tmp/test.txt"}}
    ]
    results = store.batch_call(calls)
    
    # 健康检查
    health = store.check_services()
    print(f"健康状态: {health}")
    
except ServiceError as e:
    print(f"服务错误: {e.message}")
except ToolError as e:
    print(f"工具错误: {e.message}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 🔗 相关文档

- [快速开始](../quickstart.md)
- [配置项说明](../api/cache-config.md)
- [服务管理指南](../services/overview.md)
- [工具使用指南](../tools/overview.md)

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0
