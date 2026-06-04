# Task Plan: MCPStore Daemon Mode (Unix Socket IPC)

## Goal
Add a daemon mode to mcpstore CLI: `mcpstore start` launches a long-running process that holds a singleton `MCPStore`, and all subsequent CLI commands (`add`, `list`, `call`, `remove`, `connect`, etc.) communicate with it via Unix Domain Socket instead of creating their own instance.

## Phases
- [ ] Phase 1: Plan and setup
- [ ] Phase 2: Implement daemon core (start/stop, UDS listener, JSON protocol)
- [ ] Phase 3: Implement CLI client (all commands route through UDS)
- [ ] Phase 4: Add `api` attach-to-daemon support
- [ ] Phase 5: Integration test against local MCP service at 21923/mcp
- [ ] Phase 6: Review and deliver

## Key Questions
1. Where should the Unix socket live? (`/tmp/mcpstore.sock` or configurable)
2. Where should the PID file live? (`/tmp/mcpstore.pid` or configurable)
3. Should `api` attach to daemon or remain independent?
4. How to handle daemon crashes / stale socket files?

## Decisions Made
- Use Unix Domain Socket for IPC (fast, local-only, no network stack)
- Use simple JSON line protocol (request/response, newline-delimited)
- Socket path: `/tmp/mcpstore.sock`
- PID file: `/tmp/mcpstore.pid`
- `api` command will attach to running daemon when possible
- All existing `mcp` subcommands will prefer daemon mode if available

## Errors Encountered
- (none yet)

## Status
**Currently in Phase 1** - Creating plan and analyzing existing code
