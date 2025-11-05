## reset_config - 配置重置


如何通过 MCPStore 重置配置。

### SDK

同步：
  - `store.for_store().reset_config(scope="all") -> bool`
  - `store.for_agent(id).reset_config(scope="all") -> bool`

异步：
  - `await store.for_store().reset_config_async(scope="all") -> bool`
  - `await store.for_agent(id).reset_config_async(scope="all") -> bool`

### 参数

| 参数名  | 类型 | 说明 |
|---------|------|------|
| `scope` | str  | 重置范围，默认 `"all"`。可选：`"all"`、`"services"`、`"agents"`、`"clients"`。 |

重置范围说明：

| 范围值      | 描述             | 影响内容 |
|-------------|------------------|----------|
| `all`       | 重置所有配置     | 服务配置、Agent 配置、客户端配置 |
| `services`  | 只重置服务配置   | `mcp.json` 中的服务配置 |
| `agents`    | 只重置 Agent 配置 | Agent 客户端映射 |
| `clients`   | 只重置客户端配置 | 客户端服务映射 |


### 返回值

- `True`：重置成功
- `False`：重置失败


### 视角
通过 `for_store()` 重置全局配置；通过 `for_agent(id)` 仅重置对应 Agent 的配置空间。


### 使用示例

Store 级别重置所有配置：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

success = store.for_store().reset_config("all")
print("所有配置已重置" if success else "配置重置失败")
```

Agent 级别重置配置：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

success = store.for_agent("agent1").reset_config()
if success:
    print("Agent1 配置已重置")
```

重置特定范围：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 只重置服务配置
store.for_store().reset_config("services")

# 只重置 Agent 配置
store.for_store().reset_config("agents")

# 只重置客户端配置
store.for_store().reset_config("clients")
```

异步版本：
```python
import asyncio
from mcpstore import MCPStore

async def main():
    store = MCPStore.setup_store()
    success = await store.for_store().reset_config_async("all")
    if success:
        services = await store.for_store().list_services_async()
        print(f"重置后服务数量: {len(services)}")

asyncio.run(main())
```

安全重置（备份后重置）：
```python
from mcpstore import MCPStore
import json
from datetime import datetime

store = MCPStore.setup_store()

def safe_reset_config(scope="all"):
    try:
        current_config = store.for_store().show_config(scope)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"config_backup_{scope}_{timestamp}.json"
        with open(backup_file, 'w') as f:
            json.dump(current_config, f, indent=2, ensure_ascii=False)
        print(f"配置已备份到: {backup_file}")
    except Exception as e:
        print(f"备份失败: {e}")
        return False

    success = store.for_store().reset_config(scope)
    print(f"配置范围 '{scope}' 重置{'成功' if success else '失败'}")
    return success

safe_reset_config("services")
```

批量重置不同范围：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

reset_scopes = ["clients", "agents", "services"]
for scope in reset_scopes:
    success = store.for_store().reset_config(scope)
    print(f"重置 {scope}: {'成功' if success else '失败'}")
    if success:
        config = store.for_store().show_config(scope)
        print(f"  重置后 {scope} 配置项数量: {len(config)}")
```

条件重置：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

def conditional_reset():
    services = store.for_store().list_services()
    health = store.for_store().check_services()
    unhealthy_count = sum(1 for st in health.values() if not st.get('healthy', False))
    if unhealthy_count > len(services) / 2:
        print(f"发现 {unhealthy_count} 个不健康服务，执行服务配置重置")
        return store.for_store().reset_config("services")
    print("服务状态正常，无需重置")
    return True

conditional_reset()
```

重置后重新初始化：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

def reset_and_reinitialize():
    success = store.for_store().reset_config("all")
    if not success:
        print("配置重置失败")
        return False

    print("配置重置成功，开始重新初始化...")
    basic_services = [
        {"mcpServers": {"mcpstore-wiki": {"url": "https://mcpstore.wiki/mcp"}}},
        {"mcpServers": {"howtocook": {"command": "npx", "args": ["-y", "howtocook-mcp"]}}}
    ]
    for cfg in basic_services:
        store.for_store().add_service(cfg)

    services = store.for_store().list_services()
    print(f"重新初始化完成，当前服务数量: {len(services)}")
    return True

reset_and_reinitialize()
```


### 重置影响

不同范围的重置影响如下：

- `all`：清空所有服务配置、Agent 客户端映射、客户端服务映射，恢复初始状态。
- `services`：清空 `mcp.json` 中的服务配置，保留 Agent 与客户端映射。
- `agents`：清空 Agent 客户端映射，保留服务与客户端配置。
- `clients`：清空客户端服务映射，保留服务与 Agent 配置。


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 查看当前配置     | `store.for_store().show_config(scope)` |
| 注册服务         | `store.for_store().add_service(config=..., ...)` |
| 列出服务         | `store.for_store().list_services()` |
| 获取服务信息     | `store.for_store().get_service_info(name)` |


### 使用场景

- 快速清理环境并恢复初始状态。
- 大量配置错误或污染后进行一次性重置。
- 按范围清理某一类配置数据（仅服务/仅 Agent/仅客户端）。


### 注意事项

- 不可逆操作：重置不可撤销，建议重置前备份配置。
- 连接影响：重置会导致相关服务连接断开。
- Agent 隔离：Agent 模式下只影响该 Agent 的配置空间。
- 文件更新：重置会更新本地配置文件与缓存。
- 合理选择范围：按需选择 `scope`，避免过度重置。


