# 插件开发

MCPStore 提供强大的插件化架构，支持多种类型的扩展开发，让您可以根据需求定制和扩展功能。

## 🔌 插件架构概览

MCPStore 的插件系统基于接口和事件驱动的设计：

```
┌─────────────────────────────────────────────────────────────┐
│                    MCPStore 核心                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   配置插件   │  │   传输插件   │  │   监控插件   │         │
│  │ConfigPlugin │  │TransportPlug│  │MonitorPlug  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   适配器插件 │  │   存储插件   │  │   认证插件   │         │
│  │AdapterPlugin│  │StoragePlugin│  │ AuthPlugin  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 插件类型

### 1. 配置插件 (Configuration Plugins)

扩展配置文件格式支持，如 YAML、TOML 等。

#### 基础接口

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class ConfigPlugin(ABC):
    """配置插件基础接口"""
    
    @abstractmethod
    def load_config(self, file_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        pass
    
    @abstractmethod
    def save_config(self, config: Dict[str, Any], file_path: str) -> bool:
        """保存配置文件"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置格式"""
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """支持的文件扩展名"""
        pass
```

#### YAML 配置插件示例

```python
import yaml
from typing import Dict, Any, List
from mcpstore.plugins.base import ConfigPlugin

class YAMLConfigPlugin(ConfigPlugin):
    """YAML 配置插件"""
    
    def load_config(self, file_path: str) -> Dict[str, Any]:
        """加载 YAML 配置文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return self._convert_to_mcp_format(config)
        except Exception as e:
            raise ConfigLoadError(f"Failed to load YAML config: {e}")
    
    def save_config(self, config: Dict[str, Any], file_path: str) -> bool:
        """保存为 YAML 格式"""
        try:
            yaml_config = self._convert_from_mcp_format(config)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_config, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save YAML config: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证 YAML 配置"""
        required_fields = ['mcpServers']
        return all(field in config for field in required_fields)
    
    @property
    def supported_extensions(self) -> List[str]:
        return ['.yaml', '.yml']
    
    def _convert_to_mcp_format(self, yaml_config: Dict[str, Any]) -> Dict[str, Any]:
        """将 YAML 格式转换为 MCP 标准格式"""
        # 实现格式转换逻辑
        return {
            "mcpServers": yaml_config.get("services", {}),
            "version": yaml_config.get("version", "1.0.0")
        }
    
    def _convert_from_mcp_format(self, mcp_config: Dict[str, Any]) -> Dict[str, Any]:
        """将 MCP 格式转换为 YAML 格式"""
        return {
            "version": mcp_config.get("version", "1.0.0"),
            "services": mcp_config.get("mcpServers", {})
        }

# 注册插件
from mcpstore.plugins import register_config_plugin
register_config_plugin(YAMLConfigPlugin())
```

### 2. 传输插件 (Transport Plugins)

支持新的传输协议，如 WebSocket、gRPC 等。

#### 基础接口

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class TransportPlugin(ABC):
    """传输插件基础接口"""
    
    @abstractmethod
    def create_client(self, config: Dict[str, Any]) -> Any:
        """创建客户端连接"""
        pass
    
    @abstractmethod
    async def call_tool(self, client: Any, tool_name: str, args: Dict[str, Any]) -> Any:
        """调用工具"""
        pass
    
    @abstractmethod
    async def list_tools(self, client: Any) -> List[Dict[str, Any]]:
        """获取工具列表"""
        pass
    
    @abstractmethod
    async def close_client(self, client: Any) -> None:
        """关闭客户端连接"""
        pass
    
    @property
    @abstractmethod
    def transport_type(self) -> str:
        """传输类型标识"""
        pass
```

#### WebSocket 传输插件示例

```python
import asyncio
import websockets
import json
from typing import Any, Dict, List
from mcpstore.plugins.base import TransportPlugin

