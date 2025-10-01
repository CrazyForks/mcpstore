# 快速上手

欢迎使用 MCPStore！本指南将带你快速上手，从安装到第一次调用工具。

## 1️⃣ 安装 MCPStore

使用 pip 安装 MCPStore：

```bash
pip install mcpstore
```

**安装完成！** 接下来让我们初始化你的第一个 Store。

---

## 2️⃣ 初始化 Store

### 基础初始化

```python
from mcpstore import MCPStore

# 初始化 Store
store = MCPStore.setup_store()
```

就这么简单！两行代码完成初始化。

### setup_store() 的作用

`setup_store()` 是 MCPStore 的核心初始化方法，它会自动完成以下工作：

- 📁 **加载配置文件**：自动读取 `mcp.json`（如果存在）
- 🔧 **初始化核心组件**：准备服务管理器、工具管理器
- 🚀 **准备就绪**：返回一个可用的 Store 实例

### 自定义配置（可选）

```python
# 指定配置文件路径
store = MCPStore.setup_store(
    mcp_config_file="path/to/custom-config.json"
)

# 启用调试模式
store = MCPStore.setup_store(debug=True)
```

> 💡 **提示**: `setup_store()` 支持更多高级配置选项（如工作空间路径、日志级别等）。  
> 📖 **详细配置请参考**：[MCPStore 类完整文档](../api-reference/mcpstore-class.md)

---

## 3️⃣ 🎉 恭喜！你现在拥有一个 MCP 服务的 Store 了

初始化完成后，你已经拥有了一个功能完整的 MCPStore 实例。

### 接下来你可以：

#### 📝 **添加服务并开始使用**
👉 [前往添加服务指南](../services/registration/add-service.md)

添加 MCP 服务是使用 MCPStore 的第一步，了解如何：
- 添加远程服务（HTTP/WebSocket）
- 添加本地服务（命令行启动）
- 使用不同的配置格式

#### 🔍 **探索完整功能**
- 📊 [服务管理概览](../services/overview.md) - 了解服务的完整生命周期管理
- 🛠️ [工具管理概览](../tools/overview.md) - 了解如何查找和使用工具
- 🔐 [权限认证配置](../authentication/overview.md) - 配置服务认证（如需要）

---

## 4️⃣ 完整示例：从零到调用工具

### 最简示例（30秒上手）

```python
from mcpstore import MCPStore

# 1. 初始化
store = MCPStore.setup_store()

# 2. 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 3. 等待服务就绪
store.for_store().wait_service("weather")

# 4. 列出可用工具
tools = store.for_store().list_tools()
print(f"✅ 可用工具: {[t.name for t in tools]}")

# 5. 调用工具
result = store.for_store().call_tool(
    "get_current_weather", 
    {"query": "北京"}
)
print(f"🌤️ 天气查询结果: {result.text_output}")
```

**运行这段代码，你将看到：**
1. Store 初始化成功
2. 服务添加并连接成功
3. 工具列表显示
4. 天气查询结果输出

### 完整示例（包含错误处理）

```python
from mcpstore import MCPStore

def main():
    # 初始化 Store
    print("📦 初始化 MCPStore...")
    store = MCPStore.setup_store()
    print("✅ Store 初始化成功")
    
    # 添加服务
    print("\n📝 添加天气服务...")
    try:
        store.for_store().add_service({
            "mcpServers": {
                "weather": {"url": "https://mcpstore.wiki/mcp"}
            }
        })
        print("✅ 服务添加成功")
    except Exception as e:
        print(f"❌ 服务添加失败: {e}")
        return
    
    # 等待服务就绪
    print("\n⏳ 等待服务就绪...")
    success = store.for_store().wait_service("weather", timeout=30.0)
    if success:
        print("✅ 服务就绪")
    else:
        print("❌ 服务启动超时")
        return
    
    # 列出工具
    print("\n🛠️ 获取工具列表...")
    tools = store.for_store().list_tools()
    print(f"✅ 发现 {len(tools)} 个工具:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # 调用工具
    if tools:
        print("\n🌤️ 调用天气查询工具...")
        try:
            result = store.for_store().call_tool(
                "get_current_weather",
                {"query": "北京"}
            )
            print(f"✅ 查询成功:")
            print(f"   {result.text_output}")
        except Exception as e:
            print(f"❌ 工具调用失败: {e}")

if __name__ == "__main__":
    main()
```

