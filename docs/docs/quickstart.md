<div align="center">
  <img src="assets/logo.svg" alt="MCPStore" width="400"/>
</div>

---

### mcpstore 是什么？

mcpstore 是面向开发者的开箱即用的 MCP 服务编排层：用一个 Store 统一管理服务，并将 MCP 适配给 AI 框架`LangChain等`使用。

### 简单示例

首先只需要需要初始化一个store

```python
from mcpstore import MCPStore
store = MCPStore.setup_store()
```

现在就有了一个 `store`，后续只需要围绕这个`store`去添加或者操作你的服务，`store` 会维护和管理这些 MCP 服务。

#### 给store添加第一个服务

```python
#在上面的代码下面加入
store.for_store().add_service({"mcpServers": {"mcpstore_wiki": {"url": "https://www.mcpstore.wiki/mcp"}}})
store.for_store().wait_service("mcpstore_wiki")
```

通过add方法便捷添加服务，add_service方法支持多种mcp服务配置格式，主流的mcp配置格式都可以直接传入。wait方法可选，是否同步等待服务就绪。

#### 将mcp适配转为langchain需要的对象

```python
tools = store.for_store().for_langchain().list_tools()
print("loaded langchain tools:", len(tools))
```

简单链上即可直观的将mcp适配为langchain直接使用的tools列表

##### 框架适配

会逐渐支持更多的框架

| 已支持框架 | 获取工具 |
| --- | --- |
| LangChain | `tools = store.for_store().for_langchain().list_tools()` |
| LangGraph | `tools = store.for_store().for_langgraph().list_tools()` |
| AutoGen | `tools = store.for_store().for_autogen().list_tools()` |
| CrewAI | `tools = store.for_store().for_crewai().list_tools()` |
| LlamaIndex | `tools = store.for_store().for_llamaindex().list_tools()` |

#### 现在就可以正常的使用langchain了

```python
#添加上面的代码
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    temperature=0, 
    model="deepseek-chat",
    api_key="sk-*****",
    base_url="https://api.deepseek.com"
)
agent = create_agent(model=llm, tools=tools, system_prompt="你是一个助手，回答的时候带上表情")
events = agent.invoke({"messages": [{"role": "user", "content": "mcpstore怎么添加服务？"}]})
print(events)
```

## 下一步

- [快速上手](quickstart.md) - 30秒快速上手 MCPStore
- [服务管理](services/overview.md) - 了解如何管理 MCP 服务
- [工具管理](tools/overview.md) - 学习如何使用工具

---

**准备好开始了吗？** 让我们从 [快速上手指南](quickstart.md) 开始吧！
