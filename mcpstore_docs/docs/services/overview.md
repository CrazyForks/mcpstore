# 服务管理概览

MCPStore 提供了完整的服务生命周期管理功能，按照功能分类为8个核心模块，涵盖从添加到删除的全流程操作。

## 📋 **服务管理8大模块**

### 1. 📝 **添加服务**
添加 MCP 服务，支持多种配置格式。

**核心方法**:
- **[add_service()](registration/add-service.md)** - 添加服务（支持单个/批量）

**相关文档**:
- [配置格式速查表](registration/config-formats.md) - 支持的配置格式
- [完整示例集合](registration/examples.md) - 各种使用示例

---

### 2. 🔍 **查找服务**
查找已注册的服务，获取服务代理对象或列表。

**核心方法**:
- **[find_service()](listing/find-service.md)** - 查找服务并返回 ServiceProxy
- **[list_services()](listing/list-services.md)** - 列出所有已注册服务

**相关文档**:
- [服务代理（ServiceProxy）](listing/service-proxy.md) - ServiceProxy 概念说明

---

### 3. 📊 **服务详情**
获取服务的详细信息和当前状态。

**核心方法**:
- **[service_info()](details/service-info.md)** - 获取服务详细信息
- **[service_status()](details/service-status.md)** - 获取服务当前状态

> 💡 **提示**: 这些方法需要先通过 `find_service()` 获取 ServiceProxy 对象后调用

---

### 4. ⏳ **等待服务**
等待服务达到指定状态，确保服务就绪后再进行操作。

**核心方法**:
- **[wait_service()](waiting/wait-service.md)** - 等待服务就绪

**使用场景**:
- 添加服务后等待初始化完成
- 重启服务后等待恢复
- 批量服务初始化同步

---

### 5. 🏥 **健康检查**
检查服务的健康状态和性能指标。

**核心方法**:
- **[check_services()](health/check-services.md)** - 检查所有服务健康状态（Context级别）
- **[check_health()](health/check-health.md)** - 检查单个服务健康摘要（ServiceProxy级别）
- **[health_details()](health/health-details.md)** - 获取单个服务详细健康信息（ServiceProxy级别）

**对比**:
| 方法 | 调用层级 | 检查范围 | 信息量 |
|------|----------|----------|--------|
| check_services() | Context | 所有服务 | 基础 |
| check_health() | ServiceProxy | 单个服务 | 摘要 |
| health_details() | ServiceProxy | 单个服务 | 详细 |

---

### 6. ⚙️ **更新服务**
更新服务配置，支持全量和增量更新。

**核心方法**:
- **[update_config()](management/update-service.md)** - 全量更新服务配置
- **[patch_config()](management/patch-service.md)** - 增量更新服务配置（推荐）

**区别**:
- `update_config()`: 完全替换配置，未提供的字段会被清空
- `patch_config()`: 只更新指定字段，其他字段保持不变

---

### 7. 🔄 **重启服务**
重启服务或刷新服务内容。

**核心方法**:
- **[restart_service()](management/restart-service.md)** - 重启服务（完全重启）
- **[refresh_content()](management/refresh-content.md)** - 刷新服务内容（仅刷新工具列表等）

**区别**:
- `restart_service()`: 断开重连，重新初始化服务
- `refresh_content()`: 保持连接，只刷新内容

---

### 8. 🗑️ **删除服务**
删除或移除服务，支持保留配置或完全清理。

**核心方法**:
- **[remove_service()](management/remove-service.md)** - 移除服务运行态（保留配置）
- **[delete_service()](management/delete-service.md)** - 完全删除服务（配置+缓存）

**区别**:
- `remove_service()`: 只清理运行态，配置保留，可快速恢复
- `delete_service()`: 完全删除，需要重新配置

---

## 🎯 **快速开始**

### 完整的服务管理流程

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 1️⃣ 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 2️⃣ 等待服务就绪
store.for_store().wait_service("weather", timeout=30.0)

# 3️⃣ 查找服务
svc = store.for_store().find_service("weather")

# 4️⃣ 获取服务详情
info = svc.service_info()
print(f"服务名称: {info.name}")
print(f"工具数量: {info.tool_count}")

