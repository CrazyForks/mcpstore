# REST API 接口

MCPStore 提供完整的 RESTful API 接口，支持通过 HTTP 请求访问所有功能。

## API 概述

- **基础URL**: `http://localhost:18200`
- **响应格式**: JSON
- **请求方式**: RESTful 风格
- **认证方式**: 无需认证（本地服务）
- **总端点数**: 56个

### API 分类

| 分类 | 端点数量 | 描述 |
|------|----------|------|
| Store 级别 | 25个 | 全局服务和工具管理 |
| Agent 级别 | 14个 | Agent 独立服务管理 |
| 监控系统 | 14个 | 系统监控和统计 |
| 应用级别 | 2个 | 应用状态和工作空间 |
| 系统级别 | 1个 | 根端点信息 |

## 启动 API 服务器

```python
from mcpstore import MCPStore

# 初始化 MCPStore
store = MCPStore.setup_store()

# 启动 API 服务器
store.start_api_server(
    host="0.0.0.0",
    port=18200,
    show_startup_info=False
)

# 服务器启动后可通过 HTTP 访问
# 访问地址: http://localhost:18200
```

## 🏪 Store 级别 API (25个端点)

### 服务管理

#### 注册服务
```http
POST /for_store/add_service
Content-Type: application/json

{
    "name": "weather-api",
    "url": "https://weather.example.com/mcp"
}
```

#### 获取服务列表
```http
GET /for_store/list_services
```

**响应示例**:
```json
{
    "success": true,
    "services": [
        {
            "name": "weather-api",
            "url": "https://weather.example.com/mcp",
            "status": "healthy",
            "tool_count": 3,
            "transport_type": "streamable_http"
        }
    ],
    "total_services": 1,
    "total_tools": 3
}
```

#### 获取服务详细信息
```http
GET /for_store/get_service_info?name=weather-api
```

### 工具管理

#### 获取工具列表
```http
GET /for_store/list_tools
```

**响应示例**:
```json
{
    "success": true,
    "tools": [
        {
            "name": "get_weather",
            "description": "获取天气信息",
            "service_name": "weather-api",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                }
            }
        }
    ],
    "total_tools": 1
}
```

#### 调用工具
```http
POST /for_store/call_tool
Content-Type: application/json

{
    "tool_name": "get_weather",
    "args": {
        "city": "北京"
    }
}
```

**响应示例**:
```json
{
    "success": true,
    "result": {
        "city": "北京",
        "temperature": 25,
        "weather": "晴天"
    }
}
```

#### 使用工具（向后兼容）
```http
POST /for_store/use_tool
Content-Type: application/json

{
    "tool_name": "get_weather",
    "args": {
        "city": "上海"
    }
}
```

### 健康检查和监控

#### 服务健康检查
```http
GET /for_store/check_services
```

#### Store 健康状态
```http
GET /for_store/health
```

#### 获取统计信息
```http
GET /for_store/get_stats
```

### 配置管理

#### 显示 MCP 配置
```http
GET /for_store/show_mcpconfig
```

#### 重置配置
```http
POST /for_store/reset_config
```

#### 重置 MCP JSON 文件
```http
POST /for_store/reset_mcp_json_file
```

### 服务生命周期

#### 等待服务状态
```http
POST /for_store/wait_service
Content-Type: application/json

{
    "client_id_or_service_name": "weather-api",
    "status": "healthy",
    "timeout": 10.0,
    "raise_on_timeout": false
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "Service wait completed: success",
    "data": {
        "client_id_or_service_name": "weather-api",
        "target_status": "healthy",
        "timeout": 10.0,
        "result": true,
        "context": "store"
    }
}
```

#### 删除服务
```http
DELETE /for_store/delete_service/{service_name}
```

#### 两步删除服务
```http
POST /for_store/delete_service_two_step
Content-Type: application/json

{
    "service_name": "weather-api"
}
```

### 系统信息

#### 获取工具记录
```http
GET /for_store/tool_records?limit=100
```

#### 网络端点检查
```http
POST /for_store/network_check
Content-Type: application/json

{
    "endpoints": ["https://api.example.com", "https://api2.example.com"]
}
```

#### 获取系统资源
```http
GET /for_store/system_resources
```

## 🤖 Agent 级别 API (14个端点)

### 服务管理

#### 注册 Agent 服务
```http
POST /for_agent/{agent_id}/add_service
Content-Type: application/json

{
    "name": "agent-tool",
    "url": "https://agent.example.com/mcp"
}
```

#### 获取 Agent 服务列表
```http
GET /for_agent/{agent_id}/list_services
```

#### 获取 Agent 工具列表
```http
GET /for_agent/{agent_id}/list_tools
```

#### 调用 Agent 工具
```http
POST /for_agent/{agent_id}/call_tool
Content-Type: application/json

{
    "tool_name": "agent_tool",
    "args": {
        "param": "value"
    }
}
```

#### 使用 Agent 工具（向后兼容）
```http
POST /for_agent/{agent_id}/use_tool
Content-Type: application/json

{
    "tool_name": "agent_tool",
    "args": {
        "param": "value"
    }
}
```

### Agent 管理

