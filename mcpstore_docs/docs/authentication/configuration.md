# 🔧 认证配置详解

本文档详细介绍如何配置 MCPStore 的各种认证方式。

## 🏗️ 配置架构

MCPStore 的认证系统采用三层配置架构：

1. **认证提供者配置**: 全局认证提供者设置
2. **服务认证配置**: 单个服务的认证设置
3. **Hub 认证配置**: Hub 级别的统一认证

## 🔑 认证构建器

### AuthServiceBuilder - 服务认证构建器

用于配置单个服务的认证保护：

```python
from mcpstore import MCPStore

store = MCPStore()

# 创建服务认证构建器
auth_builder = store.for_store().auth_service("my-service")
```

#### 方法列表

| 方法 | 参数 | 说明 |
|------|------|------|
| `require_scopes(*scopes)` | scopes: str | 设置必需的权限范围 |
| `use_bearer_auth(...)` | jwks_uri, issuer, audience, algorithm | 配置 Bearer Token 认证 |
| `use_oauth_auth(...)` | client_id, client_secret, base_url, provider | 配置 OAuth 认证 |
| `use_google_auth(...)` | client_id, client_secret, base_url, scopes | 配置 Google OAuth |
| `use_github_auth(...)` | client_id, client_secret, base_url, scopes | 配置 GitHub OAuth |
| `use_workos_auth(...)` | authkit_domain, base_url | 配置 WorkOS 认证 |
| `generate_fastmcp_config()` | - | 生成 FastMCP 配置 |

### AuthProviderBuilder - 认证提供者构建器

用于配置全局认证提供者：

```python
# 创建认证提供者构建器
provider_builder = store.for_store().auth_provider("bearer")
```

#### 方法列表

| 方法 | 参数 | 说明 |
|------|------|------|
| `set_client_credentials(client_id, client_secret)` | client_id: str, client_secret: str | 设置 OAuth 客户端凭据 |
| `set_base_url(base_url)` | base_url: str | 设置服务器基础 URL |
| `set_jwks_config(...)` | jwks_uri, issuer, audience, algorithm | 设置 JWKS 配置 |
| `set_scopes(scopes)` | scopes: List[str] | 设置权限范围 |
| `generate_fastmcp_config()` | - | 生成 FastMCP 配置 |

### AuthTokenBuilder - Token 构建器

用于生成 JWT Payload：

```python
# 创建 Token 构建器
token_builder = store.for_store().auth_jwt_payload("user123")
```

#### 方法列表

| 方法 | 参数 | 说明 |
|------|------|------|
| `add_scopes(*scopes)` | scopes: str | 添加权限范围 |
| `add_claim(key, value)` | key: str, value: Any | 添加自定义声明 |
| `generate_payload()` | - | 生成 JWT Payload |

## 🔐 认证方式配置

### 1. Bearer Token (JWT) 认证

最常用的认证方式，基于 JWT 标准：

```python
# 基础配置
bearer_config = store.for_store().auth_service("secure-api")\
    .require_scopes("api:read", "api:write")\
    .use_bearer_auth(
        jwks_uri="https://auth.company.com/.well-known/jwks.json",
        issuer="https://auth.company.com",
        audience="secure-api",
        algorithm="RS256"  # 支持 RS256, HS256 等
    )\
    .generate_fastmcp_config()
```

#### 配置参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `jwks_uri` | str | ✅ | JWKS 密钥集合 URI |
| `issuer` | str | ✅ | JWT 发行者 |
| `audience` | str | ✅ | JWT 受众 |
| `algorithm` | str | ❌ | 签名算法，默认 RS256 |

### 2. Google OAuth 认证

集成 Google 企业认证：

```python
google_config = store.for_store().auth_service("google-protected")\
    .require_scopes("profile", "email")\
    .use_google_auth(
        client_id="your-google-client-id",
        client_secret="your-google-client-secret",
        base_url="https://myapp.com",
        required_scopes=["openid", "email", "profile"]
    )\
    .generate_fastmcp_config()
```

#### 环境变量配置

```bash
# 推荐使用环境变量
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

```python
import os

google_config = store.for_store().auth_service("google-protected")\
    .use_google_auth(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        base_url="https://myapp.com"
    )\
    .generate_fastmcp_config()
```

### 3. GitHub OAuth 认证

集成 GitHub 认证：

```python
github_config = store.for_store().auth_service("github-tools")\
    .require_scopes("repo:read", "user:read")\
    .use_github_auth(
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        base_url="https://myapp.com",
        required_scopes=["read:user", "user:email", "repo"]
    )\
    .generate_fastmcp_config()
