
# AI 旅行助手 - Docker 部署指南

## 项目概述

本项目是一个基于 **FastAPI + LangChain + LangGraph** 的智能旅行助手应用，提供航班查询、酒店预订、旅游产品推荐等功能。

## 技术栈

- **框架**: FastAPI 0.115.0
- **语言**: Python 3.11
- **AI 引擎**: LangChain 0.3.7 + LangGraph 0.2.45
- **数据库**: SQLite (aiosqlite)
- **模板引擎**: Jinja2
- **ASGI 服务器**: Uvicorn

## 项目结构

```
travel-agent/
├── app/                      # 应用主目录
│   ├── main.py              # FastAPI 主应用
│   ├── core/                # 核心模块
│   │   └── config.py        # 配置管理
│   ├── db/                  # 数据库模块
│   │   └── connection.py    # 数据库连接
│   ├── agent/               # AI Agent 模块
│   │   ├── graph.py         # LangGraph 对话图
│   │   ├── prompts.py       # 提示词模板
│   │   └── tools.py         # 工具函数
│   ├── routers/             # API 路由
│   │   ├── chat.py          # 对话接口
│   │   └── orders.py        # 订单接口
│   └── templates/           # HTML 模板
│       └── index.html       # 主页模板
├── requirements.txt         # 依赖列表
├── Dockerfile               # Docker 镜像构建文件
└── DOCKER.md               # Docker 部署文档
```

## 快速开始

### 1. 构建 Docker 镜像

```bash
# 进入项目目录
cd d:\travel_agent

# 构建 Docker 镜像（使用默认标签）
docker build -t travel_agent .

# 或者指定版本标签
docker build -t travel_agent:v1.0.0 .
```

### 2. 运行容器

#### 方式一：基础运行（使用默认配置）

```bash
docker run -d \
  -p 8000:8000 \
  --name travel_agent \
  travel_agent
```

#### 方式二：自定义端口映射

```bash
docker run -d \
  -p 5000:8000 \
  --name travel_agent \
  travel_agent
```

#### 方式三：使用环境变量配置

```bash
docker run -d \
  -p 8000:8000 \
  --name travel_agent \
  -e API_KEY="your-api-key" \
  -e MODEL_NAME="deepseek-v3" \
  -e DEBUG=false \
  travel_agent
```

#### 方式四：挂载外部数据库（推荐生产环境）

```bash
docker run -d \
  -p 8000:8000 \
  --name travel_agent \
  -v /path/to/your/database:/app \
  -e DATABASE_URL="sqlite+aiosqlite:///./travel_assistant.db" \
  travel_agent
```

### 3. 访问服务

启动后，服务将在以下地址提供：

| 地址 | 说明 |
|------|------|
| `http://localhost:8000` | 主页（Web 界面） |
| `http://localhost:8000/docs` | API 文档（Swagger UI） |
| `http://localhost:8000/redoc` | API 文档（ReDoc） |
| `http://localhost:8000/health` | 健康检查接口 |
| `http://localhost:8000/cities` | 获取可用城市列表 |

> 💡 **提示**：如果使用 `-p 5000:8000` 映射端口，请将上述地址中的 `8000` 替换为 `5000`。

## 环境变量配置

以下是支持的环境变量列表：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `API_BASE_URL` | `https://ai-api-prod.qingjiao.art/v1` | AI API 基础地址 |
| `API_KEY` | `1XajEZXRr9YzCW0C2cB5A1B11d03441a8fA32f30F96d5459` | API 密钥（生产环境需替换） |
| `MODEL_NAME` | `deepseek-v3` | 使用的 AI 模型名称 |
| `APP_NAME` | `AI 旅行助手` | 应用名称 |
| `APP_VERSION` | `1.0.0` | 应用版本号 |
| `DEBUG` | `true` | 调试模式开关 |
| `DATABASE_URL` | `sqlite+aiosqlite:///./travel_assistant.db` | 数据库连接 URL |
| `HOST` | `0.0.0.0` | 服务绑定地址 |
| `PORT` | `8000` | 服务端口 |

