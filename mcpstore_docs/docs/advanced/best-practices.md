# 最佳实践

基于 MCPStore 的生产环境经验，总结出的最佳实践指南，帮助您构建稳定、高效、可维护的智能体工具系统。

## 🎯 架构设计最佳实践

### 1. 上下文选择策略

#### Store 模式 vs Agent 模式

```python
# ✅ 推荐：单一应用使用 Store 模式
store = MCPStore.setup_store()
context = store.for_store()
context.add_service({"name": "global-tool", "url": "https://api.com/mcp"})

# ✅ 推荐：多智能体系统使用 Agent 模式
agent1_context = store.for_agent("research_agent")
agent1_context.add_service({"name": "research-tools", "url": "https://research.com/mcp"})

agent2_context = store.for_agent("analysis_agent")
agent2_context.add_service({"name": "analysis-tools", "url": "https://analysis.com/mcp"})

# ❌ 避免：在单一应用中混用两种模式
# 这会导致服务管理混乱
```

#### 数据空间隔离

```python
# ✅ 推荐：不同项目使用独立数据空间
project_a_store = MCPStore.setup_store(mcp_config_file="projects/project_a/mcp.json")
project_b_store = MCPStore.setup_store(mcp_config_file="projects/project_b/mcp.json")

# ✅ 推荐：环境隔离
dev_store = MCPStore.setup_store(mcp_config_file="config/dev/mcp.json")
prod_store = MCPStore.setup_store(mcp_config_file="config/prod/mcp.json")

# ❌ 避免：在同一配置文件中混合不同环境的服务
```

### 2. 服务配置最佳实践

#### 配置文件组织

```json
{
  "mcpServers": {
    "weather-api": {
      "url": "https://weather.example.com/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer ${WEATHER_API_TOKEN}",
        "User-Agent": "MCPStore/1.0"
      },
      "timeout": 30,
      "description": "天气查询服务 - 提供全球天气信息",
      "tags": ["weather", "external-api"],
      "contact": "weather-team@example.com"
    },
    "local-filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
      "env": {
        "LOG_LEVEL": "info"
      },
      "working_dir": "/workspace",
      "description": "本地文件系统操作",
      "tags": ["filesystem", "local"]
    }
  },
  "version": "1.0.0",
  "description": "Production MCPStore configuration",
  "metadata": {
    "environment": "production",
    "team": "ai-platform",
    "last_updated": "2024-01-01T00:00:00Z"
  }
}
```

#### 环境变量管理

```bash
# ✅ 推荐：使用环境变量管理敏感信息
export WEATHER_API_TOKEN="your-secret-token"
export DATABASE_URL="postgresql://user:pass@host:5432/db"
export LOG_LEVEL="info"

# ✅ 推荐：使用 .env 文件（不要提交到版本控制）
echo "WEATHER_API_TOKEN=your-secret-token" > .env
echo ".env" >> .gitignore
```

### 3. 监控配置最佳实践

```python
# ✅ 推荐：生产环境监控配置
production_monitoring = {
    "health_check_seconds": 60,        # 生产环境较长间隔
    "tools_update_hours": 4,           # 4小时更新一次工具
    "reconnection_seconds": 120,       # 2分钟重连间隔
    "cleanup_hours": 24,               # 每天清理一次
    "enable_tools_update": True,
    "enable_reconnection": True,
    "update_tools_on_reconnection": True
}

# ✅ 推荐：开发环境监控配置
development_monitoring = {
    "health_check_seconds": 15,        # 开发环境快速检查
    "tools_update_hours": 1,           # 1小时更新一次
    "reconnection_seconds": 30,        # 30秒重连间隔
    "enable_tools_update": True,
    "enable_reconnection": True
}

store = MCPStore.setup_store(
    mcp_config_file="config/prod/mcp.json",
    monitoring=production_monitoring
)
```

## 🚀 性能优化最佳实践

### 1. 缓存策略

```python
# ✅ 推荐：利用缓存优先架构
# 查询操作直接从缓存返回，速度极快
services = store.for_store().list_services()  # < 100ms
tools = store.for_store().list_tools()        # < 100ms

# ✅ 推荐：批量操作减少网络开销
services_config = [
    {"name": "service1", "url": "https://api1.com/mcp"},
    {"name": "service2", "url": "https://api2.com/mcp"},
    {"name": "service3", "url": "https://api3.com/mcp"}
]
result = store.for_store().batch_add_services(services_config)

# ❌ 避免：频繁的单个服务操作
# for config in services_config:
#     store.for_store().add_service(config)  # 多次网络请求
```

### 2. 异步操作

