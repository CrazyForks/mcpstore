# 配置管理

MCPStore CLI 提供强大的配置文件管理功能，支持跨平台的配置文件查找、验证和管理。

## 配置文件概述

### 配置文件格式

MCPStore 使用 JSON 格式的配置文件 (`mcp.json`)：

```json
{
  "mcpServers": {
    "service-name": {
      "url": "https://example.com/mcp",
      "transport": "streamable-http",
      "description": "服务描述"
    }
  },
  "version": "1.0.0",
  "description": "MCPStore configuration file",
  "created_by": "MCPStore CLI"
}
```

### 支持的传输类型

| 传输类型 | 描述 | 使用场景 |
|----------|------|----------|
| `streamable-http` | HTTP 流式传输 | 远程 HTTP 服务 |
| `sse` | Server-Sent Events | 实时数据流 |
| `stdio` | 标准输入输出 | 本地命令行程序 |

## 配置文件查找

### 查找优先级

MCPStore 按以下优先级查找配置文件：

1. **当前工作目录**: `./mcp.json`
2. **用户配置目录**: `~/.mcpstore/mcp.json`
3. **系统配置目录**: 
   - Windows: `%PROGRAMDATA%\mcpstore\mcp.json`
   - macOS: `/Library/Application Support/mcpstore/mcp.json`
   - Linux: `/etc/mcpstore/mcp.json`

### 配置文件位置示例

```bash
# 查看当前使用的配置文件
ls -la mcp.json

# 查看用户配置目录
ls -la ~/.mcpstore/mcp.json

# 查看系统配置目录（Linux）
ls -la /etc/mcpstore/mcp.json
```

## 服务配置类型

### 1. 远程 HTTP 服务

适用于通过 HTTP 访问的远程 MCP 服务。

```json
{
  "mcpServers": {
    "weather-api": {
      "url": "https://weather.example.com/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "User-Agent": "MCPStore/1.0"
      },
      "timeout": 30,
      "description": "天气查询服务"
    }
  }
}
```

**必需字段**:
- `url`: 服务端点 URL

**可选字段**:
- `transport`: 传输类型（默认: `streamable-http`）
- `headers`: HTTP 请求头
- `timeout`: 超时时间（秒）
- `description`: 服务描述

### 2. 本地命令服务

适用于本地运行的命令行 MCP 服务。

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["-m", "mcp_filesystem_server"],
      "env": {
        "DEBUG": "true",
        "LOG_LEVEL": "info"
      },
      "working_dir": "/path/to/workspace",
      "description": "文件系统操作服务"
    }
  }
}
```

**必需字段**:
- `command`: 执行命令

**可选字段**:
- `args`: 命令参数列表
- `env`: 环境变量
- `working_dir`: 工作目录
- `description`: 服务描述

### 3. NPM 包服务

适用于通过 NPM 安装的 MCP 服务包。

```json
{
  "mcpServers": {
    "calculator": {
      "command": "npx",
      "args": ["-y", "@example/calculator-mcp"],
      "description": "计算器服务"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "description": "文件系统服务"
    }
  }
}
```

## 配置验证

### 自动验证

MCPStore 会自动验证配置文件的格式和内容：

#### JSON 语法验证

```json
// ❌ 错误：缺少逗号
{
  "mcpServers": {
    "service1": {"url": "https://api1.com"}
    "service2": {"url": "https://api2.com"}
  }
}

// ✅ 正确：语法正确
{
  "mcpServers": {
    "service1": {"url": "https://api1.com"},
    "service2": {"url": "https://api2.com"}
  }
}
```

#### 必需字段验证

```json
// ❌ 错误：URL 服务缺少 url 字段
{
  "mcpServers": {
    "weather": {
      "transport": "streamable-http"
    }
  }
}

// ✅ 正确：包含必需的 url 字段
{
  "mcpServers": {
    "weather": {
      "url": "https://weather.com/mcp",
      "transport": "streamable-http"
    }
  }
}
```

#### 传输类型验证

```json
// ❌ 错误：不支持的传输类型
{
  "mcpServers": {
    "service": {
      "url": "https://api.com",
      "transport": "unsupported-transport"
    }
  }
}

// ✅ 正确：支持的传输类型
{
  "mcpServers": {
    "service": {
      "url": "https://api.com",
      "transport": "streamable-http"
    }
  }
}
```

### 配置备份和恢复

当检测到配置文件损坏时，MCPStore 会自动创建备份：

```bash
# 原始文件（损坏）
mcp.json

# 自动备份文件
mcp.json.backup.20240101_120000

# 重建的配置文件
mcp.json
```

## 环境变量支持

### 配置相关环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `MCPSTORE_CONFIG` | 配置文件路径 | `mcp.json` |
| `MCPSTORE_CONFIG_DIR` | 配置目录路径 | 自动检测 |
| `MCPSTORE_DATA_DIR` | 数据目录路径 | 自动检测 |

### 使用环境变量

```bash
# 指定自定义配置文件
export MCPSTORE_CONFIG="/path/to/custom-mcp.json"
mcpstore run api

