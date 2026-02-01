## call_tool - 工具调用


MCPStore 推荐的工具调用方法，兼容 MCPStore 命名与能力，支持多种工具名格式、参数处理与完善的错误处理。

### SDK

同步：
  - `store.for_store().call_tool(tool_name, args=None, return_extracted=False, **kwargs) -> Any`
  - `store.for_agent(id).call_tool(tool_name, args=None, return_extracted=False, **kwargs) -> Any`

异步：
  - `await store.for_store().call_tool_async(tool_name, args=None, return_extracted=False, **kwargs) -> Any`
  - `await store.for_agent(id).call_tool_async(tool_name, args=None, return_extracted=False, **kwargs) -> Any`

### 参数

| 参数名             | 类型                    | 说明 |
|--------------------|-------------------------|------|
| `tool_name`        | str                     | 工具名称，支持多种格式（见“工具名称解析”）。 |
| `args`             | dict 或 str             | 工具参数；同步版本支持字典或 JSON 字符串；异步版本使用字典。 |
| `return_extracted` | bool                    | 是否提取返回数据；True 返回提取后的数据，False 返回完整结果对象。 |
| `timeout`          | float                   | 超时时间（秒），通过 `**kwargs` 传入。 |
| `progress_handler` | Callable[[Any], None]   | 进度回调，通过 `**kwargs` 传入。 |
| `raise_on_error`   | bool                    | 发生错误时是否抛出异常（默认 True），通过 `**kwargs` 传入。 |
| `session_id`       | str                     | 会话 ID（可选），通过 `**kwargs` 传入。 |

### 返回值

- 类型：`Any`
- 说明：
  - 当 `return_extracted=False`：返回完整的 MCPStore CallToolResult 对象（含元数据）。
  - 当 `return_extracted=True`：返回提取后的数据（自动提取 content/text/data）。


### 视角
通过 `for_store()` 调用全局工具（使用全名）。通过 `for_agent(id)` 在 Agent 空间内调用（支持本地工具名，自动映射为全局名称）。


### 工具名称解析

支持的格式：
- 直接工具名：`"get_weather"`
- 服务前缀格式：`"weather-api_get_weather"`
- 旧格式兼容：`"weather-api.get_weather"`
- Agent 本地格式：在 Agent 模式下使用本地服务名视角

解析优先级：
- 精确匹配（当前上下文）
- 前缀匹配（服务前缀）
- 模糊匹配（唯一时）
- 无匹配时返回可用工具建议


### 使用示例

基础工具调用：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 调用天气查询工具
result = store.for_store().call_tool(
    "weather-api_get_current",
    {"location": "北京"}
)
print("天气查询结果:", result)

# 调用无参数工具
result = store.for_store().call_tool("system_info_get_time")
print("系统时间:", result)

# 使用 JSON 字符串参数（同步版本支持）
result = store.for_store().call_tool(
    "maps-api_search_location",
    '{"query": "天安门", "limit": 5}'
)
print("地点搜索结果:", result)
```

Agent 模式调用：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "research_agent"

# 使用本地工具名（自动映射为全局名称）
result = store.for_agent(agent_id).call_tool(
    "weather-api_get_current",
    {"location": "上海"}
)
print(f"Agent {agent_id} 天气查询:", result)

# 调用多个工具
tools_to_call = [
    ("weather-api_get_current", {"location": "广州"}),
    ("maps-api_search_location", {"query": "珠江"}),
    ("calculator_add", {"a": 10, "b": 20})
]

for tool_name, args in tools_to_call:
    try:
        result = store.for_agent(agent_id).call_tool(tool_name, args)
        print(tool_name, "调用成功:", result)
    except Exception as e:
        print(tool_name, "调用失败:", e)
```

高级参数与额外选项：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

complex_args = {
    "location": {"lat": 39.9042, "lng": 116.4074},
    "options": {"units": "metric", "lang": "zh-CN", "include_forecast": True},
    "filters": ["temperature", "humidity", "wind"]
}

detail = store.for_store().call_tool(
    "weather-api_get_detailed",
    complex_args
)

# 使用额外参数（超时与进度回调）
processed = store.for_store().call_tool(
    "slow-service_process_data",
    {"data": "large_dataset"},
    timeout=30.0,
    progress_handler=lambda p: print(f"进度: {p}%")
)
```

错误处理与重试：
```python
from mcpstore import MCPStore
import time

store = MCPStore.setup_store()

