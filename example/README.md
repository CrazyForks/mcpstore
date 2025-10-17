# MCPStore 测试示例

本目录包含 MCPStore 的完整测试示例，按功能模块组织。

## 📁 目录结构

```
example/
├── utils/                          # 公共工具模块
│   ├── __init__.py
│   └── import_helper.py           # 导入路径配置
├── init/                          # 初始化测试
│   ├── test_store_init_basic.py
│   ├── test_store_init_redis.py
│   ├── test_agent_init_basic.py
│   ├── test_mixed_init_comparison.py
│   └── README.md
├── service/                       # 服务管理测试（待创建）
├── tool/                          # 工具管理测试（待创建）
├── integration/                   # 框架集成测试（待创建）
├── database/                      # 数据库测试（待创建）
└── auth/                          # 认证测试（待创建）
```

## 🎯 命名规则

所有测试文件遵循统一的命名规则：

```
test_{上下文模式}_{功能板块}_{具体场景}.py
```

### 上下文模式
- `store` - Store 级别（全局共享）
- `agent` - Agent 级别（独立隔离）
- `mixed` - 混合模式（对比测试）

### 功能板块
- `init` - 初始化
- `service_*` - 服务管理（add/find/detail/wait/health/update/restart/delete/config）
- `tool_*` - 工具管理（find/detail/use/config/stats）
- `integration_*` - 框架集成（langchain/llamaindex/crewai等）
- `database_*` - 数据库支持（redis等）
- `auth` - 权限认证

## 🚀 快速开始

### 运行单个测试

```bash
# 运行 Store 基础初始化测试
python example/init/test_store_init_basic.py
```

### 运行某个模块的所有测试

```bash
# Windows
for %f in (example\init\test_*.py) do python %f

# Linux/Mac
for f in example/init/test_*.py; do python "$f"; done
```

## 💡 导入机制

所有测试文件使用统一的导入配置：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.import_helper import setup_import_path
setup_import_path()

from mcpstore import MCPStore
```

### 导入优先级
1. **本地开发版本**: 优先使用 `src/mcpstore`（如果存在）
2. **环境安装版本**: 如果本地不存在，使用 pip 安装的版本

### 为什么这样设计？
- ✅ 开发时可以直接测试本地代码
- ✅ 不需要每次都重新安装包
- ✅ 支持同时测试多个版本
- ✅ 对环境友好，自动回退

## 📝 测试设计原则

1. **无 try-except 包裹核心测试**
   - 核心测试代码不使用 try-except
   - 让错误自然抛出，方便调试
   - 可以清晰看到项目的错误反馈

2. **简单直接**
   - 不定义复杂函数
   - 代码顺序执行
   - 输出清晰易读

3. **完整覆盖**
   - 每个功能板块都有对应测试
   - Store 和 Agent 模式都测试
   - 覆盖常见使用场景

4. **输出友好**
   - ✅ 成功操作
   - ⚠️ 警告提示
   - ❌ 错误信息
   - 💡 使用建议

## 📚 模块说明

### ✅ 已完成模块

- **init/** - 初始化测试
  - Store 基础初始化
  - Store + Redis 初始化
  - Agent 基础初始化
  - Store vs Agent 对比

### 🚧 计划中模块

详见完整的测试文件规划文档。

## 🔗 相关文档

- [MCPStore 文档](../mcpstore_docs/docs/)
- [快速上手](../mcpstore_docs/docs/getting-started/quickstart.md)
- [服务管理](../mcpstore_docs/docs/services/overview.md)
- [工具管理](../mcpstore_docs/docs/tools/overview.md)

## 🤝 贡献

欢迎提交新的测试用例！请遵循现有的命名规则和代码风格。

---

**开始测试吧！** 🚀

