# call_tool() - 工具调用方法

MCPStore 的 `call_tool()` 方法是**推荐的工具调用方法**，与 FastMCP 命名保持一致。支持多种工具名称格式、智能参数处理和完整的错误处理机制。

## 🎯 方法签名

### 同步版本

```python
def call_tool(
    self, 
    tool_name: str, 
    args: Union[Dict[str, Any], str] = None, 
    **kwargs
) -> Any
```

### 异步版本

```python
async def call_tool_async(
    self, 
    tool_name: str, 
    args: Union[Dict[str, Any], str] = None, 
    **kwargs
) -> Any
```

#### 参数说明

- `tool_name`: 工具名称，支持多种格式
  - **直接工具名**: `"get_weather"`
  - **服务前缀格式**: `"weather-api_get_weather"`
  - **旧格式兼容**: `"weather-api.get_weather"`
- `args`: 工具参数
  - **字典格式**: `{"location": "北京", "units": "celsius"}`
  - **JSON字符串**: `'{"location": "北京"}'`
  - **None**: 无参数工具
- `**kwargs`: 额外参数
  - `timeout`: 超时时间（秒）
  - `progress_handler`: 进度处理器
  - `raise_on_error`: 是否抛出异常（默认 True）

#### 返回值

- **类型**: `Any`
- **说明**: 工具执行结果，格式取决于具体工具

## 🤖 Agent 模式支持

### 支持状态
- ✅ **完全支持** - `call_tool()` 在 Agent 模式下完全可用，支持智能名称解析

### Agent 模式调用
```python
# Agent 模式调用（推荐）
result = store.for_agent("research_agent").call_tool(
    "weather-api_get_current",  # 使用本地工具名
    {"location": "北京"}
)

# 异步 Agent 模式调用
result = await store.for_agent("research_agent").call_tool_async(
    "weather-api_get_current",
    {"location": "北京"}
)

# 对比 Store 模式调用
result = store.for_store().call_tool(
    "weather-apibyagent1_get_current",  # 需要完整工具名
    {"location": "北京"}
)
```

### 模式差异说明
- **Store 模式**: 使用全局工具名称，可以调用所有注册的工具
- **Agent 模式**: 支持本地工具名称，自动转换为全局名称进行调用
- **主要区别**: Agent 模式提供透明的名称映射，Agent 无需关心工具名后缀

### 工具名称映射示例

#### Store 模式调用
```python
# Store 模式需要使用完整的工具名称
result = store.for_store().call_tool(
    "weather-apibyagent1_get_current",  # 完整工具名
    {"location": "北京"}
)
```

#### Agent 模式调用
```python
# Agent 模式使用本地工具名称
result = store.for_agent("agent1").call_tool(
    "weather-api_get_current",  # 本地工具名（Agent 视角）
    {"location": "北京"}
)
# 系统自动映射为: weather-apibyagent1_get_current
```

### 名称解析优先级
在 Agent 模式下，工具名称解析遵循以下优先级：
1. **精确匹配**: 当前 Agent 的工具精确匹配
2. **前缀匹配**: 当前 Agent 的服务前缀匹配
3. **模糊匹配**: 当前 Agent 的工具部分匹配（如果唯一）
4. **错误提示**: 无匹配时提供当前 Agent 可用工具建议

### 使用建议
- **Agent 开发**: 强烈推荐使用 Agent 模式，工具名称简洁直观
- **系统集成**: 使用 Store 模式进行跨 Agent 的工具调用
- **错误处理**: Agent 模式提供更精确的错误提示和工具建议

## 🎭 上下文模式详解

### 🏪 Store 模式特点

```python
store.for_store().call_tool(tool_name, args)
```

**核心特点**:
- ✅ 使用全局工具名称调用
- ✅ 可以调用所有注册的工具
- ✅ 跨 Agent 的工具调用能力
- ✅ 完整的工具管理权限

### 🤖 Agent 模式特点

```python
store.for_agent(agent_id).call_tool(tool_name, args)
```

**核心特点**:
- ✅ 支持本地工具名称
- ✅ 自动名称映射和转换
- ✅ 完全隔离的调用环境
- ✅ 智能错误提示和建议

## 🚀 使用示例

### 基础工具调用

```python
from mcpstore import MCPStore

def basic_tool_calling():
    """基础工具调用"""
    store = MCPStore.setup_store()
    
    # 调用天气查询工具
    result = store.for_store().call_tool(
        "weather-api_get_current", 
        {"location": "北京"}
    )
    
    print(f"天气查询结果: {result}")
    
    # 调用无参数工具
    result = store.for_store().call_tool("system_info_get_time")
    print(f"系统时间: {result}")
    
    # 使用JSON字符串参数
    result = store.for_store().call_tool(
        "maps-api_search_location",
        '{"query": "天安门", "limit": 5}'
    )
    print(f"地点搜索结果: {result}")

# 使用
basic_tool_calling()
```

### Agent 模式工具调用

