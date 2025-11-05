# 服务代理（ServiceProxy）

> 通过 `find_service(name)` 获得的对象，封装了“该服务”相关的全部操作，方法命名采用两词法。

- 实现位置：src/mcpstore/core/context/service_proxy.py
- 设计目标：
  - 缩小作用域：所有操作都绑定在一个具体服务上
  - 命名统一：方法采用“两词法”，与 SDK 其他接口风格一致
  - 兼容 agent/store 两种上下文，透明处理服务名映射（Agent 本地名 ↔ 全局名）

## 核心方法与属性

- 信息与状态
  - service_info() → 返回服务详情（ServiceInfo + 工具清单）
  - service_status() → 返回缓存状态快照（status、healthy、last_check、response_time 等）
  - check_health() → 返回健康摘要（service_name、status、healthy、response_time、error_message）
  - health_details() → 返回健康详情（effective_name、lifecycle_state、response_time、timestamp、error_message、details）
  - is_healthy() → bool
  - is_connected → bool（属性，带回退判断）

- 工具
  - list_tools() → List[ToolInfo]（优先 Registry 按服务获取，失败回退全量过滤）
  - tools_stats() → Dict（仅当前服务的工具统计 + 清单）

- 配置与运行态管理
  - update_config(config) → bool（单一数据源 mcp.json 写入 + 同步 + 缓存更新）
  - patch_config(updates) → bool（增量更新）
  - restart_service() → bool
  - refresh_content() → bool（同步封装 await）
  - remove_service() → bool（运行态移除/断连）
  - delete_service() → bool（配置+缓存删除）

- 便捷属性
  - name：服务名
  - context_type：上下文类型（store/agent）
  - tools_count：工具数量

## 返回结构与字段说明

- ServiceInfo（主要字段）
  - name、url、transport_type、status（7 状态）、tool_count、keep_alive、working_dir、env、command、args、package_name
  - state_metadata（consecutive_failures、last_ping_time、error_message、service_config 等）
  - last_state_change、client_id、config

- 工具详情（工具列表元素字段）
  - name（显示名）、display_name（友好展示名）、original_name（FastMCP 原始名）、description
  - inputSchema（JSON Schema）、service_name、client_id

## Agent 上下文的透明映射

- find_service 返回的 ServiceProxy 在 Agent 上下文会自动处理“本地名 ↔ 全局名”映射：
  - health_details 会对 effective_name 使用全局名
  - list_tools/tools_stats 会在内部以全局名查工具后转换为本地名展示

## 示例

```python
from mcpstore import MCPStore
store = MCPStore.setup_store()

# Store
svc = store.for_store().find_service("mcpstore-demo-weather")
print(svc.service_info())
print(svc.tools_stats())
print(svc.check_health())

# Agent
svc2 = store.for_agent("agent_demo").find_service("mcpstore-demo-weather")
print(svc2.service_status())
print(svc2.health_details())
```

