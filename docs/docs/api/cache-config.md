# 缓存配置 API

本文档描述 MCPStore 基于 py-key-value 的缓存配置 API。

## 概述

MCPStore 使用 [py-key-value](https://github.com/parnell/py-key-value) 作为统一的缓存抽象层，支持：

- **多种存储后端**：Memory、Redis
- **企业级包装器**：统计、大小限制、压缩
- **灵活工作模式**：本地、混合、共享
- **运行时热插拔**：动态切换缓存后端

---

## 初始化配置

### 基础配置

```python
from mcpstore import MCPStore

# 本地模式（Memory 后端）
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json"
)
```

### Redis 后端配置

```python
# 混合模式（JSON + Redis）
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            "password": "your_password",  # 可选
            "namespace": "mcpstore_prod"
        }
    }
)
```

### 共享模式配置

```python
# 共享模式（Redis Only）
store = MCPStore.setup_store(
    mcpjson_path=None,
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            "namespace": "team_workspace",
            "mode": "shared",
            "load_from_cache": True
        }
    }
)
```

---

## 包装器配置

### 缓存快照统计

Rust-backed Python SDK 当前通过 Rust cache inspect 暴露缓存快照计数。它不会伪造请求命中率、请求数或延迟指标；这些字段在返回值中会标记为不可用。

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
        }
    }
)

# 获取 Rust cache inspect 统计
stats = await store.registry.get_cache_statistics()
print(f"后端: {stats['backend']}")
print(f"实体数: {stats['entity_count']}")
print(f"关系数: {stats['relation_count']}")
print(f"请求指标可用: {stats['request_metrics_available']}")
```


### 当前支持的配置字段

Python SDK 会把 `external_db.cache` 解析成 Rust cache backend 配置，再通过 PyO3 初始化 Rust core。当前不会启用旧 Python wrapper；未列出的字段不会产生额外行为。

**配置项**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `type` | `str` | `"memory"` | `memory` / `redis` / `openkeyv_memory` / `openkeyv_redis` |
| `url` | `str` | `None` | Redis URL；Redis 后端推荐显式提供 |
| `host` | `str` | `None` | 未提供 URL 时用于拼接 Redis 地址 |
| `port` | `int` | `None` | 未提供 URL 时用于拼接 Redis 地址 |
| `db` | `int` | `None` | Redis database |
| `password` | `str` | `None` | Redis 密码 |
| `namespace` | `str` | `None` | Rust cache namespace |
| `max_connections` | `int` | `50` | Redis 连接池上限 |
| `retry_on_timeout` | `bool` | `True` | Redis 超时时是否重试 |
| `socket_keepalive` | `bool` | `True` | Redis keepalive |
| `socket_connect_timeout` | `float` | `5.0` | Redis 连接超时 |
| `socket_timeout` | `float` | `5.0` | Redis socket 超时 |
| `health_check_interval` | `int` | `30` | Redis health check interval |
| `allow_partial` | `bool` | `False` | Redis 部分不可用时是否允许继续 |
| `timeout` | `float` | `2.0` | cache 操作超时 |
| `retry_attempts` | `int` | `3` | cache 操作重试次数 |
| `health_check` | `bool` | `True` | 是否执行健康检查 |
| `max_size` | `int` | `None` | Memory/OpenKeyv memory 后端可使用的最大尺寸配置 |

### 组合配置

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            "namespace": "mcpstore_prod",
            "max_connections": 50,
            "socket_timeout": 2.0,
            "socket_connect_timeout": 2.0,
            "health_check_interval": 30,
            "retry_attempts": 3,
        }
    }
)
```

---

## Redis 连接配置

### 基础连接参数

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            
            # 基础连接
            "url": "redis://localhost:6379/0",
            "password": "your_password",
            
            # 超时配置
            "socket_timeout": 2.0,
            "socket_connect_timeout": 2.0
        }
    }
)
```

**配置项**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | `str` | 必填 | Redis 连接 URL |
| `password` | `str` | `None` | Redis 密码 |
| `socket_timeout` | `float` | `2.0` | 套接字超时（秒） |
| `socket_connect_timeout` | `float` | `2.0` | 连接超时（秒） |

### 连接池配置

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            
            # 连接池配置
            "max_connections": 50,
            "health_check_interval": 30
        }
    }
)
```

**配置项**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_connections` | `int` | `50` | 最大连接数 |
| `health_check_interval` | `int` | `30` | 健康检查间隔（秒） |

### 命名空间配置

使用命名空间隔离不同应用的数据：

```python
# 应用 A
store_a = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            "namespace": "app_a"  # 独立命名空间
        }
    }
)

# 应用 B
store_b = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            "namespace": "app_b"  # 独立命名空间
        }
    }
)
```

---

## 工作模式配置

### 自动模式检测

```python
# 自动检测工作模式
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",  # 可选
    external_db={...},           # 可选
    cache_mode="auto"            # 默认
)
```

**检测逻辑**：
- 无 JSON + Redis → 共享模式
- 有 JSON + Redis → 混合模式
- 有 JSON + 无 Redis → 本地模式

### 显式指定模式

```python
# 显式指定本地模式
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    cache_mode="local"
)

# 显式指定混合模式
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={"cache": {"type": "redis", ...}},
    cache_mode="hybrid"
)

