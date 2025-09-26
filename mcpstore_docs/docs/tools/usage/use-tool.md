# use_tool() - 工具使用方法（兼容别名）

MCPStore 的 `use_tool()` 方法是 `call_tool()` 的**向后兼容别名**，保持与旧版本代码的兼容性。推荐新项目使用 `call_tool()` 方法，与 FastMCP 命名保持一致。

## 🔄 兼容性说明

### 推荐使用 call_tool()

```python
# ✅ 推荐：使用 call_tool() 方法
result = store.for_store().call_tool("weather_get_current", {"location": "北京"})
```

### 兼容使用 use_tool()

```python
# ✅ 兼容：使用 use_tool() 方法（功能完全相同）
result = store.for_store().use_tool("weather_get_current", {"location": "北京"})
```

## 🎯 方法签名

### 同步版本

```python
def use_tool(
    self, 
    tool_name: str, 
    args: Union[Dict[str, Any], str] = None, 
    **kwargs
) -> Any
```

### 异步版本

```python
async def use_tool_async(
    self, 
    tool_name: str, 
    args: Union[Dict[str, Any], str] = None, 
    **kwargs
) -> Any
```

> **注意**: `use_tool()` 和 `call_tool()` 的方法签名、参数和返回值完全相同。

## 🤖 Agent 模式支持

### 支持状态
- ✅ **完全支持** - `use_tool()` 在 Agent 模式下完全可用（与 `call_tool()` 功能相同）

### Agent 模式调用
```python
# Agent 模式调用（兼容方式）
result = store.for_agent("research_agent").use_tool(
    "weather-api_get_current",
    {"location": "北京"}
)

# 推荐的等价调用
result = store.for_agent("research_agent").call_tool(
    "weather-api_get_current",
    {"location": "北京"}
)

# 异步 Agent 模式调用
result = await store.for_agent("research_agent").use_tool_async(
    "weather-api_get_current",
    {"location": "北京"}
)
```

### 模式差异说明
- **Store 模式**: `use_tool()` 和 `call_tool()` 在 Store 模式下功能完全相同
- **Agent 模式**: `use_tool()` 和 `call_tool()` 在 Agent 模式下功能完全相同
- **主要区别**: 仅在方法命名上有差异，内部实现完全一致

### 功能对等性验证
```python
def verify_agent_mode_equivalence():
    """验证 Agent 模式下两个方法的功能对等性"""
    store = MCPStore.setup_store()
    agent_id = "test_agent"

    # 使用相同参数调用两个方法
    tool_name = "weather-api_get_current"
    args = {"location": "北京"}

    # use_tool 调用
    result1 = store.for_agent(agent_id).use_tool(tool_name, args)

    # call_tool 调用
    result2 = store.for_agent(agent_id).call_tool(tool_name, args)

    # 验证结果相同
    print(f"结果相同: {result1 == result2}")  # True
    print(f"use_tool 结果: {result1}")
    print(f"call_tool 结果: {result2}")

# 使用
verify_agent_mode_equivalence()
```

### 使用建议
- **新 Agent 项目**: 推荐使用 `call_tool()`，与 FastMCP 命名一致
- **现有 Agent 项目**: 可继续使用 `use_tool()`，无需修改
- **团队协作**: 建议统一使用 `call_tool()` 提高代码一致性

## 📋 功能对比

| 特性 | use_tool() | call_tool() | 说明 |
|------|------------|-------------|------|
| **功能** | ✅ 完全相同 | ✅ 完全相同 | 内部调用相同的实现 |
| **参数** | ✅ 完全相同 | ✅ 完全相同 | 支持相同的参数格式 |
| **返回值** | ✅ 完全相同 | ✅ 完全相同 | 返回相同的结果格式 |
| **错误处理** | ✅ 完全相同 | ✅ 完全相同 | 相同的异常处理机制 |
| **性能** | ✅ 完全相同 | ✅ 完全相同 | 无性能差异 |
| **FastMCP一致性** | ❌ 旧命名 | ✅ 官方命名 | call_tool 与 FastMCP 一致 |
| **推荐程度** | ⚠️ 兼容使用 | ✅ 推荐使用 | 新项目推荐 call_tool |

