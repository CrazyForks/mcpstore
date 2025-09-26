# list_tools() - 工具列表查询

MCPStore 的 `list_tools()` 方法提供完整的工具列表查询功能，支持 **Store/Agent 双模式**，返回详细的 `ToolInfo` 对象，包含工具描述、输入模式和服务归属信息。

## 🎯 方法签名

### 同步版本

```python
def list_tools(self) -> List[ToolInfo]
```

### 异步版本

```python
async def list_tools_async(self) -> List[ToolInfo]
```

## 📊 ToolInfo 完整模型

基于真实代码分析，`ToolInfo` 包含以下完整属性：

```python
class ToolInfo:
    name: str                           # 工具名称
    description: str                    # 工具描述
    service_name: str                   # 所属服务名
    client_id: Optional[str]            # 客户端ID
    inputSchema: Optional[Dict[str, Any]] # 输入模式（JSON Schema）
```

### inputSchema 详细结构

```python
# 典型的 inputSchema 结构
{
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": "城市名称或坐标"
        },
        "units": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "温度单位"
        }
    },
    "required": ["location"]
}
```

## 🤖 Agent 模式支持

### 支持状态
- ✅ **完全支持** - `list_tools()` 在 Agent 模式下完全可用，并支持智能等待机制

### Agent 模式调用
```python
# Agent 模式调用
agent_tools = store.for_agent("research_agent").list_tools()

# 异步 Agent 模式调用
agent_tools = await store.for_agent("research_agent").list_tools_async()

# 对比 Store 模式调用
store_tools = store.for_store().list_tools()
```

### 模式差异说明
- **Store 模式**: 返回所有全局工具，包括带后缀的 Agent 服务工具
- **Agent 模式**: 只返回当前 Agent 的工具，自动转换为本地名称
- **主要区别**: Agent 模式提供完全隔离的工具视图，工具名和服务名都是本地视图

### 返回值对比

#### Store 模式返回示例
```python
[
    ToolInfo(
        name="weather_get_current",
        service_name="weather-api",
        client_id="global_agent_store:weather-api"
    ),
    ToolInfo(
        name="maps_search_locationbyagent1",
        service_name="maps-apibyagent1",
        client_id="agent1:maps-api"
    ),
    ToolInfo(
        name="calculator_addbyagent2",
        service_name="calculator-apibyagent2",
        client_id="agent2:calculator-api"
    )
]
```

#### Agent 模式返回示例
```python
# Agent "agent1" 的视图
[
    ToolInfo(
        name="weather_get_current",
        service_name="weather-api",     # 本地服务名
        client_id="agent1:weather-api"
    ),
    ToolInfo(
        name="maps_search_location",    # 本地工具名
        service_name="maps-api",        # 本地服务名
        client_id="agent1:maps-api"
    )
]
```

### 智能等待机制
- **Store 模式**: 等待所有服务初始化完成
- **Agent 模式**: 只等待当前 Agent 的服务初始化
- **性能优势**: Agent 模式等待时间更短，只关注相关服务

### 使用建议
- **Agent 开发**: 推荐使用 Agent 模式，获得干净的工具列表
- **工具管理**: 使用 Store 模式，查看所有工具的全局状态
- **性能考虑**: Agent 模式在大型系统中性能更好，等待时间更短

## 🎭 上下文模式详解

### 🏪 Store 模式特点

```python
store.for_store().list_tools()
```

**核心特点**:
- ✅ 返回所有全局注册的工具
- ✅ 包括带后缀的 Agent 服务工具
- ✅ 显示完整的工具名称和服务名称
- ✅ 跨上下文的工具管理视图

### 🤖 Agent 模式特点

```python
store.for_agent(agent_id).list_tools()
```

**核心特点**:
- ✅ 只返回当前 Agent 的工具
- ✅ 自动转换为本地名称
- ✅ 完全隔离的工具视图
- ✅ 智能等待优化

## 🚀 使用示例

### 基础工具列表查询