def call_tool_with_retry(tool_name, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return store.for_store().call_tool(tool_name, args, timeout=10.0)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避

try:
    result = call_tool_with_retry("unreliable-service_process", {"input": "test_data"})
    print("重试成功:", result)
except Exception as e:
    print("最终失败:", e)

# 不抛出异常的调用
result = store.for_store().call_tool(
    "might-fail_operation",
    {"param": "value"},
    raise_on_error=False
)
print("调用结果:", result)
```

批量工具调用：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

tool_calls = [
    ("weather-api_get_current", {"location": "北京"}),
    ("weather-api_get_current", {"location": "上海"}),
    ("weather-api_get_current", {"location": "广州"}),
    ("weather-api_get_current", {"location": "深圳"})
]

results = []
for tool_name, args in tool_calls:
    try:
        out = store.for_store().call_tool(tool_name, args)
        results.append({"location": args["location"], "result": out, "success": True})
        print(args["location"], "查询成功")
    except Exception as e:
        results.append({"location": args["location"], "error": str(e), "success": False})
        print(args["location"], "查询失败", e)

successful = sum(1 for r in results if r["success"]) 
print(f"批量调用结果: {successful}/{len(results)} 成功")
```

异步工具调用与并发：
```python
import asyncio
from mcpstore import MCPStore

async def async_tool_calling():
    store = MCPStore.setup_store()

    # 单个异步调用
    result = await store.for_store().call_tool_async(
        "weather-api_get_current",
        {"location": "北京"}
    )
    print("异步天气查询:", result)

    # 并发调用多个工具
    cities = ["北京", "上海", "广州", "深圳"]
    tasks = [
        store.for_store().call_tool_async("weather-api_get_current", {"location": city})
        for city in cities
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for city, r in zip(cities, results):
        print(city, "结果:", r)

# asyncio.run(async_tool_calling())
```

链式调用：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 第一步：获取当前位置
loc = store.for_store().call_tool("location-api_get_current_location")
if not loc or "lat" not in loc:
    raise RuntimeError("无法获取当前位置")

# 第二步：根据位置获取天气
weather = store.for_store().call_tool(
    "weather-api_get_by_coordinates",
    {"lat": loc["lat"], "lng": loc["lng"]}
)

# 第三步：根据天气推荐活动
activities = store.for_store().call_tool(
    "recommendation-api_suggest_activities",
    {"weather": weather.get("condition", "unknown"), "temperature": weather.get("temperature", 20)}
)

result = {"location": loc, "weather": weather, "activities": activities}
print(result)
```

调用监控：
```python
from mcpstore import MCPStore
import time

store = MCPStore.setup_store()

def monitor_tool_call(tool_name, args):
    start_time = time.time()
    try:
        print("开始调用工具:", tool_name)
        print("参数:", args)
        result = store.for_store().call_tool(tool_name, args)
        duration = time.time() - start_time
        print("调用成功，耗时(秒):", f"{duration:.2f}")
        return {"success": True, "result": result, "duration": duration, "tool_name": tool_name}
    except Exception as e:
        duration = time.time() - start_time
        print("调用失败，耗时(秒):", f"{duration:.2f}")
        print("错误:", e)
        return {"success": False, "error": str(e), "duration": duration, "tool_name": tool_name}

tool_calls = [
    ("weather-api_get_current", {"location": "北京"}),
    ("maps-api_search_location", {"query": "故宫"}),
    ("calculator_multiply", {"a": 123, "b": 456})
]

results = [monitor_tool_call(name, params) for name, params in tool_calls]
total_duration = sum(r["duration"] for r in results)
successful_calls = sum(1 for r in results if r["success"])
print("总调用数:", len(results))
print("成功调用:", successful_calls)
print("失败调用:", len(results) - successful_calls)
print("总耗时(秒):", f"{total_duration:.2f}")
print("平均耗时(秒):", f"{(total_duration / len(results)):.2f}")
```


### 返回示例

成功：
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

失败：
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


### 你可能想找的方法

| 场景/方法     | 同步方法 |
|----------------|----------|
| 兼容调用       | `store.for_store().use_tool(...)` |
| 获取工具列表   | `store.for_store().list_tools()` |
| 服务列表       | `store.for_store().list_services()` |
| 服务信息       | `store.for_store().get_service_info(name)` |
| 服务状态       | `store.for_store().get_service_status(name)` |


### 使用场景

- 统一入口调用远程或本地工具，屏蔽传输细节。
- Agent 模式下用本地工具名开发与调试。
- 批量和并发调用场景下的统一封装与监控。
- 需要返回提取、错误吞吐与重试策略的生产用例。


### 注意事项

- 名称解析：在 Agent 模式下支持本地名称，系统自动映射为全局名称。
- 参数约束：异步版本 `args` 使用字典；同步版本支持字典或 JSON 字符串。
- 错误处理：`raise_on_error=False` 时不抛异常，请检查返回对象中的错误字段。
- 性能：密集调用建议设置 `timeout` 并采用异步并发以提升吞吐。
- 会话：在需要上下文粘性的场景可传入 `session_id`。


