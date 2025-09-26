# 持久化架构（单源配置）

本页更新持久化说明，反映最新“单源 mcp.json + 内存缓存”的实现。

## 📦 配置持久化
- 单源文件：mcp.json（由 MCPConfig 读写）
- 结构：
  - mcpServers: { serviceName: { transport, ... } }
  - 其他扩展字段：监控策略等
- 写入时机：add_service/update/delete 等管理操作

## 🗂️ 不再存在的持久化
- client_services.json（已删除）
- agent_clients.json（已删除）
- schemas/ 目录与 SchemaManager（已删除）

## 🔄 启动与重建
- 启动读取 mcp.json，注册服务 → 连接 → 拉取工具 → 填充缓存
- 任何时刻都以 mcp.json 为最终真实来源（Single Source of Truth）

## 🧯 异常与回退
- 不再回退到分片文件
- 连接失败与重连：交由生命周期管理器（状态 RECONNECTING/HEALTHY 等）

## 📘 与 API/SDK 的一致性
- SDK 与 API 返回值结构以缓存视图为准
- 所有查询接口均与 FastMCP 协议保持一致的工具/服务结构

更新时间：2025-08-18