```python
def agent_tool_calling():
    """Agent 模式工具调用"""
    store = MCPStore.setup_store()
    
    agent_id = "research_agent"
    
    # Agent 使用原始服务名调用工具
    result = store.for_agent(agent_id).call_tool(
        "weather-api_get_current",  # 使用本地名称
        {"location": "上海"}
    )
    
    print(f"🤖 Agent '{agent_id}' 天气查询: {result}")
    
    # Agent 调用多个工具
    tools_to_call = [
        ("weather-api_get_current", {"location": "广州"}),
        ("maps-api_search_location", {"query": "珠江"}),
        ("calculator_add", {"a": 10, "b": 20})
    ]
    
    for tool_name, args in tools_to_call:
        try:
            result = store.for_agent(agent_id).call_tool(tool_name, args)
            print(f"  🔧 {tool_name}: {result}")
        except Exception as e:
            print(f"  ❌ {tool_name}: 调用失败 - {e}")

# 使用
agent_tool_calling()
```

### 高级参数处理

```python
def advanced_parameter_handling():
    """高级参数处理"""
    store = MCPStore.setup_store()
    
    # 复杂参数结构
    complex_args = {
        "location": {
            "lat": 39.9042,
            "lng": 116.4074
        },
        "options": {
            "units": "metric",
            "lang": "zh-CN",
            "include_forecast": True
        },
        "filters": ["temperature", "humidity", "wind"]
    }
    
    result = store.for_store().call_tool(
        "weather-api_get_detailed",
        complex_args
    )
    print(f"详细天气信息: {result}")
    
    # 使用额外参数
    result = store.for_store().call_tool(
        "slow-service_process_data",
        {"data": "large_dataset"},
        timeout=30.0,  # 30秒超时
        progress_handler=lambda p: print(f"进度: {p}%")
    )
    print(f"处理结果: {result}")

# 使用
advanced_parameter_handling()
```

### 错误处理和重试

```python
def error_handling_and_retry():
    """错误处理和重试"""
    store = MCPStore.setup_store()
    
    def call_tool_with_retry(tool_name, args, max_retries=3):
        """带重试的工具调用"""
        for attempt in range(max_retries):
            try:
                result = store.for_store().call_tool(
                    tool_name, 
                    args,
                    timeout=10.0
                )
                return result
            except Exception as e:
                print(f"尝试 {attempt + 1} 失败: {e}")
                if attempt == max_retries - 1:
                    raise
                import time
                time.sleep(2 ** attempt)  # 指数退避
    
    # 使用重试机制
    try:
        result = call_tool_with_retry(
            "unreliable-service_process",
            {"input": "test_data"}
        )
        print(f"重试成功: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
    
    # 不抛出异常的调用
    result = store.for_store().call_tool(
        "might-fail_operation",
        {"param": "value"},
        raise_on_error=False
    )
    
    if hasattr(result, 'is_error') and result.is_error:
        print(f"工具调用失败: {result.error_message}")
    else:
        print(f"工具调用成功: {result}")

# 使用
error_handling_and_retry()
```

### 批量工具调用

```python
def batch_tool_calling():
    """批量工具调用"""
    store = MCPStore.setup_store()
    
    # 定义要调用的工具列表
    tool_calls = [
        ("weather-api_get_current", {"location": "北京"}),
        ("weather-api_get_current", {"location": "上海"}),
        ("weather-api_get_current", {"location": "广州"}),
        ("weather-api_get_current", {"location": "深圳"})
    ]
    
    results = []
    
    print("🔄 批量调用天气查询工具:")
    for tool_name, args in tool_calls:
        try:
            result = store.for_store().call_tool(tool_name, args)
            results.append({
                "location": args["location"],
                "result": result,
                "success": True
            })
            print(f"  ✅ {args['location']}: 查询成功")
        except Exception as e:
            results.append({
                "location": args["location"],
                "error": str(e),
                "success": False
            })
            print(f"  ❌ {args['location']}: 查询失败 - {e}")
    
    # 统计结果
    successful = sum(1 for r in results if r["success"])
    print(f"\n📊 批量调用结果: {successful}/{len(results)} 成功")
    
    return results

# 使用
batch_results = batch_tool_calling()
```

### 异步工具调用

```python
import asyncio

async def async_tool_calling():
    """异步工具调用"""
    store = MCPStore.setup_store()
    
    # 单个异步调用
    result = await store.for_store().call_tool_async(
        "weather-api_get_current",
        {"location": "北京"}
    )
    print(f"异步天气查询: {result}")
    
    # 并发调用多个工具
    tasks = [
        store.for_store().call_tool_async(
            "weather-api_get_current",
            {"location": city}
        )
        for city in ["北京", "上海", "广州", "深圳"]
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    print("🔄 并发天气查询结果:")
    cities = ["北京", "上海", "广州", "深圳"]
    for i, result in enumerate(results):
        city = cities[i]
        if isinstance(result, Exception):
            print(f"  ❌ {city}: {result}")
        else:
            print(f"  ✅ {city}: 查询成功")

# 使用
# asyncio.run(async_tool_calling())
```

### 工具链式调用

