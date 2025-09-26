# create_safe_tool()

创建安全版本的工具（带验证）。

## 方法特性

- ✅ **异步版本**: `create_safe_tool_async()`
- ✅ **Store级别**: `store.for_store().create_safe_tool()`
- ✅ **Agent级别**: `store.for_agent("agent1").create_safe_tool()`
- 📁 **文件位置**: `advanced_features.py`
- 🏷️ **所属类**: `AdvancedFeaturesMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `original_tool` | `str` | ✅ | - | 原始工具名称 |
| `validation_rules` | `Dict[str, Any]` | ✅ | - | 验证规则字典 |

## 返回值

返回上下文对象，支持链式调用。

## 验证规则格式

```python
validation_rules = {
    # 参数验证
    "required_params": ["param1", "param2"],
    "optional_params": ["param3"],
    "param_types": {
        "param1": "str",
        "param2": "int",
        "param3": "bool"
    },
    "param_ranges": {
        "param2": {"min": 1, "max": 100}
    },
    "param_patterns": {
        "param1": r"^[a-zA-Z0-9_]+$"
    },
    
    # 文件安全验证
    "allowed_extensions": [".txt", ".json", ".csv"],
    "forbidden_paths": ["/etc", "/sys", "/proc"],
    "max_file_size": 1024 * 1024,  # 1MB
    
    # 网络安全验证
    "allowed_domains": ["api.example.com", "safe-api.com"],
    "forbidden_ips": ["127.0.0.1", "localhost"],
    "max_request_size": 1024,
    
    # 执行限制
    "max_execution_time": 30,  # 秒
    "max_memory_usage": 100,   # MB
    "rate_limit": {"calls": 10, "period": 60},  # 每分钟10次
    
    # 自定义验证函数
    "custom_validators": [
        {
            "name": "business_rule_check",
            "function": "validate_business_rules"
        }
    ]
}
```

## 使用示例

### Store级别创建安全工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 为文件操作创建安全工具
file_validation_rules = {
    "required_params": ["path"],
    "param_types": {
        "path": "str"
    },
    "param_patterns": {
        "path": r"^/tmp/[a-zA-Z0-9_\-\.]+$"  # 只允许/tmp目录下的安全文件名
    },
    "allowed_extensions": [".txt", ".json", ".csv", ".log"],
    "forbidden_paths": ["/etc", "/sys", "/proc", "/root"],
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "max_execution_time": 10
}

# 创建安全的文件读取工具
store.for_store().create_safe_tool(
    "filesystem_read_file",
    file_validation_rules
)

# 安全调用（会通过验证）
try:
    result = store.for_store().call_tool("filesystem_read_file", {
        "path": "/tmp/safe_file.txt"
    })
    print(f"安全读取成功: {result}")
except Exception as e:
    print(f"验证失败: {e}")

# 不安全调用（会被拒绝）
try:
    result = store.for_store().call_tool("filesystem_read_file", {
        "path": "/etc/passwd"  # 被forbidden_paths拒绝
    })
except Exception as e:
    print(f"安全验证拒绝: {e}")
```

### Agent级别创建安全工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式创建安全工具
agent_context = store.for_agent("agent1")

# 为数据库查询创建安全工具
db_validation_rules = {
    "required_params": ["query"],
    "param_types": {
        "query": "str",
        "limit": "int"
    },
    "param_patterns": {
        "query": r"^SELECT\s+.*$"  # 只允许SELECT查询
    },
    "param_ranges": {
        "limit": {"min": 1, "max": 1000}
    },
    "rate_limit": {"calls": 50, "period": 60},  # 每分钟50次查询
    "max_execution_time": 30
}

agent_context.create_safe_tool(
    "database_execute_query",
    db_validation_rules
)

# Agent安全查询
try:
    result = agent_context.call_tool("database_execute_query", {
        "query": "SELECT * FROM users WHERE active = 1",
        "limit": 100
    })
    print(f"Agent安全查询成功")
except Exception as e:
    print(f"Agent验证失败: {e}")
