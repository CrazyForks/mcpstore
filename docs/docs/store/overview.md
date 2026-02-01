# 构建 Store

本页聚焦 Store 的构建与入口函数 `MCPStore.setup_store()` / `setup_store_async()`，帮助你快速拉起一个可用的 Store 上下文。

## 目标
- 了解构建 Store 的入口与返回对象。
- 明确初始化时的主要参数与默认行为。
- 知道初始化完成后可立即调用的核心能力。

## 入口函数
| 方法 | 场景 | 返回值 | 说明 |
| ---- | ---- | ------ | ---- |
| `MCPStore.setup_store(**kwargs)` | 同步初始化 | `MCPStore` | 创建默认配置的 Store，并返回可链式调用的上下文 |
| `await MCPStore.setup_store_async(**kwargs)` | 异步初始化 | `MCPStore` | 在异步环境中初始化，避免事件循环冲突 |

> 返回的 `MCPStore` 支持 `for_store()` / `for_agent(agent_id)` 获取上下文代理，进而调用服务、工具、Hub、配置等功能。

## 常用参数
- `config_path`：自定义配置文件路径（缺省读取默认 `mcp.json`）。
- `cache_config`：切换缓存后端（如 Redis），详见缓存配置文档。
- `debug`：启用调试日志。
- 其他参数通常保持默认即可快速起步；高级参数可参考 SDK 文档与源码注释。

## 构建后的立即可用能力
| 能力 | 入口示例 | 说明 |
| ---- | -------- | ---- |
| 服务管理 | `store.for_store().add_service(...)` | 添加/更新/重启/删除服务 |
| 服务列表 | `store.for_store().list_services()` | 查看当前可见的服务列表 |
| 健康检查 | `store.for_store().check_services()` | 查看全局服务健康摘要 |
| Agent 分组 | `store.for_agent("agentA")...` | 在分组内添加/管理服务，实现隔离 |
| Hub 暴露 | `store.for_store().hub_http(...)` | 将已注册服务对外暴露为 MCP 端点 |
| 配置查看 | `store.for_store().show_config("all")` | 查看当前运行配置与映射 |

## store 与 agent 的关系
- `for_store()`：全局视角，服务对所有 Agent 可见，适合公共能力。
- `for_agent(agent_id)`：分组视角，服务仅在该 Agent 下可见，便于隔离上下文与依赖。
- 方法形态一致：`add_service/list_services/update_service/restart_service/delete_service/show_config` 等在两种视角下保持同名，区别在作用域。
- 常见用法：先用 `for_store()` 管公共服务，再为特定 Agent 用 `for_agent(...)` 添加专属服务，避免上下文过长或认证混用。

## 快速示例
```python
from mcpstore import MCPStore

# 同步构建
store = MCPStore.setup_store()

# 添加一个服务并等待就绪
store.for_store().add_service({"name": "weather", "url": "https://mcpstore.wiki/mcp"})
store.for_store().wait_service("weather", status="healthy", timeout=30)

# 查看列表与健康
services = store.for_store().list_services()
health = store.for_store().check_services()
```

### 异步环境示例
```python
import asyncio
from mcpstore import MCPStore

async def main():
    store = await MCPStore.setup_store_async()
    await store.for_store().add_service_async({"name": "weather", "url": "https://mcpstore.wiki/mcp"})
    await store.for_store().wait_service_async("weather", status="healthy", timeout=30)
    services = await store.for_store().list_services_async()
    print("服务数:", len(services))

asyncio.run(main())
```

## 相关文档
- 服务管理总览：`../services/overview.md`
- 添加服务：`../services/add-service.md`
- 更新/补丁：`../services/update-service.md`、`../services/patch-service.md`
- 重启/等待：`../services/restart-service.md`
- 健康检查：`../services/check-health.md`
- store 与 agent 的关系：本页「store 与 agent 的关系」章节
- Hub 暴露：`../hub/services.md`
