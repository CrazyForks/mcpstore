# Semantic Kernel 集成：for_semantic_kernel().list_tools()

本页介绍如何将 MCPStore 的工具注册为 Semantic Kernel 的 native functions。

## 安装（可选依赖）

```bash
pip install mcpstore[semantic-kernel]
```

## 获取可注册的函数列表

适配器会根据 inputSchema 生成可直接注册为 SK native function 的 Python 函数，内部调用 `context.call_tool`。

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
ctx = store.for_store()

fns = ctx.for_semantic_kernel().list_tools()
print(fns[:1], callable(fns[0]))
```

## 在 SK 中注册（示意）

不同版本 API 略有差异，以下为 Python 版本的思路：

```python
# 参见官方文档：Provide native code to your agents | Microsoft Learn
# https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/adding-native-plugins

# 将 fns 中的函数注册到 Kernel/Plugin（示意）
# kernel.plugins.add_from_object(MyPluginClass())
# 或直接将函数包装到带 @kernel_function 的类中再注册
```

