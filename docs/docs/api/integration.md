# 项目结合

如何在项目中结合 API 与 SDK、CLI 使用，快速落地常见场景。

## 典型流程
1) 通过 SDK 构建 Store：`MCPStore.setup_store()`。
2) 使用 API 对外暴露管理能力：`mcpstore run api --host ... --port ...`。
3) 通过 API 调用服务管理接口：如 `add_service`、`list_services`、`check_services`。
4) SDK/Agent 端消费工具：`for_store().list_tools()` 或 Agent 分组 `for_agent(...).list_tools()`。
5) 需要对外复用时，启动 Hub：`for_store().hub_http(...)` 供外部 MCP 客户端连接。

## 结合 CLI
- 管理配置：`mcpstore config show/validate/init`。
- 服务管理：`mcpstore add/list/get/remove`（支持 `--for-agent`）。
- API 服务启动：`mcpstore run api` 或 `mcpstore serve`。
- 传输/认证：`--transport`、`--env`/headers 规则同 SDK。

## 结合 SDK
- 服务添加/等待：`store.for_store().add_service(...)` + `wait_service(...)`。
- 配置查看：`show_config("all")`。
- 健康检查：`check_services()`。
- Agent 隔离：`for_agent(agent_id)` 管理专属服务。

## 相关文档
- 响应结构：`response.md`
- API 总览：`apis.md`
- CLI 使用：`../cli/commands.md`
- SDK 参考：`../store/overview.md`、`../services/overview.md`
