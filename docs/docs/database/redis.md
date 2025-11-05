## Redis 支持

MCPStore 提供了完整的 Redis 数据库支持，用于实现服务配置、缓存数据和状态信息的持久化存储。

## Redis 的作用

在 MCPStore 中，Redis 主要用于：

- 服务配置持久化 - 保存已注册的服务配置
- 缓存数据存储 - 缓存服务工具列表、工具模式等数据
- 状态信息同步 - 跨进程/实例共享服务状态
- 多 Store 协作 - 支持多个 Store 实例共享数据

---

## 快速开始

### 最简单的 Redis 配置

```python
from mcpstore import MCPStore

# Redis 配置
redis_config = {
    "url": "redis://localhost:6379/0",
    "password": None,
    "namespace": "default",
    "dataspace": "auto",
    "socket_timeout": 2.0,
    "healthcheck_interval": 30
}

# 初始化 Store 并启用 Redis
store = MCPStore.setup_store(debug=True, redis=redis_config)
```

---

## 配置参数详解

### 完整配置选项

```python
redis_config = {
    # 连接配置
    "url": "redis://localhost:6379/0",        # Redis 连接 URL
    "password": None,                         # Redis 密码（可选）
    
    # 命名空间配置
    "namespace": "default",                   # 命名空间，用于隔离不同应用
    "dataspace": "auto",                      # 数据空间，"auto" 或自定义字符串
    
    # 性能配置
    "socket_timeout": 2.0,                    # Socket 超时（秒）
    "healthcheck_interval": 30                # 健康检查间隔（秒）
}
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | `str` | 必填 | Redis 连接 URL，格式：`redis://host:port/db` |
| `password` | `str \| None` | `None` | Redis 密码，无密码时设为 `None` |
| `namespace` | `str` | `"default"` | 命名空间，用于隔离不同应用的数据 |
| `dataspace` | `str` | `"auto"` | 数据空间，`"auto"` 表示自动生成，也可指定固定值 |
| `socket_timeout` | `float` | `2.0` | Socket 连接超时时间（秒） |
| `healthcheck_interval` | `int` | `30` | 健康检查间隔（秒） |

---

## 使用示例

### 示例 1：本地服务 + Redis

```python
from mcpstore import MCPStore

# 服务配置（本地 MCP 服务）
demo_mcp = {
    "mcpServers": {
        "howtocook": {
            "command": "npx",
            "args": ["-y", "howtocook-mcp"]
        }
    }
}

# Redis 配置
redis_config = {
    "url": "redis://localhost:6379/0",
    "password": None,
    "namespace": "bendi",           # 本地服务使用 "bendi" 命名空间
    "dataspace": "auto",
    "socket_timeout": 2.0,
    "healthcheck_interval": 30
}

# 初始化 Store
store = MCPStore.setup_store(debug=True, redis=redis_config)

# 添加服务
store.for_store().add_service(demo_mcp)

# 等待服务就绪
ws = store.for_store().wait_service("howtocook")
print(f"服务状态: {ws}")

# 列出服务
services = store.for_store().list_services()
print(f"已注册服务: {[s.name for s in services]}")

# 列出工具
tools = store.for_store().list_tools()
print(f"可用工具: {[t.name for t in tools]}")

# 调用工具
result = store.for_store().use_tool('mcp_howtocook_getAllRecipes', {})
print(f"调用结果: {result}")
```

### 示例 2：远程服务 + Redis

```python
from mcpstore import MCPStore

# 服务配置（远程 MCP 服务）
demo_mcp = {
    "mcpServers": {
        "weather": {
            "url": "https://mcpstore.wiki/mcp"
        }
    }
}

# Redis 配置
redis_config = {
    "url": "redis://localhost:6379/0",
    "password": None,
    "namespace": "default",         # 远程服务使用 "default" 命名空间
    "dataspace": "auto",
    "socket_timeout": 2.0,
    "healthcheck_interval": 30
}

# 初始化 Store
store = MCPStore.setup_store(debug=True, redis=redis_config)

# 添加服务
store.for_store().add_service(demo_mcp)

# 等待服务就绪
ws = store.for_store().wait_service("weather")
print(f"服务状态: {ws}")

# 列出服务
services = store.for_store().list_services()
print(f"已注册服务: {[s.name for s in services]}")

# 列出工具
tools = store.for_store().list_tools()
print(f"可用工具: {[t.name for t in tools]}")

# 调用工具
result = store.for_store().use_tool('get_current_weather', {"query": "北京"})
print(f"调用结果: {result}")
```

