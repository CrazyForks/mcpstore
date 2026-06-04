# 测试指南

## 目标

确保功能变更后，核心链路与文档命令都可正常工作。

## 运行测试

```bash
uv run --with pytest pytest
```

如果当前分支暂无测试用例，`pytest` 可能显示 0 tests collected。这表示当前仓库测试覆盖仍需补充，不代表功能一定正确。

## 最小验证清单

1. `uv run mcpstore version`
2. `uv run mcpstore run api --help`
3. 文档构建：`uv run --with mkdocs --with mkdocs-material --with mkdocs-minify-plugin --with pymdown-extensions mkdocs build -f docs/mkdocs.yml`

## 文档相关验证

- 新页面是否加入 `docs/mkdocs.yml`
- 站内链接是否可跳转
- 命令示例是否与真实 CLI 参数一致
