# 配置指南

## 📋 概述

MCPStore 提供了灵活的配置系统，支持多种配置方式和格式。本文档详细介绍如何配置 MCPStore 以满足不同的使用场景和需求。

## 🔧 基础配置

### 初始化配置

```python
from mcpstore import MCPStore

# 基础初始化
store = MCPStore()

# 带配置的初始化
store = MCPStore(config={
    "data_dir": "/path/to/data",
    "log_level": "INFO",
    "timeout": 30,
    "max_connections": 10
})
```

### 配置文件格式

MCPStore 支持多种配置文件格式：

#### JSON 格式

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": {
        "NODE_ENV": "production"
      },
      "timeout": 30
    },
    "web_search": {
      "command": "python",
      "args": ["-m", "web_search_server"],
      "cwd": "/path/to/server",
      "env": {
        "API_KEY": "${WEB_SEARCH_API_KEY}"
      }
    }
  },
  "global": {
    "timeout": 60,
    "retry_count": 3,
    "log_level": "INFO"
  }
}
```

#### YAML 格式

```yaml
mcpServers:
  filesystem:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "/tmp"
    env:
      NODE_ENV: production
    timeout: 30
  
  web_search:
    command: python
    args:
      - "-m"
      - "web_search_server"
    cwd: "/path/to/server"
    env:
      API_KEY: "${WEB_SEARCH_API_KEY}"

global:
  timeout: 60
  retry_count: 3
  log_level: INFO
```

## ⚙️ 详细配置选项

### 全局配置

```python
global_config = {
    # 基础设置
    "data_dir": "/path/to/mcpstore/data",  # 数据目录
    "log_level": "INFO",                   # 日志级别: DEBUG, INFO, WARNING, ERROR
    "log_file": "/path/to/mcpstore.log",   # 日志文件路径
    
    # 连接设置
    "timeout": 30,                         # 默认超时时间（秒）
    "max_connections": 10,                 # 最大连接数
    "connection_pool_size": 5,             # 连接池大小
    "keepalive_interval": 60,              # 心跳间隔（秒）
    
    # 重试设置
    "retry_count": 3,                      # 重试次数
    "retry_delay": 1.0,                    # 重试延迟（秒）
    "exponential_backoff": True,           # 指数退避
    
    # 缓存设置
    "enable_cache": True,                  # 启用缓存
    "cache_size": 1000,                    # 缓存大小
    "cache_ttl": 300,                      # 缓存TTL（秒）
    
    # 监控设置
    "enable_monitoring": True,             # 启用监控
    "monitoring_interval": 30,             # 监控间隔（秒）
    "health_check_interval": 60,           # 健康检查间隔（秒）
    
    # 安全设置
    "enable_auth": False,                  # 启用认证
    "auth_token": None,                    # 认证令牌
    "allowed_hosts": ["localhost"],        # 允许的主机
    
    # 性能设置
    "max_workers": 5,                      # 最大工作线程数
    "batch_size": 10,                      # 批量操作大小
    "async_mode": False                    # 异步模式
}
```

### 服务配置

```python
service_config = {
    # 基础配置
    "command": "npx",                      # 启动命令
    "args": ["-y", "server-package"],      # 命令参数
    "cwd": "/path/to/working/dir",         # 工作目录
    "env": {                               # 环境变量
        "NODE_ENV": "production",
        "API_KEY": "${API_KEY}"
    },
    
    # 连接配置
    "timeout": 30,                         # 连接超时
    "retry_count": 3,                      # 重试次数
    "retry_delay": 1.0,                    # 重试延迟
    
    # 健康检查
    "health_check": {
        "enabled": True,
        "interval": 60,                    # 检查间隔
        "timeout": 10,                     # 检查超时
        "max_failures": 3                  # 最大失败次数
    },
    
    # 资源限制
    "resources": {
        "memory_limit": "512MB",           # 内存限制
        "cpu_limit": "1.0",                # CPU限制
        "disk_limit": "1GB"                # 磁盘限制
    },
    
    # 日志配置
    "logging": {
        "level": "INFO",
        "file": "/path/to/service.log",
        "max_size": "10MB",
        "backup_count": 5
    },
    
    # 自定义配置
    "custom": {
        "feature_flags": ["feature1", "feature2"],
        "api_version": "v1",
        "debug_mode": False
    }
}
```

## 📁 配置文件管理

### 配置文件位置

MCPStore 按以下顺序查找配置文件：

1. 命令行指定的配置文件
2. 当前目录的 `mcpstore.json`
3. 用户主目录的 `.mcpstore/config.json`
4. 系统配置目录的 `mcpstore/config.json`

```python
from mcpstore import MCPStore

# 指定配置文件
store = MCPStore(config_file="/path/to/config.json")

# 使用默认配置文件查找顺序
store = MCPStore()
```

### 配置文件加载

```python
import json
import yaml
from pathlib import Path

