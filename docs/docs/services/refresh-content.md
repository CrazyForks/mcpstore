## refresh_content - 内容刷新


如何通过 MCPStore 刷新服务内容（重新获取工具列表等）。

### SDK

同步：
  - `svc.refresh_content() -> dict`

异步：
  - `await svc.refresh_content_async() -> dict`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 无     | -    | 该方法不需要参数。 |

### 返回值

| 字段          | 类型 | 说明             |
|---------------|------|------------------|
| `success`     | bool | 刷新是否成功。   |
| `message`     | str  | 操作消息。       |
| `tool_count`  | int  | 刷新后的工具数量。|
| `refreshed_at`| str  | 刷新时间戳。     |


### 视角
在通过 `find_service()` 获取的 `ServiceProxy` 上调用。支持 Store 级与 Agent 级：
`svc = store.for_store().find_service(name)` 或 `svc = store.for_agent(agent_id).find_service(name)`。


### 使用示例

Store 级刷新服务内容：
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
print(f"刷新前工具数: {len(svc.list_tools())}")

result = svc.refresh_content()
print(f"刷新结果: {result}")
print(f"刷新后工具数: {len(svc.list_tools())}")
```

Agent 级刷新服务内容：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_agent("agent1").wait_service("weather")
svc = store.for_agent("agent1").find_service("weather")

result = svc.refresh_content()
print(f"Agent 服务刷新结果: {result}")
```

服务更新后刷新：
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

original_tools = svc.list_tools()
print(f"原始工具数: {len(original_tools)}")

# 假设服务端更新了工具，刷新以获取最新工具列表
result = svc.refresh_content()

if result["success"]:
    print("刷新成功")
    print(f"工具数量: {result['tool_count']}")
    print(f"刷新时间: {result['refreshed_at']}")
    new_tools = svc.list_tools()
    print(f"新工具数: {len(new_tools)}")
else:
    print(f"刷新失败: {result['message']}")
```

定期刷新：
```python
import time
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

print("开始定期刷新...")
for i in range(5):
    print(f"[刷新 {i+1}]")
    result = svc.refresh_content()
    if result["success"]:
        print(f"成功 - 工具数: {result['tool_count']}")
    else:
        print(f"失败 - {result['message']}")
    if i < 4:
        time.sleep(30)
```

批量刷新多个服务：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

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
    result = svc.refresh_content()
    print(name)
    print(f"  工具数: {result.get('tool_count', 'N/A')}")
    print(f"  消息: {result['message']}")
```

刷新失败重试：
```python
import time
from mcpstore import MCPStore

store = MCPStore.setup_store()

store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

max_retries = 3
retry_delay = 2

for attempt in range(max_retries):
    print(f"尝试刷新 (第 {attempt + 1} 次)...")
    result = svc.refresh_content()
    if result["success"]:
        print(f"刷新成功 - 工具数: {result['tool_count']}")
        break
    else:
        print(f"刷新失败: {result['message']}")
        if attempt < max_retries - 1:
            print(f"等待 {retry_delay} 秒后重试...")
            time.sleep(retry_delay)
        else:
            print("达到最大重试次数，放弃刷新")
```

结合健康检查使用：
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

health = svc.check_health()
print(f"服务健康: {health['healthy']}")

if health["healthy"]:
    result = svc.refresh_content()
    if result["success"]:
        print(f"刷新成功 - 工具数: {result['tool_count']}")
    else:
        print(f"刷新失败: {result['message']}")
else:
    print("服务不健康，跳过刷新")
```


## 与 restart_service 的区别

| 对比项   | refresh_content | restart_service |
|----------|------------------|-----------------|
| 操作范围 | 只刷新内容      | 完全重启服务    |
| 连接状态 | 保持连接        | 断开并重新连接  |
| 影响范围 | 较小            | 较大            |
| 执行时间 | 较快            | 较慢            |
| 使用场景 | 内容同步        | 故障恢复        |

```python
# refresh_content — 只刷新内容
result = svc.refresh_content()

# restart_service — 完全重启
result = svc.restart_service()
```


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 重启服务         | `svc.restart_service()` |
| 更新服务         | `store.for_store().update_service(name, config)` |
| 增量更新服务     | `store.for_store().patch_service(name, patch)` |
| 获取服务信息     | `svc.service_info()` |
| 获取服务状态     | `svc.service_status()` |
| 列出工具         | `svc.list_tools()` |


### 使用场景

- 服务工具更新：远程服务新增或删除工具后同步本地工具列表。
- 服务配置变更：修改配置后刷新以确保使用最新内容。
- 定期同步：长期运行的应用中定期刷新保持最新状态。
- 故障恢复：服务从异常恢复后刷新以验证功能正常。


### 注意事项

- 调用前提：请先通过 `find_service()` 获取 `ServiceProxy` 对象。
- 服务状态：建议在服务健康时执行刷新。
- 性能影响：刷新会触发网络请求，有一定开销。
- 工具变化：刷新后工具数量可能变化。
- 频率控制：避免过于频繁刷新。

