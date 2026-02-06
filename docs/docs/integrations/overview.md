## 框架集成概览

MCPStore 提供了与主流 AI 框架的无缝集成，让你可以轻松地在各种 AI 开发框架中使用 MCP 工具。

## 支持的框架

MCPStore 目前支持以下主流 AI 框架：

| 框架 | 状态 | 集成方式 |
|------|------|----------|
| **LangChain** | 完全支持 | `for_langchain()` |
| **LlamaIndex** | 完全支持 | `for_llamaindex()` |
| **CrewAI** | 完全支持 | `for_crewai()` |
| **LangGraph** | 完全支持 | `for_langgraph()` |
| **AutoGen** | 完全支持 | `for_autogen()` |
| **Semantic Kernel** | 完全支持 | `for_semantic_kernel()` |

---

## 快速开始

### 通用集成模式

所有框架集成都遵循相同的模式：

```python
from mcpstore import MCPStore

# 1. 初始化 Store
store = MCPStore.setup_store()

# 2. 添加 MCP 服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 3. 等待服务就绪
store.for_store().wait_service("weather")

# 4. 转换为目标框架的工具格式
# LangChain
langchain_tools = store.for_store().for_langchain().list_tools()

# LlamaIndex
llamaindex_tools = store.for_store().for_llamaindex().list_tools()

# CrewAI
crewai_tools = store.for_store().for_crewai().list_tools()

# ... 其他框架类似
```

---

## LangChain 集成示例

### 基础集成

```python
from mcpstore import MCPStore
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 初始化 MCPStore
store = MCPStore.setup_store()

# 添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_agent("agent1").wait_service("weather")

# 转换为 LangChain 工具
lc_tools = store.for_agent("agent1").for_langchain().list_tools()

# 创建 LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# 创建 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 创建 Agent
agent = create_tool_calling_agent(llm, lc_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=lc_tools, verbose=True)

# 执行查询
response = agent_executor.invoke({"input": "北京的天气怎么样？"})
print(response.get('output'))
```

### 设置 return_direct

MCPStore 支持为工具设置 `return_direct` 标记：

```python
# 设置工具重定向（LangChain return_direct）
store.for_agent("agent1").find_tool("get_weather").set_redirect(True)

# 转换为 LangChain 工具时，return_direct 会自动应用
lc_tools = store.for_agent("agent1").for_langchain().list_tools()

# 验证
for tool in lc_tools:
    if tool.name == "get_weather":
        print(f"return_direct: {tool.return_direct}")  # True
```

更多使用示例可参考本页的代码片段和 [工具概览](../tools/overview.md) 中的指南。

---

## 集成特性

### 统一接口
所有框架集成都使用相同的 API 模式：

```python
# 统一的调用方式
framework_tools = store.for_store().for_{framework}().list_tools()
```

### 自动转换
MCPStore 会自动将 MCP 工具转换为目标框架的工具格式：

- **LangChain**: 转换为 `StructuredTool`
- **LlamaIndex**: 转换为 `FunctionTool`
- **CrewAI**: 转换为 CrewAI 工具格式
- **LangGraph**: 转换为 LangGraph 工具格式
- **AutoGen**: 转换为 AutoGen 工具格式
- **Semantic Kernel**: 转换为 SK 函数

### 保持同步
工具配置（如 `return_direct`）会自动同步到转换后的框架工具。

### Agent 隔离
每个 Agent 可以有独立的服务和工具集成：

```python
# Agent1 使用天气服务
store.for_agent("agent1").add_service({...})
agent1_tools = store.for_agent("agent1").for_langchain().list_tools()

# Agent2 使用搜索服务
store.for_agent("agent2").add_service({...})
agent2_tools = store.for_agent("agent2").for_langchain().list_tools()

# 两个 Agent 的工具完全隔离
```

---

## 集成对比

| 特性 | LangChain | LlamaIndex | CrewAI | LangGraph | AutoGen | SK |
|------|-----------|------------|--------|-----------|---------|-----|
| 工具转换 | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| return_direct | 支持 | 不支持 | 不支持 | 支持 | 不支持 | 不支持 |
| 异步支持 | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| Agent 隔离 | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| 工具配置 | 支持 | 部分 | 部分 | 支持 | 部分 | 部分 |



## 最佳实践

### 使用 Agent 模式进行隔离

```python
# 为不同用途创建独立的 Agent
research_tools = store.for_agent("research").for_langchain().list_tools()
writing_tools = store.for_agent("writing").for_langchain().list_tools()
```

### 设置合适的 return_direct

```python
# 查询类工具适合 return_direct
store.for_agent("agent1").find_tool("search").set_redirect(True)

# 需要 Agent 解释的工具不设置
# store.for_agent("agent1").find_tool("analyze").set_redirect(False)
```

### 等待服务就绪

```python
# 在转换工具前确保服务就绪
store.for_store().wait_service("service_name", timeout=30.0)
tools = store.for_store().for_langchain().list_tools()
```

### 错误处理

```python
try:
    tools = store.for_store().for_langchain().list_tools()
    if not tools:
        print("警告：没有可用工具")
except Exception as e:
    print(f"工具转换失败: {e}")
```

---

## 常见问题

### Q: 可以同时在多个框架中使用同一个 Store 吗？
**A**: 可以！MCPStore 支持同时为多个框架提供工具：

```python
store = MCPStore.setup_store()
store.for_store().add_service({...})

# 同时使用
lc_tools = store.for_store().for_langchain().list_tools()
li_tools = store.for_store().for_llamaindex().list_tools()
```

### Q: 框架集成会影响性能吗？
**A**: 不会。工具转换是轻量级操作，不会显著影响性能。

### Q: 如何在框架中使用会话功能？
**A**: 部分框架支持会话。请参考各框架的详细文档。

### Q: 集成后如何调试？
**A**: 启用调试模式：

```python
store = MCPStore.setup_store(debug=True)
```

---

## 相关文档

- [工具管理概览](../tools/overview.md) - 了解工具管理基础
- [服务管理概览](../services/overview.md) - 了解服务管理
- [快速上手指南](../quickstart.md) - 快速入门

---

选择你使用的框架，查看详细的集成文档。
