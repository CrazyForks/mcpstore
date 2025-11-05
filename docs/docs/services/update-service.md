## update_service - 服务更新


完全替换服务配置。

### SDK

同步：
  - `store.for_store().update_service(name, config) -> bool`
  - `store.for_agent(id).update_service(name, config) -> bool`

异步：
  - `await store.for_store().update_service_async(name, config) -> bool`
  - `await store.for_agent(id).update_service_async(name, config) -> bool`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `name` | str  | 服务名称 |
| `config` | dict | 新的服务配置（完全替换） |

### 返回值

- `True`：更新成功
- `False`：更新失败

### 视角
通过 `for_store()` 或 `for_agent(id)` 在对应命名空间内更新指定服务。

### 使用示例

### Store级别更新服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 完全替换服务配置
new_config = {
    "url": "https://api.newweather.com/mcp",
    "transport": "http",
    "timeout": 30,
    "headers": {
        "Authorization": "Bearer new-token"
    }
}

success = store.for_store().update_service("weather", new_config)
if success:
    print("Weather服务配置已更新")
else:
    print("Weather服务配置更新失败")
```

### Agent级别更新服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式更新服务
new_config = {
    "command": "python",
    "args": ["weather_server.py", "--port", "8080"],
    "env": {
        "API_KEY": "new-api-key"
    }
}

success = store.for_agent("agent1").update_service("weather-local", new_config)
if success:
    print("Agent Weather服务配置已更新")
```

### 更新URL服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 更新URL类型服务
url_config = {
    "url": "https://api.upgraded-weather.com/mcp",
    "transport": "http",
    "headers": {
        "User-Agent": "MCPStore/1.0",
        "API-Version": "v2"
    },
    "timeout": 60
}

success = store.for_store().update_service("weather", url_config)
print(f"URL服务更新: {'成功' if success else '失败'}")
```

### 更新命令服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 更新命令类型服务
command_config = {
    "command": "node",
    "args": ["weather-server.js", "--config", "production.json"],
    "cwd": "/opt/weather-service",
    "env": {
        "NODE_ENV": "production",
        "LOG_LEVEL": "info"
    }
}

success = store.for_store().update_service("weather", command_config)
print(f"命令服务更新: {'成功' if success else '失败'}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_update_service():
    # 初始化
    store = MCPStore.setup_store()
    
    # 新配置
    new_config = {
        "url": "https://api.async-weather.com/mcp",
        "transport": "websocket",
        "reconnect": True
    }
    
    # 异步更新服务
    success = await store.for_store().update_service_async("weather", new_config)
    
    if success:
        print("异步更新成功")
        # 验证更新结果
        service_info = await store.for_store().get_service_info_async("weather")
        print(f"更新后的服务信息: {service_info}")
    
    return success

# 运行异步更新
result = asyncio.run(async_update_service())
```

### 批量更新服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 批量更新多个服务
services_to_update = {
    "weather": {
        "url": "https://api.weather-v2.com/mcp",
        "timeout": 30
    },
    "database": {
        "command": "python",
        "args": ["db_server.py", "--version", "2.0"]
    }
}

for service_name, config in services_to_update.items():
    success = store.for_store().update_service(service_name, config)
    print(f"更新 {service_name}: {'成功' if success else '失败'}")
```

## 配置格式

### URL服务配置
```python
{
    "url": "https://api.example.com/mcp",
    "transport": "http|websocket",
    "headers": {"key": "value"},
    "timeout": 30,
    "reconnect": True
}
```

### 命令服务配置
```python
{
    "command": "executable",
    "args": ["arg1", "arg2"],
    "cwd": "/working/directory",
    "env": {"VAR": "value"}
}
```

## 与 patch_service() 的区别

| 特性 | update_service() | patch_service() |
|------|------------------|-----------------|
| 更新方式 | 完全替换 | 增量更新 |
| 原有配置 | 会被清除 | 会被保留 |
| 使用场景 | 重大配置变更 | 小幅调整 |
| 安全性 | 需要完整配置 | 更安全 |

### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 增量更新服务     | `store.for_store().patch_service(name, patch)` |
| 重启服务         | `store.for_store().restart_service(name)` |
| 获取服务信息     | `store.for_store().get_service_info(name)` |
| 获取服务状态     | `store.for_store().get_service_status(name)` |
| 删除服务         | `store.for_store().delete_service(name)` |
| 注册服务         | `store.for_store().add_service(config=..., ...)` |
| 查找服务         | `store.for_store().find_service(name)` |
| Agent 更新       | `store.for_agent(id).update_service(name, config)` |

## 注意事项

- 完全替换：会清除所有原有配置，只保留新配置
- 服务重启：更新配置后服务可能自动重启
- 配置验证：新配置会进行格式验证
- Agent 映射：Agent 模式下自动处理服务名映射
- 推荐：小幅修改建议使用 `patch_service()`
