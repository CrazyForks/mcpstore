# patch_service()

增量更新服务配置（推荐）。

## 方法特性

- ✅ **异步版本**: `patch_service_async()`
- ✅ **Store级别**: `store.for_store().patch_service()`
- ✅ **Agent级别**: `store.for_agent("agent1").patch_service()`
- 📁 **文件位置**: `service_management.py`
- 🏷️ **所属类**: `ServiceManagementMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `name` | `str` | ✅ | - | 服务名称 |
| `updates` | `Dict[str, Any]` | ✅ | - | 要更新的配置项 |

## 返回值

- **成功**: 返回 `True`
- **失败**: 返回 `False`

## 使用示例

### Store级别增量更新

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 只更新超时时间，保留其他配置
updates = {
    "timeout": 60
}

success = store.for_store().patch_service("weather", updates)
if success:
    print("Weather服务超时时间已更新")
else:
    print("Weather服务配置更新失败")
```

### Agent级别增量更新

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式增量更新
updates = {
    "env": {
        "LOG_LEVEL": "debug",  # 只更新日志级别
        "API_KEY": "new-key"   # 更新API密钥
    }
}

success = store.for_agent("agent1").patch_service("weather-local", updates)
if success:
    print("Agent Weather服务环境变量已更新")
```

### 更新请求头

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 只更新请求头
updates = {
    "headers": {
        "Authorization": "Bearer new-token",
        "User-Agent": "MCPStore/2.0"
    }
}

success = store.for_store().patch_service("weather", updates)
print(f"请求头更新: {'成功' if success else '失败'}")
```

### 更新命令参数

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 只更新命令参数
updates = {
    "args": ["weather-server.py", "--port", "9090", "--debug"]
}

success = store.for_store().patch_service("weather", updates)
print(f"命令参数更新: {'成功' if success else '失败'}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_patch_service():
    # 初始化
    store = MCPStore.setup_store()
    
    # 增量更新配置
    updates = {
        "timeout": 45,
        "reconnect": True
    }
    
    # 异步增量更新
    success = await store.for_store().patch_service_async("weather", updates)
    
    if success:
        print("异步增量更新成功")
        # 验证更新结果
        service_info = await store.for_store().get_service_info_async("weather")
        print(f"更新后超时时间: {service_info.get('timeout')}")
    
    return success

# 运行异步更新
result = asyncio.run(async_patch_service())
```

### 批量增量更新

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 批量增量更新多个服务
services_updates = {
    "weather": {
        "timeout": 30
    },
    "database": {
        "env": {
            "POOL_SIZE": "20"
        }
    },
    "filesystem": {
        "args": ["fs-server.py", "--cache-size", "1GB"]
    }
}

for service_name, updates in services_updates.items():
    success = store.for_store().patch_service(service_name, updates)
    print(f"增量更新 {service_name}: {'成功' if success else '失败'}")
```

### 嵌套配置更新

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 更新嵌套配置
updates = {
    "headers": {
        "Authorization": "Bearer updated-token"
    },
    "env": {
        "DEBUG": "true",
        "CACHE_TTL": "3600"
    },
    "timeout": 120
}

success = store.for_store().patch_service("weather", updates)
if success:
    print("嵌套配置更新成功")
```

## 常见更新场景

### 1. 更新认证信息
```python
updates = {
    "headers": {
        "Authorization": "Bearer new-access-token"
    }
}
```

### 2. 调整性能参数
```python
updates = {
    "timeout": 60,
    "reconnect": True,
    "max_retries": 3
}
```

### 3. 更新环境变量
```python
updates = {
    "env": {
        "LOG_LEVEL": "info",
        "CACHE_SIZE": "512MB"
    }
}
```

### 4. 修改命令参数
```python
updates = {
    "args": ["server.py", "--workers", "4", "--port", "8080"]
}
```

## 与 update_service() 的区别

| 特性 | patch_service() | update_service() |
|------|-----------------|------------------|
| 更新方式 | 增量更新 | 完全替换 |
| 原有配置 | 保留未修改的 | 全部清除 |
| 安全性 | 更安全 | 需要完整配置 |
| 使用场景 | 小幅调整（推荐） | 重大配置变更 |

## 相关方法

- [update_service()](update-service.md) - 完全替换服务配置
- [get_service_info()](../listing/get-service-info.md) - 获取当前服务配置
- [restart_service()](restart-service.md) - 重启服务使配置生效

## 注意事项

1. **增量更新**: 只修改指定的配置项，保留其他配置
2. **深度合并**: 对于嵌套对象（如headers、env），会进行深度合并
3. **服务重启**: 更新配置后服务会自动重启
4. **配置验证**: 更新的配置会进行格式验证
5. **推荐使用**: 对于大多数配置修改场景，推荐使用此方法