#### 配置优先级

配置加载优先级（从高到低）：

1. **环境变量** - 最高优先级
2. **`.env` 文件** - 次优先级
3. **默认值** - 代码中的默认值

#### `.env` 文件示例

在使用 Docker 时，可以创建 `.env` 文件并通过卷挂载到容器中：

```env
# AI API 配置
API_BASE_URL=https://ai-api-prod.qingjiao.art/v1
API_KEY=your_api_key_here
MODEL_NAME=deepseek-v3

# 应用配置
APP_NAME=AI 旅行助手
APP_VERSION=1.0.0
DEBUG=False

# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./travel_assistant.db

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

使用 `.env` 文件启动：

```bash
docker run -d \
  -p 8000:8000 \
  --name travel_agent \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/travel_assistant.db:/app/travel_assistant.db \
  travel_agent
```

#### 修改 AI 模型

如需更换 AI 模型，在 Docker 环境中配置：

```bash
# 使用 OpenAI
docker run -d \
  -p 8000:8000 \
  --name travel_agent \
  -e API_BASE_URL=https://api.openai.com/v1 \
  -e API_KEY=sk-your-openai-key \
  -e MODEL_NAME=gpt-4 \
  travel_agent

# 或使用 DeepSeek
docker run -d \
  -p 8000:8000 \
  --name travel_agent \
  -e API_BASE_URL=https://api.deepseek.com/v1 \
  -e API_KEY=sk-your-deepseek-key \
  -e MODEL_NAME=deepseek-chat \
  travel_agent
```

## Docker Compose 示例

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  travel_agent:
    build: .
    container_name: travel_agent
    ports:
      - "8000:8000"
    environment:
      - API_KEY=your-production-api-key
      - DEBUG=false
      - MODEL_NAME=deepseek-v3
    volumes:
      - ./travel_assistant.db:/app/travel_assistant.db
    restart: unless-stopped
```

运行：

```bash
docker-compose up -d
```

## Dockerfile 详解

当前项目的 `Dockerfile` 内容如下：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY travel_assistant.db .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```


### 构建优化建议

如需优化镜像大小，可使用多阶段构建：

```dockerfile
# 构建阶段
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 运行阶段
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app ./app
COPY travel_assistant.db .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境镜像构建

```bash
# 构建生产镜像（禁用调试，压缩体积）
docker build \
  --build-arg DEBUG=false \
  -t travel_agent:latest \
  --target production \
  .

# 使用 BuildKit 进行优化构建
DOCKER_BUILDKIT=1 docker build -t travel_agent:latest .
```

## API 接口说明

### 核心接口

| 接口地址 | 方法 | 说明 |
|---------|------|------|
| `/` | GET | 主页（Web 界面） |
| `/docs` | GET | API 文档（Swagger UI） |
| `/redoc` | GET | API 文档（ReDoc） |
| `/health` | GET | 健康检查接口 |
| `/cities` | GET | 获取所有可用城市列表 |

### 对话接口

#### `POST /api/chat`

发送对话消息，支持流式响应。

**请求体：**
```json
{
  "message": "帮我查询北京到上海的航班",
  "session_id": "user_session_001"
}
```

**响应：** SSE 流式事件

#### `GET /api/chat/history/{session_id}`

获取会话历史记录。

### 订单接口

| 接口地址 | 方法 | 说明 |
|---------|------|------|
| `/api/orders` | GET | 获取订单列表 |
| `/api/orders` | POST | 创建新订单 |

## 常见问题

### 1. 端口冲突

**问题**: 容器启动失败，提示端口已被占用

**解决方案**:

```bash
# 查看端口占用
netstat -ano | findstr :8000

# 使用其他端口启动
docker run -d -p 8080:8000 --name travel_agent travel_agent
```

### 2. 数据库权限问题

