# 命令参考

MCPStore CLI 提供的所有命令的详细参考文档。

## 命令概览

| 命令 | 功能 | 用途 |
|------|------|------|
| `run` | 运行服务 | 启动 API 服务器等 |
| `test` | 运行测试 | 执行各种测试套件 |
| `config` | 配置管理 | 管理配置文件 |
| `version` | 版本信息 | 显示版本号 |

## run - 运行服务

启动 MCPStore 相关服务。

### 语法

```bash
mcpstore run SERVICE [OPTIONS]
```

### 参数

#### 位置参数

- `SERVICE`: 要运行的服务名称
  - `api`: 启动 MCPStore API 服务器

#### 选项参数

| 选项 | 短选项 | 类型 | 默认值 | 描述 |
|------|--------|------|--------|------|
| `--host` | `-h` | str | `0.0.0.0` | 绑定的主机地址 |
| `--port` | `-p` | int | `18200` | 绑定的端口号 |
| `--reload` | `-r` | bool | `False` | 启用自动重载（开发模式） |
| `--log-level` | `-l` | str | `info` | 日志级别 |

#### 日志级别选项

- `critical`: 只显示严重错误
- `error`: 显示错误信息
- `warning`: 显示警告信息
- `info`: 显示一般信息（默认）
- `debug`: 显示调试信息

### 使用示例

#### 基本用法

```bash
# 使用默认配置启动 API 服务器
mcpstore run api
```

**输出**:
```
🚀 Starting MCPStore API Server...
   Host: 0.0.0.0:18200
   Press Ctrl+C to stop

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:18200 (Press CTRL+C to quit)
```

#### 自定义配置

```bash
# 自定义主机和端口
mcpstore run api --host 127.0.0.1 --port 8080

# 开发模式（自动重载）
mcpstore run api --reload --log-level debug

# 生产模式（最小日志）
mcpstore run api --host 0.0.0.0 --port 18200 --log-level warning
```

#### 开发环境配置

```bash
# 完整的开发环境配置
mcpstore run api \
  --host 127.0.0.1 \
  --port 8080 \
  --reload \
  --log-level debug
```

**输出**:
```
🚀 Starting MCPStore API Server...
   Host: 127.0.0.1:8080
   Mode: Development (auto-reload enabled)
   Press Ctrl+C to stop

INFO:     Will watch for changes in these directories: ['/path/to/mcpstore']
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
```

### 错误处理

#### 端口被占用

```bash
mcpstore run api --port 80
```

**错误输出**:
```
❌ Failed to start server: [Errno 48] Address already in use
```

**解决方案**:
```bash
# 使用其他端口
mcpstore run api --port 8080

# 或者停止占用端口的进程
sudo lsof -ti:80 | xargs kill -9
```

#### 权限不足

```bash
mcpstore run api --port 80
```

**错误输出**:
```
❌ Failed to start server: [Errno 13] Permission denied
```

**解决方案**:
```bash
# 使用非特权端口
mcpstore run api --port 8080

# 或者使用 sudo（不推荐）
sudo mcpstore run api --port 80
```

## test - 运行测试

执行 MCPStore 的各种测试套件。

### 语法

```bash
mcpstore test [SUITE] [OPTIONS]
```

### 参数

#### 位置参数

- `SUITE`: 测试套件名称（可选，默认: `all`）
  - `all`: 运行所有测试
  - `basic`: 基础功能测试
  - `api`: API 接口测试
  - `integration`: 集成测试
  - `performance`: 性能测试

#### 选项参数

| 选项 | 短选项 | 类型 | 默认值 | 描述 |
|------|--------|------|--------|------|
| `--host` | | str | `localhost` | API 服务器主机 |
| `--port` | | int | `18611` | API 服务器端口 |
| `--verbose` | `-v` | bool | `False` | 详细输出 |
| `--performance` | `-p` | bool | `False` | 包含性能测试 |
| `--max-concurrent` | | int | `10` | 性能测试最大并发数 |

### 使用示例

#### 基本测试

```bash
# 运行所有测试
mcpstore test

# 运行特定测试套件
mcpstore test basic
mcpstore test api
mcpstore test integration
```

#### 详细输出

```bash
# 启用详细输出
mcpstore test --verbose

# 运行特定测试并显示详细信息
mcpstore test api --verbose
```

**输出示例**:
```
🧪 Running MCPStore Tests...
   Suite: api
   Host: localhost:18611
   Verbose: enabled

✅ Test 1/5: API Server Health Check
   - Server responding: OK
   - Response time: 45ms

✅ Test 2/5: Service Registration
   - Add service: OK
   - Service listed: OK
   - Service info: OK

...

📊 Test Results:
   Total: 5
   Passed: 5
   Failed: 0
   Duration: 2.3s
```

#### 性能测试

```bash
# 运行性能测试
mcpstore test --performance

# 自定义并发数
mcpstore test performance --max-concurrent 20 --verbose
```

**输出示例**:
```
🚀 Running Performance Tests...
   Max Concurrent: 20
   Target: localhost:18611

📈 Performance Test Results:
   Total Requests: 1000
   Successful: 998
   Failed: 2
   Average Response Time: 125ms
   95th Percentile: 250ms
   Throughput: 45 req/s
```

#### 自定义测试目标

```bash
# 测试远程 API 服务器
mcpstore test api --host api.example.com --port 443

# 测试本地开发服务器
mcpstore test --host 127.0.0.1 --port 8080 --verbose
```

