# 快速上手

本文目标：在最短路径内完成“安装 -> 接入一个 MCP 服务 -> 列出工具”。

## 1. 安装

```bash
pip install mcpstore
```

如果你需要 Redis 作为共享缓存后端：

```bash
pip install "mcpstore[redis]"
```

## 2. 初始化 Store

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
```

## 3. 添加服务并等待就绪

```python
store.for_store().add_service(
    {"mcpServers": {"mcpstore_wiki": {"url": "https://www.mcpstore.wiki/mcp"}}}
)
store.for_store().wait_service("mcpstore_wiki")
```

## 4. 列出工具

```python
tools = store.for_store().list_tools()
print(f"工具数量: {len(tools)}")
```

## 5. 适配到 LangChain（可选）

```python
langchain_tools = store.for_store().for_langchain().list_tools()
print(f"LangChain 工具数量: {len(langchain_tools)}")
```

## 常见下一步

- 了解分组隔离：`store.for_agent(agent_id)`
- 学习服务管理：`services/overview.md`
- 学习工具管理：`tools/overview.md`
- 使用 CLI：`cli/commands.md`
