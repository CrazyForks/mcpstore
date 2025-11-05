## Session - 会话


会话用于在多次工具调用之间保持服务状态（如浏览器页面、登录态、长连接等），避免每次调用新建/关闭连接带来的状态丢失与性能浪费。MCPStore 提供稳定、易用的会话管理，适用于 Store 与 Agent 两种上下文。

### SDK

同步：
  - `for_store().with_session(session_id) -> Session(cm)`
  - `for_agent(id).with_session(session_id) -> Session(cm)`
  - `for_store().create_session(session_id) -> Session`
  - `for_store().session_auto() / session_manual()`

异步：
  - `await for_store().with_session_async(session_id) -> Session(cm)`
  - `await for_agent(id).with_session_async(session_id) -> Session(cm)`
  - `await session.bind_service_async(name)` / `await session.use_tool_async(name, args)`

### 参数

| 参数名        | 类型 | 说明 |
|---------------|------|------|
| `session_id`  | str  | 会话标识；用于关联与复用同一次会话上下文。 |
| `name`        | str  | 服务或工具名称；用于绑定或调用时指定目标。 |
| `seconds`     | int  | `extend_session(seconds)` 的扩展秒数。 |

### 返回值

- `with_session(...)`：返回可用作上下文管理器的 `Session` 对象。
- `create_session(...)`：返回 `Session` 对象（手动管理生命周期）。


### 视角
通过 `for_store()` 在全局空间下创建与使用会话；通过 `for_agent(id)` 在隔离的 Agent 空间内创建与使用会话（服务/工具/会话按 `agent_id` 隔离，互不影响）。


### 常见打开方式

同步上下文管理器（推荐）：
```python
store = MCPStore.setup_store()
store.for_store().add_service({"name":"browser","url":"http://127.0.0.1:8931/sse"})
store.for_store().wait_service("browser")

with store.for_store().with_session("browser_task") as s:
    s.bind_service("browser")
    s.use_tool("browser_navigate", {"url": "https://baidu.com"})
```

异步上下文管理器：
```python
async with store.for_store().with_session_async("browser_task") as s:
    await s.bind_service_async("browser")
    await s.use_tool_async("browser_navigate", {"url": "https://baidu.com"})
```

自动会话（透明复用）：
```python
store.for_store().session_auto()
store.for_store().use_tool("browser_navigate", {"url": "https://baidu.com"})
store.for_store().use_tool("browser_screenshot", {})
store.for_store().session_manual()
```

显式 Session 对象（精确控制）：
```python
session = store.for_store().create_session("langchain_browser")
session.bind_service("browser")
session.use_tool("browser_navigate", {"url": "https://baidu.com"})
session.close_session()
```


### Session 常用方法

- 基础属性：`session.session_id`、`session.is_active`、`session.service_count`、`session.tool_count`
- 信息查询：`session.session_info()`、`session.list_services()`、`session.list_tools()`、`session.connection_status()`
- 使用与管理：`session.bind_service(name)`、`session.use_tool(name, args)`、`session.restart_session()`、`session.extend_session(seconds=3600)`、`session.clear_cache()`、`session.close_session()`


### Store 与 Agent 上下文

Store 模式（全局共享）：
```python
with store.for_store().with_session("store_browser") as s:
    s.bind_service("browser")
    s.use_tool("browser_navigate", {"url": "https://baidu.com"})
```

Agent 模式（隔离空间）：
```python
agent = store.for_agent("team_1")
with agent.with_session("team1_browser") as s:
    s.bind_service("browser")
    s.use_tool("browser_navigate", {"url": "https://baidu.com"})
```


### 与 LangChain 集成（隐式会话路由）

- 在 `with_session(...)` 作用域内调用 `for_langchain().list_tools()`，会自动返回绑定当前会话的工具集合。
- 在 `session_auto()` 模式下，直接 `for_langchain().list_tools()` 也会走自动会话。

示例（同步）：
```python
with store.for_store().with_session("langchain_browser"):
    tools = store.for_store().for_langchain().list_tools()
    agent = create_tool_calling_agent(llm, tools, prompt)
    AgentExecutor(agent=agent, tools=tools).invoke({"input": "打开百度并截图"})
```

示例（自动会话）：
```python
store.for_store().session_auto()
tools = store.for_store().for_langchain().list_tools()
agent = create_tool_calling_agent(llm, tools, prompt)
AgentExecutor(agent=agent, tools=tools).invoke({"input": "打开百度并截图"})
```


### 使用场景

- 需要跨多次调用保留服务运行态（浏览器页面、登录态、连接等）。
- 长事务或多步操作串联调用的连贯性保证。
- Agent 场景中将不同任务隔离在不同会话内并行执行。


### 实用提示

- 在 `add_service(...)` 后使用 `wait_service(name)` 确认服务已就绪。
- 在 `with_session` 作用域内再获取工具，确保工具绑定当前会话。
- 并发与多任务：为不同任务使用不同 `session_id`，或分别进入独立的 `with_session` 作用域。
- 清理日志：偶发的 “Failed to close current client ...” 多为无害清理失败，连接会自动重建。


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 开启自动会话     | `for_store().session_auto()` |
| 关闭自动会话     | `for_store().session_manual()` |
| 创建会话对象     | `for_store().create_session(session_id)` |
| 会话内列工具     | `for_store().for_langchain().list_tools()` |
| 绑定服务         | `session.bind_service(name)` |
| 使用工具         | `session.use_tool(name, args)` |


### 相关文档

- 入门 · 使用模式: `getting-started/usage-modes.md`
- 工具使用总览: `tools/overview.md`
- 服务管理总览: `services/overview.md`
- 设计来源与完整方案：项目根目录《会话重构计划.md`

