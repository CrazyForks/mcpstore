# 迁移指南

## 📋 概述

本指南帮助您从其他 MCP 客户端或旧版本的 MCPStore 迁移到最新版本。我们提供了详细的迁移步骤、兼容性说明和最佳实践。

## 🔄 从其他 MCP 客户端迁移

### 从原生 MCP 客户端迁移

```python
# 原生 MCP 客户端代码示例
"""
import mcp
from mcp.client import Client
from mcp.transport.stdio import StdioTransport

# 原生方式
transport = StdioTransport("npx", ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"])
client = Client(transport)

async def old_way():
    await client.connect()
    
    # 列出工具
    tools = await client.list_tools()
    
    # 调用工具
    result = await client.call_tool("read_file", {"path": "/tmp/test.txt"})
    
    await client.disconnect()
"""

# 迁移到 MCPStore
from mcpstore import MCPStore

def migrate_from_native_mcp():
    """从原生 MCP 迁移到 MCPStore"""
    
    # 1. 初始化 MCPStore（更简单）
    store = MCPStore()
    
    # 2. 添加服务（配置格式更友好）
    store.add_service({
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        }
    })
    
    # 3. 列出工具（同步调用，更简单）
    tools = store.list_tools()
    print(f"✅ 迁移完成，发现 {len(tools)} 个工具")
    
    # 4. 调用工具（同步调用）
    result = store.call_tool("read_file", {"path": "/tmp/test.txt"})
    print(f"📄 文件内容: {result}")
    
    return store

# 执行迁移
migrated_store = migrate_from_native_mcp()
```

### 从 LangChain MCP 适配器迁移

```python
# LangChain MCP 适配器代码示例
"""
from langchain_mcp import MCPToolkit
from langchain.agents import initialize_agent

# 原有方式
toolkit = MCPToolkit()
toolkit.add_server("filesystem", "npx", ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"])

tools = toolkit.get_tools()
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
"""

# 迁移到 MCPStore + LangChain 集成
from mcpstore import MCPStore
from mcpstore.langchain import MCPStoreLangChainAdapter

def migrate_from_langchain_mcp():
    """从 LangChain MCP 适配器迁移"""
    
    # 1. 创建 MCPStore
    store = MCPStore()
    
    # 2. 添加服务
    store.add_service({
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            }
        }
    })
    
    # 3. 创建 LangChain 适配器
    adapter = MCPStoreLangChainAdapter(store)
    tools = adapter.get_langchain_tools()
    
    # 4. 使用现有的 LangChain 代码
    from langchain.agents import initialize_agent, AgentType
    from langchain.llms import OpenAI
    
    agent = initialize_agent(
        tools, 
        OpenAI(temperature=0), 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    
    print(f"✅ LangChain 迁移完成，{len(tools)} 个工具可用")
    return agent

# 执行迁移
migrated_agent = migrate_from_langchain_mcp()
```

## 📈 版本升级指南

### 从 MCPStore 0.x 升级到 1.x

```python
# MCPStore 0.x 代码示例
"""
from mcpstore_old import MCPClient

# 旧版本方式
client = MCPClient()
client.register_service("filesystem", {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
})

# 旧的工具调用方式
result = client.invoke_tool("filesystem", "read_file", {"path": "/tmp/test.txt"})
"""

# 升级到 MCPStore 1.x
from mcpstore import MCPStore

class MCPStoreUpgrader:
    """MCPStore 升级助手"""
    
    def __init__(self):
        self.migration_log = []
    
    def upgrade_from_0x(self, old_config):
        """从 0.x 版本升级"""
        
        # 1. 创建新的 MCPStore 实例
        store = MCPStore()
        
        # 2. 迁移服务配置
        new_config = self._convert_service_config(old_config)
        store.add_service(new_config)
        
        # 3. 验证迁移
        self._verify_migration(store, old_config)
        
        return store
    
    def _convert_service_config(self, old_config):
        """转换服务配置格式"""
        new_config = {"mcpServers": {}}
        
        for service_name, service_config in old_config.items():
            # 转换配置格式
            if isinstance(service_config, dict):
                new_config["mcpServers"][service_name] = {
                    "command": service_config.get("command"),
                    "args": service_config.get("args", []),
                    "env": service_config.get("env", {})
                }
            
            self.migration_log.append(f"✅ 转换服务配置: {service_name}")
        
        return new_config
    
    def _verify_migration(self, store, old_config):
        """验证迁移结果"""
        # 检查服务数量
        services = store.list_services()
        expected_count = len(old_config)
        actual_count = len(services)
        
        if actual_count == expected_count:
            self.migration_log.append(f"✅ 服务数量验证通过: {actual_count}/{expected_count}")
        else:
            self.migration_log.append(f"⚠️ 服务数量不匹配: {actual_count}/{expected_count}")
        
        # 检查工具可用性
        tools = store.list_tools()
        self.migration_log.append(f"✅ 发现工具: {len(tools)} 个")
    
    def get_migration_report(self):
        """获取迁移报告"""
        return "\n".join(self.migration_log)

# 使用升级助手
upgrader = MCPStoreUpgrader()

# 旧版本配置示例
old_config = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    },
    "web_search": {
        "command": "python",
        "args": ["-m", "web_search_server"]
    }
}

# 执行升级
new_store = upgrader.upgrade_from_0x(old_config)
print("📊 升级报告:")
print(upgrader.get_migration_report())
```