# 5️⃣ 检查健康状态
health = svc.check_health()
print(f"健康状态: {health['healthy']}")

# 6️⃣ 更新配置（如需要）
svc.patch_config({"keep_alive": True})

# 7️⃣ 使用服务
tools = svc.list_tools()
print(f"可用工具: {len(tools)} 个")

# 8️⃣ 清理（可选）
svc.remove_service()  # 或 svc.delete_service()
```

### Store vs Agent 模式

MCPStore 支持两种服务管理模式：

```python
# Store 级别（全局共享）
store.for_store().add_service({"mcpServers": {...}})
store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# Agent 级别（独立隔离）
store.for_agent("agent1").add_service({"mcpServers": {...}})
store.for_agent("agent1").wait_service("weather")
svc = store.for_agent("agent1").find_service("weather")
```

| 特性 | Store 级别 | Agent 级别 |
|------|------------|------------|
| **访问范围** | 全局共享 | 独立隔离 |
| **配置文件** | mcp.json | agent配置 |
| **适用场景** | 基础服务 | 专用服务 |

---

## 📋 **配置管理**

除了8大服务管理模块外，还提供配置管理功能：

**核心方法**:
- **[reset_config()](config/reset-config.md)** - 重置配置
- **[show_config()](config/show-config.md)** - 显示配置信息

---

## 🎭 **调用层级说明**

MCPStore 的服务方法分为两个调用层级：

### Context 层级
通过 `store.for_store()` 或 `store.for_agent()` 调用：

```python
# Context 层级方法
store.for_store().add_service(...)       # 添加服务
store.for_store().list_services()        # 列出服务
store.for_store().find_service("name")   # 查找服务
store.for_store().wait_service("name")   # 等待服务
store.for_store().check_services()       # 检查所有服务
```

### ServiceProxy 层级
通过 `find_service()` 返回的代理对象调用：

```python
# ServiceProxy 层级方法
svc = store.for_store().find_service("name")

svc.service_info()        # 服务详情
svc.service_status()      # 服务状态
svc.check_health()        # 健康检查
svc.health_details()      # 详细健康信息
svc.update_config({})     # 更新配置
svc.patch_config({})      # 增量更新
svc.restart_service()     # 重启服务
svc.refresh_content()     # 刷新内容
svc.remove_service()      # 移除服务
svc.delete_service()      # 删除服务
```

---

## 🔗 **相关文档**

- [服务架构设计](architecture.md) - 了解服务管理的架构设计
- [配置格式说明](registration/config-formats.md) - 学习各种服务配置格式
- [ServiceProxy 概念](listing/service-proxy.md) - 理解服务代理机制
- [最佳实践](../advanced/best-practices.md) - 服务管理最佳实践

---

## 📊 **方法速查表**

| 功能 | 方法 | 调用层级 | 文档 |
|------|------|----------|------|
| **添加** | add_service() | Context | [查看](registration/add-service.md) |
| **查找** | find_service() | Context | [查看](listing/find-service.md) |
| **列表** | list_services() | Context | [查看](listing/list-services.md) |
| **详情** | service_info() | ServiceProxy | [查看](details/service-info.md) |
| **状态** | service_status() | ServiceProxy | [查看](details/service-status.md) |
| **等待** | wait_service() | Context | [查看](waiting/wait-service.md) |
| **健康** | check_services() | Context | [查看](health/check-services.md) |
| **健康** | check_health() | ServiceProxy | [查看](health/check-health.md) |
| **健康详情** | health_details() | ServiceProxy | [查看](health/health-details.md) |
| **更新** | update_config() | ServiceProxy | [查看](management/update-service.md) |
| **增量更新** | patch_config() | ServiceProxy | [查看](management/patch-service.md) |
| **重启** | restart_service() | ServiceProxy | [查看](management/restart-service.md) |
| **刷新** | refresh_content() | ServiceProxy | [查看](management/refresh-content.md) |
| **移除** | remove_service() | ServiceProxy | [查看](management/remove-service.md) |
| **删除** | delete_service() | ServiceProxy | [查看](management/delete-service.md) |

---

**更新时间**: 2025-01-09  
**版本**: 2.0.0
