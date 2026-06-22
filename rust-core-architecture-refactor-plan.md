# Rust Core Architecture Refactor Plan

## 理解复述

当前重点只放在 Rust 源码，核心范围是 `rust/crates/mcpstore`。`rust/apps/*`、Python 包和文档站点暂不作为主要重构对象，除非为了保持 API 兼容或验证行为必须触碰。

这次整理的目标不是简单移动文件，而是把 Rust core 拆成面向用户心智更清晰的领域结构：store 是门面，service 处理 MCP 服务生命周期与调用，agent 处理作用域视图，cache 只负责 mcpstore 的业务缓存语义，control/health/perspective 等能力各自独立。

cache 的边界必须重新收紧：mcpstore 不应再维护通用 KV 抽象和存储实现。KV store 的唯一真源是 `openkeyv`。本地调试和源码改动优先使用 `/Users/yuuu/work/2026_4/openkeyv`。如果 openkeyv 缺少 mcpstore 需要的能力，不在 mcpstore 里绕一层长期适配，而是优先完善 openkeyv 本身。

## 方案 A：预期目录结构

```text
rust/crates/mcpstore/src/
  lib.rs

  store/
    mod.rs              # MCPStore facade: struct, setup, composition
    options.rs          # StoreOptions, SourceMode, public construction options
    runtime.rs          # runtime config, namespace, active cache storage state

  service/
    mod.rs
    lifecycle.rs        # add/update/remove/connect/disconnect/restart
    discovery.rs        # list_tools/list_resources/list_prompts
    invocation.rs       # call_tool
    config.rs           # show_config/reset/load_from_config/get_service_config

  agent/
    mod.rs
    scope.rs            # assign/unassign/list/resolve services for agents
    view.rs             # agent-scoped service/tool/resource/prompt APIs

  cache/
    mod.rs
    layer.rs            # business cache API only
    models.rs           # cache DTOs and snapshots
    naming.rs           # collection/key naming rules
    projection.rs       # service/tool/status relation projection
    inspect.rs          # cache health, snapshot, diagnostics
    storage.rs          # thin openkeyv binding/config; no custom KV trait

  control/
    mod.rs
    request.rs          # typed control requests
    queue.rs            # pending/retry control queue
    refresh.rs          # refresh from DB/config after mutations

  health/
    mod.rs
    status.rs           # status models and transitions
    retry.rs            # retry policy and counters
    check.rs            # active health checks

  perspective/
    mod.rs
    names.rs            # perspective/source naming
    resolve.rs          # source/agent/global perspective resolution

  transport/
  registry/
  config/
  events/
  error.rs
```

## 为什么不是继续堆在 `core/`

`core` 现在承担了太多职责：store facade、agent scope、cache 管理、健康检查、控制队列、DB refresh、scoped view 都混在同一层级。它短期可运行，但长期会让用户无法判断某个 API 属于“服务管理”“agent 视图”“缓存投影”还是“运行时控制”。

方案 A 的原则是按业务语言拆分，而不是按技术细节拆分。用户理解 mcpstore 时看到的是 service、agent、cache、control、health、perspective，而不是一个越来越大的 `core/store/*`。

## Cache 重构目标

当前 cache 里仍有 mcpstore 自己的 `KvStore`、`MemoryStore`、`RedisStore`，同时又有 `OpenKeyvAdapter`、`OpenKeyvRedisStore`。目标状态是去掉 mcpstore 对通用 KV 的所有长期所有权。

保留在 mcpstore 的内容：

- 业务层 cache API：entity、relations、state、event 四类缓存。
- 命名规则：`{namespace}:entity:{type}`、`{namespace}:relations:{type}`、`{namespace}:state:{type}`、`{namespace}:event:{type}`。
- 业务模型和快照：`CacheSnapshot`、服务/工具/状态投影模型。
- 诊断能力：cache health、snapshot、inspect、migration verification。
- 从服务状态生成 cache projection 的逻辑。

迁移到 openkeyv 或直接使用 openkeyv 的内容：

