# 示例：find_service 与服务代理

## Store 上下文

```python
from mcpstore import MCPStore
store = MCPStore.setup_store()

# 注册演示服务
store.for_store().add_service({
  "mcpServers": {"mcpstore-demo-weather": {"url": "https://mcpstore.wiki/mcp"}}
})
store.for_store().wait_service("mcpstore-demo-weather")

svc = store.for_store().find_service("mcpstore-demo-weather")
print(svc.service_info())
print(svc.list_tools())
print(svc.tools_stats())
print(svc.check_health())
print(svc.health_details())
```

## Agent 上下文

```python
store = MCPStore.setup_store()
agent_id = "agent_demo"

store.for_agent(agent_id).add_service({
  "mcpServers": {"mcpstore-demo-weather": {"url": "https://mcpstore.wiki/mcp"}}
})
store.for_agent(agent_id).wait_service("mcpstore-demo-weather")

svc = store.for_agent(agent_id).find_service("mcpstore-demo-weather")
print(svc.service_status())
print(svc.update_config({"url": "https://mcpstore.wiki/mcp", "keep_alive": True}))
print(svc.patch_config({"working_dir": "."}))
print(svc.refresh_content())
print(svc.remove_service())
print(svc.delete_service())
```

