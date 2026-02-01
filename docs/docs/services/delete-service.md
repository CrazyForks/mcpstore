# 删除服务（delete_service）

从 Store 或指定 Agent 分组中移除服务及其工具，不等待也不做清理补救操作。

## 概念与前置
- Store：全局服务仓库，`for_store()` 操作全局可见服务（参见 [服务管理概览](overview.md)）。
- Agent：逻辑分组，`for_agent(agent_id)` 仅在该分组内可见，适合隔离上下文。
- 删除行为：从配置和注册表移除指定服务，工具将不可用；不自动重连或备份。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化 Store，且目标服务已存在。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局删除 | `store.for_store().delete_service(name)` | `bool` | 同步删除指定服务 |
| Agent 删除 | `store.for_agent("agentA").delete_service(name)` | `bool` | 仅删除该 Agent 分组下的服务 |
| 异步形式 | `await store.for_store().delete_service_async(name)` | `bool` | 异步删除 |

## 参数说明
| 参数 | 类型 | 必填 | 说明 | 示例 |
| ---- | ---- | ---- | ---- | ---- |
| `name` | str | 是 | 要删除的服务名称 | `"weather"` |

## 标准使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 删除全局服务
ok = store.for_store().delete_service("weather")
print("删除结果:", ok)
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

ok = store.for_agent(agent_id).delete_service("local_calc")
print("删除结果:", ok)
```

## 返回值
- `True`：删除请求已执行。
- `False`：删除失败（如服务不存在或执行异常）。

## 相关与下一步
- 重新添加：`add-service.md`
- 查看当前服务：`list-services.md`
- 重启/等待：`restart-service.md`
