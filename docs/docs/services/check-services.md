## check_services - 服务健康检查


如何通过 MCPStore 检查服务健康状态，验证连接与可用性。

### SDK

同步：
  - `store.for_store().check_services() -> Dict[str, Any]`
  - `store.for_agent(id).check_services() -> Dict[str, Any]`

异步：
  - `await store.for_store().check_services_async() -> Dict[str, Any]`
  - `await store.for_agent(id).check_services_async() -> Dict[str, Any]`

### 参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| 无     | -    | 该方法不需要参数。 |

### 返回值

- 类型：`Dict[str, Any]`
- 说明：以服务名为键的健康检查结果字典。常见字段：

| 字段            | 类型   | 说明 |
|-----------------|--------|------|
| `healthy`       | bool   | 是否健康 |
| `response_time` | float  | 响应时间（毫秒） |
| `last_check`    | str    | 检查时间（ISO 字符串） |
| `error`         | str    | 错误信息（失败时可用） |
| `actual_service`| str    | Agent 视角返回的实际全局服务名（Agent 模式可用） |


### 视角
通过 `for_store()` 检查全局所有服务；通过 `for_agent(id)` 仅检查当前 Agent 的服务，并自动处理名称映射。


### 使用示例

基本健康检查：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

health_report = store.for_store().check_services()

print("服务健康检查报告:")
print("=" * 40)

for service_name, status in health_report.items():
    if status.get('healthy', False):
        print(f"{service_name}: 健康")
    else:
        print(f"{service_name}: 异常")
        if 'error' in status:
            print(f"  错误: {status['error']}")
```

Store 级别健康检查：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

health_report = store.for_store().check_services()

healthy_count = 0
total_count = len(health_report)

for service_name, status in health_report.items():
    is_healthy = status.get('healthy', False)
    response_time = status.get('response_time', 'N/A')
    if is_healthy:
        healthy_count += 1
        print(f"{service_name}: 健康 ({response_time}ms)")
    else:
        print(f"{service_name}: 异常")
        if 'error' in status:
            print(f"  错误信息: {status['error']}")

print(f"健康统计: {healthy_count}/{total_count} 服务正常")
```

Agent 级别健康检查：
```python
from mcpstore import MCPStore

store = MCPStore.setup_store()

agent_id = "my_agent"
health_report = store.for_agent(agent_id).check_services()

print(f"Agent {agent_id} 健康检查:")
print("=" * 40)

for service_name, status in health_report.items():
    if status.get('healthy', False):
        print(f"{service_name}: 健康")
    else:
        print(f"{service_name}: 需要关注")
```

定期健康检查：
```python
from mcpstore import MCPStore
import time
import schedule

def periodic_health_check():
    store = MCPStore.setup_store()
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 执行健康检查")
    health_report = store.for_store().check_services()
    unhealthy_services = [name for name, st in health_report.items() if not st.get('healthy', False)]
    if unhealthy_services:
        print(f"发现 {len(unhealthy_services)} 个异常服务:")
        for service in unhealthy_services:
            print(f"  - {service}")
    else:
        print("所有服务运行正常")

schedule.every(5).minutes.do(periodic_health_check)
periodic_health_check()

while True:
    schedule.run_pending()
    time.sleep(1)
```

异步版本：
```python
import asyncio
from mcpstore import MCPStore

async def main():
    store = MCPStore.setup_store()
    report = await store.for_store().check_services_async()
    for name, st in report.items():
        print(name, "健康" if st.get('healthy', False) else "异常")

asyncio.run(main())
```

异步批量检查多个 Agent：
```python
import asyncio
from mcpstore import MCPStore

async def check_all_agents_health():
    store = MCPStore.setup_store()
    agent_ids = ["agent1", "agent2", "agent3"]
    tasks = [store.for_agent(agent_id).check_services_async() for agent_id in agent_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for agent_id, result in zip(agent_ids, results):
        if isinstance(result, Exception):
            print(f"Agent {agent_id}: 检查异常 - {result}")
        else:
            healthy_count = sum(1 for st in result.values() if st.get('healthy', False))
            total_count = len(result)
            print(f"Agent {agent_id}: {healthy_count}/{total_count} 服务健康")

asyncio.run(check_all_agents_health())
```

健康检查结果分析：
```python
def analyze_health_report(health_report):
    healthy_services = []
    unhealthy_services = []
    slow_services = []
    for service_name, status in health_report.items():
        if status.get('healthy', False):
            response_time = status.get('response_time', 0)
            if response_time > 3000:
                slow_services.append((service_name, response_time))
            else:
                healthy_services.append(service_name)
        else:
            unhealthy_services.append((service_name, status.get('error', '未知错误')))

    print("健康检查分析报告:")
    print("=" * 50)
    print(f"健康服务: {len(healthy_services)} 个")
    print(f"响应较慢: {len(slow_services)} 个")
    print(f"异常服务: {len(unhealthy_services)} 个")
    if slow_services:
        print("\n响应较慢的服务:")
        for service, time_ms in slow_services:
            print(f"  - {service}: {time_ms}ms")
    if unhealthy_services:
        print("\n异常服务详情:")
        for service, error in unhealthy_services:
            print(f"  - {service}: {error}")

from mcpstore import MCPStore
store = MCPStore.setup_store()
report = store.for_store().check_services()
analyze_health_report(report)
```

错误处理：
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
    print(f"健康检查时发生错误: {e}")
```


### 你可能想找的方法

| 场景/方法       | 同步方法 |
|------------------|----------|
| 获取服务信息     | `store.for_store().get_service_info(name)` |
| 获取服务状态     | `store.for_store().get_service_status(name)` |
| 重启服务         | `store.for_store().restart_service(name)` |
| 列出服务         | `store.for_store().list_services()` |
| 刷新内容         | `svc.refresh_content()` |


### 使用场景

- 定期检查所有服务的可用性与响应时间。
- 故障排查时快速定位异常服务。
- 部署发布后做全量回归检查。
- 在 Agent 侧仅关注本 Agent 的服务健康状况。


### 注意事项

- 名称映射：Agent 模式自动处理本地名与全局名映射。
- 时延与负载：健康检查可能产生网络请求与耗时，建议控制频率。
- 返回结构：不同服务可能返回字段略有差异，请做健壮性判断。
- 异常处理：失败场景请读取 `error` 字段并做好重试或告警。
