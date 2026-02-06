# 添加服务（add_service）

面向 Store 或 Agent 分组，把 MCP 服务注册到 MCPStore 的入口，支持本地/远程/批量/兼容 IDE mcpServers 等多种配置。

## 概念与前置
- Store：全局服务仓库，`for_store()` 操作全局可见的服务（参见 [服务管理概览](overview.md)）。
- Agent：逻辑分组，`for_agent(agent_id)` 仅在该分组内可见，适合隔离上下文。
- MCP 服务：遵循 MCP 协议的服务，可以是 HTTP/SSE 远程端点，也可以是本地进程。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化 Store（参见 [快速上手](../quickstart.md)）。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局注册 | `store.for_store().add_service(config=..., json_file=..., headers=...)` | `MCPStoreContext`（可链式继续调用） | 同步注册，不等待就绪 |
| Agent 注册 | `store.for_agent("agentA").add_service(config=..., ...)` | `MCPStoreContext` | 仅对指定 Agent 可见 |
| 异步形式 | `await store.for_store().add_service_async(config)` | `bool` | 异步注册；同样不等待就绪 |

## 参数说明
| 参数 | 类型 | 必填 | 说明 | 示例 |
| ---- | ---- | ---- | ---- | ---- |
| `config` | dict / list / str | 是（与 json_file 二选一） | 服务配置；支持单个、批量、mcpServers、宽字典；字符串时需为 JSON | 见下方示例 |
| `json_file` | str | 否 | 从 JSON 文件读取配置；若同时提供 `config`，以文件为准 | `/path/to/mcp.json` |
| `headers` | dict | 否 | 认证请求头，最终写入配置；`token/api_key/auth` 会被标准化为 headers | `{"Authorization": "Bearer <token>"}` |

## config 参数说明
- 类型：dict / list / str（字符串需为 JSON，等价于 dict 或 list）。
- 作用：描述要注册的服务集合，支持单个、批量、mcpServers 兼容格式、宽字典等。
- 认证：`token/api_key/auth` 会被标准化为 `headers` 并随配置保存。

| 场景 | 最小配置示例 |
| ---- | ------------ |
| 单个远程服务 | `{"name": "mcpstore_wiki", "url": "https://www.mcpstore.wiki/mcp"}` |
| 单个本地服务 | `{"name": "assistant", "command": "python", "args": ["./assistant_server.py"], "env": {"DEBUG": "true"}}` |
| mcpServers 兼容格式（IDE 导出） | `{"mcpServers": {"weather": {"url": "..."}, "assistant": {"command": "..."}}}` |
| 宽字典（服务名作键） | `{"weather": {"url": "https://weather.example.com/mcp"}, "assistant": {"command": "python", "args": ["./assistant.py"]}}` |
| 批量列表 | `[{"name": "weather", "url": "https://weather.example.com/mcp"}, {"name": "assistant", "command": "python", "args": ["./assistant.py"]}]` |

传输类型自动推断：未声明时默认 `streamable-http`；URL 包含 `/sse` 时推断为 `sse`。如需固定传输，可显式设置 `transport`。

## 标准使用
1) 初始化 Store（全局视角）
```python
from mcpstore import MCPStore
store = MCPStore.setup_store()
```

2) 注册服务
```python
cfg = {"name": "weather", "url": "https://weather.example.com/mcp"}
store.for_store().add_service(config=cfg)
```

3) 如需等待就绪，单独调用
```python
store.for_store().wait_service("weather", status="healthy", timeout=30)
```

4) 验证已登记
```python
services = store.for_store().list_services()
print([s.name for s in services])  # 期望包含 "weather"
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 在 agentA 分组注册服务，只在该分组可见
agent_id = "agentA"
cfg = {"name": "local_calc", "command": "python", "args": ["./calc.py"]}
store.for_agent(agent_id).add_service(cfg)

# 等待就绪（可选）
store.for_agent(agent_id).wait_service("local_calc", status="healthy", timeout=60)

# 列出该 Agent 下的服务
agent_services = store.for_agent(agent_id).list_services()
print([s.name for s in agent_services])  # 期望包含 "local_calc"
```

## 返回值
- `add_service` / `add_service_async`：完成注册动作但不等待连接，返回上下文或布尔值。
- 连接与健康状态需通过 `wait_service` 或 `check_health`（见本目录的其他页面）确认。

## 相关与下一步
- 鉴权配置：`../auth/headers.md`（例如 token/api_key/header 规范）
- 查询当前服务列表：`list-services.md`
- 更新配置：`update-service.md`
- 重启或删除：`restart-service.md`、`delete-service.md`
- 查看服务代理能力：`service-proxy.md`

## 常见问题
- 为什么添加后立即调用工具报“未就绪”？  
  add_service 只登记并触发初始化，请先等待服务健康状态正常再调用工具。
- 配置是字符串怎么办？  
  提供 JSON 字符串即可，内部会解析；非法 JSON 会抛异常。
- headers 和 token 的关系？  
  `token/api_key/auth` 会被统一写入 headers，最终以 headers 形式落盘和请求。
