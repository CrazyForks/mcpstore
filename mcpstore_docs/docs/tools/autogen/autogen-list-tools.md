# AutoGen 集成：for_autogen().list_tools()

本页介绍如何将 MCPStore 的工具注册到 Microsoft AutoGen。

## 安装（可选依赖）

```bash
pip install mcpstore[autogen]
```

## 获取可注册的函数列表

适配器会根据 inputSchema 生成带注解/可 introspect 的 Python 函数，内部调用 `context.call_tool`。

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
ctx = store.for_store()

fns = ctx.for_autogen().list_tools()
print(fns[:1], callable(fns[0]))
```

## 在 AutoGen 中注册（示意）

不同版本 API 略有差异，以下为 0.2 文档中的示意：

```python
# 参考 AutoGen 官方教程：Tool Use | AutoGen 0.2
# https://microsoft.github.io/autogen/0.2/docs/tutorial/tool-use/

# 将 fns 中的函数注册到你的 Agent（示意）
# user_proxy.register_tool(fns[0])
```

