# batch_add_services()

批量添加多个服务。

## 方法特性

- ✅ **异步版本**: `batch_add_services_async()`
- ✅ **Store级别**: `store.for_store().batch_add_services()`
- ✅ **Agent级别**: `store.for_agent("agent1").batch_add_services()`
- 📁 **文件位置**: `tool_operations.py`
- 🏷️ **所属类**: `ToolOperationsMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `services` | `List[Union[str, Dict[str, Any]]]` | ✅ | - | 服务配置列表 |

## 返回值

返回批量添加结果字典：

```python
{
    "success": True,
    "total_requested": 3,
    "total_added": 2,
    "successful_services": ["service1", "service2"],
    "failed_services": ["service3"],
    "errors": ["Service3 connection failed"],
    "summary": {
        "success_rate": 0.67,
        "total_time": 5.23
    }
}
```

## 使用示例

### Store级别批量添加

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 批量添加服务
services = [
    {
        "mcpServers": {
            "weather": {"url": "https://api.weather.com/mcp"}
        }
    },
    {
        "mcpServers": {
            "database": {"command": "python", "args": ["db_server.py"]}
        }
    },
    {
        "mcpServers": {
            "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]}
        }
    }
]

result = store.for_store().batch_add_services(services)
print(f"批量添加结果: {result}")

if result["success"]:
    print(f"✅ 成功添加 {result['total_added']}/{result['total_requested']} 个服务")
    print(f"成功率: {result['summary']['success_rate']:.1%}")
else:
    print(f"❌ 批量添加失败")
    print(f"失败服务: {result['failed_services']}")
```

### Agent级别批量添加

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式批量添加
agent_services = [
    {
        "mcpServers": {
            "weather-local": {"url": "https://api.weather.com/mcp"}
        }
    },
    {
        "mcpServers": {
            "tools-local": {"command": "python", "args": ["tools_server.py"]}
        }
    }
]

result = store.for_agent("agent1").batch_add_services(agent_services)
print(f"Agent批量添加: {result['total_added']} 个服务")
```

### 混合配置格式批量添加

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 混合不同格式的服务配置
mixed_services = [
    # 字典格式
    {
        "mcpServers": {
            "weather": {"url": "https://api.weather.com/mcp"}
        }
    },
    # JSON文件路径
    "config/database_service.json",
    # 另一个字典格式
    {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        }
    }
]

result = store.for_store().batch_add_services(mixed_services)

print("=== 混合格式批量添加结果 ===")
print(f"请求添加: {result['total_requested']} 个")
print(f"成功添加: {result['total_added']} 个")
print(f"成功服务: {result['successful_services']}")

if result['failed_services']:
    print(f"失败服务: {result['failed_services']}")
    print(f"错误信息: {result['errors']}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_batch_add():
    # 初始化
    store = MCPStore.setup_store()
    
    # 准备服务列表
    services = [
        {
            "mcpServers": {
                "weather": {"url": "https://api.weather.com/mcp"}
            }
        },
        {
            "mcpServers": {
                "database": {"command": "python", "args": ["db_server.py"]}
            }
        }
    ]
    
    # 异步批量添加
    result = await store.for_store().batch_add_services_async(services)
    
    print(f"异步批量添加完成:")
    print(f"  总耗时: {result['summary']['total_time']:.2f}秒")
    print(f"  成功率: {result['summary']['success_rate']:.1%}")
    
    return result

# 运行异步批量添加
result = asyncio.run(async_batch_add())
```

### 大批量添加优化

