# API 文档

按领域归类的接口总览，结合《接口文档-*》系列整理。详细字段与示例请参考对应专题。

## Store 管理
- 配置查看：`GET /for_store/show_config`、`GET /for_store/show_mcpjson`、`GET /for_store/setup_config`
- 配置变更：`PUT /for_store/update_config/{id}`、`DELETE /for_store/delete_config/{id}`、`POST /for_store/reset_config`
- 同步状态：`GET /for_store/sync_status`
- Agent 汇总：`GET /for_store/list_agents`
- 工具记录：`GET /for_store/tool_records`
- 参考：`接口文档-store管理v1.md`

## Agent 管理
- Agent 列表与信息：`GET /for_store/list_agents`
- Agent 视角服务/工具：`/for_agent/{agent_id}/...` 与 Store 端对应接口一致
- 参考：`接口文档-Agent管理v1.md`

## 服务相关
- 添加/更新/补丁/删除：`add_service`、`update_service`、`patch_service`、`delete_service`（对应 HTTP PUT/POST/DELETE 路径）
- 列表/状态/详情：`list_services`、`service_status`、`service_info`
- 健康/等待：`check_services`、`wait_service`
- 重启/断开：`restart_service`、`disconnect_service`
- 参考：`接口文档-服务相关v1.md`

## 工具相关
- 列表/查询：`list_tools`
- 调用：`call_tool`
- 记录：`tool_records`
- 参考：`接口文档-工具相关v1.md`

## 缓存只读
- 只读查询接口：见 `接口文档-缓存只读v1.md`

## 其他接口
- 见 `接口文档-其他接口v1.md`
