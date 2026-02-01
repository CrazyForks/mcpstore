# 配置显示（show_config）

展示当前 Store/Agent 的配置快照，可按范围筛选（服务配置、Agent 配置、客户端映射等）。

## 概念与前置
- Store：全局配置视角，`for_store()` 返回完整配置或全局范围切片。
- Agent：逻辑分组视角，`for_agent(agent_id)` 返回该分组相关配置。
- 范围：通过 `scope` 指定返回内容，默认 `"all"`。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化 Store。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局配置 | `store.for_store().show_config(scope="all")` | dict | 同步获取配置快照 |
| Agent 配置 | `store.for_agent("agentA").show_config(scope="all")` | dict | 仅包含该 Agent 相关配置 |
| 异步形式 | `await store.for_store().show_config_async(scope="all")` | dict | 异步获取 |

## 参数说明
| 参数 | 类型 | 必填 | 说明 | 默认值 |
| ---- | ---- | ---- | ---- | ---- |
| `scope` | str | 否 | 配置范围：`"all"` / `"mcp"` / `"agent"` / `"client"` | `"all"` |

## 返回值
- 类型：dict，键取决于 `scope`，常见键：
  - `mcpServers`：服务配置
  - `agents`：Agent 配置与服务映射
  - `clients`：客户端配置

## 范围选项
| scope | 含义 | 返回内容示例 |
| ----- | ---- | ------------ |
| `"all"` | 完整配置 | `mcpServers`/`agents`/`clients` |
| `"mcp"` | 服务配置 | 仅返回 `mcpServers` |
| `"agent"` | Agent 配置 | 仅返回 `agents` |
| `"client"` | 客户端映射 | 仅返回 `clients` |

## 标准使用
```python
from mcpstore import MCPStore
import json

store = MCPStore.setup_store()

# 全量配置
cfg = store.for_store().show_config("all")
print(json.dumps(cfg, indent=2, ensure_ascii=False))

# 仅服务配置
mcp_cfg = store.for_store().show_config("mcp")
print("服务数:", len(mcp_cfg.get("mcpServers", {})))
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

agent_cfg = store.for_agent(agent_id).show_config("all")
print(agent_cfg)
```

## 相关与下一步
- 添加/更新服务：`add-service.md`、`update-service.md`、`patch-service.md`
- 删除/重启：`delete-service.md`、`restart-service.md`
- 查看服务列表：`list-services.md`
