# 服务注册完整示例

本文档提供 MCPStore 服务注册的完整实际示例，涵盖各种使用场景。

## 🚀 基础示例

### 单个服务注册

```python
from mcpstore import MCPStore

# 初始化 MCPStore
store = MCPStore.setup_store()

# 注册远程天气服务
store.for_store().add_service({
    "name": "weather",
    "url": "https://weather-api.example.com/mcp",
    "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
    }
})

# 注册本地文件系统服务
store.for_store().add_service({
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
})

# 验证注册结果
services = store.for_store().list_services()
print(f"已注册 {len(services)} 个服务")
```

### 链式调用示例

```python
# 链式注册多个服务
(store.for_store()
 .add_service({
     "name": "weather",
     "url": "https://weather.example.com/mcp"
 })
 .add_service({
     "name": "maps",
     "url": "https://maps.example.com/mcp"
 })
 .add_service({
     "name": "calculator",
     "command": "python",
     "args": ["calculator_server.py"]
 }))

print("链式注册完成")
```

## 🏢 企业级示例

### 完整的企业服务配置

```python
import os
from mcpstore import MCPStore

# 企业级配置
def setup_enterprise_services():
    store = MCPStore.setup_store()
    
    # 认证服务
    store.for_store().add_service({
        "name": "auth_service",
        "url": "https://auth.company.com/mcp",
        "transport": "streamable-http",
        "headers": {
            "Authorization": f"Bearer {os.getenv('AUTH_SERVICE_TOKEN')}",
            "X-Company-ID": os.getenv('COMPANY_ID'),
            "X-Environment": os.getenv('ENVIRONMENT', 'production')
        }
    })
    
    # 数据库服务
    store.for_store().add_service({
        "name": "database_service",
        "command": "python",
        "args": [
            "/opt/services/db_server.py",
            "--config", "/etc/db/config.json",
            "--log-level", "INFO"
        ],
        "env": {
            "DB_HOST": os.getenv('DB_HOST', 'localhost'),
            "DB_PORT": os.getenv('DB_PORT', '5432'),
            "DB_NAME": os.getenv('DB_NAME'),
            "DB_USER": os.getenv('DB_USER'),
            "DB_PASSWORD": os.getenv('DB_PASSWORD'),
            "CONNECTION_POOL_SIZE": "20",
            "QUERY_TIMEOUT": "30"
        },
        "working_dir": "/opt/services"
    })
    
    # 文件处理服务
    store.for_store().add_service({
        "name": "file_processor",
        "command": "npx",
        "args": [
            "-y", "@company/file-processor",
            "--data-dir", "/data",
            "--temp-dir", "/tmp/processing",
            "--max-file-size", "100MB"
        ],
        "env": {
            "PROCESSOR_MODE": "production",
            "WORKER_THREADS": "4",
            "MEMORY_LIMIT": "2GB",
            "LOG_LEVEL": "INFO"
        }
    })
    
    # 外部 API 集成
    store.for_store().add_service({
        "name": "external_api",
        "url": "https://api.partner.com/mcp",
        "transport": "sse",
        "headers": {
            "Authorization": f"Bearer {os.getenv('PARTNER_API_KEY')}",
            "X-Client-Version": "1.0",
            "Accept": "application/json"
        }
    })
    
    return store

# 使用
store = setup_enterprise_services()
print("企业服务配置完成")
```

### 多环境配置

