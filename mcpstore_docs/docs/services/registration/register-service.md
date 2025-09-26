# 服务注册

MCPStore 提供强大而灵活的服务注册功能，支持多种配置方式和服务类型。

## 🚀 add_service()

MCPStore 的主要服务注册方法是 `add_service()`，支持多种不同的配置格式。

### 快速开始

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 注册远程服务
store.for_store().add_service({
    "name": "weather",
    "url": "https://weather-api.example.com/mcp"
})

# 注册本地服务
store.for_store().add_service({
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
})

```

## 📋 支持的配置格式

MCPStore 支持多种配置格式，满足不同使用场景：

### 1. 单个服务配置
```python
# URL 方式
store.for_store().add_service({
    "name": "weather",
    "url": "https://weather.example.com/mcp"
})

# 本地命令方式
store.for_store().add_service({
    "name": "calculator",
    "command": "python",
    "args": ["calculator_server.py"],
    "env": {"DEBUG": "true"}
})
```

### 2. MCPConfig 格式
```python
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://weather.com/mcp"},
        "maps": {"url": "https://maps.com/mcp"}
    }
})
```

### 3. 服务名称列表
```python
# 从现有配置中选择服务
store.for_store().add_service(['weather', 'maps', 'calculator'])
```

### 4. JSON 文件方式
```python
# 从 JSON 文件读取配置
store.for_store().add_service(json_file="config/services.json")
```

### 5. 批量服务列表
```python
services = [
    {"name": "weather", "url": "https://weather.com/mcp"},
    {"name": "maps", "url": "https://maps.com/mcp"}
]
store.for_store().add_service(services)
```

## 🎯 Store vs Agent 级别

| 特性 | Store 级别 | Agent 级别 |
|------|------------|------------|
| **访问范围** | 全局共享 | 独立隔离 |
| **配置文件** | mcp.json | agent配置 |
| **适用场景** | 基础服务 | 专用服务 |

```python
# Store 级别（全局共享）
store.for_store().add_service({
    "name": "shared_weather",
    "url": "https://weather.com/mcp"
})

# Agent 级别（独立隔离）
store.for_agent("my_agent").add_service({
    "name": "private_service",
    "url": "https://private.com/mcp"
})
```


## 🛡️ 智能配置处理

- **自动 Transport 推断**: 根据 URL 自动选择传输协议
- **配置验证**: 自动验证和清理配置

## 📚 详细文档

要了解完整的功能和高级用法，请查看：

### 📖 [add_service() 完整指南](add-service.md)

包含以下详细内容：
- 🚀 三阶段架构详解
- 📋 完整方法签名和参数
- 🎯 8种配置格式详解
- 🔧 智能配置处理
- 🚀 实际使用示例
- ⚡ 等待策略
- 🛡️ 错误处理
- 📚 最佳实践
- 🔍 调试和监控

## 🔗 相关文档

- [add_service() 完整指南](add-service.md) - 详细的服务注册文档
- [服务列表查询](../listing/list-services.md) - 查看已注册的服务
- [服务管理](../management/service-management.md) - 管理服务生命周期
- [工具调用](../../tools/usage/call-tool.md) - 调用服务工具
- [配置文件管理](../../cli/configuration.md) - 配置文件操作

## 🎯 下一步

1. 阅读 [add_service() 完整指南](add-service.md) 了解所有功能
2. 学习 [工具调用方法](../../tools/usage/call-tool.md)
3. 掌握 [最佳实践](../../advanced/best-practices.md)
