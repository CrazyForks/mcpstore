# 架构：ServiceProxy 与上下文

## 位置与关系

- MCPStoreContext（store/agent）
  - find_service(name) → 返回 ServiceProxy
- ServiceProxy（服务作用域）
  - 封装“服务详情、健康、工具、配置、运行态”的两词法方法
  - 通过 context.sync_helper 同步封装 orchestrator 的异步能力
- Orchestrator
  - service_management：状态缓存、状态查询、连接/断连、刷新等
  - health_monitoring：详细健康检查、状态桥映射（health → lifecycle）
- Registry（缓存）
  - 工具缓存、服务状态、元数据（包含 service_config）
  - agent_to_global_mappings / global_to_agent_mappings：Agent 透明代理映射

## 关键流程

- find_service → ServiceProxy
  - ServiceProxy 内部保留 service_name、context_type、agent_id
- health_details
  - Agent：本地名 → 全局名（service_mapper）→ orchestrator.check_service_health_detailed → HealthStatusBridge 映射 → 结构化字典返回
- list_tools/tools_stats
  - 优先 Registry 按服务直接获取；Agent 视图下进行本地名转换
- update_config/patch_config
  - 写入 mcp.json（单一数据源）→ orchestrator.sync_manager 同步 → registry.metadata.service_config 更新

## 设计要点

- 两词法命名：统一 SDK 风格，便于记忆与检索
- 作用域收敛：避免在各处重复传 service_name，减少歧义
- 分层清晰：API 只负责 HTTP/路由；SDK（Store/Context/Orchestrator/Registry）承载业务逻辑
- 一致性：工具详情字段统一（name/display_name/original_name/description/inputSchema/service_name/client_id）
- 健康状态：health → lifecycle 的桥接，HEALTHY/WARNING 视为 positive 状态

