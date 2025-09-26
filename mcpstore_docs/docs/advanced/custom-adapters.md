# 自定义适配器

MCPStore 提供强大的适配器系统，让您可以轻松集成各种 AI 框架和工具库，实现无缝的工具共享和调用。

## 🎯 适配器概述

适配器是 MCPStore 与其他 AI 框架之间的桥梁，负责：

- **格式转换**: 将 MCP 工具转换为目标框架的工具格式
- **参数映射**: 处理不同框架间的参数差异
- **调用代理**: 代理工具调用并处理结果
- **错误处理**: 统一错误处理和异常转换

## 🏗️ 适配器架构

```
┌─────────────────────────────────────────────────────────────┐
│                    MCPStore 核心                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              适配器层 (Adapter Layer)                   │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │ LangChain   │ │   CrewAI    │ │  AutoGen    │      │ │
│  │  │  Adapter    │ │  Adapter    │ │  Adapter    │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │ │
│  │  │   Haystack  │ │   Custom    │ │   Future    │      │ │
│  │  │   Adapter   │ │   Adapter   │ │   Adapter   │      │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               MCPStore 工具层                           │ │
│  │        list_tools() / call_tool()                      │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 基础适配器接口

### 适配器设计模式

MCPStore 的适配器采用组合模式设计，通过包装 MCPStoreContext 来提供特定框架的接口：

```python
from typing import List, Any, Dict
from mcpstore.core.context import MCPStoreContext

class CustomAdapter:
    """
    自定义适配器示例

    适配器通过组合 MCPStoreContext 来提供特定框架的接口
    """

    def __init__(self, context: MCPStoreContext):
        """
        初始化适配器

        Args:
            context: MCPStoreContext 实例
        """
        self.context = context
        self._tool_cache = {}
        self._framework_tools = []

    def convert_tools(self) -> List[Any]:
        """
        转换工具为目标框架格式

        Returns:
            目标框架的工具对象列表
        """
        mcp_tools = self.context.list_tools()
        framework_tools = []

        for tool in mcp_tools:
            framework_tool = self.create_tool_wrapper(tool)
            framework_tools.append(framework_tool)

        return framework_tools

    def create_tool_wrapper(self, tool_info) -> Any:
        """
        为单个工具创建包装器

        Args:
            tool_info: MCP 工具信息

        Returns:
            目标框架的工具对象
        """
        # 实现具体的工具包装逻辑
        def tool_function(**kwargs):
            return self.context.call_tool(tool_info.name, kwargs)

        # 返回适合目标框架的工具对象
        return {
            'name': tool_info.name,
            'description': tool_info.description,
            'function': tool_function,
            'schema': tool_info.input_schema
        }

    def get_tools(self):
        """获取 MCP 工具列表"""
        return self.context.list_tools()

    def call_mcp_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """调用 MCP 工具"""
        return self.context.call_tool(tool_name, args)

    def refresh_tools(self):
        """刷新工具缓存"""
        self._tool_cache.clear()
        self._framework_tools = self.convert_tools()
```

## 🚀 LangChain 适配器实现

MCPStore 内置的 LangChain 适配器是最完整的实现示例：

```python
from typing import List, Type, Any, Dict
from pydantic import BaseModel, Field, create_model
from langchain_core.tools import BaseTool
from mcpstore.adapters.base import AdapterBase

