# Task Plan: Python API Contract and PyO3 Runtime Hardening

## Goal
Preserve the documented Python MCPStore API contract while moving the Python runtime surface toward high-performance PyO3-native data conversion.

## Phases
- [x] Phase 1: Protect README Python API contract with tests
- [x] Phase 2: Replace first hot-path service/tool returns with direct PyO3 converters
- [x] Phase 3: Inventory remaining PyO3 generic conversion paths
- [x] Phase 4: Convert the next safe high-traffic paths without changing Python API shape
- [x] Phase 5: Run verification and commit each large change
- [ ] Phase 6: Produce final progress summary

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
- Scoped service/tool list bindings must preserve old Python dict shape, including agent-localized service names and scoped tool fields such as `original_name`, `service_name`, and `global_service_name`.
- `core_store.rs` should use `serde_value_to_py` directly when the Rust core already returns `serde_json::Value`; `to_py_object` is only needed for typed structs that still rely on generic serialization.
- Keep unrelated untracked report file out of implementation commits.

## Errors Encountered
- `uv run pytest` failed because `pytest` was not installed; used `python -m unittest` for current Python verification.
- Direct conversion for scoped service/tool lists could not be applied immediately because Rust core returns `serde_json::Value` for those methods, not `ServiceEntry` / `ToolDescription`.
- `cargo fmt` and `maturin develop` from the repository root failed because the Rust workspace/binding manifests are under `rust/`; use `cargo fmt --manifest-path rust/Cargo.toml --all` and `uv run --with maturin maturin develop --manifest-path rust/bindings/python/Cargo.toml`.

## Status
**Currently after Phase 5** - `core_store.rs` no longer uses `to_py_object`; next step is either typing the remaining perspective binding conversions or cleaning the unused `py_to_serde_object_or_empty` helper.
