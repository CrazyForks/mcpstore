# MCPStore

MCPStore 是一个强大的 MCP（Model Context Protocol）工具管理库。对于许多的 agent 或者 chain 来说，我们想要使用 MCP 的 tool，但是使用 MCP 的配置和管理有些复杂。针对这个情况，我开发了 MCPStore。对于智能体来说，我们相当于创建了一个 store，agent 可以挑选他需要的 MCP 服务。我的目的是让现有的 agent 开发项目可以无感添加 tool，只需要几行代码的配置，就可以在原来的代码上添加这些工具。

## 特性

- 🚀 简单集成：仅需几行代码即可完成工具调用
- 🔄 链式操作：直观的 API 设计，支持流畅的链式调用
- 🎯 精确控制：支持全局 Store 模式和独立 Agent 模式
- 🔒 隔离管理：不同 Agent 之间的服务和工具完全隔离
- 📦 配置集中：统一的配置管理，支持动态服务注册

## 快速开始

### 安装

```bash
pip install mcpstore
```

### 基础使用

只需三行代码即可实现工具调用。支持多种方式：

1. 通过配置文件注册：
```python
# 1. 创建 Store 实例
from mcpstore import MCPStore
store = MCPStore.setup_store()

# 2. 注册配置文件中的服务
reg_result = await store.for_store().add_service()

# 3. 使用工具
result = await store.for_store().use_tool(
    "高德_maps_direction_driving",
    {
        "origin": "116.481028,39.989643",
        "destination": "116.434446,39.90816"
    }
)
```

2. 直接配置方式：
```python
# 1. 创建 Store 实例
from mcpstore import MCPStore
store = MCPStore.setup_store()

# 2. 直接添加服务配置
reg_result = await store.for_store().add_service({
    "name": "高德",
    "url": "https://mcp.amap.com/sse?key=your_key",
    "transport": "sse"
})

# 3. 使用工具
result = await store.for_store().use_tool(
    "高德_maps_direction_driving",
    {
        "origin": "116.481028,39.989643",
        "destination": "116.434446,39.90816"
    }
)
```

### 服务注册方式

MCPStore 提供了灵活的服务注册机制，通过 `add_service` 方法支持多种注册方式：

#### 1. 配置文件注册
从 mcp.json 注册所有服务：
```python
await store.for_store().add_service()
```

#### 2. 服务名称注册
指定服务名称进行注册（适用于 Agent 模式）：
```python
await store.for_agent("agent_id").add_service(['高德', 'context7'])
```

#### 3. HTTP/SSE 服务配置
直接添加 HTTP 或 SSE 类型的服务：
```python
await store.for_store().add_service({
    "name": "高德",
    "url": "https://mcp.amap.com/sse?key=your_key",
    "transport": "sse",
    "headers": {  # 可选
        "Authorization": "Bearer token"
    }
})
```

#### 4. 本地命令服务配置
添加基于本地命令的服务：
```python
await store.for_store().add_service({
    "name": "local_service",
    "command": "python",
    "args": ["service.py"],
    "env": {"DEBUG": "true"},
    "working_dir": "/path/to/service"  # 可选
})
```

#### 5. NPX 工具服务配置
添加基于 NPX 的工具服务：
```python
await store.for_store().add_service({
    "name": "context7",
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"]
})
```

#### 配置同步机制

- 所有通过 `add_service` 添加的服务配置都会自动同步到 mcp.json 文件
- Store 模式下添加的服务对所有 Agent 可见
- Agent 模式下添加的服务会：
  - 更新到 mcp.json（如果是新服务）
  - 在 agent_clients.json 中创建 Agent-Client 映射
  - 在 client_services.json 中添加客户端配置

#### 最佳实践

1. Store 模式使用建议：
   - 全局服务优先使用配置文件注册
   - 动态服务使用直接配置方式添加

2. Agent 模式使用建议：
   - 已有服务使用服务名称列表注册
   - 特定服务使用直接配置方式添加
   - 注意服务隔离，避免相互影响

3. 配置管理：
   - 定期检查配置文件同步状态
   - 重要配置变更前备份配置文件
   - 使用健康检查确保服务可用

## 使用场景

我采用直观的方法来设计 store，当你执行 `store = MCPStore.setup_store()` 之后你就拥有了一个 store，此时你可以围绕 store 进行各种操作。

### Store 模式（全局工具管理）

Store 模式下，你可以进行链式操作，代码示例：

