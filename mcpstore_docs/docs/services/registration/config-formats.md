# 配置格式速查表

MCPStore 支持多种灵活的配置格式，本文档提供快速参考和示例。

## 🎯 支持的8种配置格式

### 1. 单个服务配置（字典格式）

#### 远程服务（URL方式）

```python
# 基础 HTTP 服务
{
    "name": "weather",
    "url": "https://weather-api.example.com/mcp"
}

# 带认证的 HTTP 服务
{
    "name": "secure-api",
    "url": "https://secure-api.example.com/mcp",
    "transport": "streamable-http",
    "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN",
        "User-Agent": "MCPStore/1.0"
    }
}

# SSE 传输方式
{
    "name": "realtime-api",
    "url": "https://realtime.example.com/sse",
    "transport": "sse"
}
```

#### 本地服务（命令方式）

```python
# Python 服务
{
    "name": "assistant",
    "command": "python",
    "args": ["./assistant_server.py"],
    "env": {"DEBUG": "true"}
}

# NPM 包服务
{
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
    "working_dir": "/workspace"
}

# Shell 脚本服务
{
    "name": "custom-tools",
    "command": "bash",
    "args": ["./start_tools.sh"],
    "env": {
        "TOOLS_CONFIG": "/etc/tools.conf",
        "LOG_LEVEL": "info"
    }
}
```

### 2. MCPConfig 字典方式

```python
{
    "mcpServers": {
        "weather": {
            "url": "https://weather-api.example.com/mcp",
            "transport": "streamable-http"
        },
        "maps": {
            "url": "https://maps-api.example.com/mcp",
            "transport": "sse"
        },
        "calculator": {
            "command": "python",
            "args": ["calculator_server.py"]
        }
    }
}
```

### 3. 服务名称列表方式

```python
# 从现有配置中选择服务
['weather', 'maps', 'assistant']

# 单个服务名称
['weather']
```

### 4. 批量服务列表方式

```python
[
    {
        "name": "weather",
        "url": "https://weather.example.com/mcp"
    },
    {
        "name": "maps", 
        "url": "https://maps.example.com/mcp"
    },
    {
        "name": "calculator",
        "command": "python",
        "args": ["calc_server.py"]
    }
]
```

### 5. JSON 文件方式

#### 格式1: 标准 MCPConfig 格式
```json
{
  "mcpServers": {
    "weather": {
      "url": "https://weather.example.com/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    }
  }
}
```

#### 格式2: 服务列表格式
```json
[
  {
    "name": "weather",
    "url": "https://weather.example.com/mcp"
  },
  {
    "name": "maps",
    "url": "https://maps.example.com/mcp"
  }
]
```

#### 格式3: 单个服务格式
```json
{
  "name": "weather",
  "url": "https://weather.example.com/mcp",
  "transport": "streamable-http"
}
```

### 6. 无参数方式（仅 Store 级别）

```python
# 注册所有配置文件中的服务
store.for_store().add_service()
```

### 7. 混合配置方式

```python
{
    "mcpServers": {
        "weather": {"url": "https://weather.com/mcp"}
    },
    "service_names": ["existing_service1", "existing_service2"]
}
```

### 8. 动态配置方式

```python
def create_dynamic_config(env: str):
    base_url = "https://api-dev.com" if env == "dev" else "https://api-prod.com"
    return {
        "name": f"{env}-api",
        "url": f"{base_url}/mcp",
        "headers": {"Environment": env}
    }

# 使用
config = create_dynamic_config("production")
```

## 🔧 配置字段说明

### 远程服务字段

| 字段 | 类型 | 必需 | 描述 | 示例 |
|------|------|------|------|------|
| `name` | string | ✅ | 服务唯一名称 | `"weather"` |
| `url` | string | ✅ | 服务端点URL | `"https://api.com/mcp"` |
| `transport` | string | ❌ | 传输协议 | `"streamable-http"`, `"sse"` |
| `headers` | object | ❌ | HTTP请求头 | `{"Authorization": "Bearer token"}` |
| `timeout` | number | ❌ | 超时时间（秒） | `30` |
| `keep_alive` | boolean | ❌ | 保持连接 | `true` |

