# Task Plan: Python API Contract and PyO3 Runtime Hardening

## Goal
Preserve the documented Python MCPStore API contract while moving the Python runtime surface toward high-performance PyO3-native data conversion.

## Phases
- [x] Phase 1: Protect README Python API contract with tests
- [x] Phase 2: Replace first hot-path service/tool returns with direct PyO3 converters
- [x] Phase 3: Inventory remaining PyO3 generic conversion paths
- [x] Phase 4: Convert the next safe high-traffic paths without changing Python API shape
- [x] Phase 5: Run verification and commit each large change
- [x] Phase 6: Produce final progress summary

## Key Questions
1. Which Python APIs are documented and therefore must remain stable?
2. Which Rust binding methods still return through generic `serde_json::Value` conversion?
3. Which remaining paths can be made more PyO3-native without changing public Python objects?
4. Which Python facade wrappers are product API and which are removable bridge internals?

## Decisions Made
- Preserve README/docs chain APIs as hard public contract: `setup_store`, `for_store`, `for_agent`, service/tool/resource/prompt methods, and adapter chains.
- Do not remove PyO3. The direction is to strengthen PyO3 usage and reduce generic conversion overhead.
- Commit after each large change. Completed commits:
  - `5cc00ed Protect README Python API contract`
  - `08db9aa Use direct PyO3 converters for hot paths`
  - `3485898 Strengthen PyO3 typed return converters`
  - `7146286 Add typed scoped PyO3 return paths`
  - `b3b5050 Use direct serde value PyO3 conversion`
  - `af3a6a5 Use direct PyO3 converters for perspective`
  - `74cc1a6 Update PyO3 refactor progress notes`
  - `73ebb6e Define public Python MCPStore facade`
  - `7d169bb Add typed scoped service status paths`
  - `2f551bf Add typed PyO3 report paths`
  - `ba1a09f Add typed PyO3 config path`
- Public Python entry should be `MCPStore`; `RustStoreBackend` remains available as a compatibility/internal name, not the preferred public API identity.
- Scoped service/tool list bindings must preserve old Python dict shape, including agent-localized service names and scoped tool fields such as `original_name`, `service_name`, and `global_service_name`.
- `core_store.rs` should use `serde_value_to_py` directly when the Rust core already returns `serde_json::Value`; `to_py_object` is only needed for typed structs that still rely on generic serialization.
- Perspective binding now has direct PyO3 converters; the generic `to_py_object` helper and unused object-or-empty helper were removed.
- Scoped service health/status reads should use typed Rust core siblings for the PyO3 path while preserving existing JSON-returning Rust methods for other callers.
- Fixed-shape reports such as event capability and cache health should expose typed Rust core siblings for PyO3, with JSON wrappers retained for Rust callers.
- `show_config` should use a typed `McpConfig` core sibling for PyO3; keep single-service config dynamic to avoid dropping user-defined fields.
- Keep unrelated untracked report file out of implementation commits.

## Errors Encountered
- `uv run pytest` failed because `pytest` was not installed; used `python -m unittest` for current Python verification.
- Direct conversion for scoped service/tool lists could not be applied immediately because Rust core returns `serde_json::Value` for those methods, not `ServiceEntry` / `ToolDescription`.
- `cargo fmt` and `maturin develop` from the repository root failed because the Rust workspace/binding manifests are under `rust/`; use `cargo fmt --manifest-path rust/Cargo.toml --all` and `uv run --with maturin maturin develop --manifest-path rust/bindings/python/Cargo.toml`.
- Follow-up quick_start verification exposed two Python contract gaps in the PyO3 typed path: service records were missing `client_id`, and successful tool call results were missing `data`. Both fields are public/example-facing and should be emitted at the PyO3/facade boundary rather than faked globally in `RustRecordView`.

## Follow-up Fixes
- Restored `client_id` on service and scoped tool payloads, derived from the Rust service global name to match current cache relation semantics.
- Restored successful tool call `data` as `None`, so historical `if tool_result.data:` access remains valid without inventing structured data.
- Verified the local quick_start example completes end to end against `http://127.0.0.1:21923/mcp`.

## Status
**Complete** - Public Python API shape is preserved, the public Python entry is `MCPStore`, and fixed-shape PyO3 reads now use typed/direct conversion paths. Remaining `serde_json::Value` use is limited to dynamic MCP/user payloads where typed conversion would risk dropping fields.
