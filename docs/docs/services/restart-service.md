# 重启服务（restart_service）

对已注册服务执行重启（重新拉起远程连接或本地进程），不自动等待恢复，需要配合等待/健康检查使用。

## 概念与前置
- Store：全局服务仓库，`for_store()` 操作全局可见的服务。
- Agent：逻辑分组，`for_agent(agent_id)` 仅作用于该分组内的服务。
- 重启行为：触发服务重连/重启命令，但不等待就绪；等待请调用 `wait_service`。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化 Store，目标服务已存在。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局重启 | `store.for_store().restart_service(name)` | `bool` | 同步重启指定服务 |
| Agent 重启 | `store.for_agent("agentA").restart_service(name)` | `bool` | 仅重启该 Agent 分组下的服务 |
| 异步形式 | `await store.for_store().restart_service_async(name)` | `bool` | 异步重启 |

## 参数说明
| 参数 | 类型 | 必填 | 说明 | 示例 |
| ---- | ---- | ---- | ---- | ---- |
| `name` | str | 是 | 要重启的服务名称 | `"weather"` |

## 标准使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 重启服务
ok = store.for_store().restart_service("weather")
print("重启结果:", ok)

# 如需等待恢复
store.for_store().wait_service("weather", status="healthy", timeout=60)
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

ok = store.for_agent(agent_id).restart_service("local_calc")
print("重启结果:", ok)

# 可选等待
store.for_agent(agent_id).wait_service("local_calc", status="healthy", timeout=60)
```

## 返回值
- `True`：重启请求已执行（不代表已恢复）。
- `False`：重启失败（服务不存在或执行异常）。

## 相关与下一步
- 等待服务就绪：`wait-service.md`
- 查看状态/健康：`check-health.md`
- 更新配置：`update-service.md`