```python
def setup_environment_specific_services(environment: str):
    """根据环境设置不同的服务配置"""
    
    # 环境配置映射
    env_configs = {
        "development": {
            "api_base": "https://api-dev.company.com",
            "db_host": "localhost",
            "log_level": "DEBUG",
            "timeout": 60
        },
        "staging": {
            "api_base": "https://api-staging.company.com",
            "db_host": "staging-db.company.com",
            "log_level": "INFO",
            "timeout": 30
        },
        "production": {
            "api_base": "https://api.company.com",
            "db_host": "prod-db.company.com",
            "log_level": "ERROR",
            "timeout": 10
        }
    }
    
    config = env_configs.get(environment, env_configs["development"])
    store = MCPStore.setup_store()
    
    # 环境特定的服务配置
    services_config = {
        "mcpServers": {
            f"{environment}_api": {
                "url": f"{config['api_base']}/mcp",
                "headers": {
                    "Authorization": f"Bearer {os.getenv(f'{environment.upper()}_API_KEY')}",
                    "X-Environment": environment
                }
            },
            f"{environment}_database": {
                "command": "python",
                "args": ["db_service.py", "--env", environment],
                "env": {
                    "DB_HOST": config["db_host"],
                    "LOG_LEVEL": config["log_level"],
                    "TIMEOUT": str(config["timeout"])
                }
            }
        }
    }
    
    store.for_store().add_service(services_config)
    return store

# 使用
dev_store = setup_environment_specific_services("development")
prod_store = setup_environment_specific_services("production")
```

## 📁 JSON 文件配置示例

### 创建配置文件

```python
import json
import os

def create_service_configs():
    """创建不同类型的服务配置文件"""
    
    # 基础服务配置
    basic_config = {
        "mcpServers": {
            "weather": {
                "url": "https://weather.example.com/mcp",
                "headers": {
                    "API-Key": os.getenv('WEATHER_API_KEY')
                }
            },
            "maps": {
                "url": "https://maps.example.com/mcp"
            },
            "calculator": {
                "command": "python",
                "args": ["calculator.py"]
            }
        }
    }
    
    # 开发环境配置
    dev_config = [
        {
            "name": "dev_api",
            "url": "https://api-dev.example.com/mcp",
            "headers": {"X-Environment": "development"}
        },
        {
            "name": "local_tools",
            "command": "python",
            "args": ["dev_tools.py"],
            "env": {"DEBUG": "true"}
        }
    ]
    
    # 生产环境配置
    prod_config = {
        "name": "production_api",
        "url": "https://api.example.com/mcp",
        "transport": "streamable-http",
        "headers": {
            "Authorization": f"Bearer {os.getenv('PROD_API_TOKEN')}",
            "X-Environment": "production"
        }
    }
    
    # 保存配置文件
    os.makedirs("config", exist_ok=True)
    
    with open("config/basic_services.json", "w") as f:
        json.dump(basic_config, f, indent=2)
    
    with open("config/dev_services.json", "w") as f:
        json.dump(dev_config, f, indent=2)
    
    with open("config/prod_service.json", "w") as f:
        json.dump(prod_config, f, indent=2)
    
    print("配置文件创建完成")

# 创建配置文件
create_service_configs()
```

### 使用配置文件

```python
def load_services_from_files():
    """从不同的配置文件加载服务"""
    store = MCPStore.setup_store()
    
    # 加载基础服务
    store.for_store().add_service(json_file="config/basic_services.json")
    
    # 根据环境加载额外服务
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "development":
        store.for_store().add_service(json_file="config/dev_services.json")
    elif environment == "production":
        store.for_store().add_service(json_file="config/prod_service.json")
    
    return store

# 使用
store = load_services_from_files()
```

## 🎭 Agent 级别示例

### 独立 Agent 服务

