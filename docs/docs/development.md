# 开发指南

本文面向希望在本仓库进行二次开发的同学。

## 环境准备

```bash
uv sync
```

## 本地运行

### 运行 CLI

```bash
uv run mcpstore version
```

### 启动 API

```bash
uv run mcpstore run api --host 127.0.0.1 --port 18200
```

## 代码结构（核心）

- `src/mcpstore/cli/`：CLI 命令入口与子命令
- `src/mcpstore/api/`：API 服务入口与路由
- `src/mcpstore/adapters/`：各 Agent 框架适配层
- `src/mcpstore/mcp/`：MCP 客户端能力与底层抽象

## 开发流程建议

1. 先阅读 `docs/docs/quickstart.md` 和 `docs/docs/services/overview.md`
2. 在目标模块附近先查现有实现，再补充或修改逻辑
3. 修改后执行测试和文档构建校验