# 指定配置目录
export MCPSTORE_CONFIG_DIR="/path/to/config"
mcpstore run api
```

## 多环境配置

### 开发环境配置

```json
{
  "mcpServers": {
    "dev-api": {
      "url": "http://localhost:3000/mcp",
      "transport": "streamable-http",
      "headers": {
        "X-Environment": "development"
      },
      "description": "开发环境 API"
    },
    "local-tools": {
      "command": "python",
      "args": ["-m", "dev_tools", "--debug"],
      "env": {
        "DEBUG": "true",
        "LOG_LEVEL": "debug"
      },
      "description": "开发工具"
    }
  },
  "version": "1.0.0",
  "description": "Development configuration"
}
```

### 生产环境配置

```json
{
  "mcpServers": {
    "prod-api": {
      "url": "https://api.production.com/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer PROD_TOKEN",
        "X-Environment": "production"
      },
      "timeout": 60,
      "description": "生产环境 API"
    },
    "monitoring": {
      "url": "https://monitoring.production.com/mcp",
      "transport": "streamable-http",
      "description": "监控服务"
    }
  },
  "version": "1.0.0",
  "description": "Production configuration"
}
```

### 环境切换

```bash
# 开发环境
export MCPSTORE_CONFIG="config/dev-mcp.json"
mcpstore run api

# 测试环境
export MCPSTORE_CONFIG="config/test-mcp.json"
mcpstore run api

# 生产环境
export MCPSTORE_CONFIG="config/prod-mcp.json"
mcpstore run api
```

## 配置模板

### 基础模板

```json
{
  "mcpServers": {},
  "version": "1.0.0",
  "description": "MCPStore configuration file",
  "created_by": "MCPStore CLI"
}
```

### 完整示例模板

```json
{
  "mcpServers": {
    "weather-service": {
      "url": "https://weather.example.com/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      },
      "timeout": 30,
      "description": "天气查询服务"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "description": "文件系统操作"
    },
    "calculator": {
      "command": "python",
      "args": ["-m", "calculator_server"],
      "env": {
        "PRECISION": "10"
      },
      "working_dir": "/path/to/calculator",
      "description": "计算器服务"
    },
    "database": {
      "url": "https://db.example.com/mcp",
      "transport": "sse",
      "headers": {
        "X-Database": "production"
      },
      "description": "数据库查询服务"
    }
  },
  "version": "1.0.0",
  "description": "Complete MCPStore configuration example",
  "created_by": "MCPStore CLI",
  "metadata": {
    "environment": "production",
    "team": "development",
    "contact": "admin@example.com"
  }
}
```

## 配置最佳实践

### 1. 安全性

```json
{
  "mcpServers": {
    "secure-api": {
      "url": "https://secure-api.com/mcp",
      "headers": {
        // ❌ 不要在配置文件中硬编码敏感信息
        "Authorization": "Bearer hardcoded-token"
      }
    }
  }
}
```

**推荐做法**：使用环境变量

```bash
# 设置环境变量
export API_TOKEN="your-secret-token"
```

```json
{
  "mcpServers": {
    "secure-api": {
      "url": "https://secure-api.com/mcp",
      "headers": {
        // ✅ 在运行时从环境变量读取
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### 2. 版本控制

```bash
# 将配置文件加入版本控制
git add mcp.json

# 忽略包含敏感信息的配置
echo "mcp.prod.json" >> .gitignore
echo "mcp.local.json" >> .gitignore
```

### 3. 文档化

```json
{
  "mcpServers": {
    "weather-api": {
      "url": "https://weather.example.com/mcp",
      "description": "天气查询服务 - 提供全球天气信息",
      "contact": "weather-team@example.com",
      "version": "v2.1",
      "documentation": "https://docs.weather.example.com"
    }
  }
}
```

### 4. 配置验证脚本

```bash
#!/bin/bash
# validate-config.sh

echo "🔍 验证 MCPStore 配置..."

# 检查配置文件是否存在
if [ ! -f "mcp.json" ]; then
    echo "❌ 配置文件 mcp.json 不存在"
    exit 1
fi

# 验证 JSON 语法
if ! python -m json.tool mcp.json > /dev/null 2>&1; then
    echo "❌ 配置文件 JSON 语法错误"
    exit 1
fi

# 启动测试验证配置
mcpstore test basic --verbose

if [ $? -eq 0 ]; then
    echo "✅ 配置验证通过"
else
    echo "❌ 配置验证失败"
    exit 1
fi
```

## 故障排除

### 常见配置错误

#### 1. JSON 语法错误

**错误信息**:
```
❌ Configuration file error: Invalid JSON format
```

**解决方案**:
```bash
# 使用 JSON 验证工具
python -m json.tool mcp.json

# 或使用在线 JSON 验证器
```

#### 2. 缺少必需字段

**错误信息**:
```
❌ Service 'weather' missing required field: url
```

**解决方案**:
```json
{
  "mcpServers": {
    "weather": {
      "url": "https://weather.com/mcp"  // 添加缺少的字段
    }
  }
}
```

#### 3. 不支持的传输类型

**错误信息**:
```
❌ Unsupported transport type: 'custom-transport'
```

**解决方案**:
使用支持的传输类型：`streamable-http`、`sse`、`stdio`

### 配置文件权限

```bash
# 检查配置文件权限
ls -la mcp.json

# 设置正确权限（仅所有者可读写）
chmod 600 mcp.json

# 检查目录权限
ls -la ~/.mcpstore/
```

## 相关文档

- [CLI 概述](overview.md) - CLI 工具介绍
- [命令参考](commands.md) - 详细命令说明
- [服务注册](../services/registration/register-service.md) - 服务注册方法

## 下一步

- 了解 [高级开发概念](../advanced/concepts.md)
- 学习 [系统架构设计](../advanced/architecture.md)
- 查看 [最佳实践指南](../advanced/best-practices.md)
