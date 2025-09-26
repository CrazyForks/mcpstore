# reset_config()

重置配置。

## 方法特性

- ✅ **异步版本**: `reset_config_async()`
- ✅ **Store级别**: `store.for_store().reset_config()`
- ✅ **Agent级别**: `store.for_agent("agent1").reset_config()`
- 📁 **文件位置**: `service_management.py`
- 🏷️ **所属类**: `ServiceManagementMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `scope` | `str` | ❌ | `"all"` | 重置范围 |

## 重置范围选项

| 范围值 | 描述 | 影响内容 |
|--------|------|----------|
| `"all"` | 重置所有配置 | 服务配置、Agent配置、客户端配置 |
| `"services"` | 只重置服务配置 | mcp.json中的服务配置 |
| `"agents"` | 只重置Agent配置 | Agent客户端映射 |
| `"clients"` | 只重置客户端配置 | 客户端服务映射 |

## 返回值

- **成功**: 返回 `True`
- **失败**: 返回 `False`

## 使用示例

### Store级别重置所有配置

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 重置所有配置
success = store.for_store().reset_config("all")
if success:
    print("所有配置已重置")
else:
    print("配置重置失败")
```

### Agent级别重置配置

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式重置配置
success = store.for_agent("agent1").reset_config()
if success:
    print("Agent1配置已重置")
```

### 重置特定范围的配置

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 只重置服务配置
success = store.for_store().reset_config("services")
if success:
    print("服务配置已重置")

# 只重置Agent配置
success = store.for_store().reset_config("agents")
if success:
    print("Agent配置已重置")

# 只重置客户端配置
success = store.for_store().reset_config("clients")
if success:
    print("客户端配置已重置")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_reset_config():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步重置配置
    success = await store.for_store().reset_config_async("all")
    
    if success:
        print("异步配置重置成功")
        # 验证重置结果
        services = await store.for_store().list_services_async()
        print(f"重置后服务数量: {len(services)}")
    else:
        print("异步配置重置失败")
    
    return success

# 运行异步重置
result = asyncio.run(async_reset_config())
```

### 安全重置（备份后重置）

```python
from mcpstore import MCPStore
import json
from datetime import datetime

# 初始化
store = MCPStore.setup_store()

def safe_reset_config(scope="all"):
    """安全重置配置（先备份）"""
    
    # 1. 备份当前配置
    try:
        current_config = store.for_store().show_config(scope)
        
        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"config_backup_{scope}_{timestamp}.json"
        
        # 保存备份
        with open(backup_file, 'w') as f:
            json.dump(current_config, f, indent=2)
        
        print(f"配置已备份到: {backup_file}")
        
    except Exception as e:
        print(f"备份失败: {e}")
        return False
    
    # 2. 执行重置
    success = store.for_store().reset_config(scope)
    if success:
        print(f"配置范围 '{scope}' 重置成功")
    else:
        print(f"配置范围 '{scope}' 重置失败")
    
    return success

# 使用安全重置
safe_reset_config("services")
```

### 批量重置不同范围

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 按顺序重置不同范围
reset_scopes = ["clients", "agents", "services"]

for scope in reset_scopes:
    success = store.for_store().reset_config(scope)
    print(f"重置 {scope}: {'成功' if success else '失败'}")
    
    if success:
        # 验证重置结果
        config = store.for_store().show_config(scope)
        print(f"  重置后 {scope} 配置项数量: {len(config)}")
```

### 条件重置

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def conditional_reset():
    """根据条件决定是否重置"""
    
    # 检查服务状态
    services = store.for_store().list_services()
    health_status = store.for_store().check_services()
    
    # 统计不健康的服务
    unhealthy_count = sum(
        1 for status in health_status.values() 
        if status.get('status') != 'healthy'
    )
    
    # 如果超过一半服务不健康，重置服务配置
    if unhealthy_count > len(services) / 2:
        print(f"发现 {unhealthy_count} 个不健康服务，执行服务配置重置")
        success = store.for_store().reset_config("services")
        return success
    else:
        print("服务状态正常，无需重置")
        return True

# 执行条件重置
conditional_reset()
```

### 重置后重新初始化

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def reset_and_reinitialize():
    """重置配置并重新初始化基础服务"""
    
    # 1. 重置所有配置
    success = store.for_store().reset_config("all")
    if not success:
        print("配置重置失败")
        return False
    
    print("配置重置成功，开始重新初始化...")
    
    # 2. 重新添加基础服务
    basic_services = [
        {
            "mcpServers": {
                "mcpstore-wiki": {
                    "url": "https://mcpstore.wiki/mcp"
                }
            }
        },
        {
            "mcpServers": {
                "howtocook": {
                    "command": "npx",
                    "args": ["-y", "howtocook-mcp"]
                }
            }
        }
    ]
    
    for service_config in basic_services:
        store.for_store().add_service(service_config)
    
    # 3. 验证重新初始化结果
    services = store.for_store().list_services()
    print(f"重新初始化完成，当前服务数量: {len(services)}")
    
    return True

# 执行重置和重新初始化
reset_and_reinitialize()
```

## 重置影响

不同范围的重置会产生以下影响：

### `"all"` - 全部重置
- 🔄 清空所有服务配置
- 🔄 清空Agent客户端映射
- 🔄 清空客户端服务映射
- 🔄 重置为初始状态

### `"services"` - 服务配置重置
- 🔄 清空mcp.json中的服务配置
- ✅ 保留Agent和客户端映射

### `"agents"` - Agent配置重置
- 🔄 清空Agent客户端映射
- ✅ 保留服务和客户端配置

### `"clients"` - 客户端配置重置
- 🔄 清空客户端服务映射
- ✅ 保留服务和Agent配置

## 相关方法

- [show_config()](show-config.md) - 查看当前配置
- [add_service()](../registration/add-service.md) - 重置后重新添加服务
- [list_services()](../listing/list-services.md) - 查看重置后的服务

## 注意事项

1. **不可逆操作**: 重置操作不可逆，建议重置前备份配置
2. **服务断开**: 重置会断开所有相关服务连接
3. **Agent隔离**: Agent模式下只影响该Agent的配置
4. **文件更新**: 重置会同时更新相关配置文件
5. **范围选择**: 根据需要选择合适的重置范围，避免过度重置
