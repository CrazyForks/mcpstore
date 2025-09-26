
# 服务管理概览

MCPStore 提供了完整的服务生命周期管理功能，支持服务注册、查询、健康监控和管理操作。

## 🚀 **服务注册**

### 核心方法
- **[add_service()](registration/add-service.md)** - 添加MCP服务，支持多种配置格式
- **[add_service_with_details()](registration/add-service-with-details.md)** - 添加服务并返回详细信息
- **[batch_add_services()](registration/batch-add-services.md)** - 批量添加多个服务

## 🔍 **服务查询**

### 核心方法
- **[list_services()](listing/list-services.md)** - 列出所有服务信息
- **[get_service_info()](listing/get-service-info.md)** - 获取指定服务的详细信息

## 🏥 **服务健康监控**

### 核心方法
- **[check_services()](health/check-services.md)** - 检查所有服务健康状态
- **[get_service_status()](health/get-service-status.md)** - 获取单个服务状态信息
- **[wait_service()](health/wait-service.md)** - 等待服务达到指定状态

## ⚙️ **服务管理操作**

### 核心方法
- **[update_service()](management/update-service.md)** - 完全替换服务配置
- **[patch_service()](management/patch-service.md)** - 增量更新服务配置（推荐）
- **[delete_service()](management/delete-service.md)** - 删除服务
- **[restart_service()](management/restart-service.md)** - 重启服务

## 📋 **配置管理**

### 核心方法
- **[reset_config()](config/reset-config.md)** - 重置配置
- **[show_config()](config/show-config.md)** - 显示配置信息

## 🎯 **快速开始**

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://api.weather.com/mcp"}
    }
})

# 检查服务状态
health = store.for_store().check_services()
print(f"服务健康状态: {health}")

# 列出所有服务
services = store.for_store().list_services()
print(f"已注册服务: {[s.name for s in services]}")
```

## 🔗 **相关文档**

- [服务架构设计](architecture.md) - 了解服务管理的架构设计
- [配置格式说明](registration/config-formats.md) - 学习各种服务配置格式
- [最佳实践](../advanced/best-practices.md) - 服务管理最佳实践