- 通用 async KV trait。
- memory/redis 等 backend 实现。
- collection/key enumeration。
- batch get/put/delete。
- namespace/prefix wrapper。
- JSON object/value 序列化策略。
- TTL、连接初始化、错误类型映射的底层语义。

最终 `cache/storage.rs` 只应该负责把 mcpstore 的 `CacheStorage` 配置映射到 openkeyv 的具体 store 或 wrapper，例如 memory、redis、prefix collection。它不再定义一个新的通用 `KvStore` 世界。

## OpenKeyv 协作计划

第一步检查本地 openkeyv：`/Users/yuuu/work/2026_4/openkeyv`。重点确认它的 Rust API 是否已经稳定支持 mcpstore 需要的能力：`get`、`put`、`delete`、`get_many`、`keys`、`collections`、namespace/prefix、Redis lazy init、JSON object round-trip。

如果 openkeyv 已经具备能力，mcpstore 使用 path dependency 做本地联调：

```toml
openkeyv = { path = "/Users/yuuu/work/2026_4/openkeyv/crates/openkeyv", default-features = false, features = ["redis"] }
```

如果 openkeyv 缺少能力，优先在 openkeyv 源码补齐，而不是在 mcpstore 新建长期 shadow abstraction。补齐后先用 path dependency 验证，再决定是否发布新版本并恢复 version dependency。

## 迁移阶段

### Phase 1：冻结行为与命名边界

记录现有 public API、Python/CLI 依赖点和 cache 行为测试。保留兼容别名，避免一次性破坏用户已有调用。

验证：`cd rust && cargo check`、`cd rust && cargo test`。

### Phase 2：整理目录，不改行为

把 `core/store/*` 中已经拆出的能力迁移到方案 A 的领域目录。`MCPStore` 保持为用户入口，内部调用新的 service/agent/cache/control/health 模块。

验证：移动后测试结果必须与移动前一致。

### Phase 3：把 cache 收缩为业务层

拆分 `cache/mod.rs`：`layer.rs` 放业务 API，`models.rs` 放 DTO，`naming.rs` 放命名，`projection.rs` 放投影，`inspect.rs` 放诊断，`storage.rs` 放 openkeyv 绑定。

验证：cache 快照、服务添加/删除、agent scope、工具列表、状态刷新测试全部保持通过。

### Phase 4：替换 mcpstore 自有 KV

移除或废弃 `KvStore`、`MemoryStore`、`RedisStore` 的 mcpstore 实现。所有底层存储走 openkeyv。短期可保留 deprecated type alias，但新代码不得继续依赖这些名字。

验证：`openkeyv_memory` 和 `openkeyv_redis` 路径覆盖现有 memory/redis 行为。

### Phase 5：清理名称和兼容层

不再使用含糊名称如 `backend`、`back`、`onlydb` 描述业务概念。推荐命名：

- `backend` 用在真正后端服务时保留；cache 存储配置改为 `storage`。
- `cache_admin` 改为 `cache/inspect.rs` 或 `cache/storage.rs`，按职责拆开。
- `db_refresh` 改为 `control/refresh.rs` 或 `registry/refresh.rs`，避免暴露实现细节。
- `types.rs` 拆到 `store/options.rs`、`health/status.rs`、`control/request.rs`，避免万能类型桶。

验证：公开 API 文档和 re-export 名称清晰，旧名称仅作为兼容入口存在。

## 验收标准

- Rust 用户仍然通过 `MCPStore` 作为主入口使用库。
- 用户可理解的领域目录替代笼统 `core` 堆叠。
- mcpstore 不再拥有通用 KV store 实现；openkeyv 是唯一 KV 真源。
- cache 层只表达 mcpstore 业务语义：entity、relations、state、event、projection、inspect。
- 本地 openkeyv 联调路径可用，并能回退到正式 version dependency。
- `cd rust && cargo check` 通过。
- `cd rust && cargo test` 通过。
- Python/CLI 合同不被无意破坏；若必须迁移，单独列出 breaking change。