class LangChainAdapter(AdapterBase):
    """LangChain 适配器"""
    
    def convert_tools(self) -> List[BaseTool]:
        """转换为 LangChain Tool 对象"""
        tools = self.get_tools()
        langchain_tools = []
        
        for tool_info in tools:
            try:
                langchain_tool = self.create_tool_wrapper(tool_info)
                langchain_tools.append(langchain_tool)
            except Exception as e:
                print(f"⚠️ Failed to convert tool {tool_info.name}: {e}")
                continue
        
        return langchain_tools
    
    def create_tool_wrapper(self, tool_info) -> BaseTool:
        """创建 LangChain Tool 包装器"""
        # 增强工具描述
        enhanced_description = self._enhance_description(tool_info)
        
        # 转换参数 Schema
        args_schema = self._convert_schema(tool_info.inputSchema)
        
        # 创建动态 Tool 类
        class MCPTool(BaseTool):
            name: str = tool_info.name
            description: str = enhanced_description
            args_schema: Type[BaseModel] = args_schema
            
            def _run(self, **kwargs) -> str:
                """执行工具调用"""
                try:
                    result = self.call_mcp_tool(tool_info.name, kwargs)
                    return self._format_result(result)
                except Exception as e:
                    return f"Error calling tool {tool_info.name}: {str(e)}"
            
            async def _arun(self, **kwargs) -> str:
                """异步执行工具调用"""
                try:
                    result = await self.context.call_tool_async(tool_info.name, kwargs)
                    return self._format_result(result)
                except Exception as e:
                    return f"Error calling tool {tool_info.name}: {str(e)}"
            
            def _format_result(self, result: Any) -> str:
                """格式化结果为字符串"""
                if isinstance(result, str):
                    return result
                elif isinstance(result, (dict, list)):
                    import json
                    return json.dumps(result, ensure_ascii=False, indent=2)
                else:
                    return str(result)
        
        return MCPTool()
    
    def _enhance_description(self, tool_info) -> str:
        """增强工具描述"""
        description = tool_info.description
        
        if tool_info.inputSchema and 'properties' in tool_info.inputSchema:
            description += "\n\n参数说明:"
            for param_name, param_info in tool_info.inputSchema['properties'].items():
                param_desc = param_info.get('description', '无描述')
                param_type = param_info.get('type', 'string')
                description += f"\n- {param_name} ({param_type}): {param_desc}"
        
        return description
    
    def _convert_schema(self, input_schema: Optional[Dict]) -> Type[BaseModel]:
        """转换 JSON Schema 为 Pydantic 模型"""
        if not input_schema or 'properties' not in input_schema:
            return BaseModel
        
        fields = {}
        properties = input_schema['properties']
        required = input_schema.get('required', [])
        
        for field_name, field_schema in properties.items():
            field_type = self._json_type_to_python(field_schema.get('type', 'string'))
            field_description = field_schema.get('description', '')
            is_required = field_name in required
            
            if is_required:
                fields[field_name] = (field_type, Field(description=field_description))
            else:
                fields[field_name] = (Optional[field_type], Field(None, description=field_description))
        
        return create_model('ToolArgs', **fields)
    
    def _json_type_to_python(self, json_type: str) -> Type:
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
def get_langchain_tools(store):
    """获取 LangChain 工具"""
    context = store.for_store()
    adapter = LangChainAdapter(context)
    return adapter.convert_tools()
```

## 🤖 CrewAI 适配器实现

```python
from typing import List, Any, Dict, Optional
from mcpstore.adapters.base import AdapterBase

