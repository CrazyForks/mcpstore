# for_langchain().list_tools()

转换为LangChain工具。

## 方法特性

- ❌ **异步版本**: 不支持异步版本
- ✅ **Store级别**: `store.for_store().for_langchain().list_tools()`
- ✅ **Agent级别**: `store.for_agent("agent1").for_langchain().list_tools()`
- 📁 **文件位置**: `base_context.py`
- 🏷️ **所属类**: `MCPStoreContext`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| 无参数 | - | - | - | 该方法不需要参数 |

## 返回值

返回LangChain工具对象列表，每个工具都是LangChain兼容的Tool实例。

## 使用示例

### Store级别LangChain集成

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加一些服务
store.for_store().add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        },
        "weather": {
            "url": "https://api.weather.com/mcp"
        }
    }
})

# 转换为LangChain工具
langchain_tools = store.for_store().for_langchain().list_tools()

print(f"转换的LangChain工具数量: {len(langchain_tools)}")

# 查看工具信息
for tool in langchain_tools:
    print(f"工具名称: {tool.name}")
    print(f"工具描述: {tool.description}")
    print(f"工具类型: {type(tool)}")
    print("---")
```

### Agent级别LangChain集成

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式转换LangChain工具
agent_langchain_tools = store.for_agent("agent1").for_langchain().list_tools()

print(f"Agent LangChain工具数量: {len(agent_langchain_tools)}")

# Agent模式下工具名称是本地化的
for tool in agent_langchain_tools:
    print(f"Agent工具: {tool.name} - {tool.description}")
```

### 与LangChain Agent集成

```python
from mcpstore import MCPStore
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

# 初始化MCPStore
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
    }
})

# 获取LangChain工具
tools = store.for_store().for_langchain().list_tools()

# 初始化LLM
llm = OpenAI(temperature=0)

# 创建LangChain Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 使用Agent执行任务
try:
    result = agent.run("请读取/tmp目录下的文件列表")
    print(f"Agent执行结果: {result}")
except Exception as e:
    print(f"Agent执行失败: {e}")
```

### 与LangChain Chain集成

```python
from mcpstore import MCPStore
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# 初始化MCPStore
store = MCPStore.setup_store()

# 添加天气服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {
            "url": "https://api.weather.com/mcp"
        }
    }
})

# 获取LangChain工具
tools = store.for_store().for_langchain().list_tools()

# 找到天气工具
weather_tool = None
for tool in tools:
    if "weather" in tool.name.lower():
        weather_tool = tool
        break

if weather_tool:
    # 创建自定义Chain
    class WeatherChain:
        def __init__(self, weather_tool, llm):
            self.weather_tool = weather_tool
            self.llm = llm
        
        def run(self, city):
            # 使用MCPStore工具获取天气
            weather_data = self.weather_tool.run({"city": city})
            
            # 使用LLM处理天气数据
            prompt = PromptTemplate(
                input_variables=["city", "weather_data"],
                template="根据以下天气数据为{city}生成天气报告：\n{weather_data}\n\n天气报告："
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = chain.run(city=city, weather_data=weather_data)
            
            return result
    
    # 使用自定义Chain
    llm = OpenAI(temperature=0.7)
    weather_chain = WeatherChain(weather_tool, llm)
    
    report = weather_chain.run("北京")
    print(f"天气报告: {report}")
```

### 工具过滤和选择

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加多个服务
store.for_store().add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        },
        "weather": {
            "url": "https://api.weather.com/mcp"
        },
        "database": {
            "command": "python",
            "args": ["db_server.py"]
        }
    }
})

# 获取所有LangChain工具
all_tools = store.for_store().for_langchain().list_tools()

# 按类型过滤工具
def filter_tools_by_service(tools, service_name):
    """按服务名过滤工具"""
    return [tool for tool in tools if service_name in tool.name.lower()]

def filter_tools_by_keyword(tools, keyword):
    """按关键词过滤工具"""
    return [tool for tool in tools 
            if keyword.lower() in tool.name.lower() 
            or keyword.lower() in tool.description.lower()]

# 过滤示例
filesystem_tools = filter_tools_by_service(all_tools, "filesystem")
read_tools = filter_tools_by_keyword(all_tools, "read")

print(f"文件系统工具: {len(filesystem_tools)} 个")
for tool in filesystem_tools:
    print(f"  - {tool.name}")

print(f"\n读取相关工具: {len(read_tools)} 个")
for tool in read_tools:
    print(f"  - {tool.name}: {tool.description}")

# 创建特定用途的工具集
file_management_tools = filter_tools_by_service(all_tools, "filesystem")
weather_tools = filter_tools_by_service(all_tools, "weather")

# 为不同任务使用不同工具集
def create_specialized_agent(tools, agent_type):
    """创建专门化的Agent"""
    from langchain.agents import initialize_agent, AgentType
    from langchain.llms import OpenAI
    
    llm = OpenAI(temperature=0)
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent

# 创建文件管理专用Agent
file_agent = create_specialized_agent(file_management_tools, "file_manager")

# 创建天气查询专用Agent
weather_agent = create_specialized_agent(weather_tools, "weather_assistant")
```

### 工具性能监控

```python
from mcpstore import MCPStore
import time
import functools

# 初始化
store = MCPStore.setup_store()