```python
import asyncio

async def efficient_tool_calls():
    """高效的异步工具调用"""
    store = MCPStore.setup_store()
    context = store.for_store()
    
    # ✅ 推荐：并发执行多个工具调用
    tasks = [
        context.call_tool_async("weather_get_current", {"city": "北京"}),
        context.call_tool_async("weather_get_current", {"city": "上海"}),
        context.call_tool_async("weather_get_current", {"city": "广州"})
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# ❌ 避免：串行执行异步操作
async def inefficient_tool_calls():
    context = store.for_store()
    results = []
    for city in ["北京", "上海", "广州"]:
        result = await context.call_tool_async("weather_get_current", {"city": city})
        results.append(result)
    return results
```

### 3. 连接管理

```python
# ✅ 推荐：合理配置连接超时
service_config = {
    "name": "external-api",
    "url": "https://api.example.com/mcp",
    "timeout": 30,  # 30秒超时
    "headers": {
        "Connection": "keep-alive",  # 保持连接
        "Keep-Alive": "timeout=60"
    }
}

# ✅ 推荐：使用连接池
# MCPStore 内部自动管理连接池，无需手动配置
```

## 🔒 安全最佳实践

### 1. 敏感信息管理

```python
# ✅ 推荐：使用环境变量
import os

api_token = os.getenv("API_TOKEN")
if not api_token:
    raise ValueError("API_TOKEN environment variable is required")

service_config = {
    "name": "secure-api",
    "url": "https://secure-api.com/mcp",
    "headers": {
        "Authorization": f"Bearer {api_token}"
    }
}

# ❌ 避免：硬编码敏感信息
# service_config = {
#     "name": "secure-api",
#     "url": "https://secure-api.com/mcp",
#     "headers": {
#         "Authorization": "Bearer hardcoded-token"  # 危险！
#     }
# }
```

### 2. 访问控制

```python
# ✅ 推荐：使用 Agent 模式实现访问隔离
def create_restricted_agent(store, agent_id: str, allowed_services: List[str]):
    """创建受限制的 Agent"""
    agent_context = store.for_agent(agent_id)
    
    # 只添加允许的服务
    for service_name in allowed_services:
        service_config = get_service_config(service_name)
        agent_context.add_service(service_config)
    
    return agent_context

# 使用示例
research_agent = create_restricted_agent(
    store, 
    "research_agent", 
    ["search-api", "wikipedia", "arxiv"]
)

analysis_agent = create_restricted_agent(
    store,
    "analysis_agent", 
    ["database", "calculator", "chart-generator"]
)
```

### 3. 输入验证

```python
def safe_tool_call(context, tool_name: str, args: dict):
    """安全的工具调用"""
    # ✅ 推荐：验证工具名称
    available_tools = {tool.name for tool in context.list_tools()}
    if tool_name not in available_tools:
        raise ValueError(f"Tool {tool_name} not available")
    
    # ✅ 推荐：验证参数
    if not isinstance(args, dict):
        raise TypeError("Arguments must be a dictionary")
    
    # ✅ 推荐：参数清理
    cleaned_args = {k: v for k, v in args.items() if not k.startswith('_')}
    
    try:
        return context.call_tool(tool_name, cleaned_args)
    except Exception as e:
        # ✅ 推荐：记录错误但不暴露敏感信息
        logger.error(f"Tool call failed: {tool_name}")
        raise RuntimeError("Tool execution failed") from e
```

## 🔧 错误处理最佳实践

### 1. 分层错误处理

```python
import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)

class MCPStoreManager:
    """MCPStore 管理器，实现分层错误处理"""
    
    def __init__(self, config_file: str):
        try:
            self.store = MCPStore.setup_store(mcp_config_file=config_file)
            self.context = self.store.for_store()
        except Exception as e:
            logger.critical(f"Failed to initialize MCPStore: {e}")
            raise
    
    def safe_add_service(self, config: dict) -> bool:
        """安全添加服务"""
        try:
            self.context.add_service(config)
            logger.info(f"Service {config.get('name')} added successfully")
            return True
        except ValidationError as e:
            logger.error(f"Service configuration invalid: {e}")
            return False
        except ConnectionError as e:
            logger.warning(f"Service connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error adding service: {e}")
            return False
    
    def safe_call_tool(self, tool_name: str, args: dict) -> Optional[Any]:
        """安全调用工具"""
        try:
            return self.context.call_tool(tool_name, args)
        except ToolNotFoundError:
            logger.warning(f"Tool {tool_name} not found")
            return None
        except ToolExecutionError as e:
            logger.error(f"Tool {tool_name} execution failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling tool {tool_name}: {e}")
            return None
```