class CrewAIAdapter(AdapterBase):
    """CrewAI 适配器"""
    
    def convert_tools(self) -> List[Any]:
        """转换为 CrewAI Tool 对象"""
        try:
            from crewai_tools import BaseTool
        except ImportError:
            raise ImportError("CrewAI not installed. Run: pip install crewai")
        
        tools = self.get_tools()
        crewai_tools = []
        
        for tool_info in tools:
            try:
                crewai_tool = self.create_tool_wrapper(tool_info)
                crewai_tools.append(crewai_tool)
            except Exception as e:
                print(f"⚠️ Failed to convert tool {tool_info.name}: {e}")
                continue
        
        return crewai_tools
    
    def create_tool_wrapper(self, tool_info) -> Any:
        """创建 CrewAI Tool 包装器"""
        from crewai_tools import BaseTool
        from pydantic import BaseModel, Field
        
        # 创建参数模型
        args_schema = self._create_args_schema(tool_info.inputSchema)
        
        class MCPCrewTool(BaseTool):
            name: str = tool_info.name
            description: str = self._enhance_description(tool_info)
            args_schema: type = args_schema
            
            def _run(self, **kwargs) -> str:
                """执行工具调用"""
                try:
                    result = self.call_mcp_tool(tool_info.name, kwargs)
                    return self._format_result(result)
                except Exception as e:
                    return f"Error: {str(e)}"
            
            def _format_result(self, result: Any) -> str:
                """格式化结果"""
                if isinstance(result, str):
                    return result
                elif isinstance(result, (dict, list)):
                    import json
                    return json.dumps(result, ensure_ascii=False, indent=2)
                else:
                    return str(result)
        
        return MCPCrewTool()
    
    def _create_args_schema(self, input_schema: Optional[Dict]) -> type:
        """创建参数 Schema"""
        from pydantic import BaseModel, Field, create_model
        
        if not input_schema or 'properties' not in input_schema:
            return BaseModel
        
        fields = {}
        properties = input_schema['properties']
        required = input_schema.get('required', [])
        
        for field_name, field_schema in properties.items():
            field_type = self._json_type_to_python(field_schema.get('type', 'string'))
            field_description = field_schema.get('description', '')
            is_required = field_name in required
            
            if is_required:
                fields[field_name] = (field_type, Field(description=field_description))
            else:
                fields[field_name] = (Optional[field_type], Field(None, description=field_description))
        
        return create_model('CrewToolArgs', **fields)
    
    def _enhance_description(self, tool_info) -> str:
        """增强工具描述"""
        description = tool_info.description
        
        if tool_info.inputSchema and 'properties' in tool_info.inputSchema:
            description += "\n\nParameters:"
            for param_name, param_info in tool_info.inputSchema['properties'].items():
                param_desc = param_info.get('description', 'No description')
                param_type = param_info.get('type', 'string')
                description += f"\n- {param_name} ({param_type}): {param_desc}"
        
        return description
    
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
def setup_crewai_agent(store):
    """设置 CrewAI Agent"""
    from crewai import Agent, Task, Crew
    
    # 获取工具
    context = store.for_store()
    adapter = CrewAIAdapter(context)
    tools = adapter.convert_tools()
    
    # 创建 Agent
    agent = Agent(
        role='Research Assistant',
        goal='Help with research and analysis tasks',
        backstory='An AI assistant with access to various MCP tools',
        tools=tools,
        verbose=True
    )
    
    return agent
```

## 🔧 AutoGen 适配器实现

```python
from typing import List, Any, Dict, Callable
from mcpstore.adapters.base import AdapterBase

class AutoGenAdapter(AdapterBase):
    """AutoGen 适配器"""
    
    def convert_tools(self) -> List[Dict[str, Any]]:
        """转换为 AutoGen 工具格式"""
        tools = self.get_tools()
        autogen_tools = []
        
        for tool_info in tools:
            try:
                autogen_tool = self.create_tool_wrapper(tool_info)
                autogen_tools.append(autogen_tool)
            except Exception as e:
                print(f"⚠️ Failed to convert tool {tool_info.name}: {e}")
                continue
        
        return autogen_tools
    
    def create_tool_wrapper(self, tool_info) -> Dict[str, Any]:
        """创建 AutoGen 工具包装器"""
        
        def tool_function(**kwargs) -> str:
            """工具执行函数"""
            try:
                result = self.call_mcp_tool(tool_info.name, kwargs)
                return self._format_result(result)
            except Exception as e:
                return f"Error calling {tool_info.name}: {str(e)}"
        
        # 构造 AutoGen 工具描述
        tool_spec = {
            "type": "function",
            "function": {
                "name": tool_info.name,
                "description": tool_info.description,
                "parameters": self._convert_schema_to_autogen(tool_info.inputSchema)
            }
        }
        
        return {
            "spec": tool_spec,
            "function": tool_function
        }
    
    def _convert_schema_to_autogen(self, input_schema: Optional[Dict]) -> Dict[str, Any]:
        """转换 Schema 为 AutoGen 格式"""
        if not input_schema:
            return {
                "type": "object",
                "properties": {},
                "required": []
            }
        
        # AutoGen 使用 OpenAI 函数调用格式
        return {
            "type": "object",
            "properties": input_schema.get("properties", {}),
            "required": input_schema.get("required", [])
        }
    
    def _format_result(self, result: Any) -> str:
        """格式化结果"""
        if isinstance(result, str):
            return result
        elif isinstance(result, (dict, list)):
            import json
            return json.dumps(result, ensure_ascii=False, indent=2)
        else:
            return str(result)
    
    def register_tools_with_agent(self, agent) -> None:
        """将工具注册到 AutoGen Agent"""
        tools = self.convert_tools()
        
        for tool in tools:
            # 注册函数
            agent.register_function(
                function_map={tool["spec"]["function"]["name"]: tool["function"]}
            )

