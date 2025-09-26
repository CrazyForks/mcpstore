# CLI 概述

MCPStore CLI 是基于 Typer 构建的命令行工具，提供便捷的 MCP 服务管理和测试功能。

## 什么是 MCPStore CLI？

MCPStore CLI 是一个功能强大的命令行界面，让您可以：

- 🚀 启动 MCPStore API 服务器
- 🧪 运行各种测试套件
- 📊 查看版本和系统信息
- ⚙️ 管理配置和服务

## 安装

CLI 工具随 MCPStore 包一起安装：

```bash
pip install mcpstore
```

安装完成后，您可以在终端中使用 `mcpstore` 命令。

## 基本用法

### 查看帮助信息

```bash
# 查看主帮助
mcpstore --help

# 查看特定命令帮助
mcpstore run --help
mcpstore test --help
```

### 快速开始

```bash
# 查看版本
mcpstore version

# 启动 API 服务器
mcpstore run api

# 运行测试
mcpstore test
```

## 主要命令

### 🚀 run - 运行服务

启动 MCPStore 相关服务。

```bash
# 启动 API 服务器（默认配置）
mcpstore run api

# 自定义主机和端口
mcpstore run api --host 127.0.0.1 --port 8080

# 开发模式（自动重载）
mcpstore run api --reload --log-level debug
```

**参数说明**:
- `--host, -h`: 绑定主机地址（默认: 0.0.0.0）
- `--port, -p`: 绑定端口（默认: 18200）
- `--reload, -r`: 启用自动重载（开发模式）
- `--log-level, -l`: 日志级别（默认: info）

### 🧪 test - 运行测试

执行各种测试套件，验证 MCPStore 功能。

```bash
# 运行所有测试
mcpstore test

# 运行特定测试套件
mcpstore test basic
mcpstore test api
mcpstore test integration

# 详细输出
mcpstore test --verbose

# 包含性能测试
mcpstore test --performance --max-concurrent 20
```

**可用测试套件**:
- `all`: 运行所有测试（默认）
- `basic`: 基础功能测试
- `api`: API 接口测试
- `integration`: 集成测试
- `performance`: 性能测试

**参数说明**:
- `--host`: API 服务器主机（默认: localhost）
- `--port`: API 服务器端口（默认: 18611）
- `--verbose, -v`: 详细输出
- `--performance, -p`: 包含性能测试
- `--max-concurrent`: 性能测试最大并发数（默认: 10）

### 📋 version - 版本信息

显示 MCPStore 版本信息。

```bash
mcpstore version
```

**输出示例**:
```
MCPStore version: 0.5.0
```

## 使用示例

### 启动开发服务器

```bash
# 启动开发模式的 API 服务器
mcpstore run api --host 127.0.0.1 --port 8080 --reload --log-level debug
```

**输出**:
```
🚀 Starting MCPStore API Server...
   Host: 127.0.0.1:8080
   Mode: Development (auto-reload enabled)
   Press Ctrl+C to stop

INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 运行完整测试

```bash
# 运行所有测试，包含性能测试
mcpstore test all --verbose --performance --max-concurrent 15
```

### 生产环境部署

```bash
# 生产环境启动 API 服务器
mcpstore run api --host 0.0.0.0 --port 18200 --log-level warning
```

## 配置文件

CLI 工具会自动查找和使用 MCPStore 配置文件：

### 默认配置文件位置

1. 当前目录的 `mcp.json`
2. MCPStore 数据目录的 `mcp.json`
3. 内置默认配置

### 配置文件格式

```json
{
  "mcpServers": {
    "weather-api": {
      "url": "https://weather.example.com/mcp"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    },
    "calculator": {
      "command": "python",
      "args": ["calculator_server.py"],
      "env": {
        "DEBUG": "true"
      }
    }
  }
}
```

## 错误处理

### 常见错误和解决方案

#### 端口被占用
```bash
❌ Failed to start server: [Errno 48] Address already in use
```
**解决方案**: 使用不同端口或停止占用端口的进程
```bash
mcpstore run api --port 8081
```

#### 权限错误
```bash
❌ Failed to start server: [Errno 13] Permission denied
```
**解决方案**: 使用非特权端口（>1024）或以管理员权限运行

#### 配置文件错误
```bash
❌ Configuration file error: Invalid JSON format
```
**解决方案**: 检查 `mcp.json` 文件格式是否正确

## 高级用法

### 自定义测试配置

```bash
# 测试特定 API 服务器
mcpstore test api --host api.example.com --port 443

# 高并发性能测试
mcpstore test performance --max-concurrent 50 --verbose
```

### 集成到 CI/CD

```bash
#!/bin/bash
# CI/CD 脚本示例

# 启动测试服务器
mcpstore run api --host 127.0.0.1 --port 18200 &
SERVER_PID=$!

# 等待服务器启动
sleep 5

# 运行测试
mcpstore test all --host 127.0.0.1 --port 18200

# 停止服务器
kill $SERVER_PID
```

## 注意事项

1. **端口冲突**: 确保指定的端口未被其他服务占用
2. **权限要求**: 绑定到特权端口（<1024）需要管理员权限
3. **防火墙设置**: 确保防火墙允许指定端口的连接
4. **资源限制**: 性能测试可能消耗大量系统资源

## 相关文档

- [命令参考](commands.md) - 详细的命令说明
- [配置管理](configuration.md) - 配置文件管理
- [REST API](../api-reference/rest-api.md) - HTTP API 接口

## 下一步

- 查看 [详细命令参考](commands.md)
- 了解 [配置管理功能](configuration.md)
- 学习 [API 接口使用](../api-reference/rest-api.md)
