# check_services()

执行服务健康检查，验证所有服务的连接状态和可用性。

## 语法

```python
store.for_store().check_services() -> Dict[str, Any]
store.for_agent(agent_id).check_services() -> Dict[str, Any]
```

## 参数

无参数

## 返回值

- **类型**: `Dict[str, Any]`
- **说明**: 包含所有服务健康检查结果的字典

## 🤖 Agent 模式支持

### 支持状态
- ✅ **完全支持** - `check_services()` 在 Agent 模式下完全可用

### Agent 模式调用
```python
# Agent 模式调用
health_report = store.for_agent("research_agent").check_services()

# 对比 Store 模式调用
health_report = store.for_store().check_services()
```

### 模式差异说明
- **Store 模式**: 检查所有全局注册的服务，包括所有 Agent 的服务
- **Agent 模式**: 只检查当前 Agent 的服务，提供隔离的健康视图
- **主要区别**: Agent 模式只关注相关服务，检查速度更快，结果更聚焦

### 返回值对比

#### Store 模式返回示例
```python
{
    "weather-api": {
        "healthy": True,
        "response_time": 150.5,
        "last_check": "2024-01-15T10:30:00Z"
    },
    "weather-apibyagent1": {
        "healthy": True,
        "response_time": 200.3,
        "last_check": "2024-01-15T10:30:00Z"
    },
    "maps-apibyagent2": {
        "healthy": False,
        "error": "Connection timeout",
        "last_check": "2024-01-15T10:30:00Z"
    }
}
```

#### Agent 模式返回示例
```python
# Agent "agent1" 的健康检查结果
{
    "weather-api": {  # 本地服务名视图
        "healthy": True,
        "response_time": 200.3,
        "last_check": "2024-01-15T10:30:00Z",
        "actual_service": "weather-apibyagent1"  # 实际服务名
    },
    "maps-api": {     # 本地服务名视图
        "healthy": True,
        "response_time": 180.1,
        "last_check": "2024-01-15T10:30:00Z",
        "actual_service": "maps-apibyagent1"
    }
}
```

### 性能优势
- **检查范围**: Agent 模式只检查相关服务，检查时间更短
- **网络开销**: 减少不必要的网络请求
- **资源使用**: 降低系统资源消耗
- **结果聚焦**: 只关注当前 Agent 关心的服务状态

### 使用建议
- **Agent 开发**: 推荐使用 Agent 模式，获得聚焦的健康视图
- **系统监控**: 使用 Store 模式，全面监控所有服务状态
- **性能考虑**: 大型系统中 Agent 模式性能更优
- **故障排查**: Agent 模式便于快速定位相关服务问题

## 使用示例

### 基本健康检查

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# 执行健康检查
health_report = store.for_store().check_services()

print("📊 服务健康检查报告:")
print("=" * 40)

for service_name, status in health_report.items():
    if status.get('healthy', False):
        print(f"✅ {service_name}: 健康")
    else:
        print(f"❌ {service_name}: 异常")
        if 'error' in status:
            print(f"   错误: {status['error']}")
```

### Store 级别健康检查

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

# Store 级别检查所有服务
health_report = store.for_store().check_services()

print("🏪 Store 级别健康检查:")
print("=" * 50)

healthy_count = 0
total_count = len(health_report)

for service_name, status in health_report.items():
    is_healthy = status.get('healthy', False)
    response_time = status.get('response_time', 'N/A')
    
    if is_healthy:
        healthy_count += 1
        print(f"✅ {service_name}: 健康 ({response_time}ms)")
    else:
        print(f"❌ {service_name}: 异常")
        if 'error' in status:
            print(f"   错误信息: {status['error']}")

print(f"\n📈 健康统计: {healthy_count}/{total_count} 服务正常")
```

### Agent 级别健康检查

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

agent_id = "my_agent"

# Agent 级别只检查自己的服务
health_report = store.for_agent(agent_id).check_services()

print(f"🤖 Agent {agent_id} 健康检查:")
print("=" * 40)

for service_name, status in health_report.items():
    if status.get('healthy', False):
        print(f"✅ {service_name}: 健康")
    else:
        print(f"❌ {service_name}: 需要关注")
```

### 定期健康检查

```python
from mcpstore import MCPStore
import time
import schedule