# 使用示例
def setup_autogen_agent(store):
    """设置 AutoGen Agent"""
    try:
        from autogen import ConversableAgent
    except ImportError:
        raise ImportError("AutoGen not installed. Run: pip install pyautogen")
    
    # 创建 Agent
    agent = ConversableAgent(
        name="assistant",
        system_message="You are a helpful assistant with access to various tools.",
        llm_config={
            "config_list": [{"model": "gpt-4", "api_key": "your-api-key"}]
        }
    )
    
    # 注册 MCP 工具
    context = store.for_store()
    adapter = AutoGenAdapter(context)
    adapter.register_tools_with_agent(agent)
    
    return agent
```

## 🎨 自定义适配器开发

### 1. 简单函数式适配器

```python
def create_simple_adapter(context):
    """创建简单的函数式适配器"""
    
    def get_tool_functions() -> Dict[str, Callable]:
        """获取工具函数字典"""
        tools = context.list_tools()
        tool_functions = {}
        
        for tool_info in tools:
            def create_tool_func(tool_name):
                def tool_func(**kwargs):
                    return context.call_tool(tool_name, kwargs)
                return tool_func
            
            tool_functions[tool_info.name] = create_tool_func(tool_info.name)
        
        return tool_functions
    
    def get_tool_descriptions() -> Dict[str, str]:
        """获取工具描述字典"""
        tools = context.list_tools()
        return {tool.name: tool.description for tool in tools}
    
    return {
        'functions': get_tool_functions(),
        'descriptions': get_tool_descriptions()
    }

# 使用示例
adapter = create_simple_adapter(store.for_store())
functions = adapter['functions']
descriptions = adapter['descriptions']

# 调用工具
result = functions['weather_get_current'](city="北京")
```

### 2. 类型安全适配器

```python
from typing import TypeVar, Generic, Protocol
from dataclasses import dataclass

T = TypeVar('T')

class ToolProtocol(Protocol):
    """工具协议定义"""
    name: str
    description: str
    
    def execute(self, **kwargs) -> Any:
        """执行工具"""
        ...

@dataclass
class TypedTool:
    """类型化工具包装器"""
    name: str
    description: str
    input_type: type
    output_type: type
    executor: Callable
    
    def execute(self, **kwargs) -> Any:
        """执行工具并进行类型检查"""
        # 输入类型验证
        if self.input_type != Any:
            try:
                validated_input = self.input_type(**kwargs)
                kwargs = validated_input.dict()
            except Exception as e:
                raise ValueError(f"Input validation failed: {e}")
        
        # 执行工具
        result = self.executor(**kwargs)
        
        # 输出类型验证
        if self.output_type != Any and not isinstance(result, self.output_type):
            try:
                result = self.output_type(result)
            except Exception:
                pass  # 类型转换失败时保持原结果
        
        return result

class TypeSafeAdapter(AdapterBase):
    """类型安全适配器"""
    
    def convert_tools(self) -> List[TypedTool]:
        """转换为类型安全工具"""
        tools = self.get_tools()
        typed_tools = []
        
        for tool_info in tools:
            typed_tool = self.create_tool_wrapper(tool_info)
            typed_tools.append(typed_tool)
        
        return typed_tools
    
    def create_tool_wrapper(self, tool_info) -> TypedTool:
        """创建类型化工具包装器"""
        input_type = self._create_input_type(tool_info.inputSchema)
        output_type = Any  # 可以根据需要推断输出类型
        
        def executor(**kwargs):
            return self.call_mcp_tool(tool_info.name, kwargs)
        
        return TypedTool(
            name=tool_info.name,
            description=tool_info.description,
            input_type=input_type,
            output_type=output_type,
            executor=executor
        )
    
    def _create_input_type(self, input_schema: Optional[Dict]) -> type:
        """从 Schema 创建输入类型"""
        if not input_schema:
            return Any
        
        from pydantic import create_model
        
        fields = {}
        properties = input_schema.get('properties', {})
        required = input_schema.get('required', [])
        
        for field_name, field_schema in properties.items():
            field_type = self._json_type_to_python(field_schema.get('type', 'string'))
            is_required = field_name in required
            
            if is_required:
                fields[field_name] = (field_type, ...)
            else:
                fields[field_name] = (Optional[field_type], None)
        
        return create_model('InputModel', **fields)
