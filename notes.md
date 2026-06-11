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
  - Generic conversion still exists through `to_py_object` and `serde_value_to_py`.
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
- `cargo check -p mcpstore_python` passes.
- `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v` passes with 51 tests, 5 FastAPI tests skipped due to missing FastAPI.
- One existing Rust warning remains: `py_to_serde_object_or_empty` is unused.

### Second Direct Converter Batch
- Converted additional strongly typed binding returns to direct PyO3 dict/list construction:
  - `event_history`: `Event`
  - `call_tool`: `ToolCallResult` and `ContentItem`
  - `resolve_tool_for_agent`: `ToolResolution`
  - `wait_service_ready`: `ServiceStatus` and nested `ToolStatusItem`
- Kept generic conversion for config/cache/resource/prompt/scoped value paths where Rust core currently returns `serde_json::Value`.
- Verification after rebuilding the extension:
  - `cargo check -p mcpstore_python`
  - `uv run --with maturin maturin develop`
  - `PYTHONPATH=python/src uv run python -m unittest discover -s python/tests -v`

### Candidate Next Batch
- Inspect remaining `to_py_object` uses in `core_store.rs`.
- Prioritize methods with typed Rust return values.
- Avoid changing scoped methods until Rust core typed return shapes are clarified.
