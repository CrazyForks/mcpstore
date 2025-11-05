## restart_service - 服务重启

重启指定服务。

### SDK

同步：
  - `store.for_store().restart_service(name) -> bool`
  - `store.for_agent(id).restart_service(name) -> bool`

异步：
  - `await store.for_store().restart_service_async(name) -> bool`
  - `await store.for_agent(id).restart_service_async(name) -> bool`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `name` | `str` | ✅ | - | 服务名称 |

## 返回值

- **成功**: 返回 `True`
- **失败**: 返回 `False`

## 使用示例

### Store级别重启服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 重启服务
success = store.for_store().restart_service("weather")
if success:
    print("Weather服务重启成功")
else:
    print("Weather服务重启失败")
```

### Agent级别重启服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式重启服务
success = store.for_agent("agent1").restart_service("weather-local")
if success:
    print("Agent Weather服务重启成功")
```

### 重启前检查状态

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 检查服务状态
status = store.for_store().get_service_status("weather")
print(f"重启前状态: {status['status']}")

if status['status'] != 'healthy':
    # 重启不健康的服务
    success = store.for_store().restart_service("weather")
    if success:
        print("服务重启成功")
        
        # 等待服务恢复
        ready = store.for_store().wait_service("weather", "healthy", timeout=30.0)
        if ready:
            print("服务已恢复健康状态")
        else:
            print("服务重启后仍未恢复")
    else:
        print("服务重启失败")
else:
    print("服务状态正常，无需重启")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_restart_service():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步重启服务
    success = await store.for_store().restart_service_async("weather")
    
    if success:
        print("异步重启成功")
        
        # 异步等待服务恢复
        ready = await store.for_store().wait_service_async("weather", "healthy", timeout=30.0)
        if ready:
            print("服务已异步恢复")
    else:
        print("异步重启失败")
    
    return success

# 运行异步重启
result = asyncio.run(async_restart_service())
```

### 批量重启服务

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 批量重启多个服务
services_to_restart = ["weather", "database", "filesystem"]

restart_results = {}
for service_name in services_to_restart:
    success = store.for_store().restart_service(service_name)
    restart_results[service_name] = success
    print(f"重启 {service_name}: {'成功' if success else '失败'}")

# 统计结果
successful_restarts = sum(1 for success in restart_results.values() if success)
print(f"总计重启成功: {successful_restarts}/{len(services_to_restart)} 个服务")
```

### 智能重启（仅重启不健康的服务）

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def smart_restart():
    """智能重启：只重启不健康的服务"""
    
    # 检查所有服务健康状态
    health_status = store.for_store().check_services()
    
    unhealthy_services = []
    for service_name, status in health_status.items():
        if status['status'] != 'healthy':
            unhealthy_services.append(service_name)
    
    if not unhealthy_services:
        print("所有服务状态正常，无需重启")
        return True
    
    print(f"发现 {len(unhealthy_services)} 个不健康服务，开始重启...")
    
    restart_success = 0
    for service_name in unhealthy_services:
        print(f"重启服务: {service_name}")
        success = store.for_store().restart_service(service_name)
        
        if success:
            restart_success += 1
            print(f"  {service_name} 重启成功")
            
            # 等待服务恢复
            ready = store.for_store().wait_service(service_name, "healthy", timeout=20.0)
            if ready:
                print(f"  {service_name} 已恢复健康")
            else:
                print(f"  {service_name} 重启后仍未恢复")
        else:
            print(f"  {service_name} 重启失败")
    
    print(f"智能重启完成: {restart_success}/{len(unhealthy_services)} 个服务重启成功")
    return restart_success == len(unhealthy_services)

# 执行智能重启
smart_restart()
```

### 重启后验证

```python
from mcpstore import MCPStore
import time

# 初始化
store = MCPStore.setup_store()

def restart_with_verification(service_name):
    """重启服务并验证结果"""
    
    print(f"开始重启服务: {service_name}")
    
    # 1. 记录重启前状态
    try:
        before_status = store.for_store().get_service_status(service_name)
        print(f"重启前状态: {before_status['status']}")
    except:
        print("无法获取重启前状态")
        before_status = None
    
    # 2. 执行重启
    restart_time = time.time()
    success = store.for_store().restart_service(service_name)
    restart_duration = time.time() - restart_time
    
    if not success:
        print(f"服务重启失败 (耗时: {restart_duration:.2f}秒)")
        return False
    
    print(f"服务重启成功 (耗时: {restart_duration:.2f}秒)")
    
    # 3. 等待服务恢复
    print("等待服务恢复...")
    ready = store.for_store().wait_service(service_name, "healthy", timeout=30.0)
    
    if ready:
        # 4. 验证重启后状态
        after_status = store.for_store().get_service_status(service_name)
        print(f"重启后状态: {after_status['status']}")
        
        # 5. 验证工具可用性
        try:
            tools = store.for_store().list_tools()
            service_tools = [t for t in tools if service_name in t.name]
            print(f"服务工具数量: {len(service_tools)}")
            
            if service_tools:
                print("✅ 服务重启验证成功")
                return True
            else:
                print("⚠️ 服务重启后工具不可用")
                return False
                
        except Exception as e:
            print(f"工具验证失败: {e}")
            return False
    else:
        print("服务重启后未能恢复健康状态")
        return False

# 使用验证重启
restart_with_verification("weather")
```

## 重启流程

重启服务包含以下步骤：

- 断开连接: 断开与服务的现有连接
- 清理资源: 清理相关的缓存和临时数据
- 重新连接: 使用原有配置重新建立连接
- 健康检查: 验证服务是否正常启动
- 工具刷新: 重新获取服务提供的工具列表

## 常见重启场景

- 配置更新后: 使新配置生效
- 服务不健康: 尝试恢复服务状态
- 连接异常: 重新建立连接
- 工具更新: 刷新工具列表
- 故障恢复: 从错误状态中恢复

## 相关方法

- [get_service_status()](../health/get-service-status.md) - 检查重启前后状态
- [wait_service()](../health/wait-service.md) - 等待重启完成
- [update_service()](update-service.md) - 更新配置后重启
- [check_services()](../health/check-services.md) - 批量检查服务状态

## 注意事项

- 服务中断: 重启过程中服务暂时不可用
- 工具影响: 重启会导致该服务的工具暂时不可用
- Agent 映射: Agent 模式下自动处理服务名映射
- 超时设置: 重启操作有内置超时机制
- 状态验证: 建议重启后验证服务状态和工具可用性
