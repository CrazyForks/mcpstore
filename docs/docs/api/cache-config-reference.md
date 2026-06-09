# Cache Configuration API Reference

Complete API reference for MCPStore's type-safe cache configuration system.

## Overview

MCPStore provides a type-safe, class-based configuration API for cache backends. The system supports:

- **Memory Cache**: Fast in-memory storage for development and testing
- **Redis Cache**: Persistent, distributed storage for production
- **Type Safety**: Full IDE autocomplete and type checking
- **Validation**: Immediate error detection at configuration time

---

## Configuration Classes

### CacheType

Enum defining available cache backend types.

```python
from enum import Enum

class CacheType(Enum):
    MEMORY = "memory"
    REDIS = "redis"
```

**Values**:
- `MEMORY`: In-memory cache backend
- `REDIS`: Redis cache backend

---

### BaseCacheConfig

Base configuration class for all cache types.

```python
from dataclasses import dataclass

@dataclass
class BaseCacheConfig:
    timeout: float = 2.0
    retry_attempts: int = 3
    health_check: bool = True
```

**Attributes**:

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` | `2.0` | Operation timeout in seconds |
| `retry_attempts` | `int` | `3` | Number of retry attempts on failure |
| `health_check` | `bool` | `True` | Enable health check monitoring |

**Example**:
```python
# Not typically used directly - use MemoryConfig or RedisConfig instead
config = BaseCacheConfig(timeout=5.0, retry_attempts=5)
```

---

### MemoryConfig

Configuration for in-memory cache backend.

```python
from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class MemoryConfig(BaseCacheConfig):
    max_size: Optional[int] = None
    cleanup_interval: int = 300
    cache_type: Literal[CacheType.MEMORY] = CacheType.MEMORY
```

**Attributes**:

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_size` | `Optional[int]` | `None` | Maximum number of items (None = unlimited) |
| `cleanup_interval` | `int` | `300` | Cleanup interval in seconds |
| `cache_type` | `CacheType` | `MEMORY` | Cache type (automatically set) |
| `timeout` | `float` | `2.0` | Inherited from BaseCacheConfig |
| `retry_attempts` | `int` | `3` | Inherited from BaseCacheConfig |
| `health_check` | `bool` | `True` | Inherited from BaseCacheConfig |

**Example**:
```python
from mcpstore.config import MemoryConfig

# Default configuration
config = MemoryConfig()

# Custom configuration
config = MemoryConfig(
    max_size=1000,
    cleanup_interval=600,
    timeout=5.0
)

# Use with MCPStore
store = MCPStore.setup_store("mcp.json", cache=config)
```

**Use Cases**:
- Development and testing
- Single-instance deployments
- Scenarios where data persistence is not required
- Fast prototyping

---

### RedisConfig

Configuration for Redis cache backend.

```python
from dataclasses import dataclass
from typing import Optional, Literal
@dataclass
class RedisConfig(BaseCacheConfig):
    # Connection options
    url: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    db: Optional[int] = None
    password: Optional[str] = None
    namespace: Optional[str] = None
    
    # Connection pool options
    max_connections: int = 50
    retry_on_timeout: bool = True
    socket_keepalive: bool = True
    socket_connect_timeout: float = 5.0
    socket_timeout: float = 5.0
    health_check_interval: int = 30
    
    cache_type: Literal[CacheType.REDIS] = CacheType.REDIS
```

**Attributes**:

#### Connection Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `Optional[str]` | `None` | Redis connection URL (e.g., `redis://localhost:6379/0`) |
| `host` | `Optional[str]` | `None` | Redis server hostname |
| `port` | `Optional[int]` | `None` | Redis server port |
| `db` | `Optional[int]` | `None` | Redis database number |
| `password` | `Optional[str]` | `None` | Redis authentication password |
| `namespace` | `Optional[str]` | `None` | Namespace for key isolation (default: "mcpstore") |

#### Connection Pool Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_connections` | `int` | `50` | Maximum number of connections in pool |
| `retry_on_timeout` | `bool` | `True` | Retry operations on timeout |
| `socket_keepalive` | `bool` | `True` | Enable TCP keepalive |
| `socket_connect_timeout` | `float` | `5.0` | Connection timeout in seconds |
| `socket_timeout` | `float` | `5.0` | Socket operation timeout in seconds |
| `health_check_interval` | `int` | `30` | Health check interval in seconds (0 = disabled) |

#### Inherited Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` | `2.0` | Inherited from BaseCacheConfig |
| `retry_attempts` | `int` | `3` | Inherited from BaseCacheConfig |
| `health_check` | `bool` | `True` | Inherited from BaseCacheConfig |
| `cache_type` | `CacheType` | `REDIS` | Cache type (automatically set) |

