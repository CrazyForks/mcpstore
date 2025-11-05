# 工具管理概览

MCPStore 提供了完整的工具管理功能，按照功能分类为5个核心模块，涵盖从查找到统计的全流程操作。

## 📋 **工具管理5大模块**

### 1. 🔍 **查找工具**
查找工具并获取工具代理对象或列表。

**核心方法**:
- **[find_tool()](finding/find-tool.md)** - 查找工具并返回 ToolProxy
- **[list_tools()](finding/list-tools.md)** - 列出所有可用工具

**相关文档**:
- [ToolProxy 概念](finding/tool-proxy.md) - 了解工具代理机制

---

### 2. 📊 **工具详情**
获取工具的详细信息、标签和输入模式。

**核心方法**:
- **[tool_info()](details/tool-info.md)** - 获取工具详细信息
- **[tool_tags()](details/tool-tags.md)** - 获取工具标签
- **[tool_schema()](details/tool-schema.md)** - 获取工具输入模式

> 💡 **提示**: 这些方法需要先通过 `find_tool()` 获取 ToolProxy 对象后调用

---

### 3. 🚀 **使用工具**
调用工具执行操作。

**核心方法**:
- **[call_tool()](usage/call-tool.md)** - 调用指定工具（推荐）
- **[use_tool()](usage/use-tool.md)** - 调用工具的向后兼容别名

**使用方式**:
- **Context 级别**: `store.for_store().call_tool("tool_name", args)`
- **ToolProxy 级别**: `tool_proxy.call_tool(args)`

---

### 4. ⚙️ **工具配置**
配置工具行为，如设置重定向标记。

**核心方法**:
- **[set_redirect()](config/set-redirect.md)** - 设置工具重定向标记（用于 LangChain return_direct）

**应用场景**:
- LangChain 集成
- 直接返回工具结果
- 跳过 Agent 后处理

---

### 5. 📈 **工具统计**
获取工具的使用统计和调用历史。

**核心方法**:
- **[usage_stats()](stats/usage-stats.md)** - 获取工具使用统计（ToolProxy）
- **[call_history()](stats/call-history.md)** - 获取工具调用历史（ToolProxy）
- **[tools_stats()](stats/tools-stats.md)** - 获取服务工具统计（ServiceProxy）

**对比**:
| 方法 | 调用层级 | 统计范围 |
|------|----------|----------|
| usage_stats() | ToolProxy | 单个工具 |
| call_history() | ToolProxy | 单个工具 |
| tools_stats() | ServiceProxy | 服务所有工具 |

---

## 🎯 **快速开始**

### 完整的工具管理流程

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 1️⃣ 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 2️⃣ 等待服务就绪
store.for_store().wait_service("weather")

# 3️⃣ 列出所有工具
tools = store.for_store().list_tools()
print(f"可用工具: {[t.name for t in tools]}")

# 4️⃣ 查找特定工具
tool_proxy = store.for_store().find_tool("get_current_weather")

# 5️⃣ 获取工具详情
info = tool_proxy.tool_info()
print(f"工具信息: {info['description']}")

# 6️⃣ 设置工具配置（可选）
tool_proxy.set_redirect(True)

# 7️⃣ 调用工具
result = tool_proxy.call_tool({"query": "北京"})
print(f"调用结果: {result.text_output}")

# 8️⃣ 查看统计
stats = tool_proxy.usage_stats()
print(f"调用次数: {stats['call_count']}")

# 9️⃣ 查看历史
history = tool_proxy.call_history(limit=5)
print(f"最近{len(history)}次调用")
```

### Store vs Agent 模式

MCPStore 支持两种工具管理模式：

```python
# Store 级别（全局共享）
tools = store.for_store().list_tools()
tool = store.for_store().find_tool("get_weather")
result = store.for_store().call_tool("get_weather", {"query": "北京"})