class LangChainToolMonitor:
    """LangChain工具性能监控"""
    
    def __init__(self):
        self.call_stats = {}
    
    def monitor_tool(self, tool):
        """为工具添加监控装饰器"""
        original_run = tool.run
        
        @functools.wraps(original_run)
        def monitored_run(*args, **kwargs):
            start_time = time.time()
            tool_name = tool.name
            
            try:
                result = original_run(*args, **kwargs)
                duration = time.time() - start_time
                
                # 记录成功调用
                self._record_call(tool_name, duration, True, None)
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # 记录失败调用
                self._record_call(tool_name, duration, False, str(e))
                raise
        
        tool.run = monitored_run
        return tool
    
    def _record_call(self, tool_name, duration, success, error):
        """记录工具调用"""
        if tool_name not in self.call_stats:
            self.call_stats[tool_name] = {
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "total_duration": 0,
                "avg_duration": 0,
                "errors": []
            }
        
        stats = self.call_stats[tool_name]
        stats["total_calls"] += 1
        stats["total_duration"] += duration
        stats["avg_duration"] = stats["total_duration"] / stats["total_calls"]
        
        if success:
            stats["successful_calls"] += 1
        else:
            stats["failed_calls"] += 1
            stats["errors"].append(error)
    
    def get_stats(self):
        """获取统计信息"""
        return self.call_stats
    
    def print_stats(self):
        """打印统计信息"""
        print("=== LangChain工具调用统计 ===")
        for tool_name, stats in self.call_stats.items():
            success_rate = stats["successful_calls"] / stats["total_calls"] if stats["total_calls"] > 0 else 0
            print(f"\n🛠️ {tool_name}:")
            print(f"  总调用: {stats['total_calls']}")
            print(f"  成功率: {success_rate:.1%}")
            print(f"  平均耗时: {stats['avg_duration']:.2f}秒")
            
            if stats["errors"]:
                print(f"  最近错误: {stats['errors'][-1]}")

# 使用监控器
monitor = LangChainToolMonitor()

# 获取LangChain工具并添加监控
tools = store.for_store().for_langchain().list_tools()
monitored_tools = [monitor.monitor_tool(tool) for tool in tools]

print(f"已为 {len(monitored_tools)} 个工具添加监控")

# 模拟工具调用
for tool in monitored_tools[:3]:  # 只测试前3个工具
    try:
        print(f"测试工具: {tool.name}")
        # 这里需要根据实际工具提供合适的参数
        # result = tool.run({"test": "parameter"})
    except Exception as e:
        print(f"工具测试失败: {e}")

# 查看统计
monitor.print_stats()
```

### 动态工具更新

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

class DynamicLangChainToolManager:
    """动态LangChain工具管理器"""
    
    def __init__(self, store_context):
        self.store_context = store_context
        self.current_tools = []
        self.tool_version = 0
    
    def refresh_tools(self):
        """刷新工具列表"""
        new_tools = self.store_context.for_langchain().list_tools()
        
        if len(new_tools) != len(self.current_tools):
            print(f"工具数量变化: {len(self.current_tools)} -> {len(new_tools)}")
            self.current_tools = new_tools
            self.tool_version += 1
            return True
        
        return False
    
    def get_tools(self):
        """获取当前工具列表"""
        return self.current_tools
    
    def get_tool_by_name(self, name):
        """按名称获取工具"""
        for tool in self.current_tools:
            if tool.name == name:
                return tool
        return None
    
    def list_tool_names(self):
        """列出所有工具名称"""
        return [tool.name for tool in self.current_tools]
    
    def get_version(self):
        """获取工具版本号"""
        return self.tool_version

# 使用动态工具管理器
tool_manager = DynamicLangChainToolManager(store.for_store())

# 初始化工具
tool_manager.refresh_tools()
print(f"初始工具: {tool_manager.list_tool_names()}")

# 添加新服务
store.for_store().add_service({
    "mcpServers": {
        "new_service": {
            "url": "https://api.newservice.com/mcp"
        }
    }
})

# 刷新工具
if tool_manager.refresh_tools():
    print(f"工具已更新 (版本 {tool_manager.get_version()})")
    print(f"新工具列表: {tool_manager.list_tool_names()}")

# 获取特定工具
specific_tool = tool_manager.get_tool_by_name("filesystem_read_file")
if specific_tool:
    print(f"找到工具: {specific_tool.name}")
```

## LangChain工具特性

### 1. **标准兼容**
- 完全兼容LangChain Tool接口
- 支持所有LangChain Agent类型
- 无缝集成到LangChain生态系统

### 2. **自动转换**
- 自动转换MCP工具为LangChain格式
- 保持工具名称和描述
- 处理参数模式转换

### 3. **Agent透明**
- Agent模式下工具名称本地化
- 保持Agent上下文隔离
- 支持Agent特定的工具集

### 4. **性能优化**
- 延迟加载工具列表
- 缓存工具转换结果
- 最小化转换开销

## 相关方法

- [list_tools()](../listing/list-tools.md) - 获取原始MCP工具列表
- [call_tool()](../usage/call-tool.md) - 直接调用MCP工具
- [LangChain集成示例](examples.md) - 更多LangChain集成示例

## 注意事项

1. **依赖要求**: 需要安装LangChain库
2. **工具同步**: LangChain工具列表与MCP工具保持同步
3. **参数格式**: 自动处理MCP和LangChain之间的参数格式差异
4. **错误处理**: LangChain工具调用错误会传播到原始MCP工具
5. **Agent隔离**: Agent模式下的工具转换保持上下文隔离