```

## 🔄 适配器注册和使用

### 适配器注册系统

```python
class AdapterRegistry:
    """适配器注册表"""
    
    def __init__(self):
        self._adapters: Dict[str, type] = {}
    
    def register(self, name: str, adapter_class: type):
        """注册适配器"""
        self._adapters[name] = adapter_class
    
    def get(self, name: str) -> Optional[type]:
        """获取适配器类"""
        return self._adapters.get(name)
    
    def list_adapters(self) -> List[str]:
        """列出所有适配器"""
        return list(self._adapters.keys())
    
    def create_adapter(self, name: str, context) -> Optional[AdapterBase]:
        """创建适配器实例"""
        adapter_class = self.get(name)
        if adapter_class:
            return adapter_class(context)
        return None

# 全局注册表
adapter_registry = AdapterRegistry()

# 注册内置适配器
adapter_registry.register('langchain', LangChainAdapter)
adapter_registry.register('crewai', CrewAIAdapter)
adapter_registry.register('autogen', AutoGenAdapter)

# 便捷函数
def register_adapter(name: str, adapter_class: type):
    """注册适配器"""
    adapter_registry.register(name, adapter_class)

def get_adapter(name: str, context) -> Optional[AdapterBase]:
    """获取适配器实例"""
    return adapter_registry.create_adapter(name, context)
```

### 统一适配器接口

```python
class MCPStoreContext:
    """扩展 MCPStoreContext 以支持适配器"""
    
    def for_framework(self, framework: str) -> Optional[AdapterBase]:
        """获取指定框架的适配器"""
        return get_adapter(framework, self)
    
    def for_langchain(self) -> LangChainAdapter:
        """获取 LangChain 适配器（向后兼容）"""
        return LangChainAdapter(self)
    
    def for_crewai(self) -> CrewAIAdapter:
        """获取 CrewAI 适配器"""
        return CrewAIAdapter(self)
    
    def for_autogen(self) -> AutoGenAdapter:
        """获取 AutoGen 适配器"""
        return AutoGenAdapter(self)

# 使用示例
store = MCPStore.setup_store()

# 统一接口
langchain_tools = store.for_store().for_framework('langchain').convert_tools()
crewai_tools = store.for_store().for_framework('crewai').convert_tools()

# 专用接口
langchain_tools = store.for_store().for_langchain().list_tools()
crewai_agent = setup_crewai_agent(store)
```

## 📊 适配器性能优化

### 1. 工具缓存

```python
class CachedAdapter(AdapterBase):
    """带缓存的适配器"""
    
    def __init__(self, context):
        super().__init__(context)
        self._converted_tools_cache = None
        self._cache_timestamp = None
    
    def convert_tools(self) -> List[Any]:
        """带缓存的工具转换"""
        current_time = time.time()
        
        # 检查缓存是否有效（5分钟过期）
        if (self._converted_tools_cache is not None and 
            self._cache_timestamp is not None and
            current_time - self._cache_timestamp < 300):
            return self._converted_tools_cache
        
        # 重新转换工具
        tools = super().convert_tools()
        self._converted_tools_cache = tools
        self._cache_timestamp = current_time
        
        return tools
    
    def refresh_cache(self):
        """手动刷新缓存"""
        self._converted_tools_cache = None
        self._cache_timestamp = None