```

### 网络API安全工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 为网络API创建安全工具
api_validation_rules = {
    "required_params": ["url"],
    "optional_params": ["method", "headers", "data"],
    "param_types": {
        "url": "str",
        "method": "str",
        "data": "dict"
    },
    "param_patterns": {
        "url": r"^https://api\.safe-domain\.com/.*$",
        "method": r"^(GET|POST)$"
    },
    "allowed_domains": ["api.safe-domain.com"],
    "max_request_size": 1024,
    "rate_limit": {"calls": 100, "period": 3600},  # 每小时100次
    "max_execution_time": 15
}

store.for_store().create_safe_tool(
    "http_request",
    api_validation_rules
)

# 安全的API调用
try:
    result = store.for_store().call_tool("http_request", {
        "url": "https://api.safe-domain.com/data",
        "method": "GET"
    })
    print(f"安全API调用成功")
except Exception as e:
    print(f"API安全验证失败: {e}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_create_safe_tools():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步创建安全工具
    validation_rules = {
        "required_params": ["input"],
        "param_types": {"input": "str"},
        "max_execution_time": 5
    }
    
    await store.for_store().create_safe_tool_async(
        "text_processor",
        validation_rules
    )
    
    # 异步安全调用
    result = await store.for_store().call_tool_async("text_processor", {
        "input": "Hello, World!"
    })
    
    print(f"异步安全处理结果: {result}")
    return result

# 运行异步创建
result = asyncio.run(async_create_safe_tools())
```

### 自定义验证函数

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

def validate_business_rules(params):
    """自定义业务规则验证"""
    
    # 示例：验证用户权限
    user_id = params.get("user_id")
    if user_id and user_id in ["admin", "root"]:
        raise ValueError("不允许操作管理员账户")
    
    # 示例：验证时间范围
    import datetime
    current_hour = datetime.datetime.now().hour
    if current_hour < 9 or current_hour > 17:
        raise ValueError("只允许在工作时间（9-17点）执行此操作")
    
    # 示例：验证数据完整性
    if "email" in params:
        email = params["email"]
        if "@" not in email or "." not in email:
            raise ValueError("邮箱格式不正确")
    
    return True

# 注册自定义验证函数
validation_rules = {
    "required_params": ["user_id", "action"],
    "param_types": {
        "user_id": "str",
        "action": "str"
    },
    "custom_validators": [
        {
            "name": "business_rule_check",
            "function": validate_business_rules
        }
    ]
}

store.for_store().create_safe_tool(
    "user_management_tool",
    validation_rules
)

# 测试自定义验证
try:
    result = store.for_store().call_tool("user_management_tool", {
        "user_id": "normal_user",
        "action": "update_profile",
        "email": "user@example.com"
    })
    print(f"自定义验证通过")
except Exception as e:
    print(f"自定义验证失败: {e}")
```

### 批量创建安全工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 定义不同类型工具的安全规则模板
security_templates = {
    "file_operations": {
        "allowed_extensions": [".txt", ".json", ".csv"],
        "forbidden_paths": ["/etc", "/sys", "/proc"],
        "max_file_size": 10 * 1024 * 1024,
        "max_execution_time": 10
    },
    "database_operations": {
        "param_patterns": {
            "query": r"^SELECT\s+.*$"
        },
        "rate_limit": {"calls": 50, "period": 60},
        "max_execution_time": 30
    },
    "network_operations": {
        "allowed_domains": ["api.safe-domain.com"],
        "max_request_size": 1024,
        "rate_limit": {"calls": 100, "period": 3600},
        "max_execution_time": 15
    }
}

# 工具分类映射
tool_categories = {
    "filesystem_read_file": "file_operations",
    "filesystem_write_file": "file_operations",
    "database_execute_query": "database_operations",
    "http_request": "network_operations"
}

# 批量创建安全工具
context = store.for_store()
for tool_name, category in tool_categories.items():
    if category in security_templates:
        rules = security_templates[category].copy()
        
        # 为每个工具添加通用规则
        rules.update({
            "required_params": ["path"] if "file" in tool_name else ["query"] if "database" in tool_name else ["url"],
            "max_execution_time": rules.get("max_execution_time", 30)
        })
        
        try:
            context.create_safe_tool(tool_name, rules)
            print(f"✅ 创建安全工具: {tool_name}")
        except Exception as e:
            print(f"❌ 创建失败 {tool_name}: {e}")

print("批量安全工具创建完成")
```

### 安全工具监控