```python
def setup_agent_services():
    """为不同 Agent 设置独立的服务"""
    store = MCPStore.setup_store()
    
    # 研究 Agent 的专用服务
    research_agent = store.for_agent("research_agent")
    research_agent.add_service({
        "name": "arxiv_search",
        "url": "https://arxiv-api.example.com/mcp",
        "headers": {"X-Agent-Type": "research"}
    })
    research_agent.add_service({
        "name": "paper_analyzer",
        "command": "python",
        "args": ["paper_analysis.py"],
        "env": {"ANALYSIS_MODE": "academic"}
    })
    
    # 数据分析 Agent 的专用服务
    analysis_agent = store.for_agent("analysis_agent")
    analysis_agent.add_service({
        "name": "data_processor",
        "command": "python",
        "args": ["data_processor.py", "--mode", "analysis"],
        "env": {
            "PANDAS_VERSION": "latest",
            "MEMORY_LIMIT": "4GB"
        }
    })
    analysis_agent.add_service({
        "name": "visualization",
        "url": "https://viz-api.example.com/mcp"
    })
    
    # 验证 Agent 服务隔离
    research_services = research_agent.list_services()
    analysis_services = analysis_agent.list_services()
    
    print(f"研究 Agent 服务: {[s.name for s in research_services]}")
    print(f"分析 Agent 服务: {[s.name for s in analysis_services]}")
    
    return store

# 使用
store = setup_agent_services()
```

## 🔄 批量操作示例

### 批量注册和验证

```python
def batch_register_with_validation():
    """批量注册服务并验证结果"""
    store = MCPStore.setup_store()
    
    # 定义多个服务
    services = [
        {
            "name": "weather",
            "url": "https://weather.example.com/mcp"
        },
        {
            "name": "news",
            "url": "https://news.example.com/mcp"
        },
        {
            "name": "calculator",
            "command": "python",
            "args": ["calculator.py"]
        },
        {
            "name": "filesystem",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/data"]
        }
    ]
    
    # 批量注册
    successful = []
    failed = []
    
    for service_config in services:
        try:
            store.for_store().add_service(service_config, wait=5000)
            
            # 验证服务状态
            service_info = store.for_store().get_service_info(service_config["name"])
            if service_info and service_info.state in ["healthy", "initializing"]:
                successful.append(service_config["name"])
            else:
                failed.append({
                    "name": service_config["name"],
                    "error": f"Service state: {service_info.state if service_info else 'unknown'}"
                })
                
        except Exception as e:
            failed.append({
                "name": service_config["name"],
                "error": str(e)
            })
    
    # 报告结果
    print(f"✅ 成功注册: {successful}")
    print(f"❌ 注册失败: {failed}")
    
    # 获取所有工具
    tools = store.for_store().list_tools()
    print(f"📋 可用工具: {len(tools)} 个")
    
    return store, successful, failed

# 使用
store, successful, failed = batch_register_with_validation()
```

## 🛡️ 错误处理示例

### 健壮的服务注册

```python
def robust_service_registration():
    """健壮的服务注册，包含完整的错误处理"""
    from mcpstore.core.exceptions import (
        InvalidConfigError,
        ServiceNotFoundError,
        ConnectionError
    )
    
    store = MCPStore.setup_store()
    
    def register_service_safely(config, max_retries=3):
        """安全地注册单个服务"""
        service_name = config.get("name", "unknown")
        
        for attempt in range(max_retries):
            try:
                # 预验证配置
                if not config.get("name"):
                    raise ValueError("服务名称不能为空")
                
                if not config.get("url") and not config.get("command"):
                    raise ValueError("必须指定 url 或 command")
                
                # 注册服务
                store.for_store().add_service(config, wait=3000)
                
                # 验证注册结果
                service_info = store.for_store().get_service_info(service_name)
                if service_info and service_info.state != "unreachable":
                    print(f"✅ {service_name} 注册成功 (状态: {service_info.state})")
                    return True
                else:
                    print(f"⚠️ {service_name} 注册但状态异常: {service_info.state if service_info else 'unknown'}")
                    
            except InvalidConfigError as e:
                print(f"❌ {service_name} 配置错误: {e}")
                break  # 配置错误不重试
                
            except (ConnectionError, Exception) as e:
                print(f"⚠️ {service_name} 注册失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)  # 指数退避
                    
        print(f"❌ {service_name} 最终注册失败")
        return False
    
    # 测试各种配置
    test_configs = [
        # 正常配置
        {
            "name": "weather",
            "url": "https://weather.example.com/mcp"
        },
        # 错误配置 - 缺少名称
        {
            "url": "https://api.example.com/mcp"
        },
        # 错误配置 - 冲突字段
        {
            "name": "conflict",
            "url": "https://api.example.com/mcp",
            "command": "python"
        },
        # 正常本地服务
        {
            "name": "calculator",
            "command": "python",
            "args": ["calculator.py"]
        }
    ]
    
    results = []
    for config in test_configs:
        success = register_service_safely(config)
        results.append({
            "config": config,
            "success": success
        })
    
    return store, results

# 使用
store, results = robust_service_registration()
```