### 2. 重试机制

```python
import time
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                        time.sleep(delay * (2 ** attempt))  # 指数退避
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                except Exception as e:
                    # 非网络错误不重试
                    logger.error(f"Non-retryable error: {e}")
                    raise
            
            raise last_exception
        return wrapper
    return decorator

class RobustMCPStore:
    """带重试机制的 MCPStore"""
    
    def __init__(self, config_file: str):
        self.store = MCPStore.setup_store(mcp_config_file=config_file)
        self.context = self.store.for_store()
    
    @retry_on_failure(max_retries=3, delay=1.0)
    def add_service(self, config: dict):
        """带重试的服务添加"""
        return self.context.add_service(config)
    
    @retry_on_failure(max_retries=2, delay=0.5)
    def call_tool(self, tool_name: str, args: dict):
        """带重试的工具调用"""
        return self.context.call_tool(tool_name, args)
```

## 📊 监控和日志最佳实践

### 1. 结构化日志

```python
import json
import logging
from datetime import datetime

class StructuredLogger:
    """结构化日志记录器"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 配置格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_service_event(self, event_type: str, service_name: str, **kwargs):
        """记录服务事件"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "service_name": service_name,
            "details": kwargs
        }
        self.logger.info(json.dumps(log_data))
    
    def log_tool_call(self, tool_name: str, args: dict, result: Any, duration: float):
        """记录工具调用"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "tool_call",
            "tool_name": tool_name,
            "args_count": len(args),
            "success": result is not None,
            "duration_ms": round(duration * 1000, 2)
        }
        self.logger.info(json.dumps(log_data))

# 使用示例
logger = StructuredLogger("mcpstore")

def monitored_tool_call(context, tool_name: str, args: dict):
    """带监控的工具调用"""
    start_time = time.time()
    try:
        result = context.call_tool(tool_name, args)
        duration = time.time() - start_time
        logger.log_tool_call(tool_name, args, result, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.log_tool_call(tool_name, args, None, duration)
        raise
```

### 2. 健康检查端点

```python
from fastapi import FastAPI, HTTPException
from typing import Dict, Any

def create_health_check_app(store: MCPStore) -> FastAPI:
    """创建健康检查应用"""
    app = FastAPI(title="MCPStore Health Check")
    
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """基础健康检查"""
        try:
            context = store.for_store()
            services = context.list_services()
            tools = context.list_tools()
            
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "services_count": len(services),
                "tools_count": len(tools)
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Health check failed: {e}")
    
    @app.get("/health/detailed")
    async def detailed_health_check() -> Dict[str, Any]:
        """详细健康检查"""
        try:
            context = store.for_store()
            health_result = context.check_services()
            
            return {
                "status": "healthy" if health_result["success"] else "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "details": health_result
            }
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Detailed health check failed: {e}")
    
    return app
```

## 🧪 测试最佳实践

### 1. 单元测试

```python
import pytest
from unittest.mock import Mock, patch
from mcpstore import MCPStore

class TestMCPStoreIntegration:
    """MCPStore 集成测试"""
    
    @pytest.fixture
    def mock_store(self):
        """模拟 MCPStore"""
        with patch('mcpstore.MCPStore.setup_store') as mock_setup:
            mock_store = Mock()
            mock_context = Mock()
            mock_store.for_store.return_value = mock_context
            mock_setup.return_value = mock_store
            yield mock_store, mock_context
    
    def test_service_registration(self, mock_store):
        """测试服务注册"""
        store, context = mock_store
        
        # 配置模拟
        context.add_service.return_value = context
        context.list_services.return_value = [
            Mock(name="test-service", status="healthy")
        ]
        
        # 执行测试
        context.add_service({"name": "test-service", "url": "https://test.com/mcp"})
        services = context.list_services()
        
        # 验证结果
        assert len(services) == 1
        assert services[0].name == "test-service"
        context.add_service.assert_called_once()
    
    def test_tool_calling(self, mock_store):
        """测试工具调用"""
        store, context = mock_store
        
        # 配置模拟
        context.call_tool.return_value = {"result": "success"}
        
        # 执行测试
        result = context.call_tool("test_tool", {"param": "value"})
        
        # 验证结果
        assert result["result"] == "success"
        context.call_tool.assert_called_once_with("test_tool", {"param": "value"})
```

### 2. 集成测试

