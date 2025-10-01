# remove_service()

移除服务运行态（保留配置）。

## 方法特性

- ✅ **调用方式**: ServiceProxy 方法
- ✅ **异步版本**: 支持异步调用
- ✅ **Store级别**: `svc = store.for_store().find_service("name")` 后调用
- ✅ **Agent级别**: `svc = store.for_agent("agent1").find_service("name")` 后调用
- 📁 **文件位置**: `service_proxy.py`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回操作结果字典：

```python
{
    "success": bool,            # 操作是否成功
    "message": str,             # 操作消息
    "service_name": str,        # 服务名称
    "removed_at": str           # 移除时间戳
}
```

## 使用示例

### Store级别移除服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_store().wait_service("weather")

# 查找服务
svc = store.for_store().find_service("weather")

# 移除服务运行态
result = svc.remove_service()
print(f"移除结果: {result}")

if result["success"]:
    print(f"✅ 服务已移除（配置保留）")
    
    # 配置仍然存在，可以重新添加
    store.for_store().add_service({
        "mcpServers": {
            "weather": {"url": "https://mcpstore.wiki/mcp"}
        }
    })
    print("✅ 服务已重新添加")
```

### Agent级别移除服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent级别添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_agent("agent1").wait_service("weather")

# 查找服务
svc = store.for_agent("agent1").find_service("weather")

# 移除服务
result = svc.remove_service()
print(f"Agent服务移除结果: {result}")
```

### 优雅停止服务

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

print("📊 服务状态:")
info = svc.service_info()
print(f"  名称: {info.name}")
print(f"  状态: {info.status}")
print(f"  工具数: {info.tool_count}")

# 移除服务（优雅停止）
print("\n🛑 移除服务...")
result = svc.remove_service()

if result["success"]:
    print(f"✅ {result['message']}")
    print(f"  移除时间: {result['removed_at']}")
    
    # 验证服务已移除
    try:
        status = svc.service_status()
        print(f"  当前状态: {status}")
    except Exception as e:
        print(f"  服务已不可访问: {e}")
else:
    print(f"❌ 移除失败: {result['message']}")
```

### 批量移除服务

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加多个服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"},
        "calculator": {"command": "python", "args": ["calc.py"]}
    }
})

# 等待所有服务
store.for_store().wait_service("weather")
store.for_store().wait_service("calculator")

# 批量移除
service_names = ["weather", "calculator"]

print("🛑 批量移除服务")
print("=" * 50)

for name in service_names:
    svc = store.for_store().find_service(name)
    result = svc.remove_service()
    
    icon = "✅" if result["success"] else "❌"
    print(f"{icon} {name}: {result['message']}")
```

### 临时停用服务

```python
from mcpstore import MCPStore
import time

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

print("✅ 服务运行中")
print(f"  工具数: {len(svc.list_tools())}")

# 临时停用（执行维护）
print("\n🛑 临时停用服务...")
result = svc.remove_service()

if result["success"]:
    print("✅ 服务已停用")
    
    # 执行一些维护操作
    print("⏳ 执行维护操作...")
    time.sleep(2)
    
    # 重新启动
    print("\n🔄 重新启动服务...")
    store.for_store().add_service({
        "mcpServers": {
            "weather": {"url": "https://mcpstore.wiki/mcp"}
        }
    })
    store.for_store().wait_service("weather")
    
    print("✅ 服务已恢复")
    svc = store.for_store().find_service("weather")
    print(f"  工具数: {len(svc.list_tools())}")
```

### 移除前保存状态

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 保存当前状态
print("📊 保存服务状态...")
service_info = svc.service_info()
service_config = service_info.config

print(f"  服务名称: {service_info.name}")
print(f"  工具数量: {service_info.tool_count}")
print(f"  配置信息: {service_config}")

# 移除服务
print("\n🛑 移除服务...")
result = svc.remove_service()

if result["success"]:
    print("✅ 服务已移除")
    print("💾 配置已保存，可随时恢复")
```

### 错误处理

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

try:
    # 尝试移除服务
    result = svc.remove_service()
    
    if result["success"]:
        print(f"✅ 服务移除成功: {result['message']}")
    else:
        print(f"⚠️ 服务移除失败: {result['message']}")
        
        # 检查服务状态
        status = svc.service_status()
        print(f"  当前状态: {status}")
        
except Exception as e:
    print(f"❌ 移除服务时发生异常: {e}")
```

## 使用场景

### 1. 临时停用
需要临时停用服务但保留配置，方便后续快速恢复。

### 2. 维护操作
在进行服务维护或更新时，先移除运行态。

### 3. 资源释放
释放服务占用的系统资源，但保留配置信息。

### 4. 测试场景
在测试中需要频繁启停服务时使用。

## 与 delete_service() 的区别

| 对比项 | remove_service() | delete_service() |
|--------|------------------|------------------|
| **操作范围** | 只移除运行态 | 删除配置和缓存 |
| **配置保留** | ✅ 保留 | ❌ 删除 |
| **可恢复性** | ✅ 可快速恢复 | ❌ 需要重新配置 |
| **影响范围** | 运行时状态 | 持久化配置 |
| **使用场景** | 临时停用 | 完全清理 |

```python
# remove_service() - 保留配置
svc.remove_service()  # 运行态清除，配置保留
# 可以通过 add_service() 快速恢复

# delete_service() - 完全删除
svc.delete_service()  # 配置和缓存都删除
# 需要重新配置才能使用
```

## 相关方法

- [delete_service()](delete-service.md) - 完全删除服务
- [restart_service()](restart-service.md) - 重启服务
- [add_service()](../registration/add-service.md) - 添加服务
- [service_status()](../details/service-status.md) - 获取服务状态

## 注意事项

1. **调用前提**: 必须先通过 `find_service()` 获取 ServiceProxy 对象
2. **配置保留**: 移除后配置文件不受影响
3. **快速恢复**: 可以通过 `add_service()` 快速恢复服务
4. **状态清理**: 运行时状态和连接会被清理
5. **Agent隔离**: Agent级别的移除不影响其他Agent

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

