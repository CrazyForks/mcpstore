# LangGraph 集成：for_langgraph().list_tools()

本页介绍如何将 MCPStore 的工具用于 LangGraph。

## 说明

LangGraph 使用 LangChain 的工具生态。因此 `for_langgraph()` 适配器复用 `for_langchain()` 输出，零额外依赖。

## 获取 LangGraph 可用工具列表

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
ctx = store.for_store()

# 输出与 LangChain 工具兼容的对象列表
lg_tools = ctx.for_langgraph().list_tools()
print(lg_tools[:1])
```

你可以将这些工具交给 LangGraph 的 ToolNode 或预置 Agent 使用。

更多参考：
- LangGraph 工具调用（官方）：https://langchain-ai.github.io/langgraph/how-tos/tool-calling/

