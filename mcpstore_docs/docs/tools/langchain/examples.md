# LangChain 集成示例

MCPStore 与 LangChain 的完整集成示例，展示各种实际应用场景。

## 基础集成示例

### 简单的天气查询 Agent

```python
from mcpstore import MCPStore
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 初始化 MCPStore 并添加天气服务
store = MCPStore.setup_store()
store.for_store().add_service({
    "name": "weather-api",
    "url": "https://weather.example.com/mcp"
})

# 2. 获取 LangChain 工具
tools = store.for_store().for_langchain().list_tools()

# 3. 创建 LLM 和提示模板
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个天气助手，可以查询各地天气信息。"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. 创建 Agent 和执行器
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. 使用 Agent
response = agent_executor.invoke({"input": "北京今天的天气怎么样？"})
print(response["output"])
```

## 异步集成示例

### 异步多服务 Agent

```python
import asyncio
from mcpstore import MCPStore
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

async def create_async_agent():
    # 1. 异步初始化和服务添加
    store = MCPStore.setup_store()
    
    # 异步添加多个服务
    await store.for_store().add_service_async({
        "name": "sequential-thinking",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    })
    
    await store.for_store().add_service_async({
        "name": "filesystem",
        "command": "npx", 
        "args": ["-y", "filesystem-mcp"]
    })
    
    # 2. 异步获取工具
    tools = await store.for_store().for_langchain().list_tools_async()
    
    # 3. 创建 Agent
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个智能助手，可以进行思考和文件操作。"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

async def main():
    agent_executor = await create_async_agent()
    
    # 使用 Agent
    response = await agent_executor.ainvoke({
        "input": "帮我分析一下当前目录的文件结构，并给出优化建议"
    })
    print(response["output"])

# 运行异步示例
asyncio.run(main())
```

## Agent 级别集成示例

### 多 Agent 协作系统

```python
from mcpstore import MCPStore
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def create_specialized_agent(store, agent_id, services, system_prompt):
    """创建专门化的 Agent"""
    
    # 为特定 Agent 添加专属服务
    agent_context = store.for_agent(agent_id)
    for service in services:
        agent_context.add_service(service)
    
    # 获取 Agent 专属工具
    tools = agent_context.for_langchain().list_tools()
    
    # 创建 LLM 和提示
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 创建 Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# 初始化 MCPStore
store = MCPStore.setup_store()

# 创建数据分析 Agent
data_agent = create_specialized_agent(
    store=store,
    agent_id="data_analyst",
    services=[
        {"name": "calculator", "command": "npx", "args": ["-y", "calculator-mcp"]},
        {"name": "filesystem", "command": "npx", "args": ["-y", "filesystem-mcp"]}
    ],
    system_prompt="你是一个数据分析专家，擅长计算和文件处理。"
)

# 创建天气 Agent
weather_agent = create_specialized_agent(
    store=store,
    agent_id="weather_specialist", 
    services=[
        {"name": "weather", "url": "https://weather.example.com/mcp"}
    ],
    system_prompt="你是一个天气专家，专门提供天气信息和预报。"
)

# 使用不同的 Agent
data_response = data_agent.invoke({
    "input": "计算 1+2+3+...+100 的和，并将结果保存到文件"
})

weather_response = weather_agent.invoke({
    "input": "查询上海明天的天气"
})

print("数据分析结果:", data_response["output"])
print("天气查询结果:", weather_response["output"])
```

## 混合工具集成示例

### MCP 工具 + 自定义工具

```python
from mcpstore import MCPStore
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from datetime import date, datetime
import requests

# 自定义 LangChain 工具
@tool
def get_current_date() -> str:
    """获取当前日期"""
    return date.today().isoformat()

@tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%H:%M:%S")

@tool
def calculate_age(birth_year: int) -> str:
    """根据出生年份计算年龄"""
    current_year = date.today().year
    age = current_year - birth_year
    return f"年龄大约是 {age} 岁"

@tool
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """获取汇率信息（模拟）"""
    # 这里是模拟实现，实际应该调用真实的汇率API
    rates = {
        ("USD", "CNY"): 7.2,
        ("EUR", "CNY"): 7.8,
        ("GBP", "CNY"): 9.1
    }
    rate = rates.get((from_currency.upper(), to_currency.upper()), 1.0)
    return f"1 {from_currency} = {rate} {to_currency}"

# 获取 MCP 工具
store = MCPStore.setup_store()
store.for_store().add_service()  # 注册所有配置的服务
mcp_tools = store.for_store().for_langchain().list_tools()

# 合并所有工具
all_tools = mcp_tools + [
    get_current_date, 
    get_current_time, 
    calculate_age, 
    get_exchange_rate
]

print(f"🔧 工具总数: {len(all_tools)}")
print(f"  MCP工具: {len(mcp_tools)} 个")
print(f"  自定义工具: {len(all_tools) - len(mcp_tools)} 个")

# 创建增强的 Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个全能助手，拥有以下能力：
    1. MCP工具：可以访问各种外部服务
    2. 时间工具：获取当前日期和时间
    3. 计算工具：进行年龄计算
    4. 汇率工具：查询货币汇率
    
    请根据用户需求选择合适的工具来完成任务。"""),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_tools_agent(llm, all_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)

# 测试混合工具使用
test_queries = [
    "现在几点了？今天是几号？",
    "我1990年出生，今年多大了？",
    "1美元等于多少人民币？",
    "帮我查询北京的天气，然后告诉我现在的时间"
]

for query in test_queries:
    print(f"\n🤔 用户问题: {query}")
    response = agent_executor.invoke({"input": query})
    print(f"🤖 助手回答: {response['output']}")
    print("-" * 50)
```