#### Agent 等待服务状态
```http
POST /for_agent/{agent_id}/wait_service
Content-Type: application/json

{
    "client_id_or_service_name": "local-service",
    "status": ["healthy", "warning"],
    "timeout": 15.0,
    "raise_on_timeout": false
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "Service wait completed: success",
    "data": {
        "agent_id": "my-agent",
        "client_id_or_service_name": "local-service",
        "target_status": ["healthy", "warning"],
        "timeout": 15.0,
        "result": true,
        "context": "agent"
    }
}
```

#### Agent 健康检查
```http
GET /for_agent/{agent_id}/check_services
```

#### 删除 Agent 服务
```http
DELETE /for_agent/{agent_id}/delete_service/{service_name}
```

#### 显示 Agent MCP 配置
```http
GET /for_agent/{agent_id}/show_mcpconfig
```

#### 重置 Agent 配置
```http
POST /for_agent/{agent_id}/reset_config
```

#### Agent 健康状态
```http
GET /for_agent/{agent_id}/health
```

#### 获取 Agent 统计信息
```http
GET /for_agent/{agent_id}/get_stats
```

#### 获取 Agent 工具记录
```http
GET /for_agent/{agent_id}/tool_records?limit=50
```

## 🚀 监控系统 API (14个端点)

### 系统监控

#### 获取所有 Agent 统计摘要
```http
GET /monitoring/agents_summary
```

#### 获取监控配置
```http
GET /monitoring/config
```

#### 获取服务状态分布
```http
GET /monitoring/services_status_distribution
```

#### 获取工具使用统计
```http
GET /monitoring/tools_usage_stats
```

### 性能监控

#### 获取系统性能指标
```http
GET /monitoring/system_performance
```

#### 获取服务响应时间
```http
GET /monitoring/services_response_time
```

#### 获取错误率统计
```http
GET /monitoring/error_rate_stats
```

### 历史数据

#### 获取历史统计数据
```http
GET /monitoring/historical_stats?days=7
```

#### 获取服务健康历史
```http
GET /monitoring/service_health_history?service_name=weather-api&hours=24
```

#### 获取工具调用历史
```http
GET /monitoring/tool_call_history?limit=100
```

### 实时监控

#### 获取实时系统状态
```http
GET /monitoring/realtime_status
```

#### 获取活跃连接数
```http
GET /monitoring/active_connections
```

#### 获取资源使用情况
```http
GET /monitoring/resource_usage
```

#### 获取告警信息
```http
GET /monitoring/alerts
```

## 🏗️ 应用级别 API (2个端点)

#### 系统健康检查
```http
GET /health
```

**响应示例**:
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00Z",
    "version": "0.5.0"
}
```

#### 获取工作空间信息
```http
GET /workspace/info
```

**响应示例**:
```json
{
    "workspace_path": "/path/to/workspace",
    "config_files": ["mcp.json", "client_services.json"],
    "data_space": "default"
}
```

## 🌐 系统级别 API (1个端点)

#### API 根端点信息
```http
GET /
```

**响应示例**:
```json
{
    "name": "MCPStore API",
    "version": "0.5.0",
    "description": "Intelligent Agent Tool Service Store",
    "endpoints": {
        "store": 25,
        "agent": 14,
        "monitoring": 14,
        "application": 2,
        "system": 1
    }
}
```

## 错误处理

### 标准错误响应

```json
{
    "success": false,
    "message": "错误描述",
    "error": "详细错误信息",
    "code": "ERROR_CODE"
}
```

### 常见 HTTP 状态码

| 状态码 | 描述 | 示例场景 |
|--------|------|----------|
| 200 | 成功 | 正常请求处理 |
| 400 | 请求错误 | 参数格式错误 |
| 404 | 未找到 | 服务或工具不存在 |
| 500 | 服务器错误 | 内部处理异常 |

## 使用示例

### Python 客户端

```python
import requests

# 基础 URL
base_url = "http://localhost:18200"

# 添加服务
response = requests.post(f"{base_url}/for_store/add_service", json={
    "name": "test-service",
    "url": "https://test.example.com/mcp"
})
print(response.json())

# 获取服务列表
response = requests.get(f"{base_url}/for_store/list_services")
services = response.json()
print(f"服务数量: {services['total_services']}")

# 调用工具
response = requests.post(f"{base_url}/for_store/call_tool", json={
    "tool_name": "test_tool",
    "args": {"param": "value"}
})
result = response.json()
print(f"工具结果: {result['result']}")
```

### curl 示例

```bash
# 获取服务列表
curl -X GET http://localhost:18200/for_store/list_services

# 添加服务
curl -X POST http://localhost:18200/for_store/add_service \
  -H "Content-Type: application/json" \
  -d '{"name": "weather", "url": "https://weather.com/mcp"}'

# 调用工具
curl -X POST http://localhost:18200/for_store/call_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_weather", "args": {"city": "北京"}}'
```

## 注意事项

1. **本地服务**: API 服务器默认只监听本地连接
2. **无认证**: 当前版本不需要认证，适用于本地开发
3. **JSON 格式**: 所有请求和响应都使用 JSON 格式
4. **错误处理**: 建议客户端实现适当的错误处理
5. **并发限制**: 注意并发请求的限制

## 相关文档

- [MCPStore 类](mcpstore-class.md) - 主入口类
- [数据模型](data-models.md) - 数据结构定义
- [服务注册](../services/registration/register-service.md) - 服务注册方法

## 下一步

- 了解 [CLI 工具使用](../cli/overview.md)
- 学习 [服务注册方法](../services/registration/register-service.md)
- 查看 [工具调用方法](../tools/usage/call-tool.md)