```

### 2. 延迟加载

```python
class LazyAdapter(AdapterBase):
    """延迟加载适配器"""
    
    def __init__(self, context):
        super().__init__(context)
        self._tool_wrappers = {}
    
    def convert_tools(self) -> List[Any]:
        """延迟创建工具包装器"""
        tools = self.get_tools()
        lazy_tools = []
        
        for tool_info in tools:
            lazy_tool = self._create_lazy_wrapper(tool_info)
            lazy_tools.append(lazy_tool)
        
        return lazy_tools
    
    def _create_lazy_wrapper(self, tool_info):
        """创建延迟包装器"""
        class LazyTool:
            def __init__(self, adapter, tool_info):
                self.adapter = adapter
                self.tool_info = tool_info
                self._wrapper = None
            
            def __getattr__(self, name):
                if self._wrapper is None:
                    self._wrapper = self.adapter.create_tool_wrapper(self.tool_info)
                return getattr(self._wrapper, name)
        
        return LazyTool(self, tool_info)
```

## 🧪 适配器测试

### 测试框架

```python
import pytest
from unittest.mock import Mock, patch
from mcpstore.adapters.base import AdapterBase

class TestCustomAdapter:
    """自定义适配器测试"""
    
    def setup_method(self):
        """设置测试环境"""
        self.mock_context = Mock()
        self.mock_context.list_tools.return_value = [
            Mock(
                name="test_tool",
                description="Test tool description",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string", "description": "Parameter 1"}
                    },
                    "required": ["param1"]
                }
            )
        ]
        self.mock_context.call_tool.return_value = "test result"
        
        self.adapter = CustomAdapter(self.mock_context)
    
    def test_convert_tools(self):
        """测试工具转换"""
        tools = self.adapter.convert_tools()
        
        assert len(tools) == 1
        assert tools[0].name == "test_tool"
        assert "Test tool description" in tools[0].description
    
    def test_tool_execution(self):
        """测试工具执行"""
        tools = self.adapter.convert_tools()
        tool = tools[0]
        
        result = tool.execute(param1="test value")
        
        assert result == "test result"
        self.mock_context.call_tool.assert_called_once_with(
            "test_tool", {"param1": "test value"}
        )
    
    def test_error_handling(self):
        """测试错误处理"""
        self.mock_context.call_tool.side_effect = Exception("Test error")
        
        tools = self.adapter.convert_tools()
        tool = tools[0]
        
        result = tool.execute(param1="test value")
        
        assert "Error" in result
```

## 📚 最佳实践

### 1. 错误处理

```python
class RobustAdapter(AdapterBase):
    """健壮的适配器实现"""
    
    def create_tool_wrapper(self, tool_info):
        """创建健壮的工具包装器"""
        
        def safe_execute(**kwargs):
            try:
                # 参数验证
                validated_args = self._validate_args(tool_info, kwargs)
                
                # 调用工具
                result = self.call_mcp_tool(tool_info.name, validated_args)
                
                # 结果验证
                return self._validate_result(result)
                
            except ValidationError as e:
                return f"参数验证失败: {e}"
            except ToolCallError as e:
                return f"工具调用失败: {e}"
            except Exception as e:
                return f"未知错误: {e}"
        
        return safe_execute
```

### 2. 性能监控

```python
import time
from functools import wraps

def monitor_performance(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            print(f"✅ {func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ {func.__name__} failed in {duration:.3f}s: {e}")
            raise
    return wrapper

class MonitoredAdapter(AdapterBase):
    """带性能监控的适配器"""
    
    @monitor_performance
    def convert_tools(self):
        return super().convert_tools()
    
    @monitor_performance
    def create_tool_wrapper(self, tool_info):
        return super().create_tool_wrapper(tool_info)
```

## 相关文档

- [插件开发](plugin-development.md) - 插件系统详解
- [核心概念](concepts.md) - 理解适配器架构
- [LangChain 集成](../tools/langchain/as-langchain-tools.md) - 内置适配器使用

## 下一步

- 学习 [最佳实践指南](best-practices.md)
- 了解 [插件开发方法](plugin-development.md)
- 查看 [API 参考文档](../api-reference/mcpstore-class.md)