## 🚀 使用示例

### 基础使用（兼容方式）

```python
from mcpstore import MCPStore

def basic_use_tool_example():
    """基础 use_tool 使用示例"""
    store = MCPStore.setup_store()
    
    # 使用 use_tool 方法（兼容方式）
    result = store.for_store().use_tool(
        "weather-api_get_current", 
        {"location": "北京"}
    )
    
    print(f"天气查询结果: {result}")
    
    # 与 call_tool 完全等价
    result_call = store.for_store().call_tool(
        "weather-api_get_current", 
        {"location": "北京"}
    )
    
    print(f"结果相同: {result == result_call}")

# 使用
basic_use_tool_example()
```

### 迁移示例

```python
def migration_example():
    """从 use_tool 迁移到 call_tool 的示例"""
    store = MCPStore.setup_store()
    
    # 旧代码（仍然可用）
    def old_way():
        return store.for_store().use_tool(
            "calculator_add",
            {"a": 10, "b": 20}
        )
    
    # 新代码（推荐方式）
    def new_way():
        return store.for_store().call_tool(
            "calculator_add",
            {"a": 10, "b": 20}
        )
    
    # 两种方式结果完全相同
    old_result = old_way()
    new_result = new_way()
    
    print(f"旧方式结果: {old_result}")
    print(f"新方式结果: {new_result}")
    print(f"结果相同: {old_result == new_result}")

# 使用
migration_example()
```

### 异步使用（兼容方式）

```python
import asyncio

async def async_use_tool_example():
    """异步 use_tool 使用示例"""
    store = MCPStore.setup_store()
    
    # 使用 use_tool_async 方法（兼容方式）
    result = await store.for_store().use_tool_async(
        "weather-api_get_current",
        {"location": "上海"}
    )
    
    print(f"异步天气查询: {result}")
    
    # 与 call_tool_async 完全等价
    result_call = await store.for_store().call_tool_async(
        "weather-api_get_current",
        {"location": "上海"}
    )
    
    print(f"异步结果相同: {result == result_call}")

# 使用
# asyncio.run(async_use_tool_example())
```

### Agent 模式使用（兼容方式）

```python
def agent_use_tool_example():
    """Agent 模式 use_tool 使用示例"""
    store = MCPStore.setup_store()
    
    agent_id = "legacy_agent"
    
    # Agent 使用 use_tool 方法（兼容方式）
    result = store.for_agent(agent_id).use_tool(
        "weather-api_get_current",
        {"location": "广州"}
    )
    
    print(f"🤖 Agent '{agent_id}' 使用 use_tool: {result}")
    
    # 与 call_tool 完全等价
    result_call = store.for_agent(agent_id).call_tool(
        "weather-api_get_current",
        {"location": "广州"}
    )
    
    print(f"🤖 Agent '{agent_id}' 使用 call_tool: {result_call}")
    print(f"Agent 结果相同: {result == result_call}")

# 使用
agent_use_tool_example()
```

## 🔄 迁移指南

### 为什么要迁移到 call_tool？

1. **FastMCP 一致性**: `call_tool` 与 FastMCP 官方命名保持一致
2. **行业标准**: 遵循 MCP 生态系统的命名规范
3. **未来兼容**: 确保与未来版本的最佳兼容性
4. **团队协作**: 统一的命名规范提高代码可读性

### 迁移步骤

#### 1. 简单替换

```python
# 旧代码
result = store.for_store().use_tool("tool_name", args)

# 新代码
result = store.for_store().call_tool("tool_name", args)
```

#### 2. 异步方法替换

```python
# 旧代码
result = await store.for_store().use_tool_async("tool_name", args)

# 新代码
result = await store.for_store().call_tool_async("tool_name", args)
```

#### 3. 批量替换脚本

```python
def migrate_codebase():
    """批量迁移代码库的示例脚本"""
    import re
    import os
    
    def replace_in_file(file_path):
        """替换单个文件中的方法调用"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换同步方法
        content = re.sub(r'\.use_tool\(', '.call_tool(', content)
        
        # 替换异步方法
        content = re.sub(r'\.use_tool_async\(', '.call_tool_async(', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已更新文件: {file_path}")
    
    # 遍历项目文件
    for root, dirs, files in os.walk("./src"):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                replace_in_file(file_path)

# 注意：实际使用时请先备份代码
# migrate_codebase()
```

