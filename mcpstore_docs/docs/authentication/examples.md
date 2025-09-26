# 🎯 认证使用示例

本文档提供丰富的认证使用示例，涵盖各种实际应用场景。

## 🚀 基础示例

### 1. 简单的 Bearer Token 认证

最基础的 JWT 认证配置：

```python
from mcpstore import MCPStore

async def basic_bearer_auth():
    store = MCPStore()
    
    # 添加需要认证的服务
    await store.for_store().add_service_async({
        "name": "secure_api",
        "url": "https://api.example.com/mcp",
        "transport": "streamable-http"
    })
    
    # 配置 Bearer Token 认证
    auth_config = store.for_store().auth_service("secure_api")\
        .require_scopes("read", "write")\
        .use_bearer_auth(
            jwks_uri="https://auth.example.com/.well-known/jwks.json",
            issuer="https://auth.example.com",
            audience="secure_api"
        )\
        .generate_fastmcp_config()
    
    print(f"✅ 认证配置完成: {auth_config.provider_class}")
    
    # 生成用户 JWT payload
    user_token = store.for_store().auth_jwt_payload("user123")\
        .add_scopes("read", "write")\
        .add_claim("role", "user")\
        .generate_payload()
    
    print(f"✅ 用户 Token: {user_token}")
    
    return auth_config, user_token
```

### 2. 环境变量安全配置

使用环境变量保护敏感信息：

```python
import os
from mcpstore import MCPStore

async def secure_env_config():
    store = MCPStore()
    
    # 从环境变量读取敏感配置
    auth_config = store.for_store().auth_service("payment_api")\
        .require_scopes("payment:read", "payment:process")\
        .use_bearer_auth(
            jwks_uri=os.getenv("AUTH_JWKS_URI"),
            issuer=os.getenv("AUTH_ISSUER"),
            audience=os.getenv("AUTH_AUDIENCE")
        )\
        .generate_fastmcp_config()
    
    # 添加带环境变量的服务
    await store.for_store().add_service_async({
        "name": "payment_service",
        "command": "python",
        "args": ["payment_server.py"],
        "env": {
            "PAYMENT_API_KEY": os.getenv("PAYMENT_API_KEY"),
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "REDIS_URL": os.getenv("REDIS_URL")
        }
    })
    
    return auth_config
```

**对应的 .env 文件:**
```bash
# 认证配置
AUTH_JWKS_URI=https://auth.company.com/.well-known/jwks.json
AUTH_ISSUER=https://auth.company.com
AUTH_AUDIENCE=payment-service

# 服务配置
PAYMENT_API_KEY=pk_live_your_payment_api_key
DATABASE_URL=postgresql://user:pass@localhost:5432/payments
JWT_SECRET=your_super_secret_jwt_key
REDIS_URL=redis://localhost:6379/0
```

## 🌐 OAuth 集成示例

### 3. Google OAuth 企业集成

```python
import os
from mcpstore import MCPStore

async def google_oauth_enterprise():
    store = MCPStore()
    
    # 配置 Google OAuth 认证
    google_auth = store.for_store().auth_service("google_workspace")\
        .require_scopes("profile", "email", "workspace:read")\
        .use_google_auth(
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            base_url="https://enterprise.myapp.com",
            required_scopes=[
                "openid",
                "email", 
                "profile",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/workspace.documents.readonly"
            ]
        )\
        .generate_fastmcp_config()
    
    # 添加 Google Workspace 服务
    await store.for_store().add_service_async({
        "name": "google_workspace",
        "url": "https://workspace-api.company.com/mcp",
        "transport": "streamable-http",
        "headers": {
            "User-Agent": "MCPStore/1.0"
        }
    })
    
    # 为不同角色生成不同的 JWT
    admin_jwt = store.for_store().auth_jwt_payload("admin@company.com")\
        .add_scopes("profile", "email", "workspace:read", "workspace:write", "admin")\
        .add_claim("role", "admin")\
        .add_claim("department", "IT")\
        .add_claim("google_workspace_domain", "company.com")\
        .generate_payload()
    
    user_jwt = store.for_store().auth_jwt_payload("user@company.com")\
        .add_scopes("profile", "email", "workspace:read")\
        .add_claim("role", "user")\
        .add_claim("department", "sales")\
        .add_claim("google_workspace_domain", "company.com")\
        .generate_payload()
    
    return {
        "auth_config": google_auth,
        "admin_jwt": admin_jwt,
        "user_jwt": user_jwt
    }
```

