# 补丁更新服务（patch_service）

以增量方式更新指定服务配置，仅修改提供的字段，不会清空未传字段。

## 概念与前置
- Store：全局视角，`for_store()` 更新全局服务。
- Agent：分组视角，`for_agent(agent_id)` 仅更新该分组服务。
- 适用场景：小范围调整（如 headers、timeout、env），避免全量覆盖风险。
- 必须前置：已通过 `MCPStore.setup_store()` 初始化，目标服务已存在。

## 主要方法
| 场景 | 标准用法 | 返回值 | 说明 |
| ---- | -------- | ------ | ---- |
| 全局补丁 | `store.for_store().patch_service(name, patch)` | `bool` | 同步增量更新 |
| Agent 补丁 | `store.for_agent("agentA").patch_service(name, patch)` | `bool` | 仅作用于指定 Agent 分组 |
| 异步形式 | `await store.for_store().patch_service_async(name, patch)` | `bool` | 异步增量更新 |

## 参数说明
| 参数 | 类型 | 必填 | 说明 | 示例 |
| ---- | ---- | ---- | ---- | ---- |
| `name` | str | 是 | 服务名称 | `"weather"` |
| `patch` | dict / str | 是 | 需修改的字段；字符串需为 JSON | `{"headers": {"Authorization": "Bearer xxx"}}` |

字符串配置会先在 Python SDK 中解析为 dict，再通过 PyO3 传入 Rust core。

## 标准使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

patch = {
    "headers": {"Authorization": "Bearer new-token"},
    "timeout": 45
}
ok = store.for_store().patch_service("weather", patch)
print("补丁更新结果:", ok)
```

### for_agent 模式使用
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()
agent_id = "agentA"

ok = store.for_agent(agent_id).patch_service("local_calc", {"env": {"MODE": "test"}})
print("补丁更新结果:", ok)
```

## 返回值
- `True`：补丁应用成功。
- `False`：更新失败（如服务不存在或执行异常）。

## 相关与下一步
- 全量更新：`update-service.md`
- 重启或等待：`restart-service.md`、`wait-service.md`
- 查看配置：`show-config.md`