### 渐进式迁移

```python
def gradual_migration_example():
    """渐进式迁移示例"""
    store = MCPStore.setup_store()
    
    # 阶段1：新功能使用 call_tool
    def new_feature():
        return store.for_store().call_tool(
            "new-service_new_tool",
            {"param": "value"}
        )
    
    # 阶段2：保持旧功能使用 use_tool（暂时）
    def legacy_feature():
        return store.for_store().use_tool(
            "legacy-service_old_tool",
            {"param": "value"}
        )
    
    # 阶段3：逐步迁移旧功能
    def migrated_legacy_feature():
        return store.for_store().call_tool(  # 已迁移
            "legacy-service_old_tool",
            {"param": "value"}
        )
    
    # 测试所有功能
    print("新功能:", new_feature())
    print("旧功能:", legacy_feature())
    print("迁移后:", migrated_legacy_feature())

# 使用
gradual_migration_example()
```

## 📊 API 兼容性

### Store API 端点

```bash
# 推荐：使用 call_tool 端点
POST /for_store/call_tool

# 兼容：使用 use_tool 端点（功能相同）
POST /for_store/use_tool
```

### Agent API 端点

```bash
# 推荐：使用 call_tool 端点
POST /for_agent/{agent_id}/call_tool

# 兼容：使用 use_tool 端点（功能相同）
POST /for_agent/{agent_id}/use_tool
```

### 请求格式

两个端点使用完全相同的请求格式：

```json
{
  "tool_name": "weather-api_get_current",
  "args": {
    "location": "北京"
  }
}
```

### 响应格式

两个端点返回完全相同的响应格式：

```json
{
  "success": true,
  "data": {
    "temperature": 22,
    "condition": "sunny"
  },
  "metadata": {
    "execution_time_ms": 1250,
    "trace_id": "abc12345",
    "tool_name": "weather-api_get_current"
  },
  "message": "Tool executed successfully"
}
```

## 🔧 内部实现

`use_tool()` 方法的内部实现非常简单，直接调用 `call_tool()`：

```python
def use_tool(self, tool_name: str, args=None, **kwargs):
    """向后兼容别名，直接调用 call_tool"""
    return self.call_tool(tool_name, args, **kwargs)

async def use_tool_async(self, tool_name: str, args=None, **kwargs):
    """向后兼容别名，直接调用 call_tool_async"""
    return await self.call_tool_async(tool_name, args, **kwargs)
```

这确保了两个方法的功能完全相同，没有任何性能差异。

## 📈 最佳实践

### 新项目

```python
# ✅ 推荐：新项目直接使用 call_tool
def new_project_example():
    store = MCPStore.setup_store()
    
    # 使用推荐的方法名
    result = store.for_store().call_tool("tool_name", args)
    return result
```

### 现有项目

```python
# ✅ 可接受：现有项目继续使用 use_tool
def existing_project_example():
    store = MCPStore.setup_store()
    
    # 现有代码无需立即修改
    result = store.for_store().use_tool("tool_name", args)
    return result
```

### 团队协作

```python
# ✅ 推荐：团队统一使用 call_tool
def team_collaboration_example():
    store = MCPStore.setup_store()
    
    # 团队约定使用统一的方法名
    result = store.for_store().call_tool("tool_name", args)
    return result
```

## 🔗 相关文档

- [call_tool()](call-tool.md) - 推荐的工具调用方法
- [工具使用概览](tool-usage-overview.md) - 工具使用概览
- [list_tools()](../listing/list-tools.md) - 获取工具列表
- [FastMCP 集成](../../advanced/fastmcp-integration.md) - FastMCP 集成指南

## 🎯 下一步

- 学习 [推荐的 call_tool() 方法](call-tool.md)
- 了解 [工具使用概览](tool-usage-overview.md)
- 掌握 [工具列表查询](../listing/list-tools.md)
- 查看 [迁移指南](../../advanced/migration-guide.md)
