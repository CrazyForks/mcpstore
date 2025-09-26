# add_service_with_details()

添加服务并返回详细信息。

## 方法特性

- ✅ **异步版本**: `add_service_with_details_async()`
- ✅ **Store级别**: `store.for_store().add_service_with_details()`
- ✅ **Agent级别**: `store.for_agent("agent1").add_service_with_details()`
- 📁 **文件位置**: `service_operations.py`
- 🏷️ **所属类**: `ServiceOperationsMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `config` | `Union[ServiceConfigUnion, List[str], None]` | ❌ | `None` | 服务配置 |
| `json_file` | `str` | ❌ | `None` | JSON配置文件路径 |

## 返回值

返回包含详细信息的字典：

```python
{
    "success": True,
    "services_added": [
        {
            "name": "service_name",
            "status": "healthy|warning|unhealthy",
            "tools_count": 5,
            "connection_time": 1.23,
            "service_info": {...}
        }
    ],
    "total_added": 1,
    "errors": []
}
```

## 使用示例

### Store级别添加服务并获取详情

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务并获取详细信息
result = store.for_store().add_service_with_details({
    "mcpServers": {
        "weather": {"url": "https://api.weather.com/mcp"}
    }
})

print(f"添加结果: {result}")

if result["success"]:
    for service in result["services_added"]:
        print(f"服务 {service['name']}:")
        print(f"  状态: {service['status']}")
        print(f"  工具数量: {service['tools_count']}")
        print(f"  连接时间: {service['connection_time']:.2f}秒")
```

### Agent级别添加服务并获取详情

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式添加服务
result = store.for_agent("agent1").add_service_with_details({
    "mcpServers": {
        "weather-local": {"url": "https://api.weather.com/mcp"}
    }
})

print(f"Agent添加结果: {result}")
if result["success"]:
    print(f"成功添加 {result['total_added']} 个服务")
```

### 从JSON文件添加并获取详情

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 从JSON文件添加服务
result = store.for_store().add_service_with_details(
    json_file="services_config.json"
)

print(f"从文件添加结果: {result}")

# 分析添加结果
if result["success"]:
    print(f"✅ 成功添加 {result['total_added']} 个服务")
    
    # 显示每个服务的详细信息
    for service in result["services_added"]:
        print(f"\n服务: {service['name']}")
        print(f"  健康状态: {service['status']}")
        print(f"  可用工具: {service['tools_count']} 个")
        print(f"  连接耗时: {service['connection_time']:.2f}秒")
        
        # 显示工具列表
        if service['tools_count'] > 0:
            tools = service['service_info'].get('tools', [])
            print(f"  工具列表: {[t.get('name', 'unknown') for t in tools[:3]]}...")

if result["errors"]:
    print(f"\n❌ 发生 {len(result['errors'])} 个错误:")
    for error in result["errors"]:
        print(f"  - {error}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_add_with_details():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步添加服务并获取详情
    result = await store.for_store().add_service_with_details_async({
        "mcpServers": {
            "weather": {"url": "https://api.weather.com/mcp"},
            "database": {"command": "python", "args": ["db_server.py"]}
        }
    })
    
    print(f"异步添加结果: {result}")
    
    # 分析性能数据
    if result["success"]:
        total_time = sum(s['connection_time'] for s in result['services_added'])
        avg_time = total_time / len(result['services_added'])
        print(f"平均连接时间: {avg_time:.2f}秒")
    
    return result

# 运行异步添加
result = asyncio.run(async_add_with_details())
```

### 批量添加并分析结果

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 批量添加多个服务
services_config = {
    "mcpServers": {
        "weather": {"url": "https://api.weather.com/mcp"},
        "database": {"command": "python", "args": ["db_server.py"]},
        "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]}
    }
}

result = store.for_store().add_service_with_details(services_config)

# 详细分析结果
print("=== 批量添加分析 ===")
print(f"总体成功: {result['success']}")
print(f"添加数量: {result['total_added']}")
print(f"错误数量: {len(result['errors'])}")

# 按状态分组
status_groups = {}
for service in result["services_added"]:
    status = service['status']
    if status not in status_groups:
        status_groups[status] = []
    status_groups[status].append(service['name'])

print("\n=== 服务状态分布 ===")
for status, services in status_groups.items():
    print(f"{status}: {len(services)} 个服务")
    for service_name in services:
        print(f"  - {service_name}")

# 性能分析
if result["services_added"]:
    connection_times = [s['connection_time'] for s in result["services_added"]]
    print(f"\n=== 性能分析 ===")
    print(f"最快连接: {min(connection_times):.2f}秒")
    print(f"最慢连接: {max(connection_times):.2f}秒")
    print(f"平均连接: {sum(connection_times)/len(connection_times):.2f}秒")

# 工具统计
total_tools = sum(s['tools_count'] for s in result["services_added"])
print(f"\n=== 工具统计 ===")
print(f"总工具数量: {total_tools}")
print(f"平均每服务: {total_tools/len(result['services_added']):.1f} 个工具")
```

### 错误处理和重试

```python
from mcpstore import MCPStore
import time

# 初始化
store = MCPStore.setup_store()

def add_service_with_retry(config, max_retries=3):
    """带重试的服务添加"""
    
    for attempt in range(max_retries):
        print(f"尝试添加服务 (第 {attempt + 1} 次)...")
        
        result = store.for_store().add_service_with_details(config)
        
        if result["success"] and not result["errors"]:
            print("✅ 服务添加成功")
            return result
        
        if result["errors"]:
            print(f"❌ 发现错误: {result['errors']}")
            
            # 如果不是最后一次尝试，等待后重试
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
    
    print("❌ 达到最大重试次数，添加失败")
    return result

# 使用重试机制
config = {
    "mcpServers": {
        "weather": {"url": "https://api.weather.com/mcp"}
    }
}

final_result = add_service_with_retry(config)
```

## 返回字段说明

### 主要字段
- `success`: 整体操作是否成功
- `services_added`: 成功添加的服务列表
- `total_added`: 成功添加的服务数量
- `errors`: 错误信息列表

### 服务详情字段
- `name`: 服务名称
- `status`: 健康状态 (healthy/warning/unhealthy)
- `tools_count`: 可用工具数量
- `connection_time`: 连接建立时间（秒）
- `service_info`: 完整的服务信息对象

## 与 add_service() 的区别

| 特性 | add_service() | add_service_with_details() |
|------|---------------|---------------------------|
| 返回值 | 上下文对象 | 详细结果字典 |
| 性能信息 | 无 | 包含连接时间等 |
| 错误信息 | 异常抛出 | 错误列表返回 |
| 使用场景 | 链式调用 | 结果分析 |

## 相关方法

- [add_service()](add-service.md) - 基础的服务添加方法
- [batch_add_services()](batch-add-services.md) - 批量添加服务
- [get_service_info()](../listing/get-service-info.md) - 获取服务详细信息

## 注意事项

1. **性能监控**: 返回连接时间等性能数据，便于监控
2. **错误收集**: 收集所有错误而不是立即抛出异常
3. **健康检查**: 添加后立即进行健康状态检查
4. **Agent映射**: Agent模式下自动处理服务名映射
5. **详细分析**: 适合需要详细了解添加结果的场景