```python
from mcpstore import MCPStore
import time

# 初始化
store = MCPStore.setup_store()

def optimized_batch_add(services_list, batch_size=5):
    """优化的大批量添加"""
    
    total_services = len(services_list)
    all_results = []
    
    print(f"开始批量添加 {total_services} 个服务，批次大小: {batch_size}")
    
    # 分批处理
    for i in range(0, total_services, batch_size):
        batch = services_list[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        print(f"\n处理第 {batch_num} 批 ({len(batch)} 个服务)...")
        
        start_time = time.time()
        result = store.for_store().batch_add_services(batch)
        end_time = time.time()
        
        print(f"  批次结果: {result['total_added']}/{result['total_requested']} 成功")
        print(f"  批次耗时: {end_time - start_time:.2f}秒")
        
        all_results.append(result)
        
        # 批次间短暂休息
        if i + batch_size < total_services:
            time.sleep(0.5)
    
    # 汇总结果
    total_requested = sum(r['total_requested'] for r in all_results)
    total_added = sum(r['total_added'] for r in all_results)
    all_successful = []
    all_failed = []
    all_errors = []
    
    for result in all_results:
        all_successful.extend(result['successful_services'])
        all_failed.extend(result['failed_services'])
        all_errors.extend(result['errors'])
    
    summary = {
        "total_requested": total_requested,
        "total_added": total_added,
        "successful_services": all_successful,
        "failed_services": all_failed,
        "errors": all_errors,
        "success_rate": total_added / total_requested if total_requested > 0 else 0
    }
    
    print(f"\n=== 最终汇总 ===")
    print(f"总计添加: {total_added}/{total_requested} 个服务")
    print(f"成功率: {summary['success_rate']:.1%}")
    
    return summary

# 准备大量服务配置
large_services_list = []
for i in range(20):
    large_services_list.append({
        "mcpServers": {
            f"service_{i}": {"url": f"https://api{i}.example.com/mcp"}
        }
    })

# 执行优化批量添加
final_result = optimized_batch_add(large_services_list, batch_size=5)
```

### 错误处理和重试

```python
from mcpstore import MCPStore
import time

# 初始化
store = MCPStore.setup_store()

def batch_add_with_retry(services, max_retries=2):
    """带重试的批量添加"""
    
    for attempt in range(max_retries):
        print(f"批量添加尝试 {attempt + 1}/{max_retries}")
        
        result = store.for_store().batch_add_services(services)
        
        # 如果全部成功，直接返回
        if result['total_added'] == result['total_requested']:
            print("✅ 所有服务添加成功")
            return result
        
        # 如果有失败，分析失败原因
        if result['failed_services']:
            print(f"❌ {len(result['failed_services'])} 个服务添加失败")
            
            # 准备重试失败的服务
            if attempt < max_retries - 1:
                failed_indices = []
                for i, service_config in enumerate(services):
                    # 这里需要根据实际情况判断哪些服务失败了
                    # 简化示例，假设按顺序失败
                    if i >= result['total_added']:
                        failed_indices.append(i)
                
                retry_services = [services[i] for i in failed_indices[:len(result['failed_services'])]]
                print(f"准备重试 {len(retry_services)} 个失败的服务...")
                
                time.sleep(2)  # 等待后重试
                services = retry_services  # 只重试失败的服务
            else:
                print("达到最大重试次数")
                break
    
    return result

# 使用重试机制
services_to_add = [
    {
        "mcpServers": {
            "weather": {"url": "https://api.weather.com/mcp"}
        }
    },
    {
        "mcpServers": {
            "database": {"url": "https://unreliable-api.com/mcp"}  # 可能失败的服务
        }
    }
]

final_result = batch_add_with_retry(services_to_add)
```

## 返回字段说明

### 主要字段
- `success`: 整体操作是否成功
- `total_requested`: 请求添加的服务总数
- `total_added`: 实际成功添加的服务数
- `successful_services`: 成功添加的服务名称列表
- `failed_services`: 添加失败的服务名称列表
- `errors`: 详细错误信息列表

### 汇总信息 (summary)
- `success_rate`: 成功率 (0.0-1.0)
- `total_time`: 总耗时（秒）

## 相关方法

- [add_service()](add-service.md) - 添加单个服务
- [add_service_with_details()](add-service-with-details.md) - 添加服务并获取详情
- [list_services()](../listing/list-services.md) - 查看添加结果

## 注意事项

1. **并发处理**: 内部会并发处理多个服务，提高效率
2. **错误隔离**: 单个服务失败不会影响其他服务的添加
3. **格式兼容**: 支持多种配置格式混合使用
4. **性能监控**: 返回详细的性能和成功率统计
5. **Agent映射**: Agent模式下自动处理所有服务的名称映射