### API 变更对照表

```python
class APIChangesGuide:
    """API 变更指南"""
    
    def __init__(self):
        self.api_changes = {
            # 服务管理
            "register_service": {
                "old": "client.register_service(name, config)",
                "new": "store.add_service({'mcpServers': {name: config}})",
                "breaking": True,
                "migration": self._migrate_register_service
            },
            
            # 工具调用
            "invoke_tool": {
                "old": "client.invoke_tool(service, tool, args)",
                "new": "store.call_tool(tool_name, args)",
                "breaking": True,
                "migration": self._migrate_invoke_tool
            },
            
            # 工具列表
            "get_tools": {
                "old": "client.get_tools(service)",
                "new": "store.list_tools(service_name=service)",
                "breaking": False,
                "migration": self._migrate_get_tools
            },
            
            # 服务状态
            "service_status": {
                "old": "client.check_service(name)",
                "new": "store.get_service_status(name)",
                "breaking": False,
                "migration": self._migrate_service_status
            }
        }
    
    def _migrate_register_service(self, old_call):
        """迁移服务注册调用"""
        # 解析旧调用
        # client.register_service("filesystem", config)
        # 转换为新调用
        # store.add_service({"mcpServers": {"filesystem": config}})
        return "store.add_service({'mcpServers': {name: config}})"
    
    def _migrate_invoke_tool(self, old_call):
        """迁移工具调用"""
        # 解析旧调用
        # client.invoke_tool("filesystem", "read_file", {"path": "/tmp/test.txt"})
        # 转换为新调用
        # store.call_tool("read_file", {"path": "/tmp/test.txt"})
        return "store.call_tool(tool_name, args)"
    
    def _migrate_get_tools(self, old_call):
        """迁移工具列表获取"""
        return "store.list_tools(service_name=service)"
    
    def _migrate_service_status(self, old_call):
        """迁移服务状态检查"""
        return "store.get_service_status(name)"
    
    def generate_migration_script(self, old_code):
        """生成迁移脚本"""
        migration_script = []
        
        migration_script.append("# MCPStore 迁移脚本")
        migration_script.append("from mcpstore import MCPStore")
        migration_script.append("")
        migration_script.append("# 初始化新的 MCPStore")
        migration_script.append("store = MCPStore()")
        migration_script.append("")
        
        # 分析旧代码并生成迁移建议
        for api_name, change_info in self.api_changes.items():
            if api_name in old_code:
                migration_script.append(f"# 迁移 {api_name}")
                migration_script.append(f"# 旧方式: {change_info['old']}")
                migration_script.append(f"# 新方式: {change_info['new']}")
                
                if change_info['breaking']:
                    migration_script.append("# ⚠️ 这是破坏性变更，需要修改代码")
                else:
                    migration_script.append("# ✅ 这是兼容性变更，建议更新")
                
                migration_script.append("")
        
        return "\n".join(migration_script)

# 使用 API 变更指南
api_guide = APIChangesGuide()

old_code_example = """
client.register_service("filesystem", config)
result = client.invoke_tool("filesystem", "read_file", args)
tools = client.get_tools("filesystem")
"""

migration_script = api_guide.generate_migration_script(old_code_example)
print("🔄 迁移脚本:")
print(migration_script)
```

## 🛠️ 配置迁移工具

### 自动配置转换器