**Initialization Methods**:

RedisConfig supports two initialization methods:

1. **Using URL**:
```python
config = RedisConfig(url="redis://localhost:6379/0")
```

2. **Using Host/Port**:
```python
config = RedisConfig(
    host="localhost",
    port=6379,
    db=0,
    password="secret"
)
```

**Validation**:

RedisConfig performs validation in `__post_init__`:

- At least one of `url` or `host` must be provided
- `timeout` must be positive
- `socket_timeout` must be positive
- `max_connections` must be positive

**Examples**:

```python
from mcpstore.config import RedisConfig

# Basic configuration with URL
config = RedisConfig(url="redis://localhost:6379/0")

# With authentication
config = RedisConfig(
    url="redis://localhost:6379/0",
    password="secret"
)

# With custom namespace
config = RedisConfig(
    url="redis://localhost:6379/0",
    namespace="production"
)

# Full production configuration
config = RedisConfig(
    url="redis://prod-redis:6379/0",
    password="secret",
    namespace="production",
    max_connections=100,
    socket_timeout=10.0,
    health_check_interval=60
)

# Use with MCPStore
store = MCPStore.setup_store("mcp.json", cache=config)
```

**Use Cases**:
- Production deployments
- Multi-instance applications
- Scenarios requiring data persistence
- Distributed systems
- High-availability setups

---

## Namespace Management

### get_namespace()

Get the namespace for Redis key isolation.

```python
def get_namespace(config: RedisConfig) -> str:
    """
    Get namespace from config or return default.
    
    Args:
        config: RedisConfig instance
    
    Returns:
        Namespace string (user-provided or default "mcpstore")
    """
```

**Behavior**:
- If `config.namespace` is set → return user value
- If `config.namespace` is None → return "mcpstore"

**Examples**:

```python
from mcpstore.config import RedisConfig
from mcpstore.config.namespace import get_namespace

# Default namespace
config = RedisConfig(url="redis://localhost:6379/0")
ns = get_namespace(config)  # Returns: "mcpstore"

# Custom namespace
config = RedisConfig(url="redis://localhost:6379/0", namespace="production")
ns = get_namespace(config)  # Returns: "production"
```

---

## MCPStore Integration

### setup_store()

Create MCPStore instance with cache configuration.

```python
def setup_store(
    mcpjson_path: str | None = None,
    debug: bool | str = False,
    cache: MemoryConfig | RedisConfig | None = None,
    static_config: dict | None = None,
    cache_mode: str = "auto",
    only_db: bool = False,
) -> "MCPStore":
    """
    Create a Rust-backed MCPStore instance.
    
    Args:
        mcpjson_path: Path to MCP JSON configuration file (optional)
        debug: Enable debug logging
        cache: Cache configuration object
        static_config: Service config added after setup through Rust facade
        cache_mode: auto/local/shared
        only_db: Use Rust db source mode
    
    Returns:
        MCPStore instance
    
    Raises:
        ValueError: If configuration is invalid
        RuntimeError: If Redis connection fails
    """
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mcpjson_path` | `Optional[Union[str, Path]]` | `None` | JSON configuration file path |
| `debug` | `bool | str` | `False` | Enable debug logging |
| `cache` | `Optional[Union[MemoryConfig, RedisConfig]]` | `None` | Cache configuration |
| `static_config` | `dict | None` | `None` | Service config added through Rust facade after setup |
| `cache_mode` | `str` | `"auto"` | One of `auto`, `local`, `shared` |
| `only_db` | `bool` | `False` | Use Rust db source mode |

**Examples**:

```python
from mcpstore import MCPStore
from mcpstore.config import MemoryConfig, RedisConfig

# Default configuration (memory cache)
store = MCPStore.setup_store()

# With JSON file
store = MCPStore.setup_store("mcp.json")

# With Redis cache
redis_config = RedisConfig(url="redis://localhost:6379/0")
store = MCPStore.setup_store("mcp.json", cache=redis_config)

# Redis only (no JSON)
redis_config = RedisConfig(url="redis://localhost:6379/0")
store = MCPStore.setup_store(cache=redis_config)

# With debug mode
store = MCPStore.setup_store("mcp.json", debug=True)
```

---

## Export Functionality

### exportjson()

Export the current Rust-backed MCP configuration to JSON format.

```python
async def exportjson(
    self,
    filepath: Optional[str] = None,
    *,
    include_sessions: bool = False
) -> Dict[str, Any]:
    """
    Export Rust-backed store configuration to standard MCP JSON format.
    
    Args:
        filepath: Output file path (optional)
        include_sessions: Must be False; Rust core does not expose serializable session state.
    
    Returns:
        Dictionary with exported data in mcpServers format
    
    Raises:
        NotImplementedError: If include_sessions=True
        IOError: If file write fails
        PermissionError: If insufficient permissions
    """
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filepath` | `Optional[str]` | `None` | Output file path (if None, only returns data) |
| `include_sessions` | `bool` | `False` | Must remain `False`; sessions are Python routing state, not Rust-serializable data |

