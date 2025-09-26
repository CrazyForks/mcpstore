# create_simple_tool()

创建简化版本的工具。

## 方法特性

- ✅ **异步版本**: `create_simple_tool_async()`
- ✅ **Store级别**: `store.for_store().create_simple_tool()`
- ✅ **Agent级别**: `store.for_agent("agent1").create_simple_tool()`
- 📁 **文件位置**: `advanced_features.py`
- 🏷️ **所属类**: `AdvancedFeaturesMixin`

## 参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `original_tool` | `str` | ✅ | - | 原始工具名称 |
| `friendly_name` | `str` | ❌ | `None` | 友好名称（可选） |

## 返回值

返回上下文对象，支持链式调用。

## 使用示例

### Store级别创建简化工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 添加一个复杂的文件系统服务
store.for_store().add_service({
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        }
    }
})

# 创建简化工具
store.for_store().create_simple_tool(
    "filesystem_read_file",  # 原始复杂工具名
    "read_file"              # 简化后的友好名称
)

# 现在可以用简化名称调用工具
result = store.for_store().call_tool("read_file", {
    "path": "/tmp/example.txt"
})
print(f"文件内容: {result}")

# 原始工具名仍然可用
original_result = store.for_store().call_tool("filesystem_read_file", {
    "path": "/tmp/example.txt"
})
```

### Agent级别创建简化工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# Agent模式创建简化工具
agent_context = store.for_agent("agent1")

# 为Agent创建简化工具
agent_context.create_simple_tool(
    "complex_weather_api_get_current_conditions",
    "weather"
)

# Agent可以用简化名称调用
weather_result = agent_context.call_tool("weather", {
    "city": "Beijing"
})
print(f"天气信息: {weather_result}")
```

### 批量创建简化工具

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 定义工具简化映射
tool_simplifications = {
    "filesystem_read_file": "read",
    "filesystem_write_file": "write",
    "filesystem_list_directory": "ls",
    "database_execute_query": "query",
    "database_insert_record": "insert",
    "weather_get_current_conditions": "weather",
    "weather_get_forecast": "forecast"
}

# 批量创建简化工具
context = store.for_store()
for original_name, simple_name in tool_simplifications.items():
    context.create_simple_tool(original_name, simple_name)

print("批量简化工具创建完成")

# 验证简化工具可用性
tools = context.list_tools()
simple_tools = [t for t in tools if t.name in tool_simplifications.values()]
print(f"可用的简化工具: {[t.name for t in simple_tools]}")
```

### 异步版本

```python
import asyncio
from mcpstore import MCPStore

async def async_create_simple_tools():
    # 初始化
    store = MCPStore.setup_store()
    
    # 异步创建简化工具
    await store.for_store().create_simple_tool_async(
        "complex_analysis_tool",
        "analyze"
    )
    
    # 异步调用简化工具
    result = await store.for_store().call_tool_async("analyze", {
        "data": "sample_data"
    })
    
    print(f"异步分析结果: {result}")
    return result

# 运行异步创建
result = asyncio.run(async_create_simple_tools())
```

### 智能简化工具创建

```python
from mcpstore import MCPStore
import re

# 初始化
store = MCPStore.setup_store()

def create_smart_simplified_tools():
    """智能创建简化工具"""
    
    # 获取所有工具
    tools = store.for_store().list_tools()
    
    print("=== 智能简化工具创建 ===")
    
    simplified_count = 0
    
    for tool in tools:
        original_name = tool.name
        
        # 智能生成简化名称
        simple_name = generate_simple_name(original_name)
        
        if simple_name and simple_name != original_name:
            try:
                store.for_store().create_simple_tool(original_name, simple_name)
                print(f"✅ {original_name} -> {simple_name}")
                simplified_count += 1
            except Exception as e:
                print(f"❌ 简化失败 {original_name}: {e}")
    
    print(f"\n总计创建 {simplified_count} 个简化工具")
    return simplified_count

def generate_simple_name(original_name):
    """智能生成简化名称"""
    
    # 移除服务前缀
    patterns = [
        r'^[a-zA-Z]+_(.+)$',  # service_action -> action
        r'^([a-zA-Z]+)_[a-zA-Z]+_(.+)$',  # service_type_action -> action
    ]
    
    for pattern in patterns:
        match = re.match(pattern, original_name)
        if match:
            simplified = match.group(-1)  # 取最后一个分组
            
            # 进一步简化
            simplified = simplified.replace('_', '')
            
            # 常见动词简化
            verb_mappings = {
                'read': 'read',
                'write': 'write',
                'list': 'ls',
                'get': 'get',
                'set': 'set',
                'delete': 'rm',
                'create': 'new',
                'update': 'edit',
                'execute': 'run',
                'query': 'query'
            }
            
            for full_verb, short_verb in verb_mappings.items():
                if simplified.lower().startswith(full_verb):
                    return short_verb + simplified[len(full_verb):]
            
            return simplified
    
    return None