### 4. GitHub OAuth 开发者工具

```python
import os
from mcpstore import MCPStore

async def github_oauth_dev_tools():
    store = MCPStore()
    
    # 配置 GitHub OAuth
    github_auth = store.for_store().auth_service("github_tools")\
        .require_scopes("repo:read", "user:read", "org:read")\
        .use_github_auth(
            client_id=os.getenv("GITHUB_CLIENT_ID"),
            client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
            base_url="https://dev.myapp.com",
            required_scopes=[
                "read:user",
                "user:email", 
                "repo",
                "read:org",
                "workflow"
            ]
        )\
        .generate_fastmcp_config()
    
    # 添加 GitHub 集成服务
    await store.for_store().add_service_async({
        "name": "github_integration",
        "command": "python",
        "args": ["github_mcp_server.py"],
        "env": {
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "GITHUB_WEBHOOK_SECRET": os.getenv("GITHUB_WEBHOOK_SECRET")
        }
    })
    
    # 为开发者生成 JWT
    developer_jwt = store.for_store().auth_jwt_payload("developer123")\
        .add_scopes("repo:read", "user:read", "org:read")\
        .add_claim("role", "developer")\
        .add_claim("team", "backend")\
        .add_claim("github_username", "developer123")\
        .add_claim("repositories", ["company/backend", "company/frontend"])\
        .generate_payload()
    
    return {
        "auth_config": github_auth,
        "developer_jwt": developer_jwt
    }
```

### 5. WorkOS 企业 SSO

```python
import os
from mcpstore import MCPStore

async def workos_enterprise_sso():
    store = MCPStore()
    
    # 配置 WorkOS 认证
    workos_auth = store.for_store().auth_service("enterprise_platform")\
        .require_scopes("admin", "user:manage", "billing:read")\
        .use_workos_auth(
            authkit_domain=os.getenv("WORKOS_AUTHKIT_DOMAIN"),
            base_url="https://enterprise.myapp.com"
        )\
        .generate_fastmcp_config()
    
    # 添加企业级服务
    await store.for_store().add_service_async({
        "name": "enterprise_platform",
        "url": "https://enterprise-api.company.com/mcp",
        "transport": "streamable-http",
        "headers": {
            "X-Enterprise-Version": "v2",
            "Authorization": f"Bearer {os.getenv('ENTERPRISE_API_TOKEN')}"
        }
    })
    
    # 为不同企业角色生成 JWT
    enterprise_admin_jwt = store.for_store().auth_jwt_payload("admin@enterprise.com")\
        .add_scopes("admin", "user:manage", "billing:read", "billing:write", "audit:read")\
        .add_claim("role", "enterprise_admin")\
        .add_claim("organization_id", "org_123456")\
        .add_claim("permissions", ["all"])\
        .add_claim("workos_org_id", os.getenv("WORKOS_ORG_ID"))\
        .generate_payload()
    
    department_manager_jwt = store.for_store().auth_jwt_payload("manager@enterprise.com")\
        .add_scopes("user:manage", "billing:read")\
        .add_claim("role", "department_manager")\
        .add_claim("organization_id", "org_123456")\
        .add_claim("department", "engineering")\
        .add_claim("managed_users", 50)\
        .generate_payload()
    
    return {
        "auth_config": workos_auth,
        "admin_jwt": enterprise_admin_jwt,
        "manager_jwt": department_manager_jwt
    }
```

## 🏢 企业级场景示例

### 6. 多租户 SaaS 平台

