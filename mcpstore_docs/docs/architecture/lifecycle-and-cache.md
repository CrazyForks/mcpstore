# 生命周期与缓存总览

该页给出压缩版总览图，帮助阅读者快速掌握“单源配置 + 内存缓存 + 7 状态生命周期”的交互关系。

```mermaid
graph TB
    subgraph 配置/持久化
      C[mcp.json]
    end

    subgraph 运行期
      SO[ServiceOperations]
      OR[MCPOrchestrator]
      RE[ServiceRegistry\n(内存缓存)]
      LC[LifecycleManager]
      TM[ToolsUpdateMonitor]
      CM[ServiceContentManager]
      FM[FastMCP]
    end

    U[用户/API/SDK] --> SO
    SO --> C
    SO --> OR
    OR --> FM
    FM --> RE
    LC --> RE

    subgraph 查询
      Q1[list_services]
      Q2[list_tools]
      Q3[get_service_status]
    end

    Q1 --> RE
    Q2 --> RE
    Q3 --> RE

    subgraph 监控
      H[30s 健康检查\nLifecycle]
      T[2h 工具变化检测\nToolsUpdateMonitor]
      B[兜底内容刷新\nContentManager]
    end

    H --> LC
    T --> CM
    B --> RE

    style RE fill:#f1f8e9
    style LC fill:#fff3e0
    style OR fill:#e8eaf6
```

要点：
- 所有列表/查询均从注册表缓存返回
- 注册/更新写回 mcp.json，同时触发编排 + 生命周期刷新缓存
- 单源模式：默认不使用分片文件；内置 `mcp.json.bak` 自动备份与损坏修复

更新时间：2025-08-18