```python
from mcpstore import MCPStore

def basic_tool_listing():
    """基础工具列表查询"""
    store = MCPStore.setup_store()
    
    # 获取 Store 级别的工具列表
    tools = store.for_store().list_tools()
    
    print(f"📋 总共有 {len(tools)} 个工具:")
    for tool in tools:
        print(f"  🔧 {tool.name}")
        print(f"     服务: {tool.service_name}")
        print(f"     描述: {tool.description}")
        print(f"     客户端ID: {tool.client_id}")
        
        # 显示输入参数
        if tool.inputSchema and "properties" in tool.inputSchema:
            properties = tool.inputSchema["properties"]
            print(f"     参数: {list(properties.keys())}")
        print()

# 使用
basic_tool_listing()
```

### Agent 级别工具列表

```python
def agent_tool_listing():
    """Agent 级别工具列表查询"""
    store = MCPStore.setup_store()
    
    agent_id = "research_agent"
    
    # 获取特定 Agent 的工具列表
    agent_tools = store.for_agent(agent_id).list_tools()
    
    print(f"🤖 Agent '{agent_id}' 有 {len(agent_tools)} 个工具:")
    for tool in agent_tools:
        print(f"  🛠️ {tool.name}")
        print(f"     服务: {tool.service_name}")  # 显示本地服务名
        print(f"     实际客户端ID: {tool.client_id}")  # 显示全局ID
        print(f"     描述: {tool.description}")
        
        # 显示参数详情
        if tool.inputSchema:
            schema = tool.inputSchema
            if "properties" in schema:
                print(f"     参数详情:")
                for param_name, param_info in schema["properties"].items():
                    param_type = param_info.get("type", "unknown")
                    param_desc = param_info.get("description", "无描述")
                    required = param_name in schema.get("required", [])
                    required_mark = " *" if required else ""
                    print(f"       - {param_name}{required_mark}: {param_type} - {param_desc}")
        print()

# 使用
agent_tool_listing()
```

### 按服务分组显示工具

```python
def tools_by_service():
    """按服务分组显示工具"""
    store = MCPStore.setup_store()
    
    tools = store.for_store().list_tools()
    
    # 按服务分组
    service_tools = {}
    for tool in tools:
        service_name = tool.service_name
        if service_name not in service_tools:
            service_tools[service_name] = []
        service_tools[service_name].append(tool)
    
    print("📊 按服务分组的工具列表")
    print("=" * 50)
    
    for service_name, tools_list in service_tools.items():
        print(f"🔸 服务: {service_name} ({len(tools_list)} 个工具)")
        for tool in tools_list:
            print(f"   🔧 {tool.name}")
            print(f"      描述: {tool.description}")
            
            # 显示必需参数
            if tool.inputSchema and "required" in tool.inputSchema:
                required_params = tool.inputSchema["required"]
                if required_params:
                    print(f"      必需参数: {', '.join(required_params)}")
        print()

# 使用
tools_by_service()
```

### 工具详细信息展示

```python
def detailed_tool_info():
    """工具详细信息展示"""
    store = MCPStore.setup_store()
    
    tools = store.for_store().list_tools()
    
    print("🔍 工具详细信息报告")
    print("=" * 60)
    
    for tool in tools:
        print(f"🛠️ 工具名称: {tool.name}")
        print(f"   所属服务: {tool.service_name}")
        print(f"   客户端ID: {tool.client_id}")
        print(f"   描述: {tool.description}")
        
        # 详细的输入模式分析
        if tool.inputSchema:
            schema = tool.inputSchema
            print(f"   输入模式:")
            print(f"     类型: {schema.get('type', 'unknown')}")
            
            if "properties" in schema:
                print(f"     参数列表:")
                properties = schema["properties"]
                required = schema.get("required", [])
                
                for param_name, param_info in properties.items():
                    param_type = param_info.get("type", "unknown")
                    param_desc = param_info.get("description", "无描述")
                    is_required = param_name in required
                    
                    print(f"       📝 {param_name}:")
                    print(f"          类型: {param_type}")
                    print(f"          必需: {'是' if is_required else '否'}")
                    print(f"          描述: {param_desc}")
                    
                    # 显示枚举值
                    if "enum" in param_info:
                        print(f"          可选值: {param_info['enum']}")
                    
                    # 显示默认值
                    if "default" in param_info:
                        print(f"          默认值: {param_info['default']}")
        else:
            print(f"   输入模式: 无参数")
        
        print("-" * 40)

# 使用
detailed_tool_info()
```