class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def load_from_file(config_file):
        """从文件加载配置"""
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        suffix = config_path.suffix.lower()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if suffix == '.json':
                return json.load(f)
            elif suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {suffix}")
    
    @staticmethod
    def save_to_file(config, config_file):
        """保存配置到文件"""
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        suffix = config_path.suffix.lower()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if suffix == '.json':
                json.dump(config, f, indent=2, ensure_ascii=False)
            elif suffix in ['.yaml', '.yml']:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

# 使用配置加载器
config = ConfigLoader.load_from_file("config.yaml")
store = MCPStore(config=config)
```

## 🔐 环境变量配置

### 环境变量支持

MCPStore 支持通过环境变量进行配置：

```bash
# 基础配置
export MCPSTORE_DATA_DIR="/path/to/data"
export MCPSTORE_LOG_LEVEL="DEBUG"
export MCPSTORE_TIMEOUT="60"

# 连接配置
export MCPSTORE_MAX_CONNECTIONS="20"
export MCPSTORE_RETRY_COUNT="5"

# 缓存配置
export MCPSTORE_CACHE_SIZE="2000"
export MCPSTORE_CACHE_TTL="600"

# 监控配置
export MCPSTORE_MONITORING_INTERVAL="15"
export MCPSTORE_HEALTH_CHECK_INTERVAL="30"
```

### 环境变量替换

配置文件中可以使用环境变量：

```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["-m", "database_server"],
      "env": {
        "DB_HOST": "${DATABASE_HOST}",
        "DB_PORT": "${DATABASE_PORT:-5432}",
        "DB_USER": "${DATABASE_USER}",
        "DB_PASSWORD": "${DATABASE_PASSWORD}"
      }
    }
  }
}
```

```python
import os
import re

class EnvironmentVariableResolver:
    """环境变量解析器"""
    
    @staticmethod
    def resolve_config(config):
        """解析配置中的环境变量"""
        if isinstance(config, dict):
            return {k: EnvironmentVariableResolver.resolve_config(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [EnvironmentVariableResolver.resolve_config(item) for item in config]
        elif isinstance(config, str):
            return EnvironmentVariableResolver._resolve_string(config)
        else:
            return config
    
    @staticmethod
    def _resolve_string(value):
        """解析字符串中的环境变量"""
        # 支持 ${VAR} 和 ${VAR:-default} 格式
        pattern = r'\$\{([^}]+)\}'
        
        def replacer(match):
            var_expr = match.group(1)
            
            if ':-' in var_expr:
                var_name, default_value = var_expr.split(':-', 1)
                return os.getenv(var_name, default_value)
            else:
                return os.getenv(var_expr, match.group(0))
        
        return re.sub(pattern, replacer, value)

# 使用环境变量解析器
config = ConfigLoader.load_from_file("config.json")
resolved_config = EnvironmentVariableResolver.resolve_config(config)
store = MCPStore(config=resolved_config)
```

## 🎛️ 动态配置

### 运行时配置更新

```python
class DynamicConfig:
    """动态配置管理"""
    
    def __init__(self, store):
        self.store = store
        self.config_watchers = []
    
    def update_global_config(self, new_config):
        """更新全局配置"""
        # 验证配置
        self._validate_config(new_config)
        
        # 应用配置
        self.store.update_config(new_config)
        
        # 通知观察者
        self._notify_config_change('global', new_config)
    
    def update_service_config(self, service_name, new_config):
        """更新服务配置"""
        # 验证服务配置
        self._validate_service_config(new_config)
        
        # 重启服务以应用新配置
        if self.store.get_service_status(service_name) == 'running':
            self.store.stop_service(service_name)
            self.store.update_service_config(service_name, new_config)
            self.store.start_service(service_name)
        else:
            self.store.update_service_config(service_name, new_config)
        
        # 通知观察者
        self._notify_config_change('service', {service_name: new_config})
    
    def add_config_watcher(self, callback):
        """添加配置变更观察者"""
        self.config_watchers.append(callback)
    
    def _validate_config(self, config):
        """验证配置"""
        required_fields = ['timeout', 'max_connections']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"缺少必需的配置字段: {field}")
    
    def _validate_service_config(self, config):
        """验证服务配置"""
        if 'command' not in config:
            raise ValueError("服务配置必须包含 command 字段")
    
    def _notify_config_change(self, config_type, config):
        """通知配置变更"""
        for watcher in self.config_watchers:
            try:
                watcher(config_type, config)
            except Exception as e:
                print(f"配置观察者错误: {e}")

# 使用动态配置
dynamic_config = DynamicConfig(store)

# 添加配置观察者
def on_config_change(config_type, config):
    print(f"配置已更新: {config_type}")

dynamic_config.add_config_watcher(on_config_change)

# 更新配置
new_global_config = {
    "timeout": 45,
    "max_connections": 15,
    "log_level": "DEBUG"
}

dynamic_config.update_global_config(new_global_config)
```

## 📊 配置验证

### 配置模式验证

```python
import jsonschema

class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.global_schema = {
            "type": "object",
            "properties": {
                "timeout": {"type": "number", "minimum": 1},
                "max_connections": {"type": "integer", "minimum": 1},
                "log_level": {"enum": ["DEBUG", "INFO", "WARNING", "ERROR"]},
                "retry_count": {"type": "integer", "minimum": 0},
                "cache_size": {"type": "integer", "minimum": 0}
            },
            "required": ["timeout", "max_connections"]
        }
        
        self.service_schema = {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "args": {"type": "array", "items": {"type": "string"}},
                "env": {"type": "object"},
                "timeout": {"type": "number", "minimum": 1},
                "retry_count": {"type": "integer", "minimum": 0}
            },
            "required": ["command"]
        }
    
    def validate_global_config(self, config):
        """验证全局配置"""
        try:
            jsonschema.validate(config, self.global_schema)
            return True, None
        except jsonschema.ValidationError as e:
            return False, str(e)
    
    def validate_service_config(self, config):
        """验证服务配置"""
        try:
            jsonschema.validate(config, self.service_schema)
            return True, None
        except jsonschema.ValidationError as e:
            return False, str(e)
    
    def validate_full_config(self, config):
        """验证完整配置"""
        errors = []
        
        # 验证全局配置
        if 'global' in config:
            valid, error = self.validate_global_config(config['global'])
            if not valid:
                errors.append(f"全局配置错误: {error}")
        
        # 验证服务配置
        if 'mcpServers' in config:
            for service_name, service_config in config['mcpServers'].items():
                valid, error = self.validate_service_config(service_config)
                if not valid:
                    errors.append(f"服务 {service_name} 配置错误: {error}")
        
        return len(errors) == 0, errors

