# Rust Core Architecture Refactor Plan

## 理解复述

当前阶段只聚焦 Rust 源码，主要范围是 `rust/crates/mcpstore`。`rust/apps/*`、Python 包、文档站点暂不作为重构重点，除非为了保持现有 API 合同、编译通过或测试验证必须触碰。

这次不是为了“移动文件而移动文件”，而是把 Rust core 拆成用户能直接理解的业务领域。`MCPStore` 仍然是对外主入口，但内部不再把 service、agent、cache、health、control 等能力堆在一个笼统的 `core` 里。`core` 最终只应保留兼容 re-export，真实实现进入清晰的领域目录。

cache 的边界必须收紧：mcpstore 的 cache 只做业务层缓存语义，例如 entity、relation、state、event、projection、inspect。底层 KV store 不属于 mcpstore，唯一真源是 `openkeyv`。本地联调和必要源码修改优先使用 `/Users/yuuu/work/2026_4/openkeyv`。如果 mcpstore 发现 openkeyv 缺少必要能力，优先修 openkeyv，而不是在 mcpstore 里重新造一套长期 KV 抽象。

## 方案 A：预期目录结构

```text
rust/crates/mcpstore/src/
  lib.rs

  store/
    mod.rs              # MCPStore facade: public entry, construction, composition
    options.rs          # StoreOptions, SourceMode, public construction options
    payload.rs          # public input/output payloads used by the facade
    runtime.rs          # runtime config, namespace, active cache storage state

  service/
    mod.rs
    lifecycle.rs        # add/update/remove/connect/disconnect/restart services
    discovery.rs        # list_tools/list_resources/list_prompts discovery APIs
    invocation.rs       # call_tool and service invocation behavior
    config.rs           # config loading, reset, show, service config lookup

  agent/
    mod.rs
    scope.rs            # assign/unassign/list/resolve services for agents
    view.rs             # agent-scoped service/tool/resource/prompt APIs
    content.rs          # agent-visible MCP content conversion and aggregation
    models.rs           # agent DTOs and public response models

  cache/
    mod.rs
    layer.rs            # CacheLayerManager shell and shared orchestration only
    entity.rs           # entity cache operations
    relation.rs         # relation cache operations
    state.rs            # state cache operations and change detection
    event.rs            # event append/list/delete operations
    models.rs           # cache DTOs and snapshots
    naming.rs           # collection/key naming rules
    projection.rs       # service/tool/status projection into cache records
    inspect.rs          # health, snapshot, diagnostics, migration verification
    serializer.rs       # JSON/object serialization helpers
    storage.rs          # thin openkeyv binding/config; no custom KV backend

  control/
    mod.rs
    request.rs          # typed control requests, if request models grow
    queue.rs            # pending/retry control queue
    refresh.rs          # refresh from config/registry after mutations

  health/
    mod.rs
    status.rs           # status models and transitions
    retry.rs            # retry policy and counters
    check.rs            # active health checks

  perspective/
    mod.rs
    names.rs            # perspective/source naming, if this grows
    resolve.rs          # source/agent/global perspective resolution, if this grows

  registry/
    mod.rs
    scope.rs            # registry scope rules
    service.rs          # service registry records
    tool.rs             # tool/resource/prompt registry records

  transport/
    mod.rs
    client.rs           # MCP client transport integration

  config/
  events/
  core/                 # compatibility re-export layer only
```

This is the target shape. Small modules should not be split prematurely, but large mixed-responsibility files should move toward this structure when the change improves readability without changing behavior.

## Naming Rules

Names should describe the domain, not an implementation accident.

- Use `storage` for cache persistence configuration, not vague names like `backend` unless it truly means a remote service backend.
- Use `control/refresh.rs` for mutation-triggered refresh behavior, not `db_refresh` if the behavior is not purely database-specific.
- Avoid generic buckets such as `types.rs`; prefer `store/options.rs`, `health/status.rs`, `control/request.rs`, or `cache/models.rs`.
- Avoid short but unclear names like `back`, `onlydb`, `misc`, `common`, or `manager` unless the type has a precise coordinating role.
- Keep compatibility aliases only at boundaries. New internal code should use the clearer domain names.

## Cache 重构目标

The final cache layer in mcpstore should express business behavior only:

- `entity`: cache concrete MCP/service entities by type.
- `relation`: cache graph-like relationships between services, tools, agents, and status records.
- `state`: cache derived state and detect state changes.
- `event`: record cache events needed by mcpstore behavior.
- `projection`: transform service/runtime state into cache records.
- `inspect`: expose health, snapshot, diagnostics, and migration checks.