### Agent 模式示例

MCPStore 支持 Agent 独立管理服务和工具：

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent 模式：每个 Agent 有独立的服务空间
agent_id = "research_agent"

# Agent 添加专属服务
store.for_agent(agent_id).add_service({
    "mcpServers": {
        "search": {"url": "https://search-api.example.com/mcp"}
    }
})

# Agent 等待服务
store.for_agent(agent_id).wait_service("search")

# Agent 使用工具
tools = store.for_agent(agent_id).list_tools()
result = store.for_agent(agent_id).call_tool("search", {"query": "AI"})

print(f"🤖 Agent '{agent_id}' 搜索结果: {result.text_output}")
```

**Agent 模式的优势：**
- 🔒 **完全隔离**：每个 Agent 的服务和工具互不影响
- 📦 **独立管理**：可以为不同 Agent 配置不同的服务
- 🎯 **精准控制**：适用于多 Agent 系统

---

## 📚 下一步学习路径

### 🌟 **推荐路线**

1. **服务管理** → 学习如何管理 MCP 服务
   - 📝 [添加服务](../services/registration/add-service.md)
   - 🔍 [查找服务](../services/listing/find-service.md)
   - 🏥 [健康检查](../services/health/check-services.md)

2. **工具使用** → 学习如何使用工具
   - 🔍 [查找工具](../tools/finding/find-tool.md)
   - 🚀 [调用工具](../tools/usage/call-tool.md)
   - 📊 [工具统计](../tools/stats/usage-stats.md)

3. **高级功能** → 深入了解 MCPStore
   - 🔗 [LangChain 集成](../tools/langchain/examples.md)
   - 🔐 [权限认证](../authentication/overview.md)
   - 🏗️ [架构设计](../architecture/overview.md)

### 📖 **完整文档导航**

- [服务管理概览](../services/overview.md) - 服务的完整生命周期
- [工具管理概览](../tools/overview.md) - 工具的查找、调用和统计
- [示例代码集合](../examples/complete-examples.md) - 更多实用示例
- [API 参考](../api-reference/mcpstore-class.md) - 完整 API 文档

---

## 💡 常见问题

### Q: 必须要有配置文件吗？
**A**: 不需要。可以直接通过代码添加服务，不需要 `mcp.json` 配置文件。

### Q: Store 级别和 Agent 级别有什么区别？
**A**: 
- **Store 级别**：全局共享，适合通用服务
- **Agent 级别**：独立隔离，适合多 Agent 系统

详见：[服务管理概览 - Store vs Agent 模式](../services/overview.md#store-vs-agent-模式)

### Q: 支持哪些类型的 MCP 服务？
**A**: 
- ✅ HTTP/HTTPS 服务（远程）
- ✅ WebSocket 服务（远程）
- ✅ 命令行启动的本地服务（如 npx、python 等）

详见：[添加服务 - 配置格式](../services/registration/add-service.md#支持的配置格式)

### Q: 如何调试服务连接问题？
**A**: 启用调试模式：

```python
store = MCPStore.setup_store(debug=True)
```

详见：[MCPStore 类文档 - 调试模式](../api-reference/mcpstore-class.md)

---

## 🆘 需要帮助？

- 📖 [完整文档](https://mcpstore.wiki)
- 🐛 [提交问题](https://github.com/whillhill/mcpstore/issues)
- 💬 [讨论区](https://github.com/whillhill/mcpstore/discussions)

---

**准备好了吗？** 🚀  
[👉 开始添加你的第一个服务](../services/registration/add-service.md)

---

**更新时间**: 2025-01-09  
**版本**: 2.0.0