```

### 4. WorkOS 企业认证

企业级 SSO 解决方案：

```python
workos_config = store.for_store().auth_service("enterprise-tools")\
    .require_scopes("admin", "user:manage")\
    .use_workos_auth(
        authkit_domain="your-domain.authkit.com",
        base_url="https://enterprise.myapp.com"
    )\
    .generate_fastmcp_config()
```

## 🎯 权限范围 (Scopes) 配置

### 标准权限范围

| Scope | 说明 | 适用场景 |
|-------|------|----------|
| `read` | 读取权限 | 查询数据、获取信息 |
| `write` | 写入权限 | 创建、更新数据 |
| `execute` | 执行权限 | 运行工具、执行操作 |
| `admin` | 管理权限 | 系统管理、用户管理 |
| `delete` | 删除权限 | 删除数据、清理资源 |

### 自定义权限范围

```python
# 业务相关的权限范围
custom_scopes = [
    "payment:process",      # 支付处理
    "user:profile:read",    # 用户资料读取
    "order:create",         # 订单创建
    "inventory:manage",     # 库存管理
    "report:generate"       # 报告生成
]

auth_config = store.for_store().auth_service("business-api")\
    .require_scopes(*custom_scopes)\
    .use_bearer_auth(...)\
    .generate_fastmcp_config()
```

## 🏷️ JWT Claims 配置

### 标准 Claims

```python
# 生成包含标准 claims 的 JWT payload
user_payload = store.for_store().auth_jwt_payload("user123")\
    .add_scopes("read", "write", "execute")\
    .add_claim("iss", "https://auth.company.com")\ # 发行者
    .add_claim("aud", "my-service")\               # 受众
    .add_claim("exp", 1735689600)\                 # 过期时间
    .add_claim("iat", 1735603200)\                 # 发行时间
    .add_claim("sub", "user123")\                  # 主题（用户ID）
    .generate_payload()
```

### 自定义 Claims

```python
# 业务相关的自定义 claims
business_payload = store.for_store().auth_jwt_payload("business_user")\
    .add_scopes("business:read", "business:write")\
    .add_claim("role", "manager")\
    .add_claim("department", "sales")\
    .add_claim("tenant_id", "company_abc")\
    .add_claim("permissions", ["create_orders", "view_reports"])\
    .add_claim("rate_limit", 1000)\
    .add_claim("features", ["advanced_analytics", "bulk_operations"])\
    .generate_payload()
```

## 🔗 配置组合示例

### 多层认证配置

```python
async def setup_multi_layer_auth():
    store = MCPStore()
    
    # 1. 配置全局认证提供者
    global_auth = store.for_store().auth_provider("bearer")\
        .set_jwks_config(
            jwks_uri="https://auth.company.com/.well-known/jwks.json",
            issuer="https://auth.company.com",
            audience="company-services",
            algorithm="RS256"
        )\
        .generate_fastmcp_config()
    
    # 2. 配置不同安全级别的服务
    
    # 公开服务 - 无需认证
    await store.for_store().add_service_async({
        "name": "public_info",
        "url": "https://api.company.com/public"
    })
    
    # 受保护服务 - 需要基础认证
    protected_auth = store.for_store().auth_service("protected_api")\
        .require_scopes("read", "write")\
        .use_bearer_auth(
            jwks_uri="https://auth.company.com/.well-known/jwks.json",
            issuer="https://auth.company.com",
            audience="protected-api"
        )\
        .generate_fastmcp_config()
    
    # 高安全服务 - 需要管理员权限
    admin_auth = store.for_store().auth_service("admin_api")\
        .require_scopes("admin", "user:manage", "system:configure")\
        .use_bearer_auth(
            jwks_uri="https://auth.company.com/.well-known/jwks.json",
            issuer="https://auth.company.com",
            audience="admin-api"
        )\
        .generate_fastmcp_config()
    
    # 3. 生成不同角色的用户 JWT
    
    # 普通用户
    user_jwt = store.for_store().auth_jwt_payload("regular_user")\
        .add_scopes("read", "write")\
        .add_claim("role", "user")\
        .add_claim("tenant_id", "company_abc")\
        .generate_payload()
    
    # 管理员用户
    admin_jwt = store.for_store().auth_jwt_payload("admin_user")\
        .add_scopes("read", "write", "admin", "user:manage", "system:configure")\
        .add_claim("role", "admin")\
        .add_claim("tenant_id", "company_abc")\
        .add_claim("permissions", ["all"])\
        .generate_payload()
    
    return {
        "global_auth": global_auth,
        "protected_auth": protected_auth,
        "admin_auth": admin_auth,
        "user_jwt": user_jwt,
        "admin_jwt": admin_jwt
    }