```python
import os
from mcpstore import MCPStore

async def multi_tenant_saas():
    store = MCPStore()
    
    # 配置主认证提供者
    main_auth = store.for_store().auth_provider("bearer")\
        .set_jwks_config(
            jwks_uri="https://auth.saasplatform.com/.well-known/jwks.json",
            issuer="https://auth.saasplatform.com",
            audience="saas-platform"
        )\
        .generate_fastmcp_config()
    
    # 为不同租户配置不同的服务
    tenants = ["tenant_a", "tenant_b", "tenant_c"]
    
    tenant_configs = {}
    
    for tenant in tenants:
        # 为每个租户配置独立的服务
        tenant_auth = store.for_store().auth_service(f"{tenant}_api")\
            .require_scopes("tenant:read", "tenant:write")\
            .use_bearer_auth(
                jwks_uri="https://auth.saasplatform.com/.well-known/jwks.json",
                issuer="https://auth.saasplatform.com",
                audience=f"{tenant}-api"
            )\
            .generate_fastmcp_config()
        
        # 添加租户特定服务
        await store.for_store().add_service_async({
            "name": f"{tenant}_service",
            "command": "python",
            "args": ["tenant_server.py"],
            "env": {
                "TENANT_ID": tenant,
                "DATABASE_URL": os.getenv(f"{tenant.upper()}_DATABASE_URL"),
                "REDIS_URL": os.getenv(f"{tenant.upper()}_REDIS_URL"),
                "S3_BUCKET": f"{tenant}-data"
            }
        })
        
        # 为租户生成不同角色的 JWT
        tenant_admin_jwt = store.for_store().auth_jwt_payload(f"admin@{tenant}.com")\
            .add_scopes("tenant:read", "tenant:write", "tenant:admin")\
            .add_claim("role", "tenant_admin")\
            .add_claim("tenant_id", tenant)\
            .add_claim("permissions", ["manage_users", "billing", "settings"])\
            .generate_payload()
        
        tenant_user_jwt = store.for_store().auth_jwt_payload(f"user@{tenant}.com")\
            .add_scopes("tenant:read", "tenant:write")\
            .add_claim("role", "tenant_user")\
            .add_claim("tenant_id", tenant)\
            .add_claim("permissions", ["read_data", "write_data"])\
            .generate_payload()
        
        tenant_configs[tenant] = {
            "auth_config": tenant_auth,
            "admin_jwt": tenant_admin_jwt,
            "user_jwt": tenant_user_jwt
        }
    
    return {
        "main_auth": main_auth,
        "tenant_configs": tenant_configs
    }
```

### 7. 微服务架构认证