### 本地服务字段

| 字段 | 类型 | 必需 | 描述 | 示例 |
|------|------|------|------|------|
| `name` | string | ✅ | 服务唯一名称 | `"calculator"` |
| `command` | string | ✅ | 启动命令 | `"python"` |
| `args` | array | ❌ | 命令参数 | `["server.py", "--port", "8080"]` |
| `env` | object | ❌ | 环境变量 | `{"DEBUG": "true"}` |
| `working_dir` | string | ❌ | 工作目录 | `"/opt/services"` |
| `timeout` | number | ❌ | 超时时间（秒） | `30` |

## 🚀 使用示例

### 基础使用

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 方式1: 单个服务字典
store.for_store().add_service({
    "name": "weather",
    "url": "https://weather.com/mcp"
})

# 方式2: MCPConfig格式
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://weather.com/mcp"}
    }
})

# 方式3: 服务名称列表
store.for_store().add_service(['weather'])

# 方式4: JSON文件
store.for_store().add_service(json_file="config.json")
```

### 链式调用

```python
# 混合使用不同格式
(store.for_store()
 .add_service({"name": "weather", "url": "https://weather.com/mcp"})
 .add_service(['maps'])
 .add_service(json_file="additional.json"))
```

### 批量注册

```python
# 批量服务配置
services = [
    {"name": "weather", "url": "https://weather.com/mcp"},
    {"name": "maps", "url": "https://maps.com/mcp"},
    {"name": "calc", "command": "python", "args": ["calc.py"]}
]

store.for_store().add_service(services)
```

## 🔍 自动配置处理

### Transport 自动推断

```python
# 自动推断为 streamable-http
{"name": "api1", "url": "https://api.example.com/mcp"}

# 自动推断为 sse
{"name": "api2", "url": "https://api.example.com/sse"}
```

### 配置验证

MCPStore 会自动：
- 验证必需字段
- 检查字段冲突（如同时指定 url 和 command）
- 清理非标准字段
- 提供友好的错误信息

### 环境变量支持

```python
import os

config = {
    "name": "secure_api",
    "url": os.getenv("API_URL", "https://default.com/mcp"),
    "headers": {
        "Authorization": f"Bearer {os.getenv('API_TOKEN')}"
    }
}
```

## 📋 配置模板

### 常用服务模板

#### OpenWeather API
```python
{
    "name": "openweather",
    "url": "https://api.openweathermap.org/mcp",
    "headers": {
        "Authorization": f"Bearer {os.getenv('OPENWEATHER_API_KEY')}"
    }
}
```

#### 文件系统服务
```python
{
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
}
```

#### 数据库服务
```python
{
    "name": "database",
    "command": "python",
    "args": ["db_server.py"],
    "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "myapp"
    }
}
```

#### Git 服务
```python
{
    "name": "git",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-git", "/repo"]
}
```

## 🚨 常见错误和解决方案

### 错误1: 缺少必需字段
```python
# ❌ 错误
{"url": "https://api.com/mcp"}  # 缺少 name

# ✅ 正确
{"name": "api", "url": "https://api.com/mcp"}
```

### 错误2: 字段冲突
```python
# ❌ 错误
{"name": "service", "url": "https://api.com", "command": "python"}

# ✅ 正确 - 选择一种方式
{"name": "service", "url": "https://api.com"}
# 或
{"name": "service", "command": "python", "args": ["server.py"]}
```

### 错误3: 无效的 transport
```python
# ❌ 错误
{"name": "api", "url": "https://api.com", "transport": "invalid"}

# ✅ 正确
{"name": "api", "url": "https://api.com", "transport": "streamable-http"}
```

## 📖 相关文档

- [add_service() 完整指南](add-service.md) - 详细的服务注册文档
- [服务注册概览](register-service.md) - 服务注册入门
- [配置文件管理](../../cli/configuration.md) - 配置文件操作
- [最佳实践](../../advanced/best-practices.md) - 使用最佳实践

## 🎯 下一步

- 学习 [add_service() 完整功能](add-service.md)
- 了解 [服务管理](../management/service-management.md)
- 掌握 [工具调用](../../tools/usage/call-tool.md)