**问题**: 容器无法访问数据库文件

**解决方案**:

```bash
# 修改数据库文件权限
chmod 644 travel_assistant.db

# 或使用卷挂载
docker run -d -p 8000:8000 -v $(pwd)/travel_assistant.db:/app/travel_assistant.db travel_agent
```

### 3. API 密钥配置

**问题**: API 调用失败，提示认证错误

**解决方案**:

```bash
# 通过环境变量传入正确的 API 密钥
docker run -d -p 8000:8000 -e API_KEY="your-actual-api-key" travel_agent
```

### 4. 调试模式

**问题**: 生产环境需要关闭调试模式

**解决方案**:

```bash
docker run -d -p 8000:8000 -e DEBUG=false travel_agent
```

## 生产环境部署建议

1. **使用环境变量管理敏感信息**：不要在代码中硬编码 API 密钥等敏感信息
2. **使用反向代理**：建议使用 Nginx 或 Traefik 作为反向代理
3. **配置健康检查**：在 Docker Compose 或 Kubernetes 中配置健康检查
4. **定期备份数据库**：定期备份 SQLite 数据库文件
5. **使用 Docker Secrets**：在生产环境中使用 Docker Secrets 管理敏感配置
6. **限制容器资源**：使用 `--memory` 和 `--cpus` 参数限制容器资源使用

### 高级配置示例

#### Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 支持 WebSocket（用于 SSE 流式响应）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### Docker 健康检查配置

在 `docker-compose.yml` 中添加健康检查：

```yaml
services:
  travel_agent:
    build: .
    container_name: travel_agent
    ports:
      - "8000:8000"
    environment:
      - API_KEY=your-api-key
      - DEBUG=false
    volumes:
      - ./travel_assistant.db:/app/travel_assistant.db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
```

## 日志查看

```bash
# 查看容器日志
docker logs travel_agent

# 实时查看日志
docker logs -f travel_agent

# 查看最近 100 条日志
docker logs --tail=100 travel_agent
```

## 容器管理

```bash
# 停止容器
docker stop travel_agent

# 启动容器
docker start travel_agent

# 重启容器
docker restart travel_agent

# 删除容器
docker rm travel_agent

# 删除镜像
docker rmi travel_agent
```

## Docker 部署 vs 本地部署

### 对比表

| 特性 | Docker 部署 | 本地部署 |
|------|-------------|---------|
| **环境依赖** | 自动包含所有依赖 | 需要手动安装 Python 和依赖 |
| **环境隔离** | 完全隔离 | 可能与其他项目冲突 |
| **部署速度** | 首次构建慢，后续启动快 | 安装依赖较慢 |
| **可移植性** | 一次构建，到处运行 | 需要在不同机器重新配置 |
| **生产就绪** | ✅ 适合生产环境 | ⚠️ 需要额外配置（gunicorn 等） |
| **调试难度** | 需要进入容器调试 | 直接本地调试 |
| **资源占用** | 占用额外资源 | 资源占用较小 |

### 选择建议

**使用 Docker 部署的场景：**
- ✅ 生产环境部署
- ✅ 团队协作（统一开发环境）
- ✅ 云服务器部署（如腾讯云、阿里云）
- ✅ 快速搭建演示环境
- ✅ 多服务架构

**使用本地部署的场景：**
- ✅ 本地开发和调试
- ✅ 资源受限环境
- ✅ 快速原型验证
- ✅ 需要频繁修改代码并查看效果

### 本地部署命令（参考）

如果选择本地部署，可使用以下命令：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 直接启动
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 或使用 Python 直接运行
python -m app.main

# 3. 开发模式（热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 4. 生产环境（需要先安装 gunicorn）
pip install gunicorn
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

## 在线部署示例

项目已部署在腾讯云 Docker 环境，可直接访问：

- **主页**: http://159.75.23.163:5000
- **API 文档**: http://159.75.23.163:5000/docs
- **健康检查**: http://159.75.23.163:5000/health