### 工具统计分析

```python
def tool_statistics():
    """工具统计分析"""
    store = MCPStore.setup_store()
    
    tools = store.for_store().list_tools()
    
    # 统计各种指标
    service_counts = {}
    param_counts = {}
    total_params = 0
    tools_with_params = 0
    
    for tool in tools:
        # 服务统计
        service = tool.service_name
        service_counts[service] = service_counts.get(service, 0) + 1
        
        # 参数统计
        if tool.inputSchema and "properties" in tool.inputSchema:
            param_count = len(tool.inputSchema["properties"])
            param_counts[param_count] = param_counts.get(param_count, 0) + 1
            total_params += param_count
            tools_with_params += 1
    
    print("📈 工具统计分析")
    print("=" * 40)
    print(f"总工具数: {len(tools)}")
    print(f"服务数: {len(service_counts)}")
    print(f"有参数的工具: {tools_with_params}")
    print(f"平均参数数: {total_params / tools_with_params if tools_with_params > 0 else 0:.1f}")
    print()
    
    print("服务工具分布:")
    for service, count in sorted(service_counts.items()):
        percentage = count / len(tools) * 100
        print(f"  {service}: {count} ({percentage:.1f}%)")
    print()
    
    print("参数数量分布:")
    for param_count, tool_count in sorted(param_counts.items()):
        print(f"  {param_count} 个参数: {tool_count} 个工具")

# 使用
tool_statistics()
```

### 工具搜索和筛选

```python
def search_and_filter_tools():
    """工具搜索和筛选"""
    store = MCPStore.setup_store()
    
    tools = store.for_store().list_tools()
    
    def search_tools(keyword):
        """按关键词搜索工具"""
        results = []
        for tool in tools:
            if (keyword.lower() in tool.name.lower() or 
                keyword.lower() in tool.description.lower() or
                keyword.lower() in tool.service_name.lower()):
                results.append(tool)
        return results
    
    def filter_by_service(service_name):
        """按服务筛选工具"""
        return [tool for tool in tools if tool.service_name == service_name]
    
    def filter_by_param_count(min_params=0, max_params=None):
        """按参数数量筛选工具"""
        results = []
        for tool in tools:
            if tool.inputSchema and "properties" in tool.inputSchema:
                param_count = len(tool.inputSchema["properties"])
            else:
                param_count = 0
            
            if param_count >= min_params:
                if max_params is None or param_count <= max_params:
                    results.append(tool)
        return results
    
    # 搜索示例
    print("🔍 搜索包含 'weather' 的工具:")
    weather_tools = search_tools("weather")
    for tool in weather_tools:
        print(f"  - {tool.name} ({tool.service_name})")
    print()
    
    # 筛选示例
    print("🔍 筛选参数较多的工具 (>= 3个参数):")
    complex_tools = filter_by_param_count(min_params=3)
    for tool in complex_tools:
        param_count = len(tool.inputSchema.get("properties", {}))
        print(f"  - {tool.name}: {param_count} 个参数")

# 使用
search_and_filter_tools()
```

### 异步工具列表查询

```python
import asyncio

async def async_tool_listing():
    """异步工具列表查询"""
    store = MCPStore.setup_store()
    
    # 异步获取工具列表
    tools = await store.for_store().list_tools_async()
    
    print(f"🔄 异步获取到 {len(tools)} 个工具")
    
    # 并发获取多个 Agent 的工具
    agent_ids = ["agent1", "agent2", "agent3"]
    
    tasks = [
        store.for_agent(agent_id).list_tools_async()
        for agent_id in agent_ids
    ]
    
    agent_tools_list = await asyncio.gather(*tasks)
    
    for i, agent_tools in enumerate(agent_tools_list):
        agent_id = agent_ids[i]
        print(f"🤖 Agent {agent_id}: {len(agent_tools)} 个工具")
        for tool in agent_tools[:2]:  # 显示前2个工具
            print(f"  - {tool.name}")

# 使用
# asyncio.run(async_tool_listing())
```