---

## 高级配置

### 1. 多 Store 共享数据

通过相同的 `namespace` 和 `dataspace`，多个 Store 实例可以共享数据：

```python
# Store 1
redis_config_1 = {
    "url": "redis://localhost:6379/0",
    "namespace": "shared",          # 相同的 namespace
    "dataspace": "workspace1"       # 相同的 dataspace
}
store1 = MCPStore.setup_store(redis=redis_config_1)

# Store 2（在另一个进程中）
redis_config_2 = {
    "url": "redis://localhost:6379/0",
    "namespace": "shared",          # 相同的 namespace
    "dataspace": "workspace1"       # 相同的 dataspace
}
store2 = MCPStore.setup_store(redis=redis_config_2)

# store1 和 store2 会共享服务配置和缓存
```

### 2. 不同应用隔离

通过不同的 `namespace`，实现不同应用的数据隔离：

```python
# 应用 A
redis_config_a = {
    "url": "redis://localhost:6379/0",
    "namespace": "app_a",           # 独立的 namespace
    "dataspace": "auto"
}
store_a = MCPStore.setup_store(redis=redis_config_a)

# 应用 B
redis_config_b = {
    "url": "redis://localhost:6379/0",
    "namespace": "app_b",           # 独立的 namespace
    "dataspace": "auto"
}
store_b = MCPStore.setup_store(redis=redis_config_b)

# store_a 和 store_b 的数据完全隔离
```

### 3. 自动 vs 显式 Dataspace

```python
# 自动 dataspace（推荐）
# 每次运行会生成唯一的 dataspace，适合临时会话
redis_config_auto = {
    "url": "redis://localhost:6379/0",
    "namespace": "default",
    "dataspace": "auto"             # 自动生成
}

# 显式 dataspace
# 固定的 dataspace，适合持久化和跨进程共享
redis_config_explicit = {
    "url": "redis://localhost:6379/0",
    "namespace": "default",
    "dataspace": "my_workspace"     # 固定值
}
```

---

## Redis 数据结构

MCPStore 在 Redis 中使用以下键结构：

```
{namespace}:{dataspace}:services:{service_name}:config       # 服务配置
{namespace}:{dataspace}:services:{service_name}:cache        # 服务缓存
{namespace}:{dataspace}:services:{service_name}:state        # 服务状态
{namespace}:{dataspace}:tools:{tool_name}:info               # 工具信息
{namespace}:{dataspace}:tools:{tool_name}:stats              # 工具统计
```

### 示例键名

假设 `namespace="default"`, `dataspace="workspace1"`:

```
default:workspace1:services:weather:config
default:workspace1:services:weather:cache
default:workspace1:services:weather:state
default:workspace1:tools:get_current_weather:info
default:workspace1:tools:get_current_weather:stats
```

---

## 性能优化

### 1. 调整超时时间

根据网络环境调整超时时间：

```python
# 快速网络环境
redis_config = {
    "url": "redis://localhost:6379/0",
    "socket_timeout": 1.0,          # 短超时
    "healthcheck_interval": 15      # 频繁健康检查
}

# 慢速网络环境
redis_config = {
    "url": "redis://localhost:6379/0",
    "socket_timeout": 5.0,          # 长超时
    "healthcheck_interval": 60      # 不频繁健康检查
}
```

### 2. 使用连接池（自动）

MCPStore 会自动使用 Redis 连接池，无需手动配置。

### 3. 批量操作

```python
# 批量添加服务
store.for_store().add_service({
    "mcpServers": {
        "service1": {...},
        "service2": {...},
        "service3": {...}
    }
})

# Redis 会自动批量存储配置
```

---

## 安全配置

### 1. 使用密码

```python
redis_config = {
    "url": "redis://localhost:6379/0",
    "password": "your_secure_password",  # 设置密码
    "namespace": "default",
    "dataspace": "auto"
}
```

### 2. 使用 Redis URL 格式的密码

```python
redis_config = {
    "url": "redis://:your_password@localhost:6379/0",  # 在 URL 中指定密码
    "namespace": "default",
    "dataspace": "auto"
}
```

### 3. SSL/TLS 连接

