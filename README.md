# AI股価診断 - 全栈落地页项目

这是一个使用 React + FastAPI 构建的AI股価診断全栈落地页项目，支持用户追踪、转换管理和数据分析。

## 🚀 功能特性

### 前端功能
- 基于React的响应式股价诊断界面
- 自动用户行为追踪（滚动、点击、停留时间）
- JWT Token验证和安全访问控制
- 动态转换链接分流
- 加载状态管理和错误处理

### 后端功能
- FastAPI + SQLAlchemy + SQLite 技术栈
- JWT Token 验证和会话管理
- 用户行为事件追踪 API
- 转换链接管理和权重分流
- 后台管理接口和数据统计
- 自动数据库迁移

### 安全特性
- URL参数验证（gclid/utm_source）
- JWT Token 过期管理
- CORS 跨域保护
- API 访问权限控制

## 📁 项目结构

```
/
├── frontend/          # React 前端
│   ├── src/
│   │   ├── services/  # API服务
│   │   ├── hooks/     # React Hooks
│   │   ├── App.jsx
│   │   └── ...
│   ├── public/
│   └── package.json
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── models/    # 数据库模型
│   │   ├── routers/   # API路由
│   │   ├── core/      # 核心配置
│   │   └── database/  # 数据库配置
│   └── requirements.txt
├── data/              # SQLite数据库文件
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── nginx.conf
```

## 🗄️ 数据库结构

### tokens 表
- `id`: 主键
- `token`: JWT Token
- `expires_at`: 过期时间
- `created_at`: 创建时间

### events 表
- `id`: 主键
- `session_id`: 会话ID
- `event_type`: 事件类型（page_load, scroll, click, etc.）
- `meta`: 事件元数据（JSON）
- `created_at`: 创建时间

### conversions 表
- `id`: 主键
- `input_value`: 用户输入值
- `target_url`: 目标URL
- `session_id`: 会话ID
- `created_at`: 创建时间

### conversion_links 表
- `id`: 主键
- `name`: 链接名称
- `target_url`: 目标URL
- `weight`: 权重
- `created_at`: 创建时间

## 🔌 API 接口

### 认证接口
- `GET /api/get_token?gclid=xxx&utm_source=xxx` - 获取访问Token

### 追踪接口
- `POST /api/track` - 记录用户行为事件

### 转换接口
- `POST /api/convert` - 执行转换并获取重定向URL
- `GET /api/conversions` - 获取转换链接列表
- `POST /api/conversions` - 创建转换链接
- `PUT /api/conversions/{id}` - 更新转换链接
- `DELETE /api/conversions/{id}` - 删除转换链接

### 管理接口
- `GET /admin/conversions` - 获取所有转换记录
- `GET /admin/events` - 获取所有事件记录
- `GET /admin/stats` - 获取统计信息

## 🚀 快速开始

### 使用 Docker（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd landing-page-project
```

2. **启动服务**
```bash
# 构建并启动服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

3. **服务端口**
- 前端页面: http://localhost:3000
- 后端API: http://localhost:8000/api/
- API文档: http://localhost:8000/docs
- 管理接口: http://localhost:8000/admin/

4. **配置反向代理**
你需要在服务器上配置反向代理（如 Nginx）来统一访问：
```nginx
server {
    listen 80;
    server_name zbfxa.xyz;
    
    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 后端 API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 后端管理
    location /admin/ {
        proxy_pass http://localhost:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # 后端文档
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 开发环境

1. **启动开发环境**
```bash
docker-compose -f docker-compose.dev.yml up -d --build
```

2. **访问开发环境**
- 统一入口: http://localhost:8080
- 所有服务通过 Nginx 代理访问

### 本地开发

1. **后端开发**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **前端开发**
```bash
cd frontend
npm install
npm run dev
```

## ⚙️ 环境配置

### 后端环境变量
创建 `backend/.env` 文件：
```env
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
DATABASE_URL=sqlite:///./db.sqlite
ALLOWED_ORIGINS=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"]
```

### 前端环境变量
创建 `frontend/.env` 文件：
```env
VITE_API_URL=http://localhost:8080
```

## 📊 使用说明

### 1. 访问控制
用户访问前端时需要在URL中包含 `gclid` 或 `utm_source` 参数：
```
http://localhost:8080/?gclid=abc123
http://localhost:8080/?utm_source=google
```

### 2. 转换链接管理
使用API创建转换链接：
```bash
curl -X POST "http://localhost:8080/api/conversions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "LINE官方账号",
    "target_url": "https://line.me/R/ti/p/@example",
    "weight": 1.0
  }'
```

### 3. 数据查看
访问管理接口查看数据：
- 转换记录: `GET /admin/conversions`
- 事件记录: `GET /admin/events`
- 统计信息: `GET /admin/stats`

## 🔧 开发指南

### 添加新的事件类型
1. 在前端使用 `trackCustomEvent` 函数
2. 后端会自动记录到 events 表

### 添加新的转换链接
1. 使用 POST `/api/conversions` 接口
2. 设置合适的权重进行分流

### 自定义追踪
```javascript
import { useTracking } from './hooks/useTracking'

const { trackCustomEvent } = useTracking()

// 追踪自定义事件
trackCustomEvent('custom_action', {
  action: 'button_click',
  value: 'special_button'
})
```

## 🐛 故障排除

### 常见问题

1. **403 错误 - Missing required parameters**
   - 确保URL包含 `gclid` 或 `utm_source` 参数

2. **401 错误 - Invalid token**
   - Token可能已过期，刷新页面重新获取

3. **数据库连接错误**
   - 检查 `data/` 目录权限
   - 确保SQLite文件可写

4. **CORS错误**
   - 检查后端 `ALLOWED_ORIGINS` 配置
   - 确保前端域名在允许列表中

### 日志查看
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📈 性能优化

1. **数据库优化**
   - 定期清理过期token
   - 为高频查询字段添加索引

2. **前端优化**
   - 事件防抖处理
   - 本地存储优化

3. **后端优化**
   - 数据库连接池
   - 缓存策略

## 🔒 安全建议

1. **生产环境**
   - 更改默认SECRET_KEY
   - 使用HTTPS
   - 设置合适的CORS策略

2. **数据保护**
   - 定期备份数据库
   - 敏感数据加密存储

## 📝 更新日志

### v1.0.0
- 初始版本发布
- 基础功能实现
- Docker部署支持

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请：
1. 创建 Issue
2. 发送邮件至 support@example.com
3. 查看文档和FAQ