```python
import pytest
import tempfile
import json
from pathlib import Path

class TestMCPStoreIntegration:
    """MCPStore 真实集成测试"""
    
    @pytest.fixture
    def temp_config(self):
        """创建临时配置文件"""
        config = {
            "mcpServers": {
                "test-service": {
                    "command": "echo",
                    "args": ["Hello, MCP!"]
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_path = f.name
        
        yield config_path
        
        # 清理
        Path(config_path).unlink(missing_ok=True)
    
    def test_real_service_integration(self, temp_config):
        """测试真实服务集成"""
        store = MCPStore.setup_store(mcp_config_file=temp_config)
        context = store.for_store()
        
        # 测试服务列表
        services = context.list_services()
        assert len(services) >= 0  # 可能没有服务，但不应该出错
        
        # 测试工具列表
        tools = context.list_tools()
        assert isinstance(tools, list)
```

## 📦 部署最佳实践

### 1. 容器化部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 mcpstore && \
    chown -R mcpstore:mcpstore /app
USER mcpstore

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:18200/health || exit 1

# 暴露端口
EXPOSE 18200

# 启动命令
CMD ["python", "-m", "mcpstore.cli", "run", "api", "--host", "0.0.0.0"]
```

### 2. 生产环境配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  mcpstore:
    build: .
    ports:
      - "18200:18200"
    volumes:
      - ./config:/app/config:ro
      - ./logs:/app/logs
    environment:
      - MCPSTORE_CONFIG=/app/config/mcp.json
      - LOG_LEVEL=info
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:18200/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - mcpstore
    restart: unless-stopped
```

### 3. 监控和告警

```python
# monitoring.py
import psutil
import time
from prometheus_client import start_http_server, Gauge, Counter, Histogram

class MCPStoreMetrics:
    """MCPStore 指标收集器"""
    
    def __init__(self):
        # 定义指标
        self.active_services = Gauge('mcpstore_active_services', 'Number of active services')
        self.tool_calls = Counter('mcpstore_tool_calls_total', 'Total tool calls', ['tool_name', 'status'])
        self.response_time = Histogram('mcpstore_response_time_seconds', 'Response time', ['operation'])
        self.memory_usage = Gauge('mcpstore_memory_usage_bytes', 'Memory usage in bytes')
        self.cpu_usage = Gauge('mcpstore_cpu_usage_percent', 'CPU usage percentage')
        
        # 启动指标服务器
        start_http_server(8000)
    
    def update_system_metrics(self):
        """更新系统指标"""
        process = psutil.Process()
        self.memory_usage.set(process.memory_info().rss)
        self.cpu_usage.set(process.cpu_percent())
    
    def record_tool_call(self, tool_name: str, success: bool, duration: float):
        """记录工具调用指标"""
        status = 'success' if success else 'error'
        self.tool_calls.labels(tool_name=tool_name, status=status).inc()
        self.response_time.labels(operation='tool_call').observe(duration)

# 使用示例
metrics = MCPStoreMetrics()

def monitored_tool_call(context, tool_name: str, args: dict):
    """带指标收集的工具调用"""
    start_time = time.time()
    try:
        result = context.call_tool(tool_name, args)
        duration = time.time() - start_time
        metrics.record_tool_call(tool_name, True, duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        metrics.record_tool_call(tool_name, False, duration)
        raise
```

## 📋 检查清单

### 🚀 部署前检查

- [ ] 配置文件格式正确且已验证
- [ ] 环境变量已正确设置
- [ ] 敏感信息未硬编码
- [ ] 监控配置适合环境（开发/生产）
- [ ] 日志级别配置正确
- [ ] 健康检查端点正常工作
- [ ] 错误处理机制完善
- [ ] 资源限制已配置
- [ ] 备份和恢复策略已制定

### 🔧 性能优化检查

- [ ] 使用缓存优先架构
- [ ] 异步操作替代同步操作
- [ ] 批量操作减少网络开销
- [ ] 连接池配置合理
- [ ] 超时设置适当
- [ ] 重试机制已实现
- [ ] 资源清理机制完善

### 🔒 安全检查

- [ ] 敏感信息使用环境变量
- [ ] 访问控制机制已实现
- [ ] 输入验证完善
- [ ] 错误信息不暴露敏感数据
- [ ] 日志记录不包含敏感信息
- [ ] HTTPS 配置正确（生产环境）
- [ ] 防火墙规则已配置

## 相关文档

- [核心概念](concepts.md) - 理解设计理念
- [系统架构](architecture.md) - 了解架构设计
- [插件开发](plugin-development.md) - 扩展功能
- [自定义适配器](custom-adapters.md) - 集成其他框架

## 下一步

- 查看 [API 参考文档](../api-reference/mcpstore-class.md)
- 学习 [服务注册方法](../services/registration/register-service.md)
- 了解 [工具调用方法](../tools/usage/call-tool.md)