```python
import json
import yaml
from pathlib import Path

class ConfigMigrationTool:
    """配置迁移工具"""
    
    def __init__(self):
        self.supported_formats = ['json', 'yaml', 'toml']
        self.conversion_rules = {
            'service_name_mapping': {},
            'parameter_mapping': {},
            'deprecated_options': []
        }
    
    def migrate_config_file(self, input_file, output_file=None):
        """迁移配置文件"""
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {input_file}")
        
        # 读取旧配置
        old_config = self._read_config_file(input_path)
        
        # 转换配置
        new_config = self._convert_config(old_config)
        
        # 写入新配置
        if output_file is None:
            output_file = input_path.parent / f"mcpstore_{input_path.name}"
        
        self._write_config_file(Path(output_file), new_config)
        
        return output_file
    
    def _read_config_file(self, file_path):
        """读取配置文件"""
        suffix = file_path.suffix.lower()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if suffix == '.json':
                return json.load(f)
            elif suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif suffix == '.toml':
                import tomli
                return tomli.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {suffix}")
    
    def _write_config_file(self, file_path, config):
        """写入配置文件"""
        suffix = file_path.suffix.lower()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            if suffix == '.json':
                json.dump(config, f, indent=2, ensure_ascii=False)
            elif suffix in ['.yaml', '.yml']:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            elif suffix == '.toml':
                import tomli_w
                tomli_w.dump(config, f)
    
    def _convert_config(self, old_config):
        """转换配置格式"""
        new_config = {
            "mcpServers": {}
        }
        
        # 处理不同的旧配置格式
        if "services" in old_config:
            # 格式1: {"services": {"name": config}}
            for name, config in old_config["services"].items():
                new_config["mcpServers"][name] = self._convert_service_config(config)
        
        elif "mcp_servers" in old_config:
            # 格式2: {"mcp_servers": {"name": config}}
            for name, config in old_config["mcp_servers"].items():
                new_config["mcpServers"][name] = self._convert_service_config(config)
        
        else:
            # 格式3: 直接是服务配置
            for name, config in old_config.items():
                if isinstance(config, dict):
                    new_config["mcpServers"][name] = self._convert_service_config(config)
        
        return new_config
    
    def _convert_service_config(self, old_service_config):
        """转换单个服务配置"""
        new_service_config = {}
        
        # 映射常见字段
        field_mapping = {
            'cmd': 'command',
            'executable': 'command',
            'arguments': 'args',
            'parameters': 'args',
            'environment': 'env',
            'env_vars': 'env'
        }
        
        for old_field, new_field in field_mapping.items():
            if old_field in old_service_config:
                new_service_config[new_field] = old_service_config[old_field]
        
        # 直接复制标准字段
        standard_fields = ['command', 'args', 'env', 'cwd', 'timeout']
        for field in standard_fields:
            if field in old_service_config:
                new_service_config[field] = old_service_config[field]
        
        return new_service_config
    
    def validate_migrated_config(self, config_file):
        """验证迁移后的配置"""
        try:
            # 尝试使用新配置创建 MCPStore
            from mcpstore import MCPStore
            
            config_path = Path(config_file)
            config = self._read_config_file(config_path)
            
            store = MCPStore()
            store.add_service(config)
            
            # 检查服务
            services = store.list_services()
            
            validation_result = {
                'valid': True,
                'services_count': len(services),
                'services': [s['name'] for s in services],
                'errors': []
            }
            
            return validation_result
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'services_count': 0,
                'services': [],
                'errors': [str(e)]
            }

# 使用配置迁移工具
migration_tool = ConfigMigrationTool()

# 创建示例旧配置
old_config_example = {
    "services": {
        "filesystem": {
            "cmd": "npx",
            "arguments": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        },
        "web_search": {
            "executable": "python",
            "parameters": ["-m", "web_search_server"],
            "env_vars": {"API_KEY": "test"}
        }
    }
}

# 保存示例配置
with open("old_config.json", "w") as f:
    json.dump(old_config_example, f, indent=2)

# 执行迁移
try:
    output_file = migration_tool.migrate_config_file("old_config.json")
    print(f"✅ 配置迁移完成: {output_file}")
    
    # 验证迁移结果
    validation = migration_tool.validate_migrated_config(output_file)
    if validation['valid']:
        print(f"✅ 配置验证通过: {validation['services_count']} 个服务")
        print(f"   服务列表: {validation['services']}")
    else:
        print(f"❌ 配置验证失败: {validation['error']}")
        
except Exception as e:
    print(f"❌ 迁移失败: {e}")
```

## 📋 迁移检查清单

### 迁移前准备

- [ ] 备份现有配置和代码
- [ ] 确认 MCPStore 版本兼容性
- [ ] 检查依赖项版本
- [ ] 准备测试环境

### 迁移过程

- [ ] 安装新版本 MCPStore
- [ ] 转换配置文件格式
- [ ] 更新代码中的 API 调用
- [ ] 测试基本功能
- [ ] 验证工具调用
- [ ] 检查性能表现

### 迁移后验证

- [ ] 所有服务正常启动
- [ ] 工具列表完整
- [ ] 工具调用功能正常
- [ ] 性能满足要求
- [ ] 错误处理正常
- [ ] 日志记录正常

## 🔗 相关文档

- [快速开始](../getting-started/quick-demo.md)
- [配置指南](../configuration.md)
- [API 参考](../api/reference.md)
- [故障排除](../troubleshooting.md)

## 📚 迁移最佳实践

1. **渐进迁移**：分阶段迁移，降低风险
2. **充分测试**：在测试环境充分验证后再部署
3. **保留备份**：保留旧版本配置和代码备份
4. **文档更新**：及时更新相关文档和注释
5. **团队培训**：确保团队成员了解新版本特性
6. **监控观察**：迁移后密切监控系统运行状态

---

**更新时间**: 2025-01-09  
**版本**: 1.0.0
