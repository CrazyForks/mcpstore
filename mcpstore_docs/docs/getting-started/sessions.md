# 会话（Session）使用说明

> 简单介绍 | 常用方法 | 常见打开方式 | Store 与 Agent | LangChain 集成

## 为什么需要会话？
- 会话用于在多次工具调用之间“保持服务状态”（如浏览器页面、登录态、长连接等）。
- 无会话时，每次调用都会新建/关闭连接，导致状态丢失与性能浪费。
- 重构后，MCPStore 支持稳定、易用的会话管理，与你的「会话重构计划」完全对齐。

## 适用范围
- 适用于 Store 模式（全局）与 Agent 模式（隔离）。
- 与 LangChain/Agent 组合时，工具调用将自动复用同一会话，确保连续多步操作的连贯性。

---

## 常见打开方式（4 种）

### 1) 同步上下文管理器（推荐）
```python
store = MCPStore.setup_store()
store.for_store().add_service({"name":"browser","url":"http://127.0.0.1:8931/sse"})
store.for_store().wait_service("browser")

with store.for_store().with_session("browser_task") as s:
    s.bind_service("browser")
    s.use_tool("browser_navigate", {"url": "https://baidu.com"})
```

### 2) 异步上下文管理器
```python
async with store.for_store().with_session_async("browser_task") as s:
    await s.bind_service_async("browser")
    await s.use_tool_async("browser_navigate", {"url": "https://baidu.com"})
```

### 3) 自动会话（透明复用）
```python
store.for_store().session_auto()  # 启用自动会话
store.for_store().use_tool("browser_navigate", {"url": "https://baidu.com"})
store.for_store().use_tool("browser_screenshot", {})  # 复用同一浏览器实例
store.for_store().session_manual()  # 关闭自动会话
```

### 4) 显式 Session 对象（精确控制）
```python
session = store.for_store().create_session("langchain_browser")
session.bind_service("browser")
session.use_tool("browser_navigate", {"url": "https://baidu.com"})
session.close_session()
```

> 以上示例皆来源并对齐于《会话重构计划.md》的核心用法范式。

---

## Session 对象常用方法（两个单词命名）
- 基础属性（只读）
  - `session.session_id`
  - `session.is_active`
  - `session.service_count` / `session.tool_count`
- 信息查询
  - `session.session_info()`
  - `session.list_services()` / `session.list_tools()`
  - `session.connection_status()`
- 使用与管理
  - `session.bind_service(name)` / `bind_service_async(name)`
  - `session.use_tool(name, args)` / `use_tool_async(name, args)`
  - `session.restart_session()`
  - `session.extend_session(seconds=3600)`
  - `session.clear_cache()`
  - `session.close_session()`

---

## Store vs Agent：如何选择上下文

- Store 模式（全局共享）
```python
with store.for_store().with_session("store_browser") as s:
    s.bind_service("browser")
    s.use_tool("browser_navigate", {"url": "https://baidu.com"})
```

- Agent 模式（隔离空间）
```python
agent = store.for_agent("team_1")
with agent.with_session("team1_browser") as s:
    s.bind_service("browser")  # 仅能使用 team_1 空间中已注册的服务
    s.use_tool("browser_navigate", {"url": "https://baidu.com"})
```

> 说明：Agent 模式下服务/工具/会话完全以 `agent_id` 隔离，互不影响。

---

## 与 LangChain 集成（隐式会话路由）

- 在 `with_session(...)` 作用域内调用 `for_langchain().list_tools()`，会自动返回“绑定当前会话”的工具集合。
- 在 `session_auto()` 自动模式下，直接 `for_langchain().list_tools()` 也会使用自动会话。

示例（同步）：
```python
with store.for_store().with_session("langchain_browser"):
    tools = store.for_store().for_langchain().list_tools()  # 会话绑定
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

> 注：不需要 `for_langchain_with_session(...)`；隐式会话已在上下文中生效。

---

## 实用提示
- 建议：`add_service(...)` 后使用 `wait_service(name)` 确认服务已就绪。
- 在 `with_session` 作用域内再获取工具，确保工具已绑定当前会话。
- 并发/多任务：为不同任务使用不同 `session_id`，或分别进入独立的 `with_session` 作用域。
- 清理日志：偶发的 “Failed to close current client ...” 多为无害清理失败，后续会自动重建连接。

---

## 相关文档
- 入门 · 使用模式: `getting-started/usage-modes.md`
- 工具使用总览: `tools/overview.md`
- 服务管理总览: `services/overview.md`
- 设计来源与完整方案：项目根目录《会话重构计划.md》

