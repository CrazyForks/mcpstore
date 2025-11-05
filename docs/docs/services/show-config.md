# show_config()

显示配置信息。

## 方法特性

- ✅ **异步版本**: `show_config_async()`
- ✅ **Store级别**: `store.for_store().show_config()`
- ✅ **Agent级别**: `store.for_agent("agent1").show_config()`
- 📁 **文件位置**: `service_management.py`
- 🏷️ **所属类**: `ServiceManagementMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `scope` | `str` | ❌ | `"all"` | 显示范围 |

## 显示范围选项

| 范围值 | 描述 | 返回内容 |
|--------|------|----------|
| `"all"` | 显示所有配置 | 服务配置、Agent配置、客户端配置 |
| `"mcp"` | 显示MCP配置 | mcp.json中的服务配置 |
| `"agent"` | 显示Agent配置 | Agent客户端映射 |
| `"client"` | 显示客户端配置 | 客户端服务映射 |

## 返回值

返回包含配置信息的字典，格式根据范围而定。

## 使用示例

### Store级别显示所有配置

```python
from mcpstore import MCPStore
import json

# 初始化
store = MCPStore.setup_store()

# 显示所有配置
config = store.for_store().show_config("all")
print("完整配置:")
print(json.dumps(config, indent=2, ensure_ascii=False))
```

### Agent级别显示配置

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式显示配置
agent_config = store.for_agent("agent1").show_config()
print(f"Agent1配置: {agent_config}")
```

### 显示特定范围的配置

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 显示MCP服务配置
mcp_config = store.for_store().show_config("mcp")
print("MCP服务配置:")
for service_name, service_config in mcp_config.get("mcpServers", {}).items():
    print(f"  {service_name}: {service_config}")

# 显示Agent配置
agent_config = store.for_store().show_config("agent")
print(f"Agent配置: {agent_config}")

# 显示客户端配置
client_config = store.for_store().show_config("client")
print(f"客户端配置: {client_config}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_show_config():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步显示配置
    config = await store.for_store().show_config_async("all")
    
    print("异步获取的配置:")
    print(f"服务数量: {len(config.get('mcpServers', {}))}")
    print(f"Agent数量: {len(config.get('agents', {}))}")
    print(f"客户端数量: {len(config.get('clients', {}))}")
    
    return config

# 运行异步显示
result = asyncio.run(async_show_config())
```

### 格式化显示配置

```python
from mcpstore import MCPStore
import json

# 初始化
store = MCPStore.setup_store()

def pretty_show_config(scope="all"):
    """格式化显示配置"""
    
    config = store.for_store().show_config(scope)
    
    print(f"\n=== {scope.upper()} 配置 ===")
    
    if scope == "all" or scope == "mcp":
        # 显示服务配置
        mcp_servers = config.get("mcpServers", {})
        print(f"\n📦 MCP服务 ({len(mcp_servers)} 个):")
        for name, cfg in mcp_servers.items():
            if "url" in cfg:
                print(f"  🌐 {name}: {cfg['url']}")
            elif "command" in cfg:
                print(f"  ⚡ {name}: {cfg['command']} {' '.join(cfg.get('args', []))}")
    
    if scope == "all" or scope == "agent":
        # 显示Agent配置
        agents = config.get("agents", {})
        print(f"\n🤖 Agent配置 ({len(agents)} 个):")
        for agent_id, agent_cfg in agents.items():
            print(f"  {agent_id}: {len(agent_cfg.get('services', []))} 个服务")
    
    if scope == "all" or scope == "client":
        # 显示客户端配置
        clients = config.get("clients", {})
        print(f"\n🔗 客户端配置 ({len(clients)} 个):")
        for client_id, client_cfg in clients.items():
            print(f"  {client_id}: {client_cfg}")
    
    return config

# 使用格式化显示
pretty_show_config("all")
```

### 配置对比

```python
from mcpstore import MCPStore
import json

# 初始化
store = MCPStore.setup_store()

def compare_configs():
    """对比不同范围的配置"""
    
    # 获取不同范围的配置
    all_config = store.for_store().show_config("all")
    mcp_config = store.for_store().show_config("mcp")
    agent_config = store.for_store().show_config("agent")
    client_config = store.for_store().show_config("client")
    
    print("配置统计对比:")
    print(f"  完整配置大小: {len(json.dumps(all_config))} 字符")
    print(f"  MCP服务数量: {len(mcp_config.get('mcpServers', {}))}")
    print(f"  Agent数量: {len(agent_config.get('agents', {}))}")
    print(f"  客户端数量: {len(client_config.get('clients', {}))}")
    
    return {
        "all": all_config,
        "mcp": mcp_config,
        "agent": agent_config,
        "client": client_config
    }

# 执行配置对比
configs = compare_configs()
```

### 配置验证

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def validate_config():
    """验证配置完整性"""
    
    config = store.for_store().show_config("all")
    
    # 验证MCP服务配置
    mcp_servers = config.get("mcpServers", {})
    valid_services = 0
    invalid_services = []
    
    for name, cfg in mcp_servers.items():
        if "url" in cfg or "command" in cfg:
            valid_services += 1
        else:
            invalid_services.append(name)
    
    print(f"配置验证结果:")
    print(f"  有效服务: {valid_services} 个")
    print(f"  无效服务: {len(invalid_services)} 个")
    
    if invalid_services:
        print(f"  无效服务列表: {invalid_services}")
    
    # 验证Agent配置
    agents = config.get("agents", {})
    print(f"  Agent配置: {len(agents)} 个")
    
    # 验证客户端配置
    clients = config.get("clients", {})
    print(f"  客户端配置: {len(clients)} 个")
    
    return len(invalid_services) == 0

# 执行配置验证
is_valid = validate_config()
print(f"配置整体有效性: {'✅ 有效' if is_valid else '❌ 无效'}")
```

### 配置导出

```python
from mcpstore import MCPStore
import json
from datetime import datetime

# 初始化
store = MCPStore.setup_store()

def export_config(scope="all", filename=None):
    """导出配置到文件"""
    
    # 获取配置
    config = store.for_store().show_config(scope)
    
    # 生成文件名
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcpstore_config_{scope}_{timestamp}.json"
    
    # 导出到文件
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"配置已导出到: {filename}")
        print(f"配置大小: {len(json.dumps(config))} 字符")
        
        return filename
        
    except Exception as e:
        print(f"导出失败: {e}")
        return None

# 导出不同范围的配置
export_config("all")
export_config("mcp")
export_config("agent")
```

## 配置结构说明

### 完整配置结构 (`"all"`)
```python
{
    "mcpServers": {
        "service_name": {
            "url": "https://api.example.com/mcp",
            "transport": "http"
        }
    },
    "agents": {
        "agent_id": {
            "services": ["service1", "service2"]
        }
    },
    "clients": {
        "client_id": {
            "service_mapping": {...}
        }
    }
}
```

## 相关方法

- [reset_config()](reset-config.md) - 重置配置
- [add_service()](../registration/add-service.md) - 添加服务配置
- [list_services()](../listing/list-services.md) - 查看服务列表

## 注意事项

1. **敏感信息**: 配置可能包含API密钥等敏感信息，注意保护
2. **实时数据**: 返回的是当前实时配置，不是缓存数据
3. **Agent隔离**: Agent模式下只显示该Agent相关的配置
4. **格式一致**: 返回格式与配置文件格式保持一致
5. **范围选择**: 根据需要选择合适的显示范围，避免信息过载
