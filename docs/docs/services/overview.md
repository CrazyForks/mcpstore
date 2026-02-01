# 关于服务

本节承上启下，概览 MCPStore 中与“服务”相关的配置与使用路径，帮助你快速跳转到具体操作。

## 你可能想要做什么？
- 如果你要**添加服务**（远程/本地、单个/批量、多格式配置），请看 [添加服务](add-service.md)。
- 如果你要**查看当前有哪些服务**（Store 全局或 Agent 分组），请看 [服务列表](list-services.md)。
- 如果你要**更新服务配置**（全量或增量），请看 [更新服务](update-service.md) 与 [补丁更新](patch-service.md)。
- 如果你要**重启服务**（重新拉起连接/进程），请看 [重启服务](restart-service.md)。
- 如果你要**删除服务**（移除注册与工具），请看 [删除服务](delete-service.md)。
- 如果你要**检查服务健康状态**，请看 [健康检查](check-health.md)。
- 如果你要**查看当前配置快照**（服务/Agent/客户端映射），请看 [配置显示](show-config.md)。
- 如果你要**把服务集合对外暴露成 Hub**（HTTP/SSE/stdio），请看 [聚合服务](../hub/services.md)。
- 如果你要**通过代理对象操作服务**（ServiceProxy 视角），请看 [ServiceProxy](service-proxy.md)。
- 如果你要**等待服务就绪或检查状态**，请结合 [重启服务](restart-service.md) 与 [健康检查](check-health.md) 里的等待/检查逻辑。

## Store vs Agent 视角
- `for_store()`：全局视角，服务对所有 Agent 可见。
- `for_agent(agent_id)`：分组视角，服务仅在该 Agent 下可见，便于隔离上下文与依赖。

## 典型链路示例
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 1) 添加服务
store.for_store().add_service({"mcpServers": {"weather": {"url": "https://mcpstore.wiki/mcp"}}})

# 2) 等待就绪
store.for_store().wait_service("weather", status="healthy", timeout=30)

# 3) 列出/查看
services = store.for_store().list_services()

# 4) 更新或重启（按需）
store.for_store().update_service("weather", {"url": "https://new.example.com/mcp"})
store.for_store().restart_service("weather")

# 5) 健康检查
health = store.for_store().check_services()

# 6) 删除或导出到 Hub（按需）
store.for_store().delete_service("weather")
# 或
store.for_store().hub_http(port=18200, path="/mcp", block=False)
```

## 相关概念
- 服务：遵循 MCP 协议的端点（HTTP/SSE）或本地命令型服务。
- ServiceProxy：通过 `find_service()` 获取的服务代理，可直接操作单个服务。
- 配置范围：`mcpServers`/`agents`/`clients` 等，通过 `show_config` 查看。

以上链接可直接跳转到对应页面，按需深入。 如果缺少某个主题的入口，请提示我补充。 
