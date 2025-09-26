# 工具管理概览

MCPStore 提供了完整的工具管理功能，支持工具查询、调用、统计分析和框架集成。

## 🔍 **工具查询**

### 核心方法
- **[list_tools()](listing/list-tools.md)** - 列出所有可用工具
- **[get_tools_with_stats()](listing/get-tools-with-stats.md)** - 获取工具列表及统计信息

## 🛠️ **工具调用**

### 核心方法
- **[call_tool()](usage/call-tool.md)** - 调用指定工具（推荐）
- **[use_tool()](usage/use-tool.md)** - 调用工具的向后兼容别名

## 📊 **工具统计分析**

### 核心方法
- **[get_system_stats()](stats/get-system-stats.md)** - 获取系统统计信息
- **[get_usage_stats()](stats/get-usage-stats.md)** - 获取使用统计
- **[get_performance_report()](stats/get-performance-report.md)** - 获取性能报告

## 🔧 **工具转换**

### 核心方法
- **[create_simple_tool()](transform/create-simple-tool.md)** - 创建简化版本的工具
- **[create_safe_tool()](transform/create-safe-tool.md)** - 创建安全版本的工具（带验证）

## 🔗 **框架集成**

### LangChain 集成
- **[for_langchain().list_tools()](langchain/langchain-list-tools.md)** - 转换为LangChain工具
- **[LangChain集成示例](langchain/examples.md)** - 完整的LangChain使用示例

## 🎯 **快速开始**

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
    }
})

# 列出所有工具
tools = store.for_store().list_tools()
print(f"可用工具: {[t.name for t in tools]}")

# 调用工具
result = store.for_store().call_tool("read_file", {"path": "/tmp/example.txt"})
print(f"工具调用结果: {result}")

# 获取工具统计
stats = store.for_store().get_tools_with_stats()
print(f"工具统计: {stats}")
```

## 🤖 **Agent 透明代理**

MCPStore 支持 Agent 透明代理模式，提供智能工具解析：

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent 模式操作
agent_context = store.for_agent("my_agent")

# Agent 只看到本地名称的工具
agent_tools = agent_context.list_tools()

# 智能工具调用（支持精确匹配、前缀匹配、模糊匹配）
result = agent_context.call_tool("read_file", {"path": "/tmp/data.txt"})
```

## 🏗️ **工具架构特性**

- **智能解析**: 支持精确匹配、前缀匹配、模糊匹配三种工具解析策略
- **透明代理**: Agent模式下自动处理工具名称映射
- **性能监控**: 内置工具调用性能统计和监控
- **框架集成**: 无缝集成LangChain等AI框架
- **安全验证**: 支持工具参数验证和安全包装

## 🔗 **相关文档**

- [工具架构设计](tool-architecture.md) - 了解工具管理的架构设计
- [Agent透明代理](../advanced/agent-transparent-proxy.md) - 深入了解Agent代理机制
- [最佳实践](../advanced/best-practices.md) - 工具使用最佳实践