# 显式指定共享模式
store = MCPStore.setup_store(
    mcpjson_path=None,
    external_db={"cache": {"type": "redis", "mode": "shared", ...}},
    cache_mode="shared"
)
```

---

## 配置导出和导入

### 导出配置到 JSON

```python
# 从缓存导出配置
await store.export_to_json("./exported_config.json")
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `output_path` | `str` | 必填 | 输出文件路径 |
| `include_sessions` | `bool` | `False` | 是否包含 Session（不可序列化） |

### 从 JSON 导入配置

```python
# 从 JSON 导入配置到缓存
await store.import_from_json("./config.json")
```

---

## 缓存热插拔

### 切换到 Redis

```python
from mcpstore.config import RedisConfig

# 初始使用内存
store = MCPStore.setup_store(mcpjson_path="./mcp.json")

# 切换到 Rust Redis backend
redis_config = RedisConfig(
    url="redis://localhost:6379/0",
    password="your_password",
    namespace="prod"
)
await store.registry.switch_backend(redis_config)
```

### 切换到内存

```python
from mcpstore.config import MemoryConfig

# 初始使用 Redis
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={"cache": {"type": "redis", ...}}
)

# 切换到 Rust memory backend
memory_config = MemoryConfig()
await store.registry.switch_backend(memory_config)
```

### 热插拔限制

**✅ 可热插拔的数据**：
- 工具缓存
- 服务状态
- 服务元数据
- 客户端映射
- 工具映射

**❌ 不可热插拔的数据**：
- Session 数据（始终在内存，不可序列化）

---

## 统计信息 API

### 获取缓存快照统计

```python
# 获取 Rust cache inspect 统计
stats = await store.registry.get_cache_statistics()

print(f"后端: {stats['backend']}")
print(f"命名空间: {stats['namespace']}")
print(f"实体数: {stats['entity_count']}")
print(f"关系数: {stats['relation_count']}")
print(f"状态数: {stats['state_count']}")
print(f"事件数: {stats['event_count']}")

if not stats["request_metrics_available"]:
    print("请求命中率/延迟指标当前未由 Rust cache inspect 提供")
```

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `backend` | `str` | 当前 Rust cache 后端 |
| `namespace` | `str` | 当前缓存命名空间 |
| `request_metrics_available` | `bool` | 请求级命中率/延迟指标是否可用；当前为 `False` |
| `total_requests` | `None` | 当前未由 Rust cache inspect 提供 |
| `hits` | `None` | 当前未由 Rust cache inspect 提供 |
| `misses` | `None` | 当前未由 Rust cache inspect 提供 |
| `hit_rate` | `None` | 当前未由 Rust cache inspect 提供 |
| `avg_latency_ms` | `None` | 当前未由 Rust cache inspect 提供 |
| `p50_latency_ms` | `None` | 当前未由 Rust cache inspect 提供 |
| `p95_latency_ms` | `None` | 当前未由 Rust cache inspect 提供 |
| `p99_latency_ms` | `None` | 当前未由 Rust cache inspect 提供 |
| `total_size_bytes` | `None` | 当前未由 Rust cache inspect 提供 |
| `entity_count` | `int` | entity collection 条目数 |
| `relation_count` | `int` | relation collection 条目数 |
| `state_count` | `int` | state collection 条目数 |
| `event_count` | `int` | event collection 条目数 |

### 重置统计信息

Rust-backed Python SDK 当前没有独立的请求统计计数器，因此 `reset_cache_statistics()` 会抛出 `NotImplementedError`，不会假装重置成功。

```python
try:
    await store.registry.reset_cache_statistics()
except NotImplementedError:
    print("Rust cache inspect 当前没有可重置的请求统计计数器")
```

---

## 完整配置示例

### 生产环境配置

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            # 存储后端
            "type": "redis",
            "url": "redis://prod-redis:6379/0",
            "password": os.getenv("REDIS_PASSWORD"),
            "namespace": "mcpstore_prod",
            
            # 连接配置
            "socket_timeout": 2.0,
            "socket_connect_timeout": 2.0,
            "max_connections": 50,
            "health_check_interval": 30,
            "retry_attempts": 3,
            "health_check": True
        }
    },
    cache_mode="hybrid"
)
```

### 开发环境配置

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "memory",
            "timeout": 2.0,
            "retry_attempts": 1,
            "health_check": True
        }
    },
    cache_mode="local"
)
```

---

## 错误处理

### Redis 连接失败

```python
try:
    store = MCPStore.setup_store(
        external_db={
            "cache": {
                "type": "redis",
                "url": "redis://invalid:6379/0"
            }
        }
    )
except RuntimeError as e:
    print(f"Redis 连接失败: {e}")
    # 使用内存后端作为备选
    store = MCPStore.setup_store(mcpjson_path="./mcp.json")
```

### 热插拔失败

```python
try:
    await store.registry.switch_backend(redis_config)
except Exception as e:
    print(f"后端切换失败: {e}")
    # switch_backend 会重新初始化 Rust core；失败时请重新 setup_store 或显式切换回可用配置。
```

---

## 相关文档

- [缓存架构](../architecture/cache-architecture.md) - 缓存架构设计
- [缓存配置示例](../examples/cache-config-examples.md) - 常见配置参考
- [快速开始](../quickstart.md) - 从配置到运行的完整流程

---

**文档版本**: v1.0  
**创建日期**: 2025-01-19  
**最后更新**: 2025-01-19
