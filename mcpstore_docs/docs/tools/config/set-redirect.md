# set_redirect()

设置工具的重定向标记（用于 LangChain return_direct）。

## 方法特性

- ✅ **调用方式**: ToolProxy 方法
- ✅ **Store级别**: `tool_proxy = store.for_store().find_tool("name")` 后调用
- ✅ **Agent级别**: `tool_proxy = store.for_agent("agent1").find_tool("name")` 后调用
- 📁 **文件位置**: `tool_proxy.py`
- 🎯 **应用场景**: LangChain 集成、直接返回工具结果

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `enabled` | `bool` | ❌ | `True` | 是否启用重定向 |

## 返回值

返回 `ToolProxy` 对象本身，支持链式调用。

## 使用示例

### Store级别设置重定向

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_store().wait_service("weather")

# 查找工具并设置重定向
tool_proxy = store.for_store().find_tool("get_current_weather")
tool_proxy.set_redirect(True)

print("✅ 工具重定向已设置")
```

### Agent级别设置重定向

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent级别添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_agent("agent1").wait_service("weather")

# 设置工具重定向
tool_proxy = store.for_agent("agent1").find_tool("get_current_weather")
tool_proxy.set_redirect(True)

print("✅ Agent工具重定向已设置")
```

### 链式调用

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 链式调用：查找工具 -> 设置重定向 -> 调用工具
result = (
    store.for_store()
    .find_tool("get_current_weather")
    .set_redirect(True)
    .call_tool({"query": "北京"})
)

print(f"调用结果: {result.text_output}")
```

### LangChain 集成示例

```python
from mcpstore import MCPStore
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_agent("agent1").wait_service("weather")

# 设置工具重定向（return_direct）
store.for_agent("agent1").find_tool("get_current_weather").set_redirect(True)

# 转换为 LangChain 工具
lc_tools = store.for_agent("agent1").for_langchain().list_tools()

# 验证 return_direct 已设置
for tool in lc_tools:
    if tool.name == "get_current_weather":
        print(f"return_direct: {getattr(tool, 'return_direct', False)}")

# 创建 Agent
llm = ChatOpenAI(temperature=0, model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, lc_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=lc_tools, verbose=True)

# 执行查询
response = agent_executor.invoke({"input": "北京的天气怎么样？"})
print(f"Agent响应: {response.get('output')}")
```

### 批量设置多个工具

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 获取所有工具
tools = store.for_store().list_tools()

# 批量设置重定向
redirect_tools = ["get_current_weather", "get_forecast"]

for tool in tools:
    if tool.name in redirect_tools:
        tool_proxy = store.for_store().find_tool(tool.name)
        tool_proxy.set_redirect(True)
        print(f"✅ {tool.name} 重定向已设置")
```

### 禁用重定向

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")

# 查找工具
tool_proxy = store.for_store().find_tool("get_current_weather")

# 启用重定向
tool_proxy.set_redirect(True)
print("✅ 重定向已启用")

# 禁用重定向
tool_proxy.set_redirect(False)
print("✅ 重定向已禁用")
```

## 功能说明

### 什么是 return_direct？

在 LangChain 中，`return_direct=True` 表示工具执行后直接返回结果，不再经过 Agent 的后续处理。这适用于：

1. **查询类工具**: 如天气查询、数据检索
2. **计算类工具**: 如数学计算、统计分析
3. **确定性工具**: 结果明确，无需 Agent 进一步解释

### 工作原理

```python
# 1. 在 MCPStore 中设置重定向标记
tool_proxy.set_redirect(True)

# 2. 转换为 LangChain 工具时，自动应用标记
lc_tools = store.for_agent("agent1").for_langchain().list_tools()

# 3. LangChain 工具的 return_direct 属性会被设置为 True
for tool in lc_tools:
    print(f"{tool.name}: return_direct={tool.return_direct}")
```

### 支持的工具名称格式

```python
# 简短名称
store.for_store().find_tool("get_weather").set_redirect(True)

# 服务前缀（双下划线）
store.for_store().find_tool("weather__get_weather").set_redirect(True)

# 服务前缀（单下划线）
store.for_store().find_tool("weather_get_weather").set_redirect(True)
```

## 使用场景

### 1. 天气查询工具
```python
# 天气工具直接返回结果，无需 Agent 解释
store.for_agent("agent1").find_tool("get_current_weather").set_redirect(True)
```

### 2. 数据库查询工具
```python
# 查询结果直接返回，避免 Agent 修改数据
store.for_agent("agent1").find_tool("query_database").set_redirect(True)
```

### 3. 计算工具
```python
# 计算结果直接返回
store.for_agent("agent1").find_tool("calculator").set_redirect(True)
```

## 相关方法

- [find_tool()](../finding/find-tool.md) - 查找工具
- [tool_info()](../details/tool-info.md) - 获取工具详情
- [call_tool()](../usage/call-tool.md) - 调用工具
- [LangChain 集成](../langchain/examples.md) - LangChain 使用示例

## 注意事项

1. **调用前提**: 必须先通过 `find_tool()` 获取 ToolProxy 对象
2. **LangChain 专用**: 此标记主要用于 LangChain 集成
3. **链式调用**: 返回 ToolProxy 对象，支持链式调用
4. **持久化**: 设置会在当前会话中生效
5. **Agent隔离**: Agent级别的设置只影响该Agent

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

