# 代理对象

MCPStore 通过多层代理对象提供一致的调用接口。常用代理与职责如下：

## Store 对象（MCPStore）
- 获取方式：`store = MCPStore.setup_store()`。
- 作用：顶层对象，提供 `for_store()` 与 `for_agent(agent_id)` 获取上下文代理。
- 典型能力：服务管理、工具/资源调用、Hub 暴露、配置查看。

## Store 代理（StoreProxy / MCPStoreContext）
- 获取方式：`store.for_store()`。
- 作用：全局视角管理服务与工具；列出/添加/更新/删除服务；健康检查；Hub 暴露。
- 示例：
```python
store_ctx = store.for_store()
store_ctx.add_service({...})
services = store_ctx.list_services()
```

## Agent 代理（AgentProxy）
- 获取方式：`store.for_agent("agentA")`。
- 作用：在指定 Agent 分组内管理服务与工具，实现隔离；方法与 StoreProxy 对齐。
- 示例：
```python
agent_ctx = store.for_agent("agentA")
agent_ctx.add_service({...})
tools = agent_ctx.list_tools()
```

## 服务代理（ServiceProxy）
- 获取方式：`store.for_store().find_service("service_name")` 或 `agent_ctx.find_service("name")`。
- 作用：操作单个服务：查看信息/状态、健康检查、更新/补丁、重启、删除、列工具。
- 示例：
```python
svc = store.for_store().find_service("weather")
info = svc.service_info()
svc.patch_config({"timeout": 30})
svc.restart_service()
```

## 工具/资源代理（通过列表返回的条目）
- 工具：`list_tools()` 返回的工具对象可直接用于调用。
- 资源：`list_resources()` / `read_resource()` 提供资源读取接口。

## 相关链接
- 构建 Store：`../store/overview.md`
- store 与 agent 的关系：`../store/overview.md#store-与-agent-的关系`
- 添加/更新/补丁服务：`add-service.md`、`update-service.md`、`patch-service.md`
- 重启/删除/列表/健康：`restart-service.md`、`delete-service.md`、`list-services.md`、`check-health.md`
- Hub 暴露：`../hub/services.md`
