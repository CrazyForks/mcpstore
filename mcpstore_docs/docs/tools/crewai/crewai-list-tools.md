# CrewAI 集成：for_crewai().list_tools()

本页介绍如何将 MCPStore 的工具用于 CrewAI。

## 说明

CrewAI 与 LangChain 工具生态兼容。因此 `for_crewai()` 适配器复用 `for_langchain()` 适配器输出，零额外依赖。

## 获取 CrewAI 可用工具列表

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
ctx = store.for_store()

# 输出与 LangChain 工具兼容的对象列表
crewai_tools = ctx.for_crewai().list_tools()
print(crewai_tools[:1])
```

然后将这些工具直接传给 Crew/Agent 的工具配置即可。

> 注意：如需 CrewAI 专属能力，可在未来扩展专用包装，但通常没有必要。

