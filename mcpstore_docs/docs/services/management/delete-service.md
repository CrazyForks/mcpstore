# delete_service()

删除服务。

## 方法特性

- ✅ **异步版本**: `delete_service_async()`
- ✅ **Store级别**: `store.for_store().delete_service()`
- ✅ **Agent级别**: `store.for_agent("agent1").delete_service()`
- 📁 **文件位置**: `service_management.py`
- 🏷️ **所属类**: `ServiceManagementMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `name` | `str` | ✅ | - | 服务名称 |

## 返回值

- **成功**: 返回 `True`
- **失败**: 返回 `False`（服务不存在或删除失败）

## 使用示例

### Store级别删除服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 删除服务
success = store.for_store().delete_service("weather")
if success:
    print("Weather服务已删除")
else:
    print("Weather服务删除失败或不存在")
```

### Agent级别删除服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式删除服务
success = store.for_agent("agent1").delete_service("weather-local")
if success:
    print("Agent Weather服务已删除")
else:
    print("Agent Weather服务删除失败")
```

### 安全删除（先检查后删除）

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 先检查服务是否存在
services = store.for_store().list_services()
service_names = [s.name for s in services]

if "weather" in service_names:
    success = store.for_store().delete_service("weather")
    if success:
        print("Weather服务已安全删除")
    else:
        print("Weather服务删除失败")
else:
    print("Weather服务不存在，无需删除")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_delete_service():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步删除服务
    success = await store.for_store().delete_service_async("weather")
    
    if success:
        print("异步删除成功")
        # 验证删除结果
        services = await store.for_store().list_services_async()
        remaining_names = [s.name for s in services]
        print(f"剩余服务: {remaining_names}")
    else:
        print("异步删除失败")
    
    return success

# 运行异步删除
result = asyncio.run(async_delete_service())
```

### 批量删除服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 批量删除多个服务
services_to_delete = ["weather", "database", "filesystem"]

deleted_count = 0
for service_name in services_to_delete:
    success = store.for_store().delete_service(service_name)
    if success:
        print(f"✅ {service_name} 删除成功")
        deleted_count += 1
    else:
        print(f"❌ {service_name} 删除失败")

print(f"总计删除 {deleted_count}/{len(services_to_delete)} 个服务")
```

### 条件删除

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 获取所有服务
services = store.for_store().list_services()

# 删除不健康的服务
health_status = store.for_store().check_services()
for service in services:
    if service.name in health_status:
        status = health_status[service.name]['status']
        if status == 'unhealthy':
            success = store.for_store().delete_service(service.name)
            print(f"删除不健康服务 {service.name}: {'成功' if success else '失败'}")
```

### 删除前备份配置

```python
from mcpstore import MCPStore
import json

# 初始化
store = MCPStore.setup_store()

# 删除前备份服务配置
service_name = "weather"
try:
    # 获取服务配置
    service_info = store.for_store().get_service_info(service_name)
    
    # 备份配置到文件
    backup_file = f"{service_name}_backup.json"
    with open(backup_file, 'w') as f:
        json.dump(service_info, f, indent=2)
    
    # 删除服务
    success = store.for_store().delete_service(service_name)
    if success:
        print(f"服务 {service_name} 已删除，配置已备份到 {backup_file}")
    else:
        print(f"服务 {service_name} 删除失败")
        
except Exception as e:
    print(f"备份或删除过程中出错: {e}")
```

### 删除并清理相关资源

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def delete_service_completely(service_name):
    """完全删除服务及相关资源"""
    
    # 1. 获取服务信息
    try:
        service_info = store.for_store().get_service_info(service_name)
        print(f"准备删除服务: {service_name}")
    except:
        print(f"服务 {service_name} 不存在")
        return False
    
    # 2. 删除服务
    success = store.for_store().delete_service(service_name)
    if not success:
        print(f"服务 {service_name} 删除失败")
        return False
    
    # 3. 验证删除结果
    services = store.for_store().list_services()
    remaining_names = [s.name for s in services]
    
    if service_name not in remaining_names:
        print(f"✅ 服务 {service_name} 已完全删除")
        return True
    else:
        print(f"❌ 服务 {service_name} 删除验证失败")
        return False

# 使用完全删除功能
delete_service_completely("weather")
```

## 删除影响

删除服务会产生以下影响：

- ✅ **服务连接**: 立即断开与服务的连接
- ✅ **工具可用性**: 该服务的所有工具将不可用
- ✅ **配置清理**: 从配置文件中移除服务配置
- ✅ **缓存清理**: 清除相关的缓存数据
- ✅ **客户端清理**: 清理相关的客户端连接

## 相关方法

- [add_service()](../registration/add-service.md) - 重新添加服务
- [list_services()](../listing/list-services.md) - 查看剩余服务
- [get_service_info()](../listing/get-service-info.md) - 删除前获取服务信息

## 注意事项

1. **不可逆操作**: 删除操作不可逆，建议删除前备份配置
2. **工具影响**: 删除服务会使其所有工具不可用
3. **Agent隔离**: Agent模式下只能删除该Agent的服务
4. **连接清理**: 删除时会自动清理相关连接和缓存
5. **配置持久化**: 删除会同时更新配置文件