```python
import os
from mcpstore import MCPStore

async def microservices_auth():
    store = MCPStore()
    
    # 服务间通信的认证配置
    services = [
        {"name": "user_service", "audience": "user-api", "scopes": ["user:read", "user:write"]},
        {"name": "order_service", "audience": "order-api", "scopes": ["order:read", "order:write"]},
        {"name": "payment_service", "audience": "payment-api", "scopes": ["payment:process"]},
        {"name": "notification_service", "audience": "notification-api", "scopes": ["notification:send"]},
        {"name": "analytics_service", "audience": "analytics-api", "scopes": ["analytics:read"]}
    ]
    
    service_configs = {}
    
    for service in services:
        # 为每个微服务配置认证
        service_auth = store.for_store().auth_service(service["name"])\
            .require_scopes(*service["scopes"])\
            .use_bearer_auth(
                jwks_uri="https://auth.microservices.com/.well-known/jwks.json",
                issuer="https://auth.microservices.com",
                audience=service["audience"]
            )\
            .generate_fastmcp_config()
        
        # 添加微服务
        await store.for_store().add_service_async({
            "name": service["name"],
            "url": f"https://{service['name'].replace('_', '-')}.microservices.com/mcp",
            "transport": "streamable-http",
            "headers": {
                "Service-Version": "v1",
                "X-Service-Name": service["name"]
            }
        })
        
        service_configs[service["name"]] = service_auth
    
    # 为不同类型的客户端生成 JWT
    
    # API 网关 JWT - 可以访问所有服务
    gateway_jwt = store.for_store().auth_jwt_payload("api_gateway")\
        .add_scopes("user:read", "user:write", "order:read", "order:write", 
                   "payment:process", "notification:send", "analytics:read")\
        .add_claim("role", "api_gateway")\
        .add_claim("client_type", "internal")\
        .generate_payload()
    
    # 前端应用 JWT - 有限权限
    frontend_jwt = store.for_store().auth_jwt_payload("frontend_app")\
        .add_scopes("user:read", "order:read", "order:write")\
        .add_claim("role", "frontend")\
        .add_claim("client_type", "web")\
        .generate_payload()
    
    # 移动应用 JWT
    mobile_jwt = store.for_store().auth_jwt_payload("mobile_app")\
        .add_scopes("user:read", "user:write", "order:read", "order:write", "notification:send")\
        .add_claim("role", "mobile")\
        .add_claim("client_type", "mobile")\
        .add_claim("platform", "ios")\
        .generate_payload()
    
    # 后台管理 JWT - 管理员权限
    admin_jwt = store.for_store().auth_jwt_payload("admin_dashboard")\
        .add_scopes("user:read", "user:write", "order:read", "order:write", 
                   "payment:process", "analytics:read", "admin")\
        .add_claim("role", "admin")\
        .add_claim("client_type", "dashboard")\
        .add_claim("permissions", ["user_management", "order_management", "system_config"])\
        .generate_payload()
    
    return {
        "service_configs": service_configs,
        "client_jwts": {
            "gateway": gateway_jwt,
            "frontend": frontend_jwt,
            "mobile": mobile_jwt,
            "admin": admin_jwt
        }
    }
```

## 🔧 Hub 认证示例

### 8. 安全工具 Hub

```python
import os
from mcpstore import MCPStore

async def secure_tools_hub():
    store = MCPStore()
    
    # 创建安全工具 Hub
    secure_hub = store.for_store().build_hub("secure-tools-hub")\
        .add_service("user_management", ["create_user", "delete_user", "update_user"])\
        .add_service("payment_processing", ["process_payment", "refund_payment"])\
        .add_service("data_analytics", ["generate_report", "export_data"])\
        .add_service("system_monitoring", ["get_metrics", "alert_status"])\
        .set_auth_config({
            "auth_enabled": True,
            "provider_type": "bearer",
            "jwks_uri": "https://auth.company.com/.well-known/jwks.json",
            "issuer": "https://auth.company.com",
            "audience": "secure-hub",
            "required_scopes": ["hub:access"],
            "protected_tools": [
                "create_user", "delete_user", "update_user",
                "process_payment", "refund_payment",
                "export_data"
            ],
            "public_tools": [
                "get_metrics", "alert_status"
            ]
        })
    
    # 生成 Hub
    hub_config = await secure_hub.generate_async()
    
    # 为不同角色生成访问 Hub 的 JWT
    
    # 系统管理员 - 可访问所有工具
    admin_jwt = store.for_store().auth_jwt_payload("system_admin")\
        .add_scopes("hub:access", "admin", "user:manage", "payment:process", "data:export")\
        .add_claim("role", "system_admin")\
        .add_claim("hub_permissions", ["all_tools"])\
        .generate_payload()
    
    # 用户管理员 - 只能管理用户
    user_admin_jwt = store.for_store().auth_jwt_payload("user_admin")\
        .add_scopes("hub:access", "user:manage")\
        .add_claim("role", "user_admin")\
        .add_claim("hub_permissions", ["create_user", "update_user", "delete_user"])\
        .generate_payload()
    
    # 财务人员 - 只能处理支付
    finance_jwt = store.for_store().auth_jwt_payload("finance_user")\
        .add_scopes("hub:access", "payment:process")\
        .add_claim("role", "finance")\
        .add_claim("hub_permissions", ["process_payment", "refund_payment"])\
        .generate_payload()
    
    # 分析师 - 只能查看数据和报告
    analyst_jwt = store.for_store().auth_jwt_payload("data_analyst")\
        .add_scopes("hub:access", "data:read")\
        .add_claim("role", "analyst")\
        .add_claim("hub_permissions", ["generate_report", "get_metrics", "alert_status"])\
        .generate_payload()
    
    return {
        "hub_config": hub_config,
        "role_jwts": {
            "admin": admin_jwt,
            "user_admin": user_admin_jwt,
            "finance": finance_jwt,
            "analyst": analyst_jwt
        }
    }
```

