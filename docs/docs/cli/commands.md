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

#### 选项参数

| 选项 | 短选项 | 类型 | 默认值 | 描述 |
|------|--------|------|--------|------|
| `--host` | | str | `localhost` | API 服务器主机 |
| `--port` | | int | `18611` | API 服务器端口 |
| `--verbose` | `-v` | bool | `False` | 详细输出 |
| `--performance` | `-p` | bool | `False` | 包含性能测试 |
| `--max-concurrent` | | int | `10` | 性能测试最大并发数 |