### 测试套件详解

#### basic - 基础功能测试

测试 MCPStore 的核心功能：

- 配置文件加载
- 服务注册和管理
- 工具列表和调用
- 基本错误处理

```bash
mcpstore test basic --verbose
```

#### api - API 接口测试

测试 REST API 的所有端点：

- Store 级别 API（25个端点）
- Agent 级别 API（14个端点）
- 监控 API（14个端点）
- 应用级别 API（2个端点）

```bash
mcpstore test api --verbose
```

#### integration - 集成测试

测试完整的工作流程：

- 端到端服务注册
- 工具调用链
- LangChain 集成
- 错误恢复机制

```bash
mcpstore test integration --verbose
```

#### performance - 性能测试

测试系统性能和并发能力：

- 并发请求处理
- 响应时间统计
- 吞吐量测试
- 资源使用监控

```bash
mcpstore test performance --max-concurrent 50 --verbose
```

### 测试命令错误处理

#### 测试运行器不可用

```bash
mcpstore test
```

**错误输出**:
```
❌ Test runner not available: No module named 'mcpstore.cli.test_runner'
```

**说明**: 当前版本的测试功能正在开发中，测试运行器模块尚未完全实现。

**临时解决方案**:
```bash
# 使用 API 健康检查替代基础测试
curl -X GET http://localhost:18200/health

# 启动 API 服务器进行手动测试
mcpstore run api

# 使用 Python 直接测试 MCPStore 功能
python -c "from mcpstore import MCPStore; store = MCPStore.setup_store(); print('✅ MCPStore 初始化成功')"
```

## config - 配置管理

管理 MCPStore 配置文件。

### 语法

```bash
mcpstore config ACTION [OPTIONS]
```

### 参数

#### 位置参数

- `ACTION`: 配置操作类型
  - `show`: 显示当前配置
  - `validate`: 验证配置文件
  - `init`: 初始化默认配置

#### 选项参数

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `--path` | str | None | 配置文件路径 |

### 使用示例

#### 显示配置

```bash
# 显示默认配置
mcpstore config show

# 显示指定配置文件
mcpstore config show --path /path/to/mcp.json
```

#### 验证配置

```bash
# 验证默认配置文件
mcpstore config validate

# 验证指定配置文件
mcpstore config validate --path config/prod-mcp.json
```

#### 初始化配置

```bash
# 在当前目录创建默认配置
mcpstore config init

# 在指定路径创建配置
mcpstore config init --path config/new-mcp.json
```

## version - 版本信息

显示 MCPStore 的版本信息。

### 语法

```bash
mcpstore version
```

### 参数

无参数。

### 使用示例

```bash
mcpstore version
```

**输出**:
```
MCPStore version: 0.5.0
```

### 在脚本中使用

```bash
#!/bin/bash

# 获取版本号
VERSION=$(mcpstore version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
echo "当前 MCPStore 版本: $VERSION"

# 版本比较
if [[ "$VERSION" < "0.5.0" ]]; then
    echo "⚠️ 版本过低，请升级到 0.5.0 或更高版本"
    exit 1
fi
```

## 全局选项

### --help

显示命令帮助信息。

```bash
# 主帮助
mcpstore --help

# 命令帮助
mcpstore run --help
mcpstore test --help
```

### 环境变量

CLI 工具支持以下环境变量：

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `MCPSTORE_HOST` | 默认主机地址 | `0.0.0.0` |
| `MCPSTORE_PORT` | 默认端口号 | `18200` |
| `MCPSTORE_LOG_LEVEL` | 默认日志级别 | `info` |
| `MCPSTORE_CONFIG` | 配置文件路径 | `mcp.json` |

#### 使用示例

```bash
# 设置环境变量
export MCPSTORE_HOST=127.0.0.1
export MCPSTORE_PORT=8080
export MCPSTORE_LOG_LEVEL=debug

# 使用环境变量启动
mcpstore run api
```

## 退出代码

| 代码 | 含义 | 描述 |
|------|------|------|
| 0 | 成功 | 命令执行成功 |
| 1 | 一般错误 | 命令执行失败 |
| 2 | 参数错误 | 命令参数不正确 |
| 130 | 用户中断 | 用户按 Ctrl+C 中断 |

### 在脚本中处理退出代码

```bash
#!/bin/bash

# 启动 API 服务器
mcpstore run api &
SERVER_PID=$!

# 等待启动
sleep 5

# 运行测试
mcpstore test api
TEST_EXIT_CODE=$?

# 停止服务器
kill $SERVER_PID

# 根据测试结果退出
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ 所有测试通过"
    exit 0
else
    echo "❌ 测试失败"
    exit 1
fi
```

## 注意事项

1. **权限要求**: 绑定到特权端口（<1024）需要管理员权限
2. **端口冲突**: 确保指定端口未被占用
3. **防火墙**: 确保防火墙允许指定端口的连接
4. **资源限制**: 性能测试可能消耗大量系统资源
5. **网络连接**: 某些测试需要网络连接

## 相关文档

- [CLI 概述](overview.md) - CLI 工具介绍
- [配置管理](configuration.md) - 配置文件管理
- [REST API](../api-reference/rest-api.md) - HTTP API 接口

## 下一步

- 了解 [配置管理功能](configuration.md)
- 学习 [API 接口使用](../api-reference/rest-api.md)
- 查看 [高级开发指南](../advanced/concepts.md)
