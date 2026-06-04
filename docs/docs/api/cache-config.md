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

### 统计包装器

启用统计功能，自动记录缓存命中率、延迟等指标：

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            
            # 启用统计
            "enable_statistics": True
        }
    }
)

# 获取统计信息
stats = await store.registry.get_cache_statistics()
print(f"命中率: {stats['hit_rate']}")
print(f"平均延迟: {stats['avg_latency_ms']}ms")
```


### 大小限制包装器

限制缓存对象的最大大小，防止内存溢出：

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            
            # 启用大小限制
            "enable_size_limit": True,
            "max_item_size": 1024 * 1024  # 1MB
        }
    }
)
```

**配置项**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enable_size_limit` | `bool` | `True` | 是否启用大小限制 |
| `max_item_size` | `int` | `1048576` | 最大对象大小（字节），默认 1MB |

### 压缩包装器

自动压缩大对象，节省存储空间：

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            
            # 启用压缩
            "enable_compression": True,
            "compression_threshold": 512 * 1024  # 512KB
        }
    }
)
```

**配置项**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enable_compression` | `bool` | `False` | 是否启用压缩 |
| `compression_threshold` | `int` | `524288` | 压缩阈值（字节），默认 512KB |

### 组合包装器

可以同时启用多个包装器：

```python
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={
        "cache": {
            "type": "redis",
            "url": "redis://localhost:6379/0",
            
            # 同时启用多个包装器
            "enable_statistics": True,
            "enable_size_limit": True,
            "max_item_size": 1024 * 1024,
            "enable_compression": True,
            "compression_threshold": 512 * 1024
        }
    }
)
```

**包装器顺序**（从内到外）：
1. 基础存储（Memory/Redis）
2. 大小限制（LimitSizeWrapper）
3. 压缩（CompressionWrapper）
4. 统计（StatisticsWrapper）

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
            "healthcheck_interval": 30
        }
    }
)
```

**配置项**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_connections` | `int` | `50` | 最大连接数 |
| `healthcheck_interval` | `int` | `30` | 健康检查间隔（秒） |

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
from key_value.aio.stores import RedisStore

# 初始使用内存
store = MCPStore.setup_store(mcpjson_path="./mcp.json")

# 切换到 Redis
redis_store = RedisStore(
    url="redis://localhost:6379/0",
    password="your_password"
)
await store.registry.switch_backend(redis_store)
```

### 切换到内存

```python
from key_value.aio.stores import MemoryStore

# 初始使用 Redis
store = MCPStore.setup_store(
    mcpjson_path="./mcp.json",
    external_db={"cache": {"type": "redis", ...}}
)

# 切换到内存
memory_store = MemoryStore()
await store.registry.switch_backend(memory_store)
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

### 获取缓存统计

```python
# 获取统计信息
stats = await store.registry.get_cache_statistics()

print(f"总请求数: {stats['total_requests']}")
print(f"命中数: {stats['hits']}")
print(f"未命中数: {stats['misses']}")
print(f"命中率: {stats['hit_rate']:.2%}")
print(f"平均延迟: {stats['avg_latency_ms']:.2f}ms")
print(f"总数据大小: {stats['total_size_bytes']} bytes")
```

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `total_requests` | `int` | 总请求数 |
| `hits` | `int` | 命中数 |
| `misses` | `int` | 未命中数 |
| `hit_rate` | `float` | 命中率（0-1） |
| `avg_latency_ms` | `float` | 平均延迟（毫秒） |
| `p50_latency_ms` | `float` | P50 延迟（毫秒） |
| `p95_latency_ms` | `float` | P95 延迟（毫秒） |
| `p99_latency_ms` | `float` | P99 延迟（毫秒） |
| `total_size_bytes` | `int` | 总数据大小（字节） |

### 重置统计信息

```python
# 重置统计计数器
await store.registry.reset_cache_statistics()
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
            "healthcheck_interval": 30,
            
            # 包装器配置
            "enable_statistics": True,
            "enable_size_limit": True,
            "max_item_size": 1024 * 1024,  # 1MB
            "enable_compression": True,
            "compression_threshold": 512 * 1024  # 512KB
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
            
            # 开发环境启用统计
            "enable_statistics": True,
            "enable_size_limit": False
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
    await store.registry.switch_backend(new_backend)
except CacheOperationError as e:
    print(f"后端切换失败: {e}")
    # 系统会自动回滚到旧后端
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
