# LlamaIndex 集成：for_llamaindex().list_tools()

本页介绍如何将 MCPStore 的工具作为 LlamaIndex 的 FunctionTool 使用。

## 安装（可选依赖）

```bash
pip install mcpstore[llamaindex]
```

> 说明：该可选依赖只在使用 LlamaIndex 适配器时需要，默认安装不会包含。

## 获取 LlamaIndex 工具列表

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
ctx = store.for_store()

# 返回 LlamaIndex 的 FunctionTool 列表
li_tools = ctx.for_llamaindex().list_tools()
print(li_tools[:1])
```

适配器行为：
- 基于 MCP 的 ToolInfo.inputSchema 动态生成 Pydantic 模型
- 自动构造同步执行函数（内部调用 `context.call_tool`）
- 自动增强 description（附加参数说明）
- 输出 `llama_index.core.tools.FunctionTool` 对象

## 用于 LlamaIndex Agent/Workflow（示意）

```python
from llama_index.core.tools import FunctionTool
# li_tools 已是 FunctionTool 对象，可直接用于你的 Agent 或 Workflow
# 具体用法请参考 LlamaIndex 官方文档
```

更多参考：
- LlamaIndex FunctionTool 文档（官方）：https://docs.llamaindex.ai/

