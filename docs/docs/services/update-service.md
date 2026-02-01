# 更新服务（update_service）

全量替换指定服务的配置，适用于需要重写服务端点、启动命令或认证信息的场景。

## 概念与前置
- Store：全局服务仓库，`for_store()` 操作全局可见的服务（参见 [服务管理概览](overview.md)）。
- Agent：逻辑分组，`for_agent(agent_id)` 仅在该分组内可见，适合隔离上下文。
- 全量更新：`update_service` 会覆盖原有配置，未提供的字段会被清空；若仅需增量修改，请改用 `patch-service.md`。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化 Store（参见 [快速上手](../quickstart.md)），目标服务已存在。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局更新 | `store.for_store().update_service(name, config)` | `bool` | 同步全量替换指定服务配置 |
| Agent 更新 | `store.for_agent("agentA").update_service(name, config)` | `bool` | 仅更新该 Agent 分组下的服务 |
| 异步形式 | `await store.for_store().update_service_async(name, config)` | `bool` | 异步全量替换 |

## 参数说明
| 参数 | 类型 | 必填 | 说明 | 示例 |
| ---- | ---- | ---- | ---- | ---- |
| `name` | str | 是 | 服务名称 | `"weather"` |
| `config` | dict / str | 是 | 新配置，完全替换旧配置；字符串时需为 JSON | 见下方示例 |

## config 参数说明
- 类型：dict / JSON 字符串。
- 要求：必须至少包含 `url` 或 `command` 字段。
- 作用：定义服务端点（HTTP/SSE）或本地启动方式，以及认证、超时等配置信息。
- 认证：`headers` 中可放置 `Authorization`/`X-API-Key` 等；`token/api_key/auth` 会被标准化为 headers。

| 场景 | 最小配置示例 |
| ---- | ------------ |
| 远程服务 | `{"url": "https://api.newweather.com/mcp", "headers": {"Authorization": "Bearer new-token"}}` |
| 本地命令服务 | `{"command": "python", "args": ["./weather_server.py"], "env": {"API_KEY": "xxx"}}` |
| 显式 transport | `{"url": "https://api.example.com/sse", "transport": "sse"}` |

传输类型：未声明时默认 `streamable-http`，URL 含 `/sse` 时推断为 `sse`。可在 config 中显式指定 `transport` 固定类型。

## 标准使用
1) 初始化 Store
```python
from mcpstore import MCPStore
store = MCPStore.setup_store()
```

2) 全量更新服务配置
```python
new_config = {
    "url": "https://api.newweather.com/mcp",
    "transport": "http",
    "timeout": 30,
    "headers": {"Authorization": "Bearer new-token"}
}
ok = store.for_store().update_service("weather", new_config)
print("更新结果:", ok)
```

3) 如需等待新配置生效（重启/重连），单独等待
```python
store.for_store().wait_service("weather", status="healthy", timeout=60)
```

4) 验证配置
```python
info = store.for_store().get_service_info("weather")
print(info)
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

cfg = {
    "command": "python",
    "args": ["./calc.py"],
    "env": {"MODE": "prod"}
}

# 仅更新 agentA 分组下的 local_calc 服务
store.for_agent(agent_id).update_service("local_calc", cfg)

# 等待就绪（可选）
store.for_agent(agent_id).wait_service("local_calc", status="healthy", timeout=60)

# 查看该分组的服务
services = store.for_agent(agent_id).list_services()
print([s.name for s in services])
```

## 返回值
- `True`：更新请求已执行（全量替换），不代表已就绪。
- `False`：更新失败（配置校验或执行异常）。
- 健康与连接状态需要结合 `wait_service` / `check_health` 另行确认。

## 相关与下一步
- 增量更新：`patch-service.md`
- 删除服务：`delete-service.md`
- 重启服务：`restart-service.md`
- 鉴权配置：`../auth/headers.md`
- 查看配置：`show-config.md`
