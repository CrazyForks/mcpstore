# 快速演示

## 5分钟快速上手

让我们通过一个简单的示例来体验 MCPStore 的强大功能。

## 基础示例

```python
store = MCPStore.setup_store()

store.for_store().add_service({"name":"mcpstore-wiki","url":"https://mcpstore.wiki/mcp"})

tools = store.for_store().list_tools()

# store.for_store().use_tool(tools[0].name,{"query":'hi!'})
```

## LangChain 集成示例

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from mcpstore import MCPStore
# ===
store = MCPStore.setup_store()
store.for_store().add_service({"name":"mcpstore-wiki","url":"https://mcpstore.wiki/mcp"})
tools = store.for_store().for_langchain().list_tools()
# ===
llm = ChatOpenAI(
    temperature=0, model="deepseek-chat",
    openai_api_key="****",
    openai_api_base="https://api.deepseek.com"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个助手，回答的时候带上表情"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# ===
query = "北京的天气怎么样？"
print(f"\n   🤔: {query}")
response = agent_executor.invoke({"input": query})
print(f"   🤖 : {response['output']}")
```

## 下一步

了解 MCPStore 的 [两种使用模式](usage-modes.md)。