```python
def chained_tool_calling():
    """工具链式调用"""
    store = MCPStore.setup_store()
    
    # 第一步：获取用户位置
    location_result = store.for_store().call_tool(
        "location-api_get_current_location"
    )
    
    if not location_result or "lat" not in location_result:
        print("❌ 无法获取当前位置")
        return
    
    print(f"📍 当前位置: {location_result}")
    
    # 第二步：根据位置获取天气
    weather_result = store.for_store().call_tool(
        "weather-api_get_by_coordinates",
        {
            "lat": location_result["lat"],
            "lng": location_result["lng"]
        }
    )
    
    print(f"🌤️ 当前天气: {weather_result}")
    
    # 第三步：根据天气推荐活动
    activity_result = store.for_store().call_tool(
        "recommendation-api_suggest_activities",
        {
            "weather": weather_result.get("condition", "unknown"),
            "temperature": weather_result.get("temperature", 20)
        }
    )
    
    print(f"🎯 推荐活动: {activity_result}")
    
    return {
        "location": location_result,
        "weather": weather_result,
        "activities": activity_result
    }

# 使用
chain_result = chained_tool_calling()
```

### 工具调用监控

```python
def tool_calling_with_monitoring():
    """带监控的工具调用"""
    store = MCPStore.setup_store()
    import time
    
    def monitor_tool_call(tool_name, args):
        """监控工具调用"""
        start_time = time.time()
        
        try:
            print(f"🚀 开始调用工具: {tool_name}")
            print(f"   参数: {args}")
            
            result = store.for_store().call_tool(tool_name, args)
            
            duration = time.time() - start_time
            print(f"✅ 调用成功，耗时: {duration:.2f}秒")
            print(f"   结果: {result}")
            
            return {
                "success": True,
                "result": result,
                "duration": duration,
                "tool_name": tool_name
            }
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ 调用失败，耗时: {duration:.2f}秒")
            print(f"   错误: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "duration": duration,
                "tool_name": tool_name
            }
    
    # 监控多个工具调用
    tool_calls = [
        ("weather-api_get_current", {"location": "北京"}),
        ("maps-api_search_location", {"query": "故宫"}),
        ("calculator_multiply", {"a": 123, "b": 456})
    ]
    
    results = []
    total_duration = 0
    
    for tool_name, args in tool_calls:
        result = monitor_tool_call(tool_name, args)
        results.append(result)
        total_duration += result["duration"]
        print("-" * 40)
    
    # 统计报告
    successful_calls = sum(1 for r in results if r["success"])
    print(f"📊 调用统计:")
    print(f"   总调用数: {len(results)}")
    print(f"   成功调用: {successful_calls}")
    print(f"   失败调用: {len(results) - successful_calls}")
    print(f"   总耗时: {total_duration:.2f}秒")
    print(f"   平均耗时: {total_duration / len(results):.2f}秒")

# 使用
tool_calling_with_monitoring()
```

## 🔧 工具名称解析

MCPStore 支持多种工具名称格式的智能解析：

### 支持的格式

1. **直接工具名**: `"get_weather"`
2. **服务前缀格式**: `"weather-api_get_weather"`
3. **旧格式兼容**: `"weather-api.get_weather"`
4. **Agent本地格式**: Agent 模式下支持本地服务名

### 解析优先级

1. **精确匹配**: 完全匹配的工具名
2. **前缀匹配**: 服务前缀匹配
3. **模糊匹配**: 部分匹配（如果唯一）
4. **错误提示**: 无匹配时提供建议

## 📊 API 响应格式

### 成功响应

```json
{
  "success": true,
  "data": {
    "temperature": 22,
    "condition": "sunny",
    "humidity": 65,
    "wind_speed": 5
  },
  "metadata": {
    "execution_time_ms": 1250,
    "trace_id": "abc12345",
    "tool_name": "weather-api_get_current",
    "service_name": "weather-api"
  },
  "message": "Tool 'weather-api_get_current' executed successfully in 1250ms"
}
```

### 错误响应

```json
{
  "success": false,
  "data": {
    "error": "Tool 'non_existent_tool' not found"
  },
  "metadata": {
    "execution_time_ms": 5,
    "trace_id": "def67890",
    "tool_name": "non_existent_tool",
    "service_name": null
  },
  "message": "Tool execution failed: Tool 'non_existent_tool' not found"
}
```

## 🎯 性能特点

- **平均耗时**: 1.0秒（取决于具体工具）
- **智能解析**: 自动解析多种工具名称格式
- **错误处理**: 完整的异常处理和错误提示
- **并发支持**: 支持异步并发调用
- **监控集成**: 内置执行时间和追踪ID

## 🔗 相关文档

- [use_tool()](use-tool.md) - 工具使用方法（兼容别名）
- [list_tools()](../listing/list-tools.md) - 获取工具列表
- [工具使用概览](tool-usage-overview.md) - 工具使用概览
- [服务管理](../../services/management/service-management.md) - 服务管理

## 🎯 下一步

- 了解 [use_tool() 兼容方法](use-tool.md)
- 学习 [工具使用概览](tool-usage-overview.md)
- 掌握 [工具列表查询](../listing/list-tools.md)
- 查看 [LangChain 集成](../../advanced/langchain-integration.md)