def periodic_health_check():
    """定期健康检查函数"""
    store = MCPStore.setup_store()
    
    print(f"\n⏰ {time.strftime('%Y-%m-%d %H:%M:%S')} - 执行健康检查")
    
    health_report = store.for_store().check_services()
    
    unhealthy_services = []
    for service_name, status in health_report.items():
        if not status.get('healthy', False):
            unhealthy_services.append(service_name)
    
    if unhealthy_services:
        print(f"⚠️ 发现 {len(unhealthy_services)} 个异常服务:")
        for service in unhealthy_services:
            print(f"   - {service}")
    else:
        print("✅ 所有服务运行正常")

# 设置定期检查（每5分钟）
schedule.every(5).minutes.do(periodic_health_check)

# 立即执行一次
periodic_health_check()

# 保持运行
while True:
    schedule.run_pending()
    time.sleep(1)
```

## 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def check_services_async_example():
    store = MCPStore.setup_store()
    
    # 异步健康检查
    health_report = await store.for_store().check_services_async()
    
    print("📊 异步健康检查结果:")
    for service_name, status in health_report.items():
        health_status = "✅ 健康" if status.get('healthy', False) else "❌ 异常"
        print(f"  {service_name}: {health_status}")

# 运行异步示例
asyncio.run(check_services_async_example())
```

### 异步批量检查多个Agent

```python
import asyncio
from mcpstore import MCPStore

async def check_all_agents_health():
    store = MCPStore.setup_store()
    
    # 假设有多个Agent
    agent_ids = ["agent1", "agent2", "agent3"]
    
    # 并发检查所有Agent的健康状态
    tasks = [
        store.for_agent(agent_id).check_services_async()
        for agent_id in agent_ids
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 显示结果
    for agent_id, result in zip(agent_ids, results):
        if isinstance(result, Exception):
            print(f"❌ Agent {agent_id}: 检查异常 - {result}")
        else:
            healthy_count = sum(1 for status in result.values() if status.get('healthy', False))
            total_count = len(result)
            print(f"🤖 Agent {agent_id}: {healthy_count}/{total_count} 服务健康")

# 运行异步批量检查
asyncio.run(check_all_agents_health())
```

## 健康检查结果分析

```python
from mcpstore import MCPStore

def analyze_health_report(health_report):
    """分析健康检查报告"""
    
    healthy_services = []
    unhealthy_services = []
    slow_services = []
    
    for service_name, status in health_report.items():
        if status.get('healthy', False):
            response_time = status.get('response_time', 0)
            if response_time > 3000:  # 超过3秒认为较慢
                slow_services.append((service_name, response_time))
            else:
                healthy_services.append(service_name)
        else:
            unhealthy_services.append((service_name, status.get('error', '未知错误')))
    
    print("📊 健康检查分析报告:")
    print("=" * 50)
    print(f"✅ 健康服务: {len(healthy_services)} 个")
    print(f"🐌 响应较慢: {len(slow_services)} 个")
    print(f"❌ 异常服务: {len(unhealthy_services)} 个")
    
    if slow_services:
        print("\n🐌 响应较慢的服务:")
        for service, time_ms in slow_services:
            print(f"   - {service}: {time_ms}ms")
    
    if unhealthy_services:
        print("\n❌ 异常服务详情:")
        for service, error in unhealthy_services:
            print(f"   - {service}: {error}")

# 使用示例
store = MCPStore.setup_store()
health_report = store.for_store().check_services()
analyze_health_report(health_report)
```

## 错误处理

```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

try:
    health_report = store.for_store().check_services()
    
    if health_report:
        print(f"健康检查完成，检查了 {len(health_report)} 个服务")
    else:
        print("没有服务需要检查")
        
except Exception as e:
    print(f"❌ 健康检查时发生错误: {e}")
```

## 注意事项

1. **Agent 名称映射**: Agent 模式下会自动处理服务名称映射
2. **异常处理**: 方法内部会捕获异常并记录到日志
3. **返回格式**: 返回字典包含每个服务的健康状态和详细信息
4. **性能考虑**: 健康检查可能需要一定时间，特别是网络服务

## 相关方法

- [restart_service()](restart-service.md) - 重启服务
- [list_services()](../listing/list-services.md) - 列出所有服务
- [get_service_info()](../listing/get-service-info.md) - 获取服务详细信息
- [add_service()](../registration/register-service.md) - 注册服务

## 下一步

- 了解 [服务重启方法](restart-service.md)
- 学习 [服务状态监控](../listing/get-service-info.md)
- 查看 [服务注册管理](../registration/register-service.md)