## 🧪 开发和测试示例

### 9. 开发环境认证配置

```python
import os
from mcpstore import MCPStore

async def development_auth_setup():
    """开发环境的认证配置 - 更宽松的设置"""
    store = MCPStore()
    
    # 开发环境使用本地认证服务
    dev_auth = store.for_store().auth_service("dev_api")\
        .require_scopes("read", "write", "debug")\
        .use_bearer_auth(
            jwks_uri="http://localhost:8080/.well-known/jwks.json",
            issuer="http://localhost:8080",
            audience="dev-api",
            algorithm="HS256"  # 开发环境使用简单算法
        )\
        .generate_fastmcp_config()
    
    # 添加开发服务
    await store.for_store().add_service_async({
        "name": "dev_service",
        "command": "python",
        "args": ["dev_server.py"],
        "env": {
            "ENVIRONMENT": "development",
            "DEBUG": "true",
            "LOG_LEVEL": "debug",
            "MOCK_EXTERNAL_APIS": "true"
        }
    })
    
    # 开发者 JWT - 拥有所有权限
    developer_jwt = store.for_store().auth_jwt_payload("developer")\
        .add_scopes("read", "write", "debug", "admin", "test")\
        .add_claim("role", "developer")\
        .add_claim("environment", "development")\
        .add_claim("debug_mode", True)\
        .generate_payload()
    
    return {
        "auth_config": dev_auth,
        "developer_jwt": developer_jwt
    }

async def testing_auth_setup():
    """测试环境的认证配置"""
    store = MCPStore()
    
    # 测试环境认证配置
    test_auth = store.for_store().auth_service("test_api")\
        .require_scopes("read", "write", "test")\
        .use_bearer_auth(
            jwks_uri="https://test-auth.company.com/.well-known/jwks.json",
            issuer="https://test-auth.company.com",
            audience="test-api"
        )\
        .generate_fastmcp_config()
    
    # 测试用户 JWT
    test_user_jwt = store.for_store().auth_jwt_payload("test_user")\
        .add_scopes("read", "write", "test")\
        .add_claim("role", "test_user")\
        .add_claim("environment", "testing")\
        .add_claim("test_suite", "integration")\
        .generate_payload()
    
    return {
        "auth_config": test_auth,
        "test_jwt": test_user_jwt
    }
```

### 10. 性能测试和监控

```python
import os
import time
from mcpstore import MCPStore

async def performance_monitoring_auth():
    """性能监控的认证配置"""
    store = MCPStore()
    
    # 配置监控服务认证
    monitoring_auth = store.for_store().auth_service("monitoring_api")\
        .require_scopes("metrics:read", "logs:read", "alerts:manage")\
        .use_bearer_auth(
            jwks_uri="https://auth.company.com/.well-known/jwks.json",
            issuer="https://auth.company.com",
            audience="monitoring-api"
        )\
        .generate_fastmcp_config()
    
    # 为监控工具生成 JWT
    monitoring_jwt = store.for_store().auth_jwt_payload("monitoring_system")\
        .add_scopes("metrics:read", "logs:read", "alerts:manage")\
        .add_claim("role", "monitoring")\
        .add_claim("system", "prometheus")\
        .add_claim("instance", "prod-monitor-01")\
        .add_claim("start_time", int(time.time()))\
        .generate_payload()
    
    # 性能测试 JWT
    perf_test_jwt = store.for_store().auth_jwt_payload("perf_tester")\
        .add_scopes("read", "write", "test:performance")\
        .add_claim("role", "performance_tester")\
        .add_claim("test_type", "load_test")\
        .add_claim("max_requests_per_second", 1000)\
        .generate_payload()
    
    return {
        "monitoring_auth": monitoring_auth,
        "monitoring_jwt": monitoring_jwt,
        "perf_test_jwt": perf_test_jwt
    }
```

