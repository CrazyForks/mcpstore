# Notes: Python API Contract and PyO3 Runtime Hardening

## Sources

### README and docs Python API contract
- Files: `README.md`, `README_en.md`, `README_zh.md`, `docs/docs/**/*.md`
- Key points:
  - `MCPStore.setup_store()` and `MCPStore.setup_store_async()` are public entrypoints.
  - `store.for_store()` and `store.for_agent(agent_id)` are central chain entrypoints.
  - README chain APIs include `add_service`, `wait_service`, `list_services`, `list_tools`, `call_tool`, `find_service`, `patch_service`, `update_service`, `delete_service`, `restart_service`, `disconnect_service`, `check_services`, `show_config`, resource APIs, prompt APIs, and adapter chains.
  - Adapter chain methods include `for_langchain`, `for_langgraph`, `for_openai`, `for_autogen`, `for_crewai`, `for_llamaindex`, and `for_semantic_kernel`.

### Current PyO3 binding
- Files: `rust/bindings/python/src/core_store.rs`, `rust/bindings/python/src/py_value.rs`
- Key points:
  - Current binding already uses native PyO3 methods, not old `*_json` string methods.
  - `add_service`, `patch_service`, and `call_tool` accept Python objects and convert them to Rust values.
  - JSON value conversion still exists through `serde_value_to_py`; the generic serialize-then-convert `to_py_object` path has been removed.
  - First direct converters were added for `ServiceEntry`, `ToolInfo`, and `ToolDescription`.

## Synthesized Findings

### Stable Contract
- Public Python API shape matters more than internal implementation.
- README/docs chain calls must continue to work after every refactor batch.
- Contract tests now protect core README API and the absence of old `*_json` methods on the Rust binding.

### PyO3 Hardening Direction
- Prefer direct PyO3 dict/list construction for high-frequency, strongly typed Rust return values.
- Keep generic conversion for paths where Rust core currently returns `serde_json::Value`.
- Convert core return types gradually. Do not force broad Rust core signature changes in the same batch unless tests require it.

### Current Verified State
- `cargo check --manifest-path rust/Cargo.toml -p mcpstore_python` passes.
- `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v` passes with 51 tests, 5 FastAPI tests skipped due to missing FastAPI.
- The previous Rust dead-code warning for `py_to_serde_object_or_empty` is gone.

### Second Direct Converter Batch
- Converted additional strongly typed binding returns to direct PyO3 dict/list construction:
  - `event_history`: `Event`
  - `call_tool`: `ToolCallResult` and `ContentItem`
  - `resolve_tool_for_agent`: `ToolResolution`
  - `wait_service_ready`: `ServiceStatus` and nested `ToolStatusItem`
- Kept generic conversion for config/cache/resource/prompt/scoped value paths where Rust core currently returns `serde_json::Value`.
- Verification after rebuilding the extension:
  - `cargo check --manifest-path rust/Cargo.toml -p mcpstore_python`
  - `uv run --with maturin maturin develop --manifest-path rust/bindings/python/Cargo.toml`
  - `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v`

### Candidate Next Batch
- No `to_py_object` usages remain in the PyO3 binding.
- Next meaningful performance work is deeper typed Rust core return shapes for resource/prompt/config/cache methods that currently model dynamic MCP payloads as `serde_json::Value`.
- Keep those deeper changes conservative because resource and prompt payload shapes are protocol-driven and more dynamic than service/tool metadata.

### Scoped Service/Tool Typed Batch
- Added typed scoped payloads in Rust core:
  - `ScopedServiceEntry` preserves service fields plus `tool_count` and optional `global_name`.
  - `ScopedToolEntry` preserves old scoped tool dict fields: `name`, `original_name`, `description`, `schema`, `input_schema`, `service_name`, `global_service_name`, `service_global_name`, and `global_tool_name`.
- Kept existing JSON-returning Rust methods (`list_services_scoped`, `list_tools_scoped`) for Rust app/server callers.
- Python binding now calls typed siblings:
  - `list_service_entries_scoped`
  - `list_tool_entries_scoped`
- Direct PyO3 converters now build scoped service/tool Python dicts without going through generic `to_py_object`.
- Verification after rebuilding the extension:
  - `cargo check --manifest-path rust/Cargo.toml -p mcpstore_python`
  - `uv run --with maturin maturin develop --manifest-path rust/bindings/python/Cargo.toml`
  - `PYTHONPATH=python/src uv run python -m unittest python.tests.test_readme_api_contract -v`
  - `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v`

### Direct serde_json::Value Conversion Batch
- Removed `to_py_object` from `core_store.rs`.
- For core methods that already return `serde_json::Value` or `Vec<serde_json::Value>`, the PyO3 binding now calls `serde_value_to_py` directly instead of serializing again through `serde_json::to_value`.
- Covered methods include event capability report, service config, agents, scoped health/status/resources/prompts, config, and cache inspection surfaces.
- No `to_py_object` usage remains after the perspective cleanup batch.
- Verification:
  - `cargo check --manifest-path rust/Cargo.toml -p mcpstore_python`
  - `uv run --with maturin maturin develop --manifest-path rust/bindings/python/Cargo.toml`
  - `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v`

### Perspective Converter Cleanup Batch
- Replaced generic `to_py_object` calls in `perspective.rs` with direct PyO3 dict converters for:
  - `AgentScopedName`
  - `ServiceResolution`
  - `ToolResolution`
- Removed the now-unused `to_py_object` helper from `py_value.rs`.
- Removed the unused `py_to_serde_object_or_empty` helper; this also removed the previous Rust dead-code warning.
- Verification:
  - `cargo check --manifest-path rust/Cargo.toml -p mcpstore_python`
  - `uv run --with maturin maturin develop --manifest-path rust/bindings/python/Cargo.toml`
  - `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v`

### Public Python MCPStore Entry Batch
- Added an explicit `MCPStore` class in `python/src/mcpstore/core/store/rust_backend.py` that subclasses `RustStoreBackend`.
- `mcpstore.core.store.MCPStore` now imports this public facade class instead of aliasing `RustStoreBackend`.
- `StoreSetupManager` now constructs `MCPStore.setup(...)`, so `MCPStore.setup_store(...)` returns the public facade type.
- `RustStoreBackend` remains available and still receives `setup_store` / `setup_store_async` for compatibility.
- Verification kept lightweight per current direction:
  - `uv run python -m py_compile python/src/mcpstore/core/store/__init__.py python/src/mcpstore/core/store/setup_manager.py python/src/mcpstore/core/store/rust_backend.py`
  - Import smoke check confirmed `MCPStore.__name__ == "MCPStore"`, `issubclass(MCPStore, RustStoreBackend)`, and both setup entrypoints are callable.
