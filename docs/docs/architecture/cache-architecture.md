# 缓存空间

MCPStore 的缓存基于 `py-key-value`（Memory/Redis 可切换），采用三层分离（实体/关系/状态）+ Collection 隔离。本文聚焦“能用、好查、好排障”的关键信息。

## 目标
- 了解缓存分层与命名，便于查找/清理。
- 明白 Agent 视角与 Store 视角的命名转换。
- 知道常用 Collection/Key 结构，方便排障与观测。

## 总览
- 底层：`py-key-value`，可切换 Memory 或 Redis。
- 分层：实体层（Entity）、关系层（Relations）、状态层（State）。
- 命名：命名空间 `mcpstore` + Collection + key，支持多租户/隔离。

## 三层模型
| 层级 | 存什么 | Collection 示例 |
| ---- | ------ | ---------------- |
| 实体层 | 服务/工具/Agent/Store/客户端的真理源 | `mcpstore:entity:services`、`mcpstore:entity:tools`、`mcpstore:entity:agents` |
| 关系层 | Agent-服务映射、服务-工具映射 | `mcpstore:relations:agent_services`、`mcpstore:relations:service_tools` |
| 状态层 | 连接状态、元数据（健康/统计） | `mcpstore:state:service_status`、`mcpstore:state:service_metadata` |

## 命名规则（Agent/Store 视角）
- Agent 视角名称：服务/工具的原始名（如 `weather`）。
- Store 视角全局名：`{original}_byagent_{agent_id}`。全局 Agent（`global_agent_store`）不加后缀。
- 典型 key：`mcpstore:entity:services:weather_byagent_agentA`。

## 常用 Collection 与 Key 例子
| Collection | Key 示例 | 说明 |
| ---------- | -------- | ---- |
| `mcpstore:entity:services` | `weather_byagent_agentA` | 服务配置与元数据 |
| `mcpstore:entity:tools` | `weather_byagent_agentA_search` | 工具定义与 Schema |
| `mcpstore:entity:agents` | `agentA` | Agent 基础信息 |
| `mcpstore:entity:store` | `mcpstore` | Store 配置 |
| `mcpstore:entity:clients` | `client_agentA_weather_001` | 客户端连接信息 |
| `mcpstore:relations:agent_services` | `agentA` | 该 Agent 拥有的服务列表 |
| `mcpstore:relations:service_tools` | `weather_byagent_agentA` | 服务下的工具列表 |
| `mcpstore:state:service_status` | `weather_byagent_agentA` | 连接/健康状态 |
| `mcpstore:state:service_metadata` | `weather_byagent_agentA` | 统计与元数据 |

## 值存储约定
- 字典直接存：`{"service_name": "...", ...}`。
- 标量需包装：`{"value": ...}`。

## 快速排障/观测指引
- 查看某 Agent 拥有哪些服务：查 `relations:agent_services` 的 key=`agentId`。
- 查看服务工具列表：查 `relations:service_tools` 的 key=`service_global_name`。
- 查看健康/状态：查 `state:service_status` / `state:service_metadata`。
- 全局服务名生成：`原始名 + _byagent_ + agent_id`（全局 Agent 直接用原名）。

## 切换后端
- 内存：默认。
- Redis：通过 `setup_store(cache=...)` 切换，保持相同命名规范。

## 相关文档
- 构建 Store：`../store/overview.md`
- 代理对象：`../services/service-proxy.md`
- 服务管理：`../services/overview.md`