### 工具对比分析

```python
def compare_store_vs_agent_tools():
    """对比 Store 和 Agent 工具"""
    store = MCPStore.setup_store()
    
    # Store 级别工具
    store_tools = store.for_store().list_tools()
    
    # Agent 级别工具
    agent_id = "test_agent"
    agent_tools = store.for_agent(agent_id).list_tools()
    
    print("🔍 Store vs Agent 工具对比")
    print("=" * 50)
    
    print(f"🏪 Store 级别工具 ({len(store_tools)} 个):")
    for tool in store_tools:
        print(f"  - {tool.name} ({tool.service_name})")
    
    print(f"\n🤖 Agent '{agent_id}' 工具 ({len(agent_tools)} 个):")
    for tool in agent_tools:
        print(f"  - {tool.name} ({tool.service_name})")
    
    # 分析隔离效果
    store_names = {t.name for t in store_tools}
    agent_names = {t.name for t in agent_tools}
    
    print(f"\n📊 隔离分析:")
    print(f"  Store 独有工具: {len(store_names - agent_names)} 个")
    print(f"  Agent 独有工具: {len(agent_names - store_names)} 个")
    print(f"  共同工具: {len(store_names & agent_names)} 个")

# 使用
compare_store_vs_agent_tools()
```

## 🔧 智能等待机制

MCPStore 实现了智能等待机制，确保工具列表的完整性：

### 等待策略

- **远程服务**: 最多等待 1.5 秒
- **本地服务**: 最多等待 5 秒
- **状态确定**: 服务状态确定后立即返回
- **快速路径**: 无 INITIALIZING 服务时跳过等待

### 实现原理

```python
# 智能等待逻辑（简化版）
if has_initializing_services():
    await wait_for_initializing_services()
    
# 获取工具列表
tools = await get_tools_from_cache()
```

## 📊 API 响应格式

### Store API 响应

```json
{
  "success": true,
  "data": [
    {
      "name": "weather_get_current",
      "description": "获取当前天气信息",
      "service_name": "weather-api",
      "client_id": "global_agent_store:weather-api",
      "inputSchema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "城市名称"
          }
        },
        "required": ["location"]
      }
    }
  ],
  "metadata": {
    "total_tools": 1,
    "services_count": 1
  },
  "message": "Retrieved 1 tools from 1 services"
}
```

### Agent API 响应

```json
{
  "success": true,
  "data": [
    {
      "name": "weather_get_current",
      "description": "获取当前天气信息",
      "service_name": "weather-api",
      "client_id": "agent1:weather-api",
      "inputSchema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "城市名称"
          }
        },
        "required": ["location"]
      }
    }
  ],
  "metadata": {
    "total_tools": 1,
    "services_count": 1
  },
  "message": "Retrieved 1 tools from 1 services for agent 'agent1'"
}
```

## 🎯 性能特点

- **平均耗时**: 0.001秒
- **缓存机制**: 内存缓存，实时更新
- **智能等待**: 自动等待服务初始化完成
- **并发支持**: 支持异步并发查询
- **数据一致性**: 实时反映工具状态

## 🔗 相关文档

- [call_tool()](../usage/call-tool.md) - 工具调用方法
- [use_tool()](../usage/use-tool.md) - 工具使用方法（兼容别名）
- [服务列表查询](../../services/listing/list-services.md) - 获取服务列表
- [工具使用概览](../usage/tool-usage-overview.md) - 工具使用概览

## 🎯 下一步

- 学习 [工具调用方法](../usage/call-tool.md)
- 了解 [工具使用概览](../usage/tool-usage-overview.md)
- 掌握 [服务列表查询](../../services/listing/list-services.md)
- 查看 [工具管理操作](../management/tool-management.md)