```python
redis_config = {
    "url": "rediss://localhost:6380/0",  # 使用 rediss:// 启用 SSL
    "password": "your_password",
    "namespace": "default",
    "dataspace": "auto"
}
```

---

## 常见问题

### Q1: Redis 是必须的吗？

**A**: 不是必须的。如果不配置 Redis，MCPStore 会使用内存存储：

```python
# 不使用 Redis（仅内存存储）
store = MCPStore.setup_store()
```

### Q2: 如何清除 Redis 中的数据？

**A**: 可以通过 Redis 客户端手动清除：

```bash
# 清除特定 namespace 的数据
redis-cli --scan --pattern "default:*" | xargs redis-cli del

# 清除所有数据（危险操作！）
redis-cli FLUSHDB
```

### Q3: 多个 Store 共享数据会冲突吗？

**A**: 不会。只要使用相同的 `namespace` 和 `dataspace`，数据会正确共享。MCPStore 会自动处理并发访问。

### Q4: dataspace 设为 "auto" 时，数据会保留吗？

**A**: 不会。`"auto"` 会在每次初始化时生成新的 dataspace，适合临时会话。如果需要持久化，请使用固定的 dataspace 值。

### Q5: Redis 连接失败怎么办？

**A**: MCPStore 会自动回退到内存存储，并在日志中输出警告：

```python
# 即使 Redis 连接失败，Store 仍可正常工作
store = MCPStore.setup_store(redis=redis_config)
# 如果 Redis 不可用，会自动使用内存存储
```

### Q6: 如何监控 Redis 使用情况？

**A**: 使用 Redis 命令监控：

```bash
# 查看所有键
redis-cli KEYS "*"

# 查看内存使用
redis-cli INFO memory

# 查看特定 namespace 的键数量
redis-cli --scan --pattern "default:*" | wc -l
```

---

## 相关配置

### Redis 配置示例对比

| 场景 | namespace | dataspace | 说明 |
|------|-----------|-----------|------|
| **开发环境** | `"dev"` | `"auto"` | 每次运行独立隔离 |
| **测试环境** | `"test"` | `"fixed_workspace"` | 持久化测试数据 |
| **生产环境** | `"prod"` | `"workspace1"` | 多实例共享数据 |
| **多租户** | `"tenant_{id}"` | `"auto"` | 按租户隔离数据 |

---

## 最佳实践

### 1. 开发环境使用 auto dataspace

```python
redis_config = {
    "url": "redis://localhost:6379/0",
    "namespace": "dev",
    "dataspace": "auto"             # 开发时使用 auto
}
```

### 2. 生产环境使用固定 dataspace

```python
redis_config = {
    "url": "redis://prod-redis:6379/0",
    "namespace": "prod",
    "dataspace": "workspace1"       # 生产环境固定
}
```

### 3. 多租户场景使用动态 namespace

```python
def create_store_for_tenant(tenant_id: str):
    redis_config = {
        "url": "redis://localhost:6379/0",
        "namespace": f"tenant_{tenant_id}",  # 动态 namespace
        "dataspace": "auto"
    }
    return MCPStore.setup_store(redis=redis_config)
```

### 4. 启用调试模式

```python
# 启用 debug 模式查看 Redis 操作日志
store = MCPStore.setup_store(debug=True, redis=redis_config)
```

---

## 相关文档

- [快速上手指南](../getting-started/quickstart.md) - 了解基础使用
- [服务管理概览](../services/overview.md) - 了解服务管理
- [MCPStore 类](../api-reference/mcpstore-class.md) - 查看完整 API
- [架构概览](../architecture/overview.md) - 了解系统架构

---

## 授构图

```
┌─────────────────────────────────────────────────────────────┐
│                        MCPStore                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐              ┌──────────────┐            │
│  │   Memory     │              │    Redis     │            │
│  │   Storage    │◄────────────►│   Storage    │            │
│  │  (Default)   │   Fallback   │  (Optional)  │            │
│  └──────────────┘              └──────────────┘            │
│         │                              │                    │
│         ├──────────────────────────────┤                    │
│         │     Unified Interface        │                    │
│         ▼                              ▼                    │
│  ┌──────────────────────────────────────────┐              │
│  │          Service Manager                 │              │
│  │  • Config Persistence                    │              │
│  │  • Cache Management                      │              │
│  │  • State Synchronization                 │              │
│  └──────────────────────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---



