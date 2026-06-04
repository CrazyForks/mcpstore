# 故障排查

## `mcpstore` 命令不可用

现象：执行 `mcpstore` 报命令不存在。

处理：

```bash
uv sync
uv run mcpstore version
```

如果第二条命令可用，说明可执行文件已在 `uv` 环境中正常安装。

## API 启动失败

现象：`uv run mcpstore run api` 启动报错。

排查：

1. 先检查端口是否被占用，改用其他端口重试
2. 检查参数是否拼写正确：`uv run mcpstore run api --help`
3. 若使用 `--reload`，不要同时设置 `--prefix`

## 文档构建失败

现象：`uv run mkdocs build -f docs/mkdocs.yml` 失败。

排查：

1. 确认已安装文档依赖
2. 检查 `mkdocs.yml` 中导航路径是否存在
3. 检查新增 Markdown 文件标题和代码块是否闭合