```

## ⚙️ 高级配置

### 条件认证

```python
# 基于环境的条件认证配置
import os

def get_auth_config(environment: str):
    store = MCPStore()
    
    if environment == "development":
        # 开发环境 - 宽松认证
        return store.for_store().auth_service("dev_api")\
            .require_scopes("read", "write")\
            .use_bearer_auth(
                jwks_uri="https://dev-auth.company.com/.well-known/jwks.json",
                issuer="https://dev-auth.company.com",
                audience="dev-api"
            )\
            .generate_fastmcp_config()
    
    elif environment == "production":
        # 生产环境 - 严格认证
        return store.for_store().auth_service("prod_api")\
            .require_scopes("read", "write", "verified")\
            .use_bearer_auth(
                jwks_uri="https://auth.company.com/.well-known/jwks.json",
                issuer="https://auth.company.com",
                audience="prod-api",
                algorithm="RS256"
            )\
            .generate_fastmcp_config()
```

### 动态权限配置

```python
def create_dynamic_auth(user_role: str, permissions: List[str]):
    store = MCPStore()
    
    # 根据角色动态生成权限范围
    role_scopes = {
        "viewer": ["read"],
        "editor": ["read", "write"],
        "admin": ["read", "write", "delete", "admin"],
        "super_admin": ["read", "write", "delete", "admin", "system:configure"]
    }
    
    scopes = role_scopes.get(user_role, ["read"])
    
    return store.for_store().auth_jwt_payload(f"{user_role}_user")\
        .add_scopes(*scopes)\
        .add_claim("role", user_role)\
        .add_claim("permissions", permissions)\
        .generate_payload()
```

## 🔍 配置验证

### 验证认证配置

```python
def validate_auth_config(auth_config):
    """验证认证配置的完整性"""
    required_fields = ["provider_class", "import_path", "config_params"]
    
    for field in required_fields:
        if not hasattr(auth_config, field):
            raise ValueError(f"Missing required field: {field}")
    
    # 验证 Bearer Token 配置
    if auth_config.provider_class == "BearerAuthProvider":
        required_params = ["jwks_uri", "issuer", "audience"]
        for param in required_params:
            if param not in auth_config.config_params:
                raise ValueError(f"Missing Bearer Token parameter: {param}")
    
    print("✅ 认证配置验证通过")
    return True

# 使用示例
auth_config = store.for_store().auth_service("test_api")\
    .use_bearer_auth(...)\
    .generate_fastmcp_config()

validate_auth_config(auth_config)
```

## 📝 配置文件管理

### 保存配置到文件

```python
import json

def save_auth_config(auth_config, filename: str):
    """保存认证配置到文件"""
    config_dict = {
        "provider_class": auth_config.provider_class,
        "import_path": auth_config.import_path,
        "config_params": auth_config.config_params
    }
    
    with open(filename, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    print(f"✅ 配置已保存到 {filename}")

# 使用示例
auth_config = store.for_store().auth_service("my_api")\
    .use_bearer_auth(...)\
    .generate_fastmcp_config()

save_auth_config(auth_config, "auth_config.json")
```

### 从文件加载配置

```python
def load_auth_config(filename: str):
    """从文件加载认证配置"""
    with open(filename, 'r') as f:
        config_dict = json.load(f)
    
    # 这里可以根据配置重新创建 FastMCPAuthConfig
    print(f"✅ 配置已从 {filename} 加载")
    return config_dict
```

## 🚨 常见错误和解决方案

### 1. JWKS URI 无法访问

```
错误: Failed to fetch JWKS from https://auth.example.com/.well-known/jwks.json
```

**解决方案**:
- 检查 JWKS URI 是否可访问
- 确认网络连接和防火墙设置
- 验证 SSL 证书是否有效

### 2. Token 验证失败

```
错误: Invalid JWT token signature
```

**解决方案**:
- 检查 issuer 和 audience 是否匹配
- 确认使用的签名算法正确
- 验证 token 是否过期

### 3. 权限不足

```
错误: Insufficient scopes for this operation
```

**解决方案**:
- 检查 JWT token 中的 scopes
- 确认服务要求的 scopes 配置
- 更新用户权限或 token scopes

## 💡 配置最佳实践

1. **使用环境变量**: 永远不要硬编码敏感信息
2. **最小权限原则**: 只授予必要的权限范围
3. **定期轮换**: 定期更换认证凭据
4. **监控日志**: 监控认证失败和异常访问
5. **测试配置**: 在生产环境前充分测试认证配置
