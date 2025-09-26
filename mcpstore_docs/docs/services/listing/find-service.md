# find_service()

> 作用：根据服务名返回一个“服务代理对象 ServiceProxy”，后续所有针对该服务的操作都在该代理上以“两词法”方法调用。

- 所属类：MCPStoreContext（store.for_store() / store.for_agent(agent_id) 返回的上下文）
- 定义位置：src/mcpstore/core/context/base_context.py
- 返回类型：ServiceProxy（src/mcpstore/core/context/service_proxy.py）

## 基本用法

- Store 上下文：
```python
from mcpstore import MCPStore
store = MCPStore.setup_store()
svc = store.for_store().find_service("mcpstore-demo-weather")
print(svc.service_info())
```

- Agent 上下文：
```python
store = MCPStore.setup_store()
svc = store.for_agent("agent_demo").find_service("mcpstore-demo-weather")
print(svc.service_status())
```

## 返回对象：ServiceProxy

ServiceProxy 将该服务的所有操作聚合到一个对象中（无需重复传服务名）。主要能力：
- 信息与状态：service_info、service_status、check_health、health_details、is_healthy、is_connected
- 工具：list_tools、tools_stats
- 管理：update_config、patch_config、restart_service、refresh_content、remove_service、delete_service
- 便捷属性：name、context_type、tools_count

详细说明见“服务代理（ServiceProxy）”章节。

