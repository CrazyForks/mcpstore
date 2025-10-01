# refresh_content()

刷新服务内容（重新获取工具列表等）。

## 方法特性

- ✅ **调用方式**: ServiceProxy 方法
- ✅ **异步版本**: 支持异步调用
- ✅ **Store级别**: `svc = store.for_store().find_service("name")` 后调用
- ✅ **Agent级别**: `svc = store.for_agent("agent1").find_service("name")` 后调用
- 📁 **文件位置**: `service_proxy.py`

## 参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| 无参数 | - | - | 该方法不需要参数 |

## 返回值

返回操作结果字典：

```python
{
    "success": bool,            # 刷新是否成功
    "message": str,             # 操作消息
    "tool_count": int,          # 刷新后的工具数量
    "refreshed_at": str         # 刷新时间戳
}
```

## 使用示例

### Store级别刷新服务内容

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_store().wait_service("weather")

# 查找服务
svc = store.for_store().find_service("weather")

# 查看当前工具
print(f"刷新前工具数: {len(svc.list_tools())}")

# 刷新服务内容
result = svc.refresh_content()
print(f"刷新结果: {result}")

# 查看刷新后工具
print(f"刷新后工具数: {len(svc.list_tools())}")
```

### Agent级别刷新服务内容

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent级别添加服务
store.for_agent("agent1").add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

# 等待服务就绪
store.for_agent("agent1").wait_service("weather")

# 查找服务
svc = store.for_agent("agent1").find_service("weather")

# 刷新服务内容
result = svc.refresh_content()
print(f"Agent服务刷新结果: {result}")
```

### 服务更新后刷新

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 记录原始工具列表
original_tools = svc.list_tools()
print(f"原始工具数: {len(original_tools)}")

# 假设服务端更新了工具
# 刷新以获取最新工具列表
print("\n刷新服务内容...")
result = svc.refresh_content()

if result["success"]:
    print(f"✅ 刷新成功")
    print(f"  工具数量: {result['tool_count']}")
    print(f"  刷新时间: {result['refreshed_at']}")
    
    # 获取新工具列表
    new_tools = svc.list_tools()
    print(f"  新工具数: {len(new_tools)}")
else:
    print(f"❌ 刷新失败: {result['message']}")
```

### 定期刷新

```python
import time
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 定期刷新（每30秒）
print("开始定期刷新...")
for i in range(5):
    print(f"\n[刷新 {i+1}]")
    result = svc.refresh_content()
    
    if result["success"]:
        print(f"  ✅ 成功 - 工具数: {result['tool_count']}")
    else:
        print(f"  ❌ 失败 - {result['message']}")
    
    if i < 4:  # 最后一次不等待
        time.sleep(30)
```

### 批量刷新多个服务

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加多个服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"},
        "calculator": {"command": "python", "args": ["calc.py"]}
    }
})

# 等待所有服务
store.for_store().wait_service("weather")
store.for_store().wait_service("calculator")

# 批量刷新
service_names = ["weather", "calculator"]

print("📊 批量刷新服务")
print("=" * 50)

for name in service_names:
    svc = store.for_store().find_service(name)
    result = svc.refresh_content()
    
    icon = "✅" if result["success"] else "❌"
    print(f"{icon} {name}")
    print(f"  工具数: {result.get('tool_count', 'N/A')}")
    print(f"  消息: {result['message']}")
    print()
```

### 刷新失败重试

```python
import time
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 刷新重试逻辑
max_retries = 3
retry_delay = 2

for attempt in range(max_retries):
    print(f"尝试刷新 (第 {attempt + 1} 次)...")
    result = svc.refresh_content()
    
    if result["success"]:
        print(f"✅ 刷新成功 - 工具数: {result['tool_count']}")
        break
    else:
        print(f"❌ 刷新失败: {result['message']}")
        
        if attempt < max_retries - 1:
            print(f"等待 {retry_delay} 秒后重试...")
            time.sleep(retry_delay)
        else:
            print("达到最大重试次数，放弃刷新")
```

### 结合健康检查使用

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 添加服务
store.for_store().add_service({
    "mcpServers": {
        "weather": {"url": "https://mcpstore.wiki/mcp"}
    }
})

store.for_store().wait_service("weather")
svc = store.for_store().find_service("weather")

# 先检查健康状态
health = svc.check_health()
print(f"服务健康: {health['healthy']}")

if health["healthy"]:
    # 健康时才刷新
    print("服务健康，执行刷新...")
    result = svc.refresh_content()
    
    if result["success"]:
        print(f"✅ 刷新成功 - 工具数: {result['tool_count']}")
    else:
        print(f"❌ 刷新失败: {result['message']}")
else:
    print("⚠️ 服务不健康，跳过刷新")
```

## 使用场景

### 1. 服务工具更新
当远程服务添加或删除了工具时，使用 `refresh_content()` 同步最新的工具列表。

### 2. 服务配置变更
修改服务配置后，刷新以确保使用最新配置。

### 3. 定期同步
在长期运行的应用中，定期刷新以保持工具列表的最新状态。

### 4. 故障恢复
服务从异常状态恢复后，刷新以验证服务功能正常。

## 与 restart_service() 的区别

| 对比项 | refresh_content() | restart_service() |
|--------|-------------------|-------------------|
| **操作范围** | 只刷新内容（工具列表等） | 完全重启服务 |
| **连接状态** | 保持连接 | 断开并重新连接 |
| **影响范围** | 较小 | 较大 |
| **执行时间** | 较快 | 较慢 |
| **使用场景** | 内容同步 | 故障恢复 |

```python
# refresh_content() - 只刷新内容
result = svc.refresh_content()  # 快速刷新工具列表

# restart_service() - 完全重启
result = svc.restart_service()  # 断开重连，重新初始化
```

## 相关方法

- [restart_service()](restart-service.md) - 重启服务
- [update_config()](update-config.md) - 更新服务配置
- [patch_config()](patch-config.md) - 增量更新配置
- [service_info()](../details/service-info.md) - 获取服务信息

## 注意事项

1. **调用前提**: 必须先通过 `find_service()` 获取 ServiceProxy 对象
2. **服务状态**: 建议在服务健康时执行刷新
3. **性能影响**: 刷新会触发网络请求，有一定开销
4. **工具变化**: 刷新后工具数量可能变化
5. **频率控制**: 避免过于频繁刷新

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0

