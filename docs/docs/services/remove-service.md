## remove_service - 服务移除


如何通过 MCPStore 移除服务运行态（保留配置）。

### SDK

同步：
  - `svc.remove_service() -> dict`

异步：
  - `await svc.remove_service_async() -> dict`

### 参数

| 参数名      | 类型     | 说明                                     |
|------------|----------|------------------------------------------|
| 无         | -        | 该方法不需要参数。                       |

### 返回值

| 字段           | 类型 | 说明           |
|----------------|------|----------------|
| `success`      | bool | 操作是否成功。 |
| `message`      | str  | 操作消息。     |
| `service_name` | str  | 服务名称。     |
| `removed_at`   | str  | 移除时间戳。   |


### 视角
在通过 `find_service()` 获取的 `ServiceProxy` 上调用。支持 Store 级与 Agent 级：
`svc = store.for_store().find_service(name)` 或 `svc = store.for_agent(agent_id).find_service(name)`。


### 使用示例

Store 级移除服务：
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

# 移除服务运行态（配置保留）
result = svc.remove_service()
print(f"移除结果: {result}")

if result["success"]:
    # 配置仍然存在，可以重新添加
    store.for_store().add_service({
        "mcpServers": {
            "weather": {"url": "https://mcpstore.wiki/mcp"}
        }
    })
    print("服务已重新添加")
```

Agent 级移除服务：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# Agent 级添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_agent("agent1").wait_service("weather")
svc = store.for_agent("agent1").find_service("weather")

result = svc.remove_service()
print(f"Agent 服务移除结果: {result}")
```

优雅停止服务：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

info = svc.service_info()
print(f"名称: {info.name}")
print(f"状态: {info.status}")
print(f"工具数: {info.tool_count}")

# 移除服务（优雅停止）
result = svc.remove_service()

if result["success"]:
    print(result["message"])
    print(f"移除时间: {result['removed_at']}")
    try:
        status = svc.service_status()
        print(f"当前状态: {status}")
    except Exception as e:
        print(f"服务已不可访问: {e}")
else:
    print(f"移除失败: {result['message']}")
```

批量移除服务：
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

store.for_store().wait_service("weather")
store.for_store().wait_service("calculator")

service_names = ["weather", "calculator"]

for name in service_names:
    svc = store.for_store().find_service(name)
    result = svc.remove_service()
    print(f"{name}: {result['message']}")
```

临时停用服务并恢复：
```python
from mcpstore import MCPStore
import time

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

print("服务运行中")
print(f"工具数: {len(svc.list_tools())}")

# 临时停用（执行维护）
result = svc.remove_service()

if result["success"]:
    print("服务已停用")
    # 执行一些维护操作
    time.sleep(2)
    # 重新启动
    store.for_store().add_service({
        "mcpServers": {
            "weather": {"url": "https://mcpstore.wiki/mcp"}
        }
    })
    store.for_store().wait_service("weather")
    print("服务已恢复")
    svc = store.for_store().find_service("weather")
    print(f"工具数: {len(svc.list_tools())}")
```

移除前保存状态：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 保存当前状态
service_info = svc.service_info()
service_config = service_info.config

print(f"服务名称: {service_info.name}")
print(f"工具数量: {service_info.tool_count}")
print(f"配置信息: {service_config}")

# 移除服务
result = svc.remove_service()

if result["success"]:
    print("服务已移除")
    print("配置已保存，可随时恢复")
```

错误处理：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

try:
    result = svc.remove_service()
    if result["success"]:
        print(f"服务移除成功: {result['message']}")
    else:
        print(f"服务移除失败: {result['message']}")
        status = svc.service_status()
        print(f"当前状态: {status}")
except Exception as e:
    print(f"移除服务时发生异常: {e}")
```


### 与 delete_service 的区别

| 对比项     | remove_service | delete_service |
|------------|----------------|----------------|
| 操作范围   | 只移除运行态   | 删除配置和缓存 |
| 配置保留   | 保留           | 删除           |
| 可恢复性   | 可快速恢复     | 需要重新配置   |
| 影响范围   | 运行时状态     | 持久化配置     |
| 使用场景   | 临时停用       | 完全清理       |

```python
# remove_service — 保留配置
svc.remove_service()  # 运行态清除，配置保留
# 可通过 add_service() 快速恢复

# delete_service — 完全删除
svc.delete_service()  # 配置和缓存都删除
# 需要重新配置后再使用
```


### 使用场景

- 临时停用：需要短暂停用服务但保留配置，便于快速恢复。
- 维护操作：在进行服务维护或更新时，先移除运行态。
- 资源释放：释放占用的系统资源，但保留配置信息。
- 测试场景：在测试中需要频繁启停服务。


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 完全删除服务     | `svc.delete_service()` |
| 重启服务         | `svc.restart_service()` |
| 添加服务         | `store.for_store().add_service(...)` |
| 获取服务状态     | `svc.service_status()` |
| 查找服务         | `store.for_store().find_service(name)` |


### 注意事项

- 调用前提：请先通过 `find_service()` 获取 `ServiceProxy` 对象。
- 配置保留：移除后持久化配置不受影响。
- 快速恢复：可通过 `add_service()` 快速恢复服务。
- 状态清理：运行时状态与连接将被清理。
- Agent 隔离：Agent 级别的移除不影响其他 Agent。


