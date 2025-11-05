## add_service - 服务注册

 

如何通过 MCPStore 注册服务 

### SDK

同步：
  - `store.for_store().add_service(config=..., ...) -> bool`
 
异步：
  - `await store.for_store().add_service_async(config=..., ...) -> bool`

### 参数

| 参数名      | 类型     | 说明                                     |
|------------|----------|------------------------------------------|
| `config`   | dict/str | 服务配置，支持多种结构。                 |
| `json_file`| str      | 从 JSON 文件加载配置（若提供则优先读取）。|
| `headers`  | dict     | 用于设置认证相关请求头。                 |

### config 参数 与 json_file 参数

config参数支持这些格式：

单个远程服务
```python
cfg = {
    "name": "mcpstore_wiki",
    "url": "https://www.mcpstore.wiki/mcp"
}
```

单个本地服务
```python
cfg = {
    "name": "assistant",
    "command": "python",
    "args": ["./assistant_server.py"],
    "env": {"DEBUG": "true"}
}
```

mcpServers JSON 格式（兼容 Cursor 等 IDE）
```python
cfg = {
    "mcpServers": {
        "weather": {"url": "..."},
        "assistant": {"command": "..."}
    }
}
 ```

宽字典 
```python
cfg = {
    "weather": {"url": "https://weather.example.com/mcp"},
    "assistant": {"command": "python", "args": ["./assistant.py"]}
}
```

批量config列表
```python
cfg = [
    {"name": "weather", "url": "https://weather.example.com/mcp"},
    {"name": "assistant", "command": "python", "args": ["./assistant.py"]},
    {"name": "calculator", "command": "node", "args": ["calc.js"]}
]
```

配置好上述的cfg然后执行add_service()即可
```python
# 字典与字符串 `str(cfg)` 都可以
store.for_store().add_service(cfg)
```

或者可以使用json_file参数 直接指定json文件
```python
cfg = "/home/work/mcp.json"
store.for_store().add_service(json_file=cfg)
```

#### config传输类型判断

可以指定传输类型 未指定时将自动推断。
```python
# 默认推断为 streamable-http
cfg = {"name": "api1", "url": "https://api.example.com/mcp"}
store.for_store().add_service(cfg)

# URL 包含 /sse → 推断为 sse
cfg = {"name": "api2", "url": "https://api.example.com/sse"}
store.for_store().add_service(cfg)
```


### headers参数
使用 Bearer Token
```python
headers = {"Authorization": "Bearer <token>"}
```
使用 API Key
```python
headers = {"X-API-Key": "<api_key>"}
 ```
自定义请求头
```python
headers = {"Authorization": "Bearer <token>", "X-Custom-Header": "value"}
```
在添加服务时配置：
```python
store.for_store().add_service(config=cfg, headers=headers)
```
如果需要后续更新服务的时候更新请求头。参考todo链接到更新服务的鉴权部分


 

### 视角
通过 `for_store()` 注册的服务名为全局名称，在全局空间可见，可以想象是为你的store添加的服务，后续的Agent可以直接通过服务名添加或者查询。
 

### 常用配合：等待
add_service 为“注册并触发初始化”操作 不阻塞等待连接与健康检查完成 常搭配 `wait_service()` 使用

```python
# 添加操作通常是ms级完成
store.for_store().add_service({"name": "weather", "url": "..."})
# 添加后可以等待服务就绪
store.for_store().wait_service("weather")
```

也可以等待服务收敛到指定状态与设置超时等待时间(本地服务一般需要更长的等待收敛时间)

使用：`store.for_store().wait_service("service_name", status=["healthy", "warning",....], timeout=30)`。

更多细节详见 `wait_service`（专题 TODO：添加链接跳转）。
 
 

### 你可能想找的方法

| 场景/方法           | 同步方法                                                                                     |
|-----------------------|--------------------------------------------------------------------------------------------|
| 注册服务              | `store.for_store().add_service(config=..., ...)`                                           |
| 等待服务              | `store.for_store().wait_service(name, status="healthy", timeout=...)`                      |
| 等待服务实现目标状态  | `store.for_store().wait_service(...)`                                                                         |
| 更新服务              | `store.for_store().update_service(...)`                                                                       |
| Patch 更新服务        | `store.for_store().patch_service(...)`                                                                        |
| 删除服务              | `store.for_store().delete_service(...)`                                                                       |
| 重启服务              | `store.for_store().restart_service(...)`                                                                      |
| 查看配置              | `store.for_store().show_config(...)`                                                                          |
| 重置配置              | `store.for_store().reset_config(...)`                                                                         |
| 获取服务信息          | `store.for_store().get_service_info(...)`                                                                     |
| 获取服务状态          | `store.for_store().get_service_status(...)`                                                                   |
| Agent 注册            | store.for_agent(id).add_service()                                                         |
| Agent 等待            | store.for_agent(id).wait_service()                                                          |

 