**Returns**:

Dictionary with structure:
```python
{
    "mcpServers": {
        "service_name": {
            "command": "...",
            "args": [...],
            "env": {...}
        },
        ...
    }
}
```

**Examples**:

```python
# Export to file
data = await store.exportjson("backup.json")

# Get data without saving
data = await store.exportjson()

# Use exported data
print(f"Exported {len(data['mcpServers'])} services")
```

---

## Health Check

### Health Check Background Task

Automatic health check for Redis connections.

**Configuration**:

```python
config = RedisConfig(
    url="redis://localhost:6379/0",
    health_check_interval=30  # Check every 30 seconds
)
```

**Behavior**:
- If `health_check_interval > 0`: Start background task
- If `health_check_interval = 0`: Disable health check
- Task runs periodic PING commands
- Failures logged as warnings (non-blocking)

**Examples**:

```python
# Enable health check (default)
config = RedisConfig(
    url="redis://localhost:6379/0",
    health_check_interval=30
)

# Disable health check
config = RedisConfig(
    url="redis://localhost:6379/0",
    health_check_interval=0
)

# Custom interval
config = RedisConfig(
    url="redis://localhost:6379/0",
    health_check_interval=60  # Check every minute
)
```

---

## Error Handling

### Configuration Errors

**ValueError**: Raised for invalid configuration

```python
# Missing connection info
try:
    config = RedisConfig()  # No url or host
except ValueError as e:
    print(e)  # "Redis configuration requires either 'url' or 'host'..."

# Invalid timeout
try:
    config = RedisConfig(url="...", timeout=-1)
except ValueError as e:
    print(e)  # "timeout must be positive, got: -1"

# Invalid max_connections
try:
    config = RedisConfig(url="...", max_connections=0)
except ValueError as e:
    print(e)  # "max_connections must be positive, got: 0"
```

### Connection Errors

**RuntimeError**: Raised for connection failures

```python
try:
    config = RedisConfig(url="redis://invalid:6379/0")
    store = MCPStore.setup_store(cache=config)
except RuntimeError as e:
    print(e)  # Detailed error with troubleshooting steps
```

---

## Type Annotations

All configuration classes include full type annotations for IDE support:

```python
from typing import Optional, Union, Literal

# Type hints for cache parameter
cache: Optional[Union[MemoryConfig, RedisConfig]] = None

# Type hints for namespace
namespace: Optional[str] = None

# Type hints for numeric parameters
max_connections: int = 50
timeout: float = 2.0
```

---

## Best Practices

### 1. Use Type Hints

```python
from mcpstore.config import RedisConfig

def create_store(config: RedisConfig) -> MCPStore:
    """Type hints enable IDE autocomplete and type checking."""
    return MCPStore.setup_store(cache=config)
```

### 2. Validate Early

```python
# Configuration is validated at creation time
try:
    config = RedisConfig(url="", max_connections=-1)
except ValueError as e:
    # Handle error before setup_store is called
    print(f"Invalid configuration: {e}")
```

### 3. Reuse Configurations

```python
# Create configuration once, reuse multiple times
redis_config = RedisConfig(url="redis://localhost:6379/0")

store1 = MCPStore.setup_store("mcp1.json", cache=redis_config)
store2 = MCPStore.setup_store("mcp2.json", cache=redis_config)
```

### 4. Use Environment Variables

```python
import os
from mcpstore.config import RedisConfig

config = RedisConfig(
    url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    password=os.getenv("REDIS_PASSWORD"),
    namespace=os.getenv("REDIS_NAMESPACE", "mcpstore")
)
```

### 5. Document Your Configuration

```python
def get_production_config() -> RedisConfig:
    """
    Get production Redis configuration.
    
    Returns:
        RedisConfig with production settings
    """
    return RedisConfig(
        url=os.getenv("REDIS_URL"),
        password=os.getenv("REDIS_PASSWORD"),
        namespace="production",
        max_connections=100,
        socket_timeout=10.0,
        health_check_interval=60
    )
```

---

## Related Documentation

- [缓存配置示例](../examples/cache-config-examples.md) - 常见配置模式
- [快速开始](../quickstart.md) - 初始化 Store 的最短路径
- [服务概览](../services/overview.md) - 将配置应用到实际服务

---

**Document Version**: v1.0  
**Created**: 2025-01-20  
**Last Updated**: 2025-01-20