## 🔄 完整的端到端示例

### 11. 电商平台完整认证方案

```python
import os
import asyncio
from mcpstore import MCPStore

async def ecommerce_platform_auth():
    """电商平台的完整认证方案"""
    store = MCPStore()
    
    # === 1. 配置全局认证提供者 ===
    global_auth = store.for_store().auth_provider("bearer")\
        .set_jwks_config(
            jwks_uri="https://auth.ecommerce.com/.well-known/jwks.json",
            issuer="https://auth.ecommerce.com",
            audience="ecommerce-platform"
        )\
        .generate_fastmcp_config()
    
    # === 2. 配置各个微服务的认证 ===
    
    services_config = {}
    
    # 用户服务
    user_auth = store.for_store().auth_service("user_service")\
        .require_scopes("user:read", "user:write")\
        .use_bearer_auth(
            jwks_uri="https://auth.ecommerce.com/.well-known/jwks.json",
            issuer="https://auth.ecommerce.com",
            audience="user-service"
        )\
        .generate_fastmcp_config()
    services_config["user"] = user_auth
    
    # 产品目录服务
    catalog_auth = store.for_store().auth_service("catalog_service")\
        .require_scopes("catalog:read")\
        .use_bearer_auth(
            jwks_uri="https://auth.ecommerce.com/.well-known/jwks.json",
            issuer="https://auth.ecommerce.com",
            audience="catalog-service"
        )\
        .generate_fastmcp_config()
    services_config["catalog"] = catalog_auth
    
    # 订单服务
    order_auth = store.for_store().auth_service("order_service")\
        .require_scopes("order:read", "order:write")\
        .use_bearer_auth(
            jwks_uri="https://auth.ecommerce.com/.well-known/jwks.json",
            issuer="https://auth.ecommerce.com",
            audience="order-service"
        )\
        .generate_fastmcp_config()
    services_config["order"] = order_auth
    
    # 支付服务 - 高安全级别
    payment_auth = store.for_store().auth_service("payment_service")\
        .require_scopes("payment:process", "payment:refund")\
        .use_bearer_auth(
            jwks_uri="https://auth.ecommerce.com/.well-known/jwks.json",
            issuer="https://auth.ecommerce.com",
            audience="payment-service"
        )\
        .generate_fastmcp_config()
    services_config["payment"] = payment_auth
    
    # === 3. 添加所有服务 ===
    
    services = [
        {
            "name": "user_service",
            "url": "https://user-api.ecommerce.com/mcp",
            "transport": "streamable-http"
        },
        {
            "name": "catalog_service", 
            "url": "https://catalog-api.ecommerce.com/mcp",
            "transport": "streamable-http"
        },
        {
            "name": "order_service",
            "url": "https://order-api.ecommerce.com/mcp", 
            "transport": "streamable-http"
        },
        {
            "name": "payment_service",
            "url": "https://payment-api.ecommerce.com/mcp",
            "transport": "streamable-http",
            "headers": {
                "X-Security-Level": "high"
            }
        }
    ]
    
    for service in services:
        await store.for_store().add_service_async(service)
    
    # === 4. 创建电商 Hub ===
    
    ecommerce_hub = store.for_store().build_hub("ecommerce-platform")\
        .add_service("user_service", ["get_user", "create_user", "update_user"])\
        .add_service("catalog_service", ["search_products", "get_product", "get_categories"])\
        .add_service("order_service", ["create_order", "get_order", "update_order", "cancel_order"])\
        .add_service("payment_service", ["process_payment", "refund_payment", "get_payment_status"])\
        .set_auth_config({
            "auth_enabled": True,
            "provider_type": "bearer",
            "jwks_uri": "https://auth.ecommerce.com/.well-known/jwks.json",
            "issuer": "https://auth.ecommerce.com", 
            "audience": "ecommerce-hub",
            "required_scopes": ["ecommerce:access"],
            "protected_tools": [
                "create_user", "update_user",
                "create_order", "update_order", "cancel_order",
                "process_payment", "refund_payment"
            ],
            "public_tools": [
                "search_products", "get_product", "get_categories",
                "get_order", "get_payment_status"
            ]
        })
    
    hub_config = await ecommerce_hub.generate_async()
    
    # === 5. 为不同角色生成 JWT ===
    
    role_jwts = {}
    
    # 顾客 JWT
    customer_jwt = store.for_store().auth_jwt_payload("customer_123")\
        .add_scopes("ecommerce:access", "catalog:read", "order:read", "order:write", "user:read")\
        .add_claim("role", "customer")\
        .add_claim("customer_id", "cust_123")\
        .add_claim("customer_tier", "premium")\
        .generate_payload()
    role_jwts["customer"] = customer_jwt
    
    # 商家 JWT
    merchant_jwt = store.for_store().auth_jwt_payload("merchant_456")\
        .add_scopes("ecommerce:access", "catalog:read", "catalog:write", "order:read", "user:read")\
        .add_claim("role", "merchant")\
        .add_claim("merchant_id", "merch_456")\
        .add_claim("store_name", "Tech Store")\
        .generate_payload()
    role_jwts["merchant"] = merchant_jwt
    
    # 客服 JWT
    support_jwt = store.for_store().auth_jwt_payload("support_789")\
        .add_scopes("ecommerce:access", "user:read", "order:read", "order:write", "catalog:read")\
        .add_claim("role", "support")\
        .add_claim("support_level", "tier2")\
        .add_claim("department", "customer_service")\
        .generate_payload()
    role_jwts["support"] = support_jwt
    
    # 管理员 JWT
    admin_jwt = store.for_store().auth_jwt_payload("admin_000")\
        .add_scopes("ecommerce:access", "user:read", "user:write", "catalog:read", "catalog:write", 
                   "order:read", "order:write", "payment:process", "payment:refund", "admin")\
        .add_claim("role", "admin")\
        .add_claim("admin_level", "super")\
        .add_claim("permissions", ["all"])\
        .generate_payload()
    role_jwts["admin"] = admin_jwt
    
    # 财务 JWT
    finance_jwt = store.for_store().auth_jwt_payload("finance_111")\
        .add_scopes("ecommerce:access", "payment:process", "payment:refund", "order:read")\
        .add_claim("role", "finance")\
        .add_claim("department", "finance")\
        .add_claim("payment_limit", 10000)\
        .generate_payload()
    role_jwts["finance"] = finance_jwt
    
    return {
        "global_auth": global_auth,
        "services_config": services_config,
        "hub_config": hub_config,
        "role_jwts": role_jwts
    }

# === 运行完整示例 ===
async def run_ecommerce_example():
    print("🛒 配置电商平台认证系统...")
    
    result = await ecommerce_platform_auth()
    
    print("✅ 全局认证配置完成")
    print(f"✅ 配置了 {len(result['services_config'])} 个服务的认证")
    print(f"✅ 创建了电商 Hub: {result['hub_config']}")
    print(f"✅ 生成了 {len(result['role_jwts'])} 种角色的 JWT")
    
    # 展示各角色的权限
    print("\n👥 角色权限总结:")
    for role, jwt in result['role_jwts'].items():
        print(f"  {role}: {jwt['scopes']}")
    
    return result

if __name__ == "__main__":
    asyncio.run(run_ecommerce_example())
```

## 🎓 学习要点总结

通过这些示例，你可以学到：

1. **基础认证配置** - Bearer Token 的基本使用
2. **环境变量安全** - 如何安全地管理敏感信息
3. **OAuth 集成** - 与第三方认证提供者的集成
4. **企业级应用** - 多租户和微服务架构的认证
5. **Hub 认证** - 工具级别的权限控制
6. **角色权限管理** - 基于角色的访问控制
7. **开发测试配置** - 不同环境的认证策略
8. **完整方案设计** - 端到端的认证架构

每个示例都可以作为你项目的起点，根据具体需求进行调整和扩展。
