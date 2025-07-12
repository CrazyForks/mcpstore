# MCPStore Vue Frontend

基于 Vue 3 + Element Plus 的 MCPStore 前端管理界面，提供完整的 MCP 服务管理功能。

## 🚀 功能特性

### 核心功能
- **🔧 服务管理**: 添加、删除、重启、监控 MCP 服务
- **🛠️ 工具管理**: 查看、执行、管理 MCP 工具
- **👤 Agent管理**: 创建和管理 Agent 实例
- **📊 系统监控**: 实时监控系统状态和性能
- **⚙️ 系统设置**: 配置管理和系统参数

### v0.5.0 新特性
- **🏠 本地服务支持**: 完整的本地服务进程管理
- **📈 实时监控**: 服务状态、工具执行、性能指标
- **🎨 现代化UI**: 响应式设计，支持暗色主题
- **🔄 智能刷新**: 自动刷新和手动刷新机制
- **📱 移动端适配**: 完整的移动端响应式支持

## 🛠️ 技术栈

- **框架**: Vue 3.4+ (Composition API)
- **构建工具**: Vite 5.0+
- **UI组件**: Element Plus 2.4+
- **状态管理**: Pinia 2.1+
- **路由**: Vue Router 4.2+
- **图表**: ECharts 5.4+ / Vue-ECharts 6.6+
- **HTTP客户端**: Axios 1.6+
- **样式**: SCSS + CSS Variables
- **工具**: ESLint + Prettier

## 📦 快速开始

### 环境要求
- Node.js >= 16.0.0
- npm >= 8.0.0

### 安装依赖
```bash
cd src/vue
npm install
```

### 开发环境
```bash
# 启动开发服务器 (端口: 5177)
npm run dev

# 后端服务需要在 18200 端口运行
# 在项目根目录执行:
# python -m mcpstore.cli.main run api --port 18200
```

### 生产构建
```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

### 代码检查
```bash
# ESLint 检查
npm run lint

# Prettier 格式化
npm run format
```

## 🏗️ 项目结构

```
src/vue/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API 接口层
│   │   ├── request.js     # HTTP 请求封装
│   │   └── services.js    # 服务相关 API
│   ├── assets/            # 资源文件
│   ├── components/        # 通用组件
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── stores/            # Pinia 状态管理
│   │   ├── app.js         # 应用状态
│   │   └── system.js      # 系统状态
│   ├── styles/            # 样式文件
│   │   ├── variables.scss # SCSS 变量
│   │   └── index.scss     # 全局样式
│   ├── utils/             # 工具函数
│   ├── views/             # 页面组件
│   │   ├── Dashboard.vue  # 仪表板
│   │   ├── services/      # 服务管理页面
│   │   ├── tools/         # 工具管理页面
│   │   ├── agents/        # Agent管理页面
│   │   ├── Monitoring.vue # 系统监控
│   │   └── Settings.vue   # 系统设置
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── .env                   # 环境变量
├── .env.development       # 开发环境变量
├── .env.production        # 生产环境变量
├── index.html             # HTML 模板
├── package.json           # 项目配置
├── vite.config.js         # Vite 配置
└── README.md              # 项目说明
```

## 🔧 配置说明

### 环境变量
```bash
# API 配置
VITE_API_BASE_URL=http://localhost:18200  # 后端 API 地址
VITE_API_TIMEOUT=30000                    # 请求超时时间

# 开发配置
VITE_DEV_PORT=5177                        # 开发服务器端口
VITE_DEV_HOST=0.0.0.0                     # 开发服务器主机
VITE_DEV_OPEN=true                        # 自动打开浏览器

# 功能开关
VITE_ENABLE_MOCK=false                    # 启用 Mock 数据
VITE_ENABLE_DEVTOOLS=true                 # 启用开发工具
VITE_ENABLE_CONSOLE_LOG=true              # 启用控制台日志
```

### Vite 配置
- **代理配置**: `/api` 路径代理到后端服务
- **别名配置**: `@` 指向 `src` 目录
- **自动导入**: Element Plus 组件和 Vue API
- **构建优化**: 代码分割和资源优化

## 📱 页面功能

### 仪表板 (`/dashboard`)
- 系统概览统计
- 服务状态图表
- 快速操作入口
- 最近活动记录

### 服务管理
- **服务列表** (`/services/list`): 查看所有服务
- **添加服务** (`/services/add`): 注册新服务
- **本地服务** (`/services/local`): 本地服务进程管理

### 工具管理
- **工具列表** (`/tools/list`): 查看所有工具
- **工具执行** (`/tools/execute`): 执行工具操作

### Agent管理
- **Agent列表** (`/agents/list`): 管理 Agent 实例
- **创建Agent** (`/agents/create`): 创建新 Agent

### 系统功能
- **系统监控** (`/monitoring`): 性能监控和日志
- **系统设置** (`/settings`): 配置管理

## 🎨 主题和样式

### 主题支持
- **亮色主题**: 默认主题
- **暗色主题**: 支持一键切换
- **自定义主题**: 支持主色调自定义

### 响应式设计
- **桌面端**: >= 1200px
- **平板端**: 768px - 1199px
- **移动端**: < 768px

### 设计规范
- **色彩系统**: 基于 Element Plus 设计规范
- **间距系统**: 4px 基础间距单位
- **字体系统**: 系统字体栈
- **圆角系统**: 4px 基础圆角

## 🔌 API 集成

### 请求拦截器
- 自动添加时间戳防缓存
- 开发环境请求日志
- 统一错误处理

### 响应拦截器
- 业务状态码检查
- 错误消息提示
- 响应数据格式化

### API 模块
- **服务管理**: Store/Agent 级别服务操作
- **工具管理**: 工具列表和执行
- **系统监控**: 健康检查和状态
- **本地服务**: 进程管理和日志

## 🚀 部署指南

### 开发部署
```bash
# 1. 启动后端服务
python -m mcpstore.cli.main run api --port 18200

# 2. 启动前端开发服务器
cd src/vue
npm run dev
```

### 生产部署
```bash
# 1. 构建前端
cd src/vue
npm run build

# 2. 部署 dist 目录到 Web 服务器
# 例如: nginx, apache, 或静态文件服务器

# 3. 配置反向代理
# 将 /api 路径代理到后端服务
```

### Docker 部署
```dockerfile
# 多阶段构建示例
FROM node:16-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

## 🐛 故障排除

### 常见问题

1. **API 连接失败**
   - 检查后端服务是否启动 (端口 18200)
   - 检查 VITE_API_BASE_URL 配置
   - 检查网络连接和防火墙

2. **页面空白**
   - 检查浏览器控制台错误
   - 检查 Node.js 版本 (>= 16.0.0)
   - 清除浏览器缓存

3. **样式异常**
   - 检查 Element Plus 是否正确加载
   - 检查 SCSS 编译是否正常
   - 检查主题切换功能

4. **路由错误**
   - 检查 Vue Router 配置
   - 检查页面组件是否存在
   - 检查路由权限

### 调试技巧
- 开启开发者工具: `VITE_ENABLE_DEVTOOLS=true`
- 查看网络请求: 浏览器开发者工具 Network 面板
- 查看状态管理: Vue DevTools Pinia 面板
- 查看路由状态: Vue DevTools Router 面板

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE) 文件

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📞 支持

- 📧 邮箱: support@mcpstore.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/your-repo/mcpstore/issues)
- 📖 文档: [MCPStore 文档](https://docs.mcpstore.com)

---

**MCPStore Vue Frontend** - 让 MCP 服务管理变得简单高效！ 🚀