## 链式调用集成示例

### 服务注册 → 工具转换 → Agent 创建

```python
from mcpstore import MCPStore
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 一行代码完成：服务注册 → 工具转换
tools = (
    MCPStore.setup_store()
    .for_store()
    .add_service({
        "name": "comprehensive-service",
        "url": "https://api.example.com/mcp"
    })
    .add_service({
        "name": "local-tools",
        "command": "npx",
        "args": ["-y", "local-tools-mcp"]
    })
    .for_langchain()
    .list_tools()
)

print(f"🚀 链式调用获得 {len(tools)} 个工具")

# 快速创建 Agent
llm = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个高效的助手，可以使用多种工具来帮助用户。"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent_executor = AgentExecutor(
    agent=create_openai_tools_agent(llm, tools, prompt),
    tools=tools,
    verbose=True
)

# 使用 Agent
response = agent_executor.invoke({
    "input": "帮我完成一个复杂的任务，需要使用多个工具"
})
print(response["output"])
```

## 错误处理和重试示例

### 带错误处理的 Agent

```python
from mcpstore import MCPStore
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_robust_agent():
    """创建带错误处理的健壮 Agent"""
    
    try:
        # 初始化 MCPStore
        store = MCPStore.setup_store()
        
        # 尝试添加服务
        services_to_add = [
            {"name": "weather", "url": "https://weather.example.com/mcp"},
            {"name": "calculator", "command": "npx", "args": ["-y", "calculator-mcp"]},
            {"name": "filesystem", "command": "npx", "args": ["-y", "filesystem-mcp"]}
        ]
        
        successful_services = []
        for service in services_to_add:
            try:
                store.for_store().add_service(service)
                successful_services.append(service["name"])
                logger.info(f"✅ 成功添加服务: {service['name']}")
            except Exception as e:
                logger.error(f"❌ 添加服务失败 {service['name']}: {e}")
        
        # 获取工具
        tools = store.for_store().for_langchain().list_tools()
        
        if not tools:
            logger.warning("⚠️ 没有可用的工具，创建基础 Agent")
            return None
        
        logger.info(f"🛠️ 成功获取 {len(tools)} 个工具")
        
        # 创建 Agent
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""你是一个智能助手，当前可用的服务有：{successful_services}
            如果某个工具不可用，请告知用户并提供替代方案。"""),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            handle_parsing_errors=True,  # 处理解析错误
            max_iterations=5  # 限制最大迭代次数
        )
        
        return agent_executor
        
    except Exception as e:
        logger.error(f"❌ 创建 Agent 失败: {e}")
        return None

def safe_agent_invoke(agent_executor, query, max_retries=3):
    """安全的 Agent 调用，带重试机制"""
    
    for attempt in range(max_retries):
        try:
            logger.info(f"🔄 尝试 {attempt + 1}/{max_retries}: {query}")
            response = agent_executor.invoke({"input": query})
            logger.info(f"✅ 调用成功")
            return response["output"]
            
        except Exception as e:
            logger.error(f"❌ 调用失败 (尝试 {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("⏳ 等待重试...")
                import time
                time.sleep(2 ** attempt)  # 指数退避
            else:
                logger.error("❌ 所有重试都失败了")
                return f"抱歉，处理您的请求时遇到了问题：{e}"

# 使用示例
agent_executor = create_robust_agent()

if agent_executor:
    queries = [
        "今天天气怎么样？",
        "计算 123 + 456",
        "列出当前目录的文件"
    ]
    
    for query in queries:
        print(f"\n🤔 用户问题: {query}")
        result = safe_agent_invoke(agent_executor, query)
        print(f"🤖 助手回答: {result}")
        print("-" * 50)
else:
    print("❌ 无法创建 Agent，请检查服务配置")
```

## 注意事项

1. **服务可用性**: 确保 MCP 服务正常运行
2. **API 密钥**: 配置必要的 API 密钥（如 OpenAI）
3. **错误处理**: 实现适当的错误处理和重试机制
4. **工具选择**: LLM 会自动选择合适的工具，但可能需要明确的指导
5. **性能考虑**: 大量工具可能影响 LLM 的选择效率

## 相关文档

- [for_langchain().list_tools()](as-langchain-tools.md) - LangChain 工具转换
- [call_tool()](../usage/call-tool.md) - 直接工具调用
- [add_service()](../../services/registration/register-service.md) - 服务注册

## 下一步

- 了解 [工具直接调用](../usage/call-tool.md)
- 学习 [服务注册方法](../../services/registration/register-service.md)
- 查看 [高级开发指南](../../advanced/concepts.md)
