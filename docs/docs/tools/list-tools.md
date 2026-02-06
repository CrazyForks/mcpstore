## list_tools - 工具列表查询

MCPStore 的 `list_tools()` 方法提供完整的工具列表查询功能，支持 **Store/Agent 双模式**，返回详细的 `ToolInfo` 对象，包含工具描述、输入模式和服务归属信息。

### SDK

同步：
  - `store.for_store().list_tools() -> List[ToolInfo]`
  - `store.for_agent(id).list_tools() -> List[ToolInfo]`

异步：
  - `await store.for_store().list_tools_async() -> List[ToolInfo]`
  - `await store.for_agent(id).list_tools_async() -> List[ToolInfo]`

### ToolInfo 模型

基于真实代码分析，`ToolInfo` 包含以下完整属性：

```python
class ToolInfo:
    name: str                           # 工具名称
    description: str                    # 工具描述
    service_name: str                   # 所属服务名
    client_id: Optional[str]            # 客户端ID
    inputSchema: Optional[Dict[str, Any]] # 输入模式（JSON Schema）
```

### inputSchema 结构

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

### Agent 模式支持

### 支持状态
- 完全支持 - `list_tools()` 在 Agent 模式下可用，并支持智能等待机制

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

## 上下文模式详解

### Store 模式特点

```python
store.for_store().list_tools()
```

**核心特点**:
- 返回所有全局注册的工具
- 包括带后缀的 Agent 服务工具
- 显示完整的工具名称和服务名称
- 跨上下文的工具管理视图

### Agent 模式特点

```python
store.for_agent(agent_id).list_tools()
```

**核心特点**:
- 只返回当前 Agent 的工具
- 自动转换为本地名称
- 完全隔离的工具视图
- 智能等待优化

## 使用示例

### 基础工具列表查询

```python
from mcpstore import MCPStore

def basic_tool_listing():
    store = MCPStore.setup_store()
    tools = store.for_store().list_tools()
    print(f"总工具数: {len(tools)}")
    for tool in tools:
        print(f"- {tool.name}")
        print(f"  服务: {tool.service_name}")
        print(f"  描述: {tool.description}")
        print(f"  客户端ID: {tool.client_id}")
        if tool.inputSchema and "properties" in tool.inputSchema:
            properties = tool.inputSchema["properties"]
            print(f"  参数: {list(properties.keys())}")

basic_tool_listing()
```

### Agent 级别工具列表

```python
from mcpstore import MCPStore

def agent_tool_listing():
    store = MCPStore.setup_store()
    agent_id = "research_agent"
    agent_tools = store.for_agent(agent_id).list_tools()
    print(f"Agent '{agent_id}' 工具数: {len(agent_tools)}")
    for tool in agent_tools:
        print(f"- {tool.name}")
        print(f"  服务: {tool.service_name}")
        print(f"  客户端ID: {tool.client_id}")
        print(f"  描述: {tool.description}")
        if tool.inputSchema and "properties" in tool.inputSchema:
            print("  参数详情:")
            for name, info in tool.inputSchema["properties"].items():
                t = info.get("type", "unknown")
                d = info.get("description", "无描述")
                req = name in tool.inputSchema.get("required", [])
                mark = " *" if req else ""
                print(f"    - {name}{mark}: {t} - {d}")

agent_tool_listing()
```

### 按服务分组显示工具

```python
from mcpstore import MCPStore

def tools_by_service():
    store = MCPStore.setup_store()
    tools = store.for_store().list_tools()
    by_service = {}
    for tool in tools:
        by_service.setdefault(tool.service_name, []).append(tool)
    print("按服务分组的工具列表")
    print("=" * 50)
    for service_name, tools_list in by_service.items():
        print(f"服务: {service_name} ({len(tools_list)})")
        for tool in tools_list:
            print(f"  - {tool.name}")
            print(f"    描述: {tool.description}")
            if tool.inputSchema and "required" in tool.inputSchema:
                req = tool.inputSchema["required"]
                if req:
                    print(f"    必需参数: {', '.join(req)}")

tools_by_service()
```

### 工具详细信息展示

```python
from mcpstore import MCPStore

def detailed_tool_info():
    store = MCPStore.setup_store()
    tools = store.for_store().list_tools()
    print("工具详细信息")
    print("=" * 60)
    for tool in tools:
        print(f"工具: {tool.name}")
        print(f"  服务: {tool.service_name}")
        print(f"  客户端ID: {tool.client_id}")
        print(f"  描述: {tool.description}")
        if tool.inputSchema:
            schema = tool.inputSchema
            print("  输入模式:")
            print(f"    类型: {schema.get('type', 'unknown')}")
            if "properties" in schema:
                print("    参数列表:")
                props = schema["properties"]
                required = schema.get("required", [])
                for name, info in props.items():
                    t = info.get("type", "unknown")
                    d = info.get("description", "无描述")
                    req = name in required
                    print(f"      - {name}:")
                    print(f"        类型: {t}")
                    print(f"        必需: {'是' if req else '否'}")
                    print(f"        描述: {d}")
                    if "enum" in info:
                        print(f"        可选值: {info['enum']}")
                    if "default" in info:
                        print(f"        默认值: {info['default']}")
        else:
            print("  输入模式: 无参数")
        print("-" * 40)

detailed_tool_info()
```