# Agent 级别（独立隔离）
tools = store.for_agent("agent1").list_tools()
tool = store.for_agent("agent1").find_tool("get_weather")
result = store.for_agent("agent1").call_tool("get_weather", {"query": "上海"})
```

| 特性 | Store 级别 | Agent 级别 |
|------|------------|------------|
| **访问范围** | 全局工具 | Agent工具 |
| **工具隔离** | 无隔离 | 完全隔离 |
| **适用场景** | 通用工具调用 | Agent专用工具 |

---

## 🎭 **调用层级说明**

MCPStore 的工具方法分为三个调用层级：

### Context 层级
通过 `store.for_store()` 或 `store.for_agent()` 调用：

```python
# Context 层级方法
store.for_store().find_tool("tool_name")   # 查找工具
store.for_store().list_tools()             # 列出工具
store.for_store().call_tool("name", args)  # 调用工具
store.for_store().use_tool("name", args)   # 调用工具别名
```

### ToolProxy 层级
通过 `find_tool()` 返回的代理对象调用：

```python
# ToolProxy 层级方法
tool_proxy = store.for_store().find_tool("tool_name")

tool_proxy.tool_info()          # 工具详情
tool_proxy.tool_tags()          # 工具标签
tool_proxy.tool_schema()        # 工具模式
tool_proxy.set_redirect(True)   # 设置重定向
tool_proxy.call_tool(args)      # 调用工具
tool_proxy.usage_stats()        # 使用统计
tool_proxy.call_history()       # 调用历史
```

### ServiceProxy 层级
通过 `find_service()` 返回的服务代理对象调用：

```python
# ServiceProxy 层级方法
svc = store.for_store().find_service("service_name")

svc.list_tools()      # 列出服务的工具
svc.tools_stats()     # 服务工具统计
```

---

## 📊 **方法速查表**

| 功能 | 方法 | 调用层级 | 文档 |
|------|------|----------|------|
| **查找** | find_tool() | Context | [查看](finding/find-tool.md) |
| **列表** | list_tools() | Context / ServiceProxy | [查看](finding/list-tools.md) |
| **详情** | tool_info() | ToolProxy | [查看](details/tool-info.md) |
| **标签** | tool_tags() | ToolProxy | [查看](details/tool-tags.md) |
| **模式** | tool_schema() | ToolProxy | [查看](details/tool-schema.md) |
| **调用** | call_tool() | Context / ToolProxy | [查看](usage/call-tool.md) |
| **别名** | use_tool() | Context | [查看](usage/use-tool.md) |
| **配置** | set_redirect() | ToolProxy | [查看](config/set-redirect.md) |
| **统计** | usage_stats() | ToolProxy | [查看](stats/usage-stats.md) |
| **历史** | call_history() | ToolProxy | [查看](stats/call-history.md) |
| **服务统计** | tools_stats() | ServiceProxy | [查看](stats/tools-stats.md) |

---

## 💡 **核心概念**

### ToolProxy
ToolProxy 是工具代理对象，类似于 ServiceProxy，提供工具级别的操作方法。

```python
# 获取 ToolProxy
tool_proxy = store.for_store().find_tool("tool_name")

# ToolProxy 提供的方法
tool_proxy.tool_info()          # 详情
tool_proxy.tool_tags()          # 标签
tool_proxy.tool_schema()        # 模式
tool_proxy.set_redirect()       # 配置
tool_proxy.call_tool()          # 调用
tool_proxy.usage_stats()        # 统计
tool_proxy.call_history()       # 历史
```

详见：[ToolProxy 概念](finding/tool-proxy.md)

### 工具名称格式
MCPStore 支持多种工具名称格式：

```python
# 1. 简短名称
tool = store.for_store().find_tool("get_weather")

# 2. 服务前缀（双下划线）
tool = store.for_store().find_tool("weather__get_weather")

# 3. 服务前缀（单下划线）
tool = store.for_store().find_tool("weather_get_weather")
```

---

## 🔗 **相关文档**

- [服务管理概览](../services/overview.md) - 了解服务管理
- [ServiceProxy 概念](../services/listing/service-proxy.md) - 理解服务代理
- [ToolProxy 概念](finding/tool-proxy.md) - 理解工具代理
- [最佳实践](../advanced/best-practices.md) - 工具使用最佳实践

---

**更新时间**: 2025-01-09  
**版本**: 2.0.0