```python
# 初始化 store
store = MCPStore.setup_store()

print('=== 1. 链式store操作 ===')
# 注册（全量）
reg_result = await store.for_store().add_service()
print('[链式store] 注册结果:', reg_result)

# 列出服务
services = await store.for_store().list_services()
print('[链式store] 服务列表:', services)

# 列出工具
tools = await store.for_store().list_tools()
print('[链式store] 工具列表:', tools)

# 健康检查
health = await store.for_store().check_services()
print('[链式store] 健康检查:', health)

# 展示单个服务详情
if services:
    detail = await store.get_service_info(services[0].name)
    print(f'[链式store] 服务详情:', detail)

# 使用工具示例
result = await store.for_store().use_tool(
    "高德_maps_direction_driving",
    {
        "origin": "116.481028,39.989643",
        "destination": "116.434446,39.90816"
    }
)
print('[链式store] 驾车导航结果:', result)
```

### Agent 模式（独立工具管理）

对于 agent 来说，如果你不希望 agent 添加所有的 MCP 工具，你希望你的 agent 可以是某一个行业的专家，你只需要指定一个 id，或者自动创建一个 id，然后你就可以对这个 agent 进行隔离的服务调用和执行。示例：

```python
print('\n=== 2. 链式agent操作 ===')
agent_id = 'agent123'

# 注册指定服务
reg_result = await store.for_agent(agent_id).add_service(['高德'])
print('[链式agent] 注册结果:', reg_result)

# 列出服务
agent_services = await store.for_agent(agent_id).list_services()
print('[链式agent] 服务列表:', agent_services)

# 列出工具
agent_tools = await store.for_agent(agent_id).list_tools()
print('[链式agent] 工具列表:', agent_tools)

# 健康检查
agent_health = await store.for_agent(agent_id).check_services()
print('[链式agent] 健康检查:', agent_health)

# 展示单个服务详情
if agent_services:
    detail = await store.get_service_info(agent_services[0].name)
    print(f'[链式agent] 服务详情:', detail)

# Agent工具调用示例
agent_result = await store.for_agent(agent_id).use_tool(
    "高德_maps_direction_walking",
    {
        "origin": "116.481028,39.989643",
        "destination": "116.434446,39.90816"
    }
)
print('[链式agent] 步行导航结果:', agent_result)
```

## 架构设计

MCPStore 采用分层架构设计：

```
MCPStore
├── Store 层：全局工具和服务管理
├── Agent 层：独立的工具和服务管理
├── 配置层：统一的配置管理
└── 执行层：工具调用和结果处理
```

### 配置文件

所有配置文件统一存放在 `data/defaults` 目录下：
- `mcp.json`: MCP 服务配置
- `client_services.json`: 客户端服务配置
- `agent_clients.json`: Agent-Client 映射配置

## API 参考

### Store API

- `for_store()`: 进入 Store 上下文
- `add_service()`: 注册服务
- `list_services()`: 列出服务
- `list_tools()`: 列出工具
- `check_services()`: 健康检查
- `use_tool()`: 调用工具

### Agent API

- `for_agent(agent_id)`: 进入 Agent 上下文
- `add_service(service_list)`: 注册指定服务
- `list_services()`: 列出 Agent 可用服务
- `list_tools()`: 列出 Agent 可用工具
- `check_services()`: Agent 服务健康检查
- `use_tool()`: 调用 Agent 可用工具

## 最佳实践

1. 合理使用 Store/Agent 模式
   - 全局工具使用 Store 模式
   - 特定场景使用 Agent 模式

2. 服务注册建议
   - Store 模式建议全量注册
   - Agent 模式按需注册

3. 错误处理
   - 注册前检查服务可用性
   - 调用时做好异常处理

## 常见问题

1. 服务注册失败
   - 检查服务配置是否正确
   - 确认服务是否可访问

2. 工具调用失败
   - 验证工具名称格式
   - 检查参数是否完整

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进 MCPStore。

## 近期计划更新 🚀

### API 增强
- [ ] 完善现有 API 的参数验证和错误处理
- [ ] 添加更多实用的工具方法
- [ ] 提供更灵活的配置选项
- [ ] 支持异步批量操作

### 服务注册增强
- [ ] 增强 `add_service` 的容错能力
- [ ] 支持多种服务注册模式（单个、批量、条件注册）
- [ ] 添加服务注册状态监控
- [ ] 支持服务热更新
- [ ] 支持自定义重试策略

### LangChain 集成
- [ ] 提供与 LangChain 的无缝集成接口
- [ ] 支持 LangChain Agent 工具链
- [ ] 实现 LangChain 工具的自动转换
- [ ] 提供标准的 LangChain 工具模板

### 配置文件管理
- [ ] 增强 JSON 配置文件的处理能力
- [ ] 支持配置文件的导入导出
- [ ] 添加配置文件的版本控制
- [ ] 提供配置文件的验证工具
- [ ] 支持配置文件的动态更新
- [ ] 添加配置文件的备份和恢复功能

### 开发者工具
- [ ] 提供更详细的调试信息
- [ ] 添加性能分析工具
- [ ] 提供服务测试工具集
- [ ] 完善开发文档

## 许可证

[License 类型]