class WebSocketTransportPlugin(TransportPlugin):
    """WebSocket 传输插件"""
    
    def create_client(self, config: Dict[str, Any]) -> Any:
        """创建 WebSocket 客户端"""
        return {
            'url': config['url'],
            'headers': config.get('headers', {}),
            'connection': None
        }
    
    async def call_tool(self, client: Any, tool_name: str, args: Dict[str, Any]) -> Any:
        """通过 WebSocket 调用工具"""
        if not client['connection']:
            client['connection'] = await websockets.connect(
                client['url'], 
                extra_headers=client['headers']
            )
        
        # 构造 MCP 请求
        request = {
            "jsonrpc": "2.0",
            "id": f"call_{tool_name}_{asyncio.get_event_loop().time()}",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        
        # 发送请求
        await client['connection'].send(json.dumps(request))
        
        # 接收响应
        response = await client['connection'].recv()
        result = json.loads(response)
        
        if 'error' in result:
            raise ToolCallError(result['error']['message'])
        
        return result.get('result')
    
    async def list_tools(self, client: Any) -> List[Dict[str, Any]]:
        """获取工具列表"""
        if not client['connection']:
            client['connection'] = await websockets.connect(
                client['url'],
                extra_headers=client['headers']
            )
        
        request = {
            "jsonrpc": "2.0",
            "id": "list_tools",
            "method": "tools/list"
        }
        
        await client['connection'].send(json.dumps(request))
        response = await client['connection'].recv()
        result = json.loads(response)
        
        return result.get('result', {}).get('tools', [])
    
    async def close_client(self, client: Any) -> None:
        """关闭 WebSocket 连接"""
        if client['connection']:
            await client['connection'].close()
            client['connection'] = None
    
    @property
    def transport_type(self) -> str:
        return "websocket"

# 注册插件
from mcpstore.plugins import register_transport_plugin
register_transport_plugin(WebSocketTransportPlugin())
```

### 3. 监控插件 (Monitoring Plugins)

扩展监控和告警功能。

#### 基础接口

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class MonitoringPlugin(ABC):
    """监控插件基础接口"""
    
    @abstractmethod
    def on_service_status_change(self, service_name: str, old_status: str, new_status: str):
        """服务状态变更事件"""
        pass
    
    @abstractmethod
    def on_tool_call(self, tool_name: str, args: Dict[str, Any], result: Any, duration: float):
        """工具调用事件"""
        pass
    
    @abstractmethod
    def on_error(self, error_type: str, error_message: str, context: Dict[str, Any]):
        """错误事件"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """获取监控指标"""
        pass
```

#### Prometheus 监控插件示例

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from typing import Dict, Any
from mcpstore.plugins.base import MonitoringPlugin

class PrometheusMonitoringPlugin(MonitoringPlugin):
    """Prometheus 监控插件"""
    
    def __init__(self, port: int = 8000):
        self.port = port
        
        # 定义指标
        self.service_status_changes = Counter(
            'mcpstore_service_status_changes_total',
            'Total service status changes',
            ['service_name', 'old_status', 'new_status']
        )
        
        self.tool_calls = Counter(
            'mcpstore_tool_calls_total',
            'Total tool calls',
            ['tool_name', 'status']
        )
        
        self.tool_call_duration = Histogram(
            'mcpstore_tool_call_duration_seconds',
            'Tool call duration',
            ['tool_name']
        )
        
        self.active_services = Gauge(
            'mcpstore_active_services',
            'Number of active services'
        )
        
        self.errors = Counter(
            'mcpstore_errors_total',
            'Total errors',
            ['error_type']
        )
        
        # 启动 Prometheus HTTP 服务器
        start_http_server(self.port)
    
    def on_service_status_change(self, service_name: str, old_status: str, new_status: str):
        """记录服务状态变更"""
        self.service_status_changes.labels(
            service_name=service_name,
            old_status=old_status,
            new_status=new_status
        ).inc()
        
        # 更新活跃服务数量
        if new_status == 'healthy':
            self.active_services.inc()
        elif old_status == 'healthy':
            self.active_services.dec()
    
    def on_tool_call(self, tool_name: str, args: Dict[str, Any], result: Any, duration: float):
        """记录工具调用"""
        status = 'success' if result is not None else 'error'
        
        self.tool_calls.labels(
            tool_name=tool_name,
            status=status
        ).inc()
        
        self.tool_call_duration.labels(
            tool_name=tool_name
        ).observe(duration)
    
    def on_error(self, error_type: str, error_message: str, context: Dict[str, Any]):
        """记录错误"""
        self.errors.labels(error_type=error_type).inc()
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取当前指标"""
        return {
            'prometheus_port': self.port,
            'metrics_endpoint': f'http://localhost:{self.port}/metrics'
        }

# 注册插件
from mcpstore.plugins import register_monitoring_plugin
register_monitoring_plugin(PrometheusMonitoringPlugin())
```

### 4. 适配器插件 (Adapter Plugins)

集成其他 AI 框架，如 CrewAI、AutoGen 等。

#### CrewAI 适配器示例

```python
from typing import List, Any, Dict
from mcpstore.plugins.base import AdapterPlugin

class CrewAIAdapter(AdapterPlugin):
    """CrewAI 适配器插件"""
    
    def __init__(self, context):
        self.context = context
    
    def to_crewai_tools(self) -> List[Any]:
        """转换为 CrewAI Tool 对象"""
        from crewai_tools import BaseTool
        
        tools = self.context.list_tools()
        crewai_tools = []
        
        for tool in tools:
            crewai_tool = self._create_crewai_tool(tool)
            crewai_tools.append(crewai_tool)
        
        return crewai_tools
    
    def _create_crewai_tool(self, tool_info) -> Any:
        """创建 CrewAI Tool 对象"""
        from crewai_tools import BaseTool
        from pydantic import BaseModel, Field
        
        # 动态创建参数模型
        if tool_info.inputSchema:
            args_schema = self._create_pydantic_model(tool_info.inputSchema)
        else:
            args_schema = BaseModel
        
        class MCPTool(BaseTool):
            name: str = tool_info.name
            description: str = tool_info.description
            args_schema: type = args_schema
            
            def _run(self, **kwargs) -> str:
                # 调用 MCPStore 工具
                result = self.context.call_tool(tool_info.name, kwargs)
                return str(result)
        
        return MCPTool()
    
    def _create_pydantic_model(self, schema: Dict[str, Any]) -> type:
        """从 JSON Schema 创建 Pydantic 模型"""
        from pydantic import BaseModel, Field, create_model
        
        fields = {}
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        
        for field_name, field_schema in properties.items():
            field_type = self._json_type_to_python(field_schema.get('type', 'string'))
            field_description = field_schema.get('description', '')
            field_required = field_name in required
            
            if field_required:
                fields[field_name] = (field_type, Field(description=field_description))
            else:
                fields[field_name] = (field_type, Field(None, description=field_description))
        
        return create_model('ToolArgs', **fields)
    
    def _json_type_to_python(self, json_type: str) -> type:
        """JSON 类型转 Python 类型"""
        type_mapping = {
            'string': str,
            'integer': int,
            'number': float,
            'boolean': bool,
            'array': list,
            'object': dict
        }
        return type_mapping.get(json_type, str)

# 使用示例
def setup_crewai_integration(store):
    """设置 CrewAI 集成"""
    from crewai import Agent, Task, Crew
    
    # 获取 MCPStore 工具
    context = store.for_store()
    adapter = CrewAIAdapter(context)
    tools = adapter.to_crewai_tools()
    
    # 创建 CrewAI Agent
    agent = Agent(
        role='Research Assistant',
        goal='Help with research tasks using MCP tools',
        backstory='An AI assistant with access to various tools',
        tools=tools,
        verbose=True
    )
    
    # 创建任务
    task = Task(
        description='Use the available tools to complete the research',
        agent=agent
    )
    
    # 创建团队
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    return crew
```

## 🔧 插件注册和管理

### 插件注册系统

```python
class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.config_plugins: Dict[str, ConfigPlugin] = {}
        self.transport_plugins: Dict[str, TransportPlugin] = {}
        self.monitoring_plugins: List[MonitoringPlugin] = []
        self.adapter_plugins: Dict[str, AdapterPlugin] = {}
    
    def register_config_plugin(self, plugin: ConfigPlugin):
        """注册配置插件"""
        for ext in plugin.supported_extensions:
            self.config_plugins[ext] = plugin
    
    def register_transport_plugin(self, plugin: TransportPlugin):
        """注册传输插件"""
        self.transport_plugins[plugin.transport_type] = plugin
    
    def register_monitoring_plugin(self, plugin: MonitoringPlugin):
        """注册监控插件"""
        self.monitoring_plugins.append(plugin)
    
    def get_config_plugin(self, file_extension: str) -> ConfigPlugin:
        """获取配置插件"""
        return self.config_plugins.get(file_extension)
    
    def get_transport_plugin(self, transport_type: str) -> TransportPlugin:
        """获取传输插件"""
        return self.transport_plugins.get(transport_type)
    
    def notify_monitoring_plugins(self, event_type: str, **kwargs):
        """通知监控插件"""
        for plugin in self.monitoring_plugins:
            if event_type == 'service_status_change':
                plugin.on_service_status_change(**kwargs)
            elif event_type == 'tool_call':
                plugin.on_tool_call(**kwargs)
            elif event_type == 'error':
                plugin.on_error(**kwargs)

# 全局插件管理器
plugin_manager = PluginManager()

# 便捷注册函数
def register_config_plugin(plugin: ConfigPlugin):
    plugin_manager.register_config_plugin(plugin)

def register_transport_plugin(plugin: TransportPlugin):
    plugin_manager.register_transport_plugin(plugin)

def register_monitoring_plugin(plugin: MonitoringPlugin):
    plugin_manager.register_monitoring_plugin(plugin)
```

### 插件发现和加载

```python
import importlib
import pkgutil
from pathlib import Path

class PluginLoader:
    """插件加载器"""
    
    def __init__(self, plugin_dirs: List[str] = None):
        self.plugin_dirs = plugin_dirs or ['mcpstore_plugins', 'plugins']
    
    def load_plugins(self):
        """加载所有插件"""
        for plugin_dir in self.plugin_dirs:
            self._load_plugins_from_directory(plugin_dir)
    
    def _load_plugins_from_directory(self, plugin_dir: str):
        """从目录加载插件"""
        try:
            # 尝试作为包导入
            package = importlib.import_module(plugin_dir)
            
            # 遍历包中的模块
            for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
                full_name = f"{plugin_dir}.{modname}"
                try:
                    importlib.import_module(full_name)
                    print(f"✅ Loaded plugin: {full_name}")
                except Exception as e:
                    print(f"❌ Failed to load plugin {full_name}: {e}")
                    
        except ImportError:
            # 尝试从文件系统路径加载
            plugin_path = Path(plugin_dir)
            if plugin_path.exists():
                self._load_plugins_from_path(plugin_path)
    
    def _load_plugins_from_path(self, plugin_path: Path):
        """从文件系统路径加载插件"""
        for plugin_file in plugin_path.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            spec = importlib.util.spec_from_file_location(
                plugin_file.stem, plugin_file
            )
            module = importlib.util.module_from_spec(spec)
            
            try:
                spec.loader.exec_module(module)
                print(f"✅ Loaded plugin: {plugin_file.name}")
            except Exception as e:
                print(f"❌ Failed to load plugin {plugin_file.name}: {e}")

# 使用示例
loader = PluginLoader()
loader.load_plugins()
```

## 📦 插件打包和分发

### 插件包结构

```
my_mcpstore_plugin/
├── setup.py
├── README.md
├── my_plugin/
│   ├── __init__.py
│   ├── config_plugin.py
│   ├── transport_plugin.py
│   └── monitoring_plugin.py
└── tests/
    ├── test_config_plugin.py
    └── test_transport_plugin.py
```

### setup.py 示例

```python
from setuptools import setup, find_packages

setup(
    name="my-mcpstore-plugin",
    version="1.0.0",
    description="Custom MCPStore plugin",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "mcpstore>=0.5.0",
        # 其他依赖
    ],
    entry_points={
        'mcpstore.plugins': [
            'my_config = my_plugin.config_plugin:MyConfigPlugin',
            'my_transport = my_plugin.transport_plugin:MyTransportPlugin',
            'my_monitoring = my_plugin.monitoring_plugin:MyMonitoringPlugin',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
```

## 🧪 插件测试

### 测试框架

```python
import pytest
from mcpstore.plugins.base import ConfigPlugin
from my_plugin.config_plugin import YAMLConfigPlugin

class TestYAMLConfigPlugin:
    """YAML 配置插件测试"""
    
    def setup_method(self):
        self.plugin = YAMLConfigPlugin()
    
    def test_supported_extensions(self):
        """测试支持的扩展名"""
        assert '.yaml' in self.plugin.supported_extensions
        assert '.yml' in self.plugin.supported_extensions
    
    def test_load_config(self, tmp_path):
        """测试配置加载"""
        # 创建测试配置文件
        config_file = tmp_path / "test.yaml"
        config_file.write_text("""
version: "1.0.0"
services:
  test-service:
    url: "https://test.com/mcp"
""")
        
        # 加载配置
        config = self.plugin.load_config(str(config_file))
        
        # 验证结果
        assert config['version'] == '1.0.0'
        assert 'mcpServers' in config
        assert 'test-service' in config['mcpServers']
    
    def test_save_config(self, tmp_path):
        """测试配置保存"""
        config = {
            'version': '1.0.0',
            'mcpServers': {
                'test-service': {
                    'url': 'https://test.com/mcp'
                }
            }
        }
        
        config_file = tmp_path / "output.yaml"
        success = self.plugin.save_config(config, str(config_file))
        
        assert success
        assert config_file.exists()
        
        # 验证保存的内容
        loaded_config = self.plugin.load_config(str(config_file))
        assert loaded_config['version'] == config['version']
```

## 📚 插件开发最佳实践

### 1. 接口设计原则

- **单一职责**: 每个插件专注于一个特定功能
- **松耦合**: 插件之间不应有直接依赖
- **可测试**: 提供清晰的接口便于测试

### 2. 错误处理

```python
class MyPlugin(ConfigPlugin):
    def load_config(self, file_path: str) -> Dict[str, Any]:
        try:
            # 插件逻辑
            return config
        except Exception as e:
            # 记录详细错误信息
            logger.error(f"Plugin {self.__class__.__name__} failed: {e}")
            # 抛出标准化异常
            raise PluginError(f"Failed to load config: {e}") from e
```

### 3. 配置管理

```python
class MyPlugin(TransportPlugin):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.timeout = self.config.get('timeout', 30)
        self.retries = self.config.get('retries', 3)
```

### 4. 资源管理

```python
class MyPlugin(TransportPlugin):
    def __init__(self):
        self.connections = {}
    
    async def close_client(self, client: Any) -> None:
        """确保资源正确释放"""
        try:
            if client['connection']:
                await client['connection'].close()
        finally:
            # 清理资源
            client['connection'] = None
```

## 相关文档

- [核心概念](concepts.md) - 理解插件架构基础
- [系统架构](architecture.md) - 了解插件在系统中的位置
- [自定义适配器](custom-adapters.md) - 适配器开发指南

## 下一步

- 学习 [自定义适配器开发](custom-adapters.md)
- 掌握 [最佳实践指南](best-practices.md)
- 查看 [API 参考文档](../api-reference/mcpstore-class.md)
