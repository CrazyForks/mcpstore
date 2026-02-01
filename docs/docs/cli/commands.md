# CLI 使用指南

基于 `技术文档-cli使用v1.md` 精简整理，涵盖常用命令、作用域与传参规则。

## 总体说明
- 全局命令：`version`、`run`/`serve`、`config ...`、`add`/`list`/`get`/`remove`。
- 作用域切换：`--for-agent <agent_id>` 作用于指定 Agent，缺省为 Store 作用域。
- 环境与认证：`--env KEY=VAL` 可重复；stdio 写入 env，http/sse 写入 headers（保留 JSON 中原有 env/headers）。
- 传输推断：未显式 `--transport` 时，JSON 有 `command`→stdio，有 `url`→http；非 JSON 且带 `--` 视为 stdio，URL 形态默认 http；SSE 请显式 `--transport sse`。

## 版本
| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `mcpstore version` | 输出包内版本号 | `mcpstore version` |

## API 启动（run/serve）
| 命令 | 选项 | 说明 | 示例 |
| --- | --- | --- | --- |
| `mcpstore run api` | `--host` `--port` `--reload` `--log-level` `--prefix` | 启动 API 服务；reload 模式下不支持 prefix（有 prefix 会直接退出提示） | `mcpstore run api --host 127.0.0.1 --port 18200 --prefix /api` |
| `mcpstore serve` | 同上 | `run api` 的别名 | `mcpstore serve --port 19000` |

## 配置管理（config）
| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `mcpstore config show` | 显示配置 | `mcpstore config show --path ./mcp.json` |
| `mcpstore config validate` | 校验配置 | `mcpstore config validate` |
| `mcpstore config init` | 初始化配置，支持 `--force` `--with-examples` | `mcpstore config init --with-examples` |
| `mcpstore config add-examples` | 向现有配置追加示例 | `mcpstore config add-examples` |
| `mcpstore config path` | 显示默认配置路径 | `mcpstore config path` |

## 服务管理（add/list/get/remove）
| 命令 | 场景 | 语法 | 示例 |
| --- | --- | --- | --- |
| `mcpstore add` | stdio（本地命令） | `mcpstore add --transport stdio <name> [--for-agent <agent_id>] [--env KEY=VAL ...] -- <command> [args...]` | `mcpstore add --transport stdio local-svc --env API_KEY=123 -- python server.py --port 9000` |
| `mcpstore add` | HTTP | `mcpstore add --transport http <name> <url> [--for-agent <agent_id>] [--env KEY=VAL ...]` | `mcpstore add --transport http wiki https://example.com/mcp -e Authorization="Bearer token"` |
| `mcpstore add` | SSE | `mcpstore add --transport sse <name> <url> [--for-agent <agent_id>] [--env KEY=VAL ...]` | `mcpstore add --transport sse stream https://example.com/sse -e X-API-Key=abc` |
| `mcpstore add` | 自动推断 + JSON | `mcpstore add <name?> '<json>' [--for-agent <agent_id>] [--env KEY=VAL ...]`；JSON 内含 `name` 则可省略位置 name | `mcpstore add '{\"name\":\"svc\",\"url\":\"https://example.com/mcp\"}'` |
| `mcpstore list` | 列出服务 | `mcpstore list [--for-agent <agent_id>]` | `mcpstore list --for-agent agentA` |
| `mcpstore get` | 查看服务详情（含 status/tools） | `mcpstore get <name> [--for-agent <agent_id>]` | `mcpstore get svc1` |
| `mcpstore remove` | 删除服务 | `mcpstore remove <name> [--for-agent <agent_id>]` | `mcpstore remove svc1 --for-agent agentA` |

## 传输推断与合并规则
- `--transport` 显式优先；JSON 内 `transport` 次之；否则按字段推断（command→stdio，URL→http，无法判定时报错）。
- `--env` 合并：命令行覆盖同名键；stdio 写 env，http/sse 写 headers；保留 JSON 中 headers/env。
- JSON 输入：首个非选项位置参数以 `{`/`[` 开头即按 JSON 解析；若 JSON 内缺少 `name` 且未提供位置 name，则报错。

## 常见注意
- reload 模式与 `--prefix` 不兼容（有 prefix 会直接退出提示）。
- 同步命令在已有事件循环环境可能报 “loop running”，异步场景请使用异步接口或分离进程。
- SSE 场景建议显式 `--transport sse`，避免 URL 默认 http 被误判。