The following must belong to openkeyv or be direct openkeyv capabilities, not mcpstore-owned abstractions:

- generic async KV traits;
- memory/redis/disk/etc. backend implementations;
- collection and key enumeration;
- batch get/put/delete behavior;
- namespace, prefix, and single-collection wrappers;
- TTL semantics and low-level connection handling;
- JSON/object round-trip details that are generic to a KV store.

`cache/storage.rs` is allowed to exist, but only as a thin adapter from mcpstore configuration to openkeyv. It should not become a second KV framework. Its responsibility is limited to constructing the correct openkeyv store/wrapper, mapping errors, and hiding openkeyv setup details from the business cache modules.

## OpenKeyv 协作方案

Local source of truth for development:

```text
/Users/yuuu/work/2026_4/openkeyv
```

Local path dependency for integration testing when needed:

```toml
openkeyv = { path = "/Users/yuuu/work/2026_4/openkeyv/crates/openkeyv", default-features = false, features = ["redis"] }
```

Before changing mcpstore cache storage, verify openkeyv supports the required Rust APIs:

- `AsyncKeyValue`: `get`, `put`, `delete`, `get_many`, `put_many`, `delete_many`.
- `AsyncEnumerateKeys`: list keys inside a collection.
- `AsyncEnumerateCollections`: list collections for diagnostics and snapshots.
- Prefix/single-collection wrappers for namespacing.
- Redis lazy initialization or a clean pattern mcpstore can wrap without leaking Redis details.
- Error types that can be mapped cleanly into `CacheError`.

If any required capability is missing or awkward, change openkeyv first, test it locally, then wire mcpstore to the improved API. The only acceptable mcpstore-side adapter is a thin boundary adapter; it must not duplicate openkeyv’s backend responsibilities.

## Migration Plan

### Phase 1：Freeze behavior and public contracts

Record current Rust public APIs, Python bridge dependencies, CLI expectations, and cache behavior tests. This gives a safety line before moving modules.

Verification:

```bash
cd rust && cargo check -p mcpstore
cd rust && cargo test
```

### Phase 2：Move from `core` to domain modules

Move implementation into `store/`, `service/`, `agent/`, `cache/`, `control/`, `health/`, and `perspective/`. Keep `MCPStore` as the stable facade. Keep `core` as compatibility re-export only while callers migrate.

Verification: moved code should pass the same tests before and after; no behavior changes are allowed in this phase.

### Phase 3：Split cache business operations

Break the business cache layer by responsibility:

- `entity.rs` for entity CRUD and agent entity helpers.
- `relation.rs` for relation put/get/delete/list.
- `state.rs` for state values and change detection.
- `event.rs` for event records.
- `layer.rs` for `CacheLayerManager` construction, namespace handling, shared snapshot/restore orchestration, and shared helpers only.

Verification: cache layer tests should cover snapshot/restore, entity operations, relation operations, state changes, event operations, and service projection.

### Phase 4：Make openkeyv the only KV source

Remove any mcpstore-owned generic KV backend implementation. Keep `CacheStorage::Memory` and `CacheStorage::Redis` only as user-facing configuration variants if needed, but internally they must construct openkeyv-backed stores.

Verification:

```bash
cd rust && cargo check -p mcpstore
cd rust && cargo test -p mcpstore
```

If using local openkeyv:

```bash
cd /Users/yuuu/work/2026_4/openkeyv && cargo test
cd /Volumes/data0/data4work/2025_6/mcpstore/rust && cargo test -p mcpstore
```

### Phase 5：Clean names and compatibility seams

After behavior is stable, clean ugly or vague names only where they directly improve the architecture. Do not rename public APIs casually. For public names, use compatibility aliases or deprecation paths.

Verification: API-facing examples still compile, and Python/CLI contracts remain unchanged unless a breaking change is explicitly documented.

## Acceptance Criteria

- `MCPStore` remains the main public Rust entrypoint.
- `core` is no longer the implementation dumping ground; it is only compatibility surface if still present.
- mcpstore cache only owns business cache semantics.
- openkeyv is the only KV store source of truth.
- Local openkeyv path can be used for development and validation.
- Large mixed files are split by user-understandable domains, not by arbitrary technical buckets.
- Vague names such as `backend`, `back`, `onlydb`, `types`, and `common` are removed or contained when they obscure intent.
- `cd rust && cargo check -p mcpstore` passes.
- `cd rust && cargo test` passes.
- Existing Python/CLI behavior is not unintentionally broken.