### 工具统计分析

```python
from mcpstore import MCPStore

def tool_statistics():
    store = MCPStore.setup_store()
    tools = store.for_store().list_tools()
    service_counts = {}
    param_counts = {}
    total_params = 0
    tools_with_params = 0
    for tool in tools:
        s = tool.service_name
        service_counts[s] = service_counts.get(s, 0) + 1
        if tool.inputSchema and "properties" in tool.inputSchema:
            c = len(tool.inputSchema["properties"])
            param_counts[c] = param_counts.get(c, 0) + 1
            total_params += c
            tools_with_params += 1
    print("工具统计分析")
    print("=" * 40)
    print(f"总工具数: {len(tools)}")
    print(f"服务数: {len(service_counts)}")
    print(f"有参数的工具: {tools_with_params}")
    print(f"平均参数数: {total_params / tools_with_params if tools_with_params > 0 else 0:.1f}")
    print("服务工具分布:")
    for service, count in sorted(service_counts.items()):
        pct = count / len(tools) * 100
        print(f"  {service}: {count} ({pct:.1f}%)")
    print("参数数量分布:")
    for param_count, tool_count in sorted(param_counts.items()):
        print(f"  {param_count} 个参数: {tool_count} 个工具")

tool_statistics()
```

### 工具搜索和筛选

```python
from mcpstore import MCPStore

def search_and_filter_tools():
    store = MCPStore.setup_store()
    tools = store.for_store().list_tools()
    def search_tools(keyword):
        results = []
        for tool in tools:
            if (keyword.lower() in tool.name.lower() or 
                keyword.lower() in tool.description.lower() or
                keyword.lower() in tool.service_name.lower()):
                results.append(tool)
        return results
    def filter_by_service(service_name):
        return [tool for tool in tools if tool.service_name == service_name]
    def filter_by_param_count(min_params=0, max_params=None):
        results = []
        for tool in tools:
            if tool.inputSchema and "properties" in tool.inputSchema:
                cnt = len(tool.inputSchema["properties"])
            else:
                cnt = 0
            if cnt >= min_params and (max_params is None or cnt <= max_params):
                results.append(tool)
        return results
    print("搜索包含 'weather' 的工具:")
    weather_tools = search_tools("weather")
    for tool in weather_tools:
        print(f"  - {tool.name} ({tool.service_name})")
    print("筛选参数较多的工具 (>= 3个参数):")
    complex_tools = filter_by_param_count(min_params=3)
    for tool in complex_tools:
        cnt = len(tool.inputSchema.get("properties", {}))
        print(f"  - {tool.name}: {cnt} 个参数")

search_and_filter_tools()
```

### 异步工具列表查询

```python
import asyncio
from mcpstore import MCPStore

async def async_tool_listing():
    store = MCPStore.setup_store()
    tools = await store.for_store().list_tools_async()
    print(f"异步获取到 {len(tools)} 个工具")
    agent_ids = ["agent1", "agent2", "agent3"]
    tasks = [store.for_agent(a).list_tools_async() for a in agent_ids]
    agent_tools_list = await asyncio.gather(*tasks)
    for agent_id, agent_tools in zip(agent_ids, agent_tools_list):
        print(f"Agent {agent_id}: {len(agent_tools)} 个工具")
        for tool in agent_tools[:2]:
            print(f"  - {tool.name}")

# asyncio.run(async_tool_listing())
```

### 工具对比分析

```python
from mcpstore import MCPStore

def compare_store_vs_agent_tools():
    store = MCPStore.setup_store()
    store_tools = store.for_store().list_tools()
    agent_id = "test_agent"
    agent_tools = store.for_agent(agent_id).list_tools()
    print("Store vs Agent 工具对比")
    print("=" * 50)
    print(f"Store 级别工具 ({len(store_tools)}):")
    for tool in store_tools:
        print(f"  - {tool.name} ({tool.service_name})")
    print(f"Agent '{agent_id}' 工具 ({len(agent_tools)}):")
    for tool in agent_tools:
        print(f"  - {tool.name} ({tool.service_name})")
    store_names = {t.name for t in store_tools}
    agent_names = {t.name for t in agent_tools}
    print("隔离分析:")
    print(f"  Store 独有工具: {len(store_names - agent_names)} 个")
    print(f"  Agent 独有工具: {len(agent_names - store_names)} 个")
    print(f"  共同工具: {len(store_names & agent_names)} 个")

compare_store_vs_agent_tools()
```

## 智能等待机制

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

## API 响应格式

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

### 性能

- **平均耗时**: 0.001秒
- **缓存机制**: 内存缓存，实时更新
- **智能等待**: 自动等待服务初始化完成
- **并发支持**: 支持异步并发查询
- **数据一致性**: 实时反映工具状态

### 相关文档

- [call_tool()](call-tool.md) - 工具调用方法
- [服务列表查询](../services/list-services.md) - 获取服务列表

### 下一步

- 学习 [工具调用方法](call-tool.md)
- 掌握 [服务列表查询](../services/list-services.md)