```python
from mcpstore import MCPStore
import time

# 初始化
store = MCPStore.setup_store()

class SafeToolMonitor:
    """安全工具监控器"""
    
    def __init__(self, context):
        self.context = context
        self.violation_log = []
    
    def log_violation(self, tool_name, violation_type, details):
        """记录安全违规"""
        violation = {
            "timestamp": time.time(),
            "tool_name": tool_name,
            "violation_type": violation_type,
            "details": details
        }
        self.violation_log.append(violation)
        print(f"🚨 安全违规: {tool_name} - {violation_type}: {details}")
    
    def get_violation_stats(self):
        """获取违规统计"""
        if not self.violation_log:
            return {"total": 0, "by_type": {}, "by_tool": {}}
        
        by_type = {}
        by_tool = {}
        
        for violation in self.violation_log:
            v_type = violation["violation_type"]
            tool_name = violation["tool_name"]
            
            by_type[v_type] = by_type.get(v_type, 0) + 1
            by_tool[tool_name] = by_tool.get(tool_name, 0) + 1
        
        return {
            "total": len(self.violation_log),
            "by_type": by_type,
            "by_tool": by_tool
        }
    
    def test_safe_tool(self, tool_name, test_cases):
        """测试安全工具的验证规则"""
        print(f"🧪 测试安全工具: {tool_name}")
        
        for i, (params, should_pass) in enumerate(test_cases):
            try:
                result = self.context.call_tool(tool_name, params)
                if should_pass:
                    print(f"  ✅ 测试 {i+1}: 通过验证（预期）")
                else:
                    print(f"  ❌ 测试 {i+1}: 应该被拒绝但通过了")
                    self.log_violation(tool_name, "validation_bypass", f"Test case {i+1}")
            except Exception as e:
                if not should_pass:
                    print(f"  ✅ 测试 {i+1}: 正确拒绝（预期）")
                else:
                    print(f"  ❌ 测试 {i+1}: 应该通过但被拒绝: {e}")

# 使用安全工具监控器
monitor = SafeToolMonitor(store.for_store())

# 创建安全工具
validation_rules = {
    "required_params": ["path"],
    "param_patterns": {
        "path": r"^/tmp/.*\.txt$"
    },
    "max_execution_time": 5
}

store.for_store().create_safe_tool("safe_read_file", validation_rules)

# 测试用例：(参数, 是否应该通过)
test_cases = [
    ({"path": "/tmp/safe.txt"}, True),      # 应该通过
    ({"path": "/etc/passwd"}, False),       # 应该被拒绝
    ({"path": "/tmp/file.json"}, False),    # 应该被拒绝（扩展名不匹配）
    ({"path": "/tmp/valid.txt"}, True),     # 应该通过
]

monitor.test_safe_tool("safe_read_file", test_cases)

# 查看违规统计
stats = monitor.get_violation_stats()
print(f"\n📊 违规统计: {stats}")
```

## 验证规则类型

### 1. **参数验证**
- `required_params`: 必需参数列表
- `optional_params`: 可选参数列表
- `param_types`: 参数类型验证
- `param_ranges`: 数值范围验证
- `param_patterns`: 正则表达式验证

### 2. **文件安全**
- `allowed_extensions`: 允许的文件扩展名
- `forbidden_paths`: 禁止访问的路径
- `max_file_size`: 最大文件大小

### 3. **网络安全**
- `allowed_domains`: 允许的域名
- `forbidden_ips`: 禁止的IP地址
- `max_request_size`: 最大请求大小

### 4. **执行限制**
- `max_execution_time`: 最大执行时间
- `max_memory_usage`: 最大内存使用
- `rate_limit`: 频率限制

### 5. **自定义验证**
- `custom_validators`: 自定义验证函数

## 相关方法

- [create_simple_tool()](create-simple-tool.md) - 创建简化版本的工具
- [call_tool()](../usage/call-tool.md) - 调用工具（包括安全工具）
- [list_tools()](../listing/list-tools.md) - 列出所有工具（包括安全工具）

## 注意事项

1. **性能影响**: 安全验证会增加工具调用的延迟
2. **验证顺序**: 验证按照规则定义的顺序执行
3. **错误处理**: 验证失败会抛出详细的错误信息
4. **Agent隔离**: Agent级别的安全工具只在该Agent中生效
5. **规则更新**: 安全规则在工具创建后通常不可修改