## 🔍 调试和监控示例

### 详细的注册监控

```python
def monitored_service_registration():
    """带有详细监控的服务注册"""
    import time
    
    # 启用调试模式
    store = MCPStore.setup_store(debug=True)
    
    def monitor_service_registration(config):
        """监控单个服务的注册过程"""
        service_name = config["name"]
        start_time = time.time()
        
        print(f"🚀 开始注册服务: {service_name}")
        
        # 注册服务
        store.for_store().add_service(config, wait=0)  # 不等待，立即返回
        
        cache_time = time.time()
        print(f"⚡ 缓存完成: {(cache_time - start_time) * 1000:.2f}ms")
        
        # 监控状态变化
        last_state = None
        timeout = 30  # 30秒超时
        
        while time.time() - start_time < timeout:
            try:
                service_info = store.for_store().get_service_info(service_name)
                current_state = service_info.state if service_info else "unknown"
                
                if current_state != last_state:
                    elapsed = (time.time() - start_time) * 1000
                    print(f"📊 {service_name} 状态变化: {last_state} -> {current_state} ({elapsed:.2f}ms)")
                    last_state = current_state
                
                if current_state == "healthy":
                    # 获取工具列表
                    tools = store.for_store().list_tools()
                    service_tools = [t for t in tools if t.service_name == service_name]
                    total_time = (time.time() - start_time) * 1000
                    print(f"✅ {service_name} 完全就绪: {len(service_tools)} 个工具 ({total_time:.2f}ms)")
                    return True
                    
                elif current_state == "unreachable":
                    total_time = (time.time() - start_time) * 1000
                    print(f"❌ {service_name} 连接失败 ({total_time:.2f}ms)")
                    return False
                
                time.sleep(0.5)  # 500ms 检查间隔
                
            except Exception as e:
                print(f"⚠️ 监控 {service_name} 时出错: {e}")
                time.sleep(1)
        
        print(f"⏰ {service_name} 监控超时")
        return False
    
    # 测试不同类型的服务
    test_services = [
        {
            "name": "fast_api",
            "url": "https://httpbin.org/delay/1"  # 快速响应
        },
        {
            "name": "slow_api", 
            "url": "https://httpbin.org/delay/5"  # 慢响应
        },
        {
            "name": "local_service",
            "command": "python",
            "args": ["-c", "import time; time.sleep(2); print('Ready')"]
        }
    ]
    
    results = {}
    for service_config in test_services:
        success = monitor_service_registration(service_config)
        results[service_config["name"]] = success
    
    print(f"\n📈 注册结果汇总: {results}")
    return store, results

# 使用
store, results = monitored_service_registration()
```

## 📚 相关文档

- [add_service() 完整指南](add-service.md) - 详细的方法文档
- [配置格式速查表](config-formats.md) - 配置格式参考
- [注册架构详解](architecture.md) - 内部架构说明
- [错误处理指南](../../advanced/error-handling.md) - 错误处理最佳实践

## 🎯 下一步

- 学习 [工具调用方法](../../tools/usage/call-tool.md)
- 了解 [服务管理](../management/service-management.md)
- 掌握 [最佳实践](../../advanced/best-practices.md)