# 使用配置验证器
validator = ConfigValidator()

config = {
    "global": {
        "timeout": 30,
        "max_connections": 10,
        "log_level": "INFO"
    },
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
    }
}

valid, errors = validator.validate_full_config(config)
if valid:
    print("✅ 配置验证通过")
else:
    print("❌ 配置验证失败:")
    for error in errors:
        print(f"  - {error}")
```

## 🔧 配置最佳实践

### 1. 分层配置

```python
# 基础配置
base_config = {
    "timeout": 30,
    "retry_count": 3,
    "log_level": "INFO"
}

# 开发环境配置
dev_config = {
    **base_config,
    "log_level": "DEBUG",
    "enable_monitoring": False
}

# 生产环境配置
prod_config = {
    **base_config,
    "timeout": 60,
    "max_connections": 20,
    "enable_monitoring": True
}
```

### 2. 配置模板

```python
def create_service_config_template(service_type):
    """创建服务配置模板"""
    templates = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "${BASE_PATH}"],
            "timeout": 30
        },
        "web_search": {
            "command": "python",
            "args": ["-m", "web_search_server"],
            "env": {"API_KEY": "${API_KEY}"},
            "timeout": 60
        },
        "database": {
            "command": "python",
            "args": ["-m", "database_server"],
            "env": {
                "DB_HOST": "${DB_HOST}",
                "DB_PORT": "${DB_PORT:-5432}",
                "DB_USER": "${DB_USER}",
                "DB_PASSWORD": "${DB_PASSWORD}"
            },
            "timeout": 45
        }
    }
    
    return templates.get(service_type, {})
```

### 3. 配置安全

```python
import keyring
from cryptography.fernet import Fernet

class SecureConfig:
    """安全配置管理"""
    
    def __init__(self):
        self.cipher = Fernet(Fernet.generate_key())
    
    def encrypt_sensitive_value(self, value):
        """加密敏感值"""
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_sensitive_value(self, encrypted_value):
        """解密敏感值"""
        return self.cipher.decrypt(encrypted_value.encode()).decode()
    
    def store_secret(self, service, key, value):
        """存储密钥到系统密钥环"""
        keyring.set_password(service, key, value)
    
    def get_secret(self, service, key):
        """从系统密钥环获取密钥"""
        return keyring.get_password(service, key)

# 使用安全配置
secure_config = SecureConfig()

# 存储敏感信息
secure_config.store_secret("mcpstore", "api_key", "your-secret-api-key")

# 在配置中引用
config = {
    "mcpServers": {
        "web_search": {
            "command": "python",
            "args": ["-m", "web_search_server"],
            "env": {
                "API_KEY": secure_config.get_secret("mcpstore", "api_key")
            }
        }
    }
}
```

## 🔗 相关文档

- [快速开始](getting-started/quick-demo.md)
- [服务管理](services/management/service-management.md)
- [API 参考](api/reference.md)
- [故障排除](troubleshooting.md)

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0
