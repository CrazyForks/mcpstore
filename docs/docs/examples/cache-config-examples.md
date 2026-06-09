# Cache Configuration Examples

Practical examples for configuring MCPStore cache in different environments and scenarios.

## Table of Contents

- [Development Environment](#development-environment)
- [Testing Environment](#testing-environment)
- [Production with JSON + Redis](#production-with-json--redis)
- [Production Redis-Only](#production-redis-only)
- [Enterprise Custom Client](#enterprise-custom-client)
- [Advanced Scenarios](#advanced-scenarios)

---

## Development Environment

### Basic Development Setup

The simplest configuration for local development - uses in-memory cache with JSON configuration file.

```python
from mcpstore import MCPStore

# Default configuration - perfect for development
store = MCPStore.setup_store("mcp.json")

# That's it! No additional configuration needed
```

**Features**:
- ✅ Fast in-memory cache
- ✅ Loads from JSON file
- ✅ No external dependencies
- ✅ Perfect for rapid prototyping

---

### Development with Custom Memory Settings

For larger development projects, you might want to customize memory cache behavior.

```python
from mcpstore import MCPStore
from mcpstore.config import MemoryConfig

# Custom memory configuration
memory_config = MemoryConfig(
    max_size=500,           # Limit to 500 items
    cleanup_interval=600,   # Cleanup every 10 minutes
    timeout=5.0             # 5 second timeout
)

store = MCPStore.setup_store("mcp.json", cache=memory_config)
```

**Use Cases**:
- Large development projects
- Memory-constrained environments
- Testing memory limits

---

### Development with Local Redis

Test Redis integration locally before deploying to production.

```python
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

# Local Redis for development
redis_config = RedisConfig(
    url="redis://localhost:6379/0",
    namespace="dev",
    health_check_interval=0  # Disable health check for dev
)

store = MCPStore.setup_store("mcp.json", cache=redis_config)
```

**Setup**:
```bash
# Start local Redis with Docker
docker run -d -p 6379:6379 redis:latest
```

---

## Testing Environment

### Unit Testing Configuration

Minimal configuration for fast unit tests.

```python
import pytest
from mcpstore import MCPStore
from mcpstore.config import MemoryConfig

@pytest.fixture
def store():
    """Create MCPStore instance for testing."""
    config = MemoryConfig()
    store = MCPStore.setup_store(cache=config)
    yield store
    # Cleanup happens automatically

def test_service_registration(store):
    """Test service registration."""
    # Your test code here
    pass
```

**Benefits**:
- ⚡ Fast execution
- 🔄 Automatic cleanup
- 🎯 Isolated tests

---

### Integration Testing with Redis

Test Redis integration with isolated namespaces.

```python
import pytest
from mcpstore import MCPStore
from mcpstore.config import RedisConfig
import uuid

@pytest.fixture
async def redis_store():
    """Create MCPStore with isolated Redis namespace."""
    # Use unique namespace for each test
    namespace = f"test_{uuid.uuid4().hex[:8]}"
    
    config = RedisConfig(
        url="redis://localhost:6379/0",
        namespace=namespace,
        health_check_interval=0  # Disable for tests
    )
    
    store = MCPStore.setup_store(cache=config)
    yield store
    
    # Cleanup: clear test data
    await store.registry.clear_all()

@pytest.mark.asyncio
async def test_redis_persistence(redis_store):
    """Test data persistence in Redis."""
    # Your test code here
    pass
```

**Features**:
- 🔒 Isolated test namespaces
- 🧹 Automatic cleanup
- 📊 Real Redis testing

---

### Testing with Isolated Redis Namespace

Use a dedicated Redis database or namespace for tests.

```python
import pytest
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

@pytest.fixture
async def redis_test_store():
    """Create MCPStore with an isolated Rust Redis backend."""
    config = RedisConfig(
        url="redis://localhost:6379/15",
        namespace="test"
    )
    
    store = MCPStore.setup_store(cache=config)
    yield store

@pytest.mark.asyncio
async def test_with_redis(redis_test_store):
    """Test with Redis through the Rust backend."""
    # Your test code here
    pass
```

---

## Production with JSON + Redis {#production-with-json--redis}

### Basic Production Setup

Standard production configuration with JSON file and Redis cache.

```python
import os
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

# Production Redis configuration
redis_config = RedisConfig(
    url=os.getenv("REDIS_URL", "redis://prod-redis:6379/0"),
    password=os.getenv("REDIS_PASSWORD"),
    namespace="production",
    max_connections=50,
    socket_timeout=5.0,
    health_check_interval=30
)

store = MCPStore.setup_store("mcp.json", cache=redis_config)
```

**Environment Variables**:
```bash
export REDIS_URL="redis://prod-redis:6379/0"
export REDIS_PASSWORD="your-secure-password"
```

---

### High-Availability Production

Production setup with optimized connection pool and health checks.

```python
import os
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

redis_config = RedisConfig(
    # Connection
    url=os.getenv("REDIS_URL"),
    password=os.getenv("REDIS_PASSWORD"),
    namespace="production",
    
    # Connection pool optimization
    max_connections=100,
    socket_timeout=10.0,
    socket_connect_timeout=5.0,
    retry_on_timeout=True,
    socket_keepalive=True,
    
    # Health monitoring
    health_check_interval=60,
    
    # Retry configuration
    retry_attempts=5,
    timeout=10.0
)

store = MCPStore.setup_store("mcp.json", cache=redis_config)
```

**Features**:
- 🔄 Connection pooling
- 💪 Retry on failure
- 🏥 Health monitoring
- ⚡ Optimized timeouts

---

### Multi-Environment Configuration

Support multiple environments with configuration factory.

```python
import os
from mcpstore import MCPStore
from mcpstore.config import MemoryConfig, RedisConfig

def get_cache_config():
    """Get cache configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return RedisConfig(
            url=os.getenv("REDIS_URL"),
            password=os.getenv("REDIS_PASSWORD"),
            namespace="production",
            max_connections=100,
            health_check_interval=60
        )
    elif env == "staging":
        return RedisConfig(
            url=os.getenv("REDIS_URL"),
            password=os.getenv("REDIS_PASSWORD"),
            namespace="staging",
            max_connections=50,
            health_check_interval=30
        )
    else:  # development
        return MemoryConfig()

# Use in application
cache_config = get_cache_config()
store = MCPStore.setup_store("mcp.json", cache=cache_config)
```

**Environment Variables**:
```bash
# Production
export ENVIRONMENT="production"
export REDIS_URL="redis://prod-redis:6379/0"
export REDIS_PASSWORD="prod-password"

# Staging
export ENVIRONMENT="staging"
export REDIS_URL="redis://staging-redis:6379/0"
export REDIS_PASSWORD="staging-password"

# Development (no Redis needed)
export ENVIRONMENT="development"
```

---

## Production Redis-Only

### Dynamic Configuration (No JSON File)

Pure Redis-based configuration without JSON file - perfect for cloud-native applications.

```python
import os
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

# Redis-only configuration (no JSON file)
redis_config = RedisConfig(
    url=os.getenv("REDIS_URL"),
    password=os.getenv("REDIS_PASSWORD"),
    namespace="dynamic",
    max_connections=50
)

# No mcpjson_path parameter - pure Redis
store = MCPStore.setup_store(cache=redis_config)

# Add services dynamically via API
await store.add_service({
    "my-service": {
        "command": "python",
        "args": ["-m", "my_mcp_server"],
        "env": {"API_KEY": "secret"}
    }
})
```

**Use Cases**:
- 🚀 Cloud-native applications
- 🔄 Dynamic service registration
- 📦 Container-based deployments
- 🎯 API-driven configuration

---

### Kubernetes Deployment

Configuration for Kubernetes with ConfigMap and Secrets.

```python
import os
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

# Read from Kubernetes environment
redis_config = RedisConfig(
    url=os.getenv("REDIS_URL"),  # From ConfigMap
    password=os.getenv("REDIS_PASSWORD"),  # From Secret
    namespace=os.getenv("POD_NAMESPACE", "default"),
    max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
    health_check_interval=int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
)

store = MCPStore.setup_store(cache=redis_config)
```

**Kubernetes ConfigMap**:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mcpstore-config
data:
  REDIS_URL: "redis://redis-service:6379/0"
  REDIS_MAX_CONNECTIONS: "100"
  HEALTH_CHECK_INTERVAL: "60"
```

**Kubernetes Secret**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mcpstore-secrets
type: Opaque
stringData:
  REDIS_PASSWORD: "your-secure-password"
```

---

### Docker Compose Setup

Complete Docker Compose configuration with Redis.

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 3s
      retries: 3

  mcpstore:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379/0
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - ENVIRONMENT=production
    depends_on:
      redis:
        condition: service_healthy

volumes:
  redis-data:
```

**Application Code**:
```python
import os
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

redis_config = RedisConfig(
    url=os.getenv("REDIS_URL"),
    password=os.getenv("REDIS_PASSWORD"),
    namespace="docker",
    max_connections=50
)

store = MCPStore.setup_store(cache=redis_config)
```

**.env file**:
```bash
REDIS_PASSWORD=your-secure-password
```

---

## Enterprise Redis URL

### Shared Connection Settings

Pass connection settings to Rust instead of passing a Python Redis client.

```python
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

# Use host/port/password directly
redis_config = RedisConfig(
    host="redis-cluster",
    port=6379,
    password="secret",
    namespace="enterprise",
    max_connections=200
)

store = MCPStore.setup_store(cache=redis_config)
```

**Benefits**:
- 🔄 Rust owns the connection pool
- 📊 Centralized monitoring
- 🎯 Unified configuration
- 💰 Resource efficiency

---

### Redis Cluster Configuration

Connect to Redis Cluster for high availability.

```python
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

redis_config = RedisConfig(
    host="redis-cluster",
    port=6379,
    password="secret",
    namespace="cluster",
    max_connections=100
)

store = MCPStore.setup_store(cache=redis_config)
```

**Features**:
- 🏢 High availability
- 📈 Horizontal scaling
- 🔄 Automatic failover
- 💪 Production-ready

---

### Redis Sentinel Configuration

Use Redis Sentinel for automatic failover.

```python
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

# Point MCPStore at the current master endpoint exposed by your Sentinel setup.
redis_config = RedisConfig(
    url="redis://:secret@redis-master.service.local:6379/0",
    namespace="sentinel",
    socket_timeout=5.0
)

store = MCPStore.setup_store(cache=redis_config)
```

**Features**:
- 🛡️ Automatic failover
- 👁️ Master monitoring
- 🔄 Slave promotion
- 🏥 Health checking

---

## Advanced Scenarios

### Multi-Tenant Configuration

Isolate data for different tenants using namespaces.

```python
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

def create_tenant_store(tenant_id: str) -> MCPStore:
    """Create isolated store for each tenant."""
    redis_config = RedisConfig(
        url="redis://localhost:6379/0",
        namespace=f"tenant_{tenant_id}",
        max_connections=50
    )
    return MCPStore.setup_store(cache=redis_config)

# Create stores for different tenants
store_tenant_a = create_tenant_store("tenant_a")
store_tenant_b = create_tenant_store("tenant_b")

# Data is completely isolated between tenants
```

**Benefits**:
- 🔒 Data isolation
- 🏢 Multi-tenancy support
- 🎯 Per-tenant configuration
- 📊 Separate monitoring

---

### Explicit Application-Level Degradation

If Redis is unavailable, the application can explicitly create a new Rust-backed store with a memory cache. MCPStore itself does not silently fall back to a Python core or hidden cache backend.

```python
import logging
from mcpstore import MCPStore
from mcpstore.config import MemoryConfig, RedisConfig

logger = logging.getLogger(__name__)

def create_store_with_memory_degradation(json_path: str) -> MCPStore:
    """Create a Rust-backed store with Redis, then explicitly retry with memory."""
    try:
        # Try Redis first
        redis_config = RedisConfig(
            url="redis://localhost:6379/0",
            namespace="production",
            timeout=2.0  # Short timeout for fast failure
        )
        store = MCPStore.setup_store(json_path, cache=redis_config)
        logger.info("Using Redis cache")
        return store
    except Exception as e:
        # Explicit application-level degradation to Rust memory backend
        logger.warning(f"Redis unavailable, using memory cache: {e}")
        memory_config = MemoryConfig()
        store = MCPStore.setup_store(json_path, cache=memory_config)
        return store

# Use in application
store = create_store_with_memory_degradation("mcp.json")
```

**Features**:
- 🛡️ Fault tolerance
- 🔄 Explicit application-level degradation
- 📊 Degraded mode operation
- 🏥 Service continuity

---

### Hot Configuration Reload

Reload configuration without restarting application.

```python
import asyncio
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

class ConfigurableStore:
    def __init__(self):
        self.store = None
        self.config = None
    
    async def initialize(self, config: RedisConfig):
        """Initialize with configuration."""
        self.config = config
        self.store = MCPStore.setup_store(cache=config)
    
    async def reload_config(self, new_config: RedisConfig):
        """Reload with new configuration."""
        # Export current data
        data = await self.store.exportjson()
        
        # Create new store with new config
        new_store = MCPStore.setup_store(cache=new_config)
        
        # Import data to new store
        for service_name, service_config in data["mcpServers"].items():
            await new_store.add_service({service_name: service_config})
        
        # Switch to new store
        old_store = self.store
        self.store = new_store
        self.config = new_config
        
        # Cleanup old store
        await old_store.cleanup()

# Usage
configurable_store = ConfigurableStore()

# Initial configuration
initial_config = RedisConfig(url="redis://localhost:6379/0")
await configurable_store.initialize(initial_config)

# Reload with new configuration
new_config = RedisConfig(url="redis://new-host:6379/0")
await configurable_store.reload_config(new_config)
```

---

### Export and Backup

Regular backup of cache data to JSON files.

```python
import asyncio
from datetime import datetime
from pathlib import Path
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

async def backup_cache(store: MCPStore, backup_dir: str):
    """Backup cache data to JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(backup_dir) / f"backup_{timestamp}.json"
    
    # Export to file
    await store.exportjson(str(backup_path))
    print(f"Backup saved to {backup_path}")

async def scheduled_backup(store: MCPStore, backup_dir: str, interval: int):
    """Run backup on schedule."""
    while True:
        await backup_cache(store, backup_dir)
        await asyncio.sleep(interval)

# Setup
redis_config = RedisConfig(url="redis://localhost:6379/0")
store = MCPStore.setup_store(cache=redis_config)

# Start scheduled backup (every hour)
asyncio.create_task(scheduled_backup(store, "./backups", 3600))
```

---

### Monitoring and Metrics

Monitor cache performance and health.

```python
import asyncio
import logging
from mcpstore import MCPStore
from mcpstore.config import RedisConfig

logger = logging.getLogger(__name__)

async def monitor_cache_health(store: MCPStore, interval: int = 60):
    """Monitor cache health and log metrics."""
    while True:
        try:
            # Check if cache is accessible
            await store.registry.ping()
            logger.info("Cache health check: OK")
            
            # Log cache statistics (if available)
            # stats = await store.registry.get_statistics()
            # logger.info(f"Cache stats: {stats}")
            
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
        
        await asyncio.sleep(interval)

# Setup with health monitoring
redis_config = RedisConfig(
    url="redis://localhost:6379/0",
    health_check_interval=30  # Built-in health check
)
store = MCPStore.setup_store(cache=redis_config)

# Additional custom monitoring
asyncio.create_task(monitor_cache_health(store, interval=60))
```

---

## Complete Application Example

Full example combining multiple patterns.

```python
import os
import asyncio
import logging
from pathlib import Path
from mcpstore import MCPStore
from mcpstore.config import MemoryConfig, RedisConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cache_config():
    """Get cache configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return RedisConfig(
            url=os.getenv("REDIS_URL"),
            password=os.getenv("REDIS_PASSWORD"),
            namespace="production",
            max_connections=100,
            socket_timeout=10.0,
            health_check_interval=60
        )
    elif env == "staging":
        return RedisConfig(
            url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            namespace="staging",
            max_connections=50
        )
    else:
        return MemoryConfig()

async def main():
    """Main application entry point."""
    # Get configuration
    cache_config = get_cache_config()
    logger.info(f"Using cache type: {cache_config.cache_type.value}")
    
    # Initialize store
    json_path = os.getenv("MCP_JSON_PATH", "mcp.json")
    store = MCPStore.setup_store(json_path, cache=cache_config)
    logger.info("MCPStore initialized")
    
    try:
        # Your application logic here
        services = await store.list_services()
        logger.info(f"Loaded {len(services)} services")
        
        # Keep application running
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        # Cleanup
        await store.cleanup()
        logger.info("Cleanup complete")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Related Documentation

- [配置说明](../api/cache-config.md) - 配置字段详解
- [API 参考](../api/cache-config-reference.md) - 完整接口说明
- [架构说明](../architecture/cache-architecture.md) - 缓存在整体架构中的位置

---

**Document Version**: v1.0  
**Created**: 2025-01-20  
**Last Updated**: 2025-01-20
