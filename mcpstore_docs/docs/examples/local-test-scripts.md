# 本地测试脚本索引（src 目录）

> 以下脚本均位于仓库根目录的 `src/` 下，风格参考 `测试_简单工具使用.py`，可单独运行，便于团队快速验证单个功能。
>
> 运行示例（Windows，UTF-8）：
>
> ```bash
> python -X utf8 src/测试_服务_服务详情.py
> ```

## 基础示例

- 测试_简单工具使用.py
  - 最小化演示：注册服务 → 等待 → 列表/调用 → 重置

## Store 场景（for_store）

- 测试_服务_服务详情.py
  - 通过 find_service 获取 ServiceProxy，打印 service_info()
- 测试_服务_服务状态.py
  - service_status() / check_health() / health_details()
- 测试_服务_工具列表与统计.py
  - list_tools() / tools_stats()
- 测试_服务_配置更新.py
  - update_config() 全量更新 / patch_config() 增量更新
- 测试_服务_重启与刷新.py
  - restart_service() / refresh_content()
- 测试_服务_移除与删除.py
  - remove_service()（运行态）/ delete_service()（配置+缓存）
- 测试_服务_服务状态_单测.py
  - 仅演示 service_status()
- 测试_服务_健康摘要.py
  - 仅演示 check_health()

## Agent 场景（for_agent）

- 测试_agent_服务详情.py
  - Agent 上下文下的 service_info()
- 测试_agent_服务状态与健康.py
  - service_status() / check_health() / health_details()
- 测试_agent_工具列表与统计.py
  - list_tools() / tools_stats()（自动进行本地名↔全局名映射）
- 测试_agent_配置更新.py
  - update_config() / patch_config()（单一数据源 mcp.json 写入 + 同步 + 缓存更新）
- 测试_agent_重启刷新移除删除.py
  - restart_service() / refresh_content() / remove_service() / delete_service()
- 测试_agent_工具调用_use_call.py
  - call_tool() / use_tool() 的 4 种名称格式（直接名、service__tool、新旧前缀）

## 注意事项

- 所有脚本末尾均调用 `reset_config()` 清理环境；如需保留配置，可临时注释该行
- 示例服务统一使用 `mcpstore-demo-weather`（https://mcpstore.wiki/mcp）
- 若网络受限，可替换为本地 MCP 服务命令配置（command + args）