# 执行智能简化
# create_smart_simplified_tools()
```

### 简化工具管理

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

class SimplifiedToolManager:
    """简化工具管理器"""
    
    def __init__(self, context):
        self.context = context
        self.simplifications = {}
    
    def add_simplification(self, original_name, simple_name):
        """添加工具简化"""
        try:
            self.context.create_simple_tool(original_name, simple_name)
            self.simplifications[simple_name] = original_name
            print(f"✅ 添加简化: {original_name} -> {simple_name}")
            return True
        except Exception as e:
            print(f"❌ 简化失败: {e}")
            return False
    
    def remove_simplification(self, simple_name):
        """移除工具简化（如果支持）"""
        if simple_name in self.simplifications:
            # 注意：实际的MCPStore可能不支持移除简化工具
            # 这里只是从本地记录中移除
            original_name = self.simplifications.pop(simple_name)
            print(f"🗑️ 移除简化: {simple_name} ({original_name})")
            return True
        return False
    
    def list_simplifications(self):
        """列出所有简化映射"""
        print("📋 当前简化工具映射:")
        for simple_name, original_name in self.simplifications.items():
            print(f"  {simple_name} -> {original_name}")
        return self.simplifications
    
    def test_simplification(self, simple_name, test_params=None):
        """测试简化工具"""
        if simple_name not in self.simplifications:
            print(f"❌ 简化工具 {simple_name} 不存在")
            return False
        
        try:
            if test_params is None:
                test_params = {}
            
            result = self.context.call_tool(simple_name, test_params)
            print(f"✅ 简化工具 {simple_name} 测试成功")
            return True
        except Exception as e:
            print(f"❌ 简化工具 {simple_name} 测试失败: {e}")
            return False

# 使用简化工具管理器
manager = SimplifiedToolManager(store.for_store())

# 添加多个简化
manager.add_simplification("filesystem_read_file", "read")
manager.add_simplification("filesystem_write_file", "write")
manager.add_simplification("database_query", "query")

# 列出简化映射
manager.list_simplifications()

# 测试简化工具
manager.test_simplification("read", {"path": "/tmp/test.txt"})
```

### 链式简化工具创建

```python
from mcpstore import MCPStore

# 初始化
store = MCPStore.setup_store()

# 链式创建多个简化工具
result = (store.for_store()
    .create_simple_tool("filesystem_read_file", "read")
    .create_simple_tool("filesystem_write_file", "write")
    .create_simple_tool("filesystem_list_directory", "ls")
    .create_simple_tool("database_execute_query", "query")
    .create_simple_tool("weather_get_current", "weather")
)

print("链式简化工具创建完成")

# 验证所有简化工具
simplified_tools = ["read", "write", "ls", "query", "weather"]
for tool_name in simplified_tools:
    try:
        # 尝试获取工具信息（不实际调用）
        tools = result.list_tools()
        tool_exists = any(t.name == tool_name for t in tools)
        print(f"{'✅' if tool_exists else '❌'} {tool_name}")
    except Exception as e:
        print(f"❌ {tool_name}: {e}")
```

## 简化工具的优势

### 1. **用户友好**
- 简短易记的工具名称
- 降低学习成本
- 提高开发效率

### 2. **向后兼容**
- 原始工具名仍然可用
- 不影响现有代码
- 渐进式迁移

### 3. **Agent优化**
- Agent可以使用更直观的工具名
- 减少Agent的认知负担
- 提高Agent的工具使用效率

### 4. **团队协作**
- 统一的工具命名规范
- 减少团队沟通成本
- 提高代码可读性

## 最佳实践

### 1. **命名规范**
```python
# 推荐的简化命名
"filesystem_read_file" -> "read"
"database_execute_query" -> "query"
"weather_get_current" -> "weather"
"email_send_message" -> "send"
```

### 2. **避免冲突**
```python
# 检查名称冲突
existing_tools = [t.name for t in store.for_store().list_tools()]
if "read" not in existing_tools:
    store.for_store().create_simple_tool("filesystem_read_file", "read")
```

### 3. **文档记录**
```python
# 记录简化映射关系
simplification_docs = {
    "read": "filesystem_read_file - 读取文件内容",
    "write": "filesystem_write_file - 写入文件内容",
    "query": "database_execute_query - 执行数据库查询"
}
```

## 相关方法

- [create_safe_tool()](create-safe-tool.md) - 创建安全版本的工具
- [call_tool()](../usage/call-tool.md) - 调用工具（包括简化工具）
- [list_tools()](../listing/list-tools.md) - 列出所有工具（包括简化工具）

## 注意事项

1. **名称唯一性**: 简化名称必须在当前上下文中唯一
2. **原始工具依赖**: 简化工具依赖原始工具的存在
3. **Agent隔离**: Agent级别的简化工具只在该Agent中可见
4. **链式调用**: 支持链式调用，便于批量创建
5. **持久性**: 简化工具的持久性取决于具体实现
