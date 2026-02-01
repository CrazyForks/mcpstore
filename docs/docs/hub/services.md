# 聚合服务（hub_*）

将当前 Store/Agent 再暴露为 MCP 服务，作为 Hub 供外部调用（HTTP / SSE / stdio），用于把已注册的工具统一对外输出。

## 概念与前置
- Hub：把 Store/Agent 封装成一个 MCP 端点，外部按 MCP 客户端方式连接。
- 适用：需要把内部服务集合对外暴露，或在多 Agent/进程之间复用同一组工具。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化，并已添加服务。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| HTTP Hub | `store.for_store().hub_http(port=8000, host="0.0.0.0", path="/mcp", block=False)` | 服务器对象或句柄 | 启动 HTTP 端点（默认非阻塞） |
| SSE Hub | `store.for_store().hub_sse(port=8000, host="0.0.0.0", path="/mcp", block=False)` | 服务器对象或句柄 | 启动 SSE 端点 |
| stdio Hub | `store.for_store().hub_stdio()` | None | 以 stdio 方式暴露（通常在嵌入式场景） |
| Agent 视角 | `store.for_agent("agentA").hub_http(...)` | 同上 | 仅暴露该 Agent 的服务集合 |

## 参数说明（HTTP/SSE）
| 参数 | 类型 | 必填 | 说明 | 默认值 |
| ---- | ---- | ---- | ---- | ---- |
| `port` | int | 否 | 监听端口 | `8000` |
| `host` | str | 否 | 绑定地址 | `"0.0.0.0"` |
| `path` | str | 否 | MCP 路径 | `"/mcp"` |
| `block` | bool | 否 | 是否阻塞当前线程 | `False` |

## 标准使用（HTTP Hub）
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
# 假设已通过 add_service 添加过服务

hub = store.for_store().hub_http(port=18200, host="0.0.0.0", path="/mcp", block=False)
print("Hub HTTP 已启动:", hub)
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

hub = store.for_agent(agent_id).hub_http(port=18201, path="/mcp-agentA", block=False)
print("Agent Hub 已启动:", hub)
```

## 返回值
- HTTP/SSE：返回服务器对象或控制句柄（实现细节依赖内部服务端实现），若 `block=True` 则阻塞直至退出。
- stdio：无返回值，直接在标准输入输出暴露。

## 相关与下一步
- 添加服务：`../services/add-service.md`
- 服务列表与健康：`../services/list-services.md`、`../services/check-health.md`
- 更新/重启：`../services/update-service.md`、`../services/restart-service.md`
