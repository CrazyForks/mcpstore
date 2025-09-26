# 运行期工具变更：检测与刷新架构

本页描述运行期“工具变更自动生效”的完整链路：监控发现变化 → 触发全量刷新 → Registry 缓存更新。

## ✨ 核心思想
- 分层职责：
  - 监控层负责“何时、为什么刷新”（定时/通知/重连后）
  - 内容层负责“一次性全量刷新工具定义”
  - 缓存层只做权威存取（无定时逻辑）
- 稳健优雅：先轻量检测，再按需全量刷新，减少不必要消耗

## 🧭 架构图
```mermaid
graph TB
    subgraph 运行期组件
      LC[LifecycleManager\n健康检查/状态机]
      TM[ToolsUpdateMonitor\n通知+2h轮询]
      CM[ServiceContentManager\n全量刷新]
      RE[ServiceRegistry\n权威缓存]
      OR[MCPOrchestrator]
      FM[FastMCP]
    end

    LC --> RE
    TM -->|检测变化| CM
    CM -->|list_tools→更新tool_cache| RE

    subgraph 触发器
      R[重连成功]
      S[文件同步(mcp.json)]
      M[手动刷新]
    end

    R --> CM
    S --> OR
    OR --> CM
    M --> CM

    OR --> FM
```

## 🔁 刷新触发清单
- 初次连接/重连成功：Orchestrator._update_service_cache() → 全量写入
- 周期检测：ToolsUpdateMonitor 遍历活跃会话，发现差异后触发 ContentManager.force_update
- 兜底轮询：ServiceContentManager 定期拉取 list_tools 对比 hash，变化则全量刷新
- 手动触发：orchestrator.refresh_service_content(service_name)

## 🧩 配置要点
- tools_update_interval_seconds：统一控制 ToolsUpdateMonitor 与 ServiceContentManager 周期（后者读取 Orchestrator config 覆盖默认值）
- update_tools_on_reconnection：重连成功后是否立刻更新工具（默认 True）

更新时间：2025-08-18

