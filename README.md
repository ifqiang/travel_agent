# 🌍 AI 旅行助手

基于 **FastAPI + LangChain + LangGraph** 构建的智能旅行助手应用，提供自然语言交互的旅行规划服务。

---

## 📖 项目介绍

AI 旅行助手是一个智能化的旅行服务平台，通过 AI 对话的方式帮助用户：

- ✈️ **查询航班信息** - 搜索航班、比较价格、查看时刻表
- 🏨 **预订酒店** - 查找酒店、比较房型、查看评价
- 🎯 **旅游产品推荐** - 根据目的地推荐旅游套餐
- 💬 **智能对话** - 自然语言交互，理解用户意图
- 📋 **订单管理** - 查看和管理预订订单

### 核心特性

| 特性 | 说明 |
|------|------|
| 🤖 AI 驱动 | 基于 LangChain + LangGraph 构建智能对话流程 |
| 🔄 流式响应 | 支持 SSE 流式输出，实时响应对话 |
| 💾 数据持久化 | SQLite 数据库存储航班、酒店、订单等数据 |
| 🎨 现代界面 | 响应式 Web 界面，支持移动端访问 |
| ⚡ 高性能 | 异步处理，FastAPI 高并发支持 |

---

## 🛠 技术栈

| 类别 | 技术 |
|------|------|
| **Web 框架** | FastAPI 0.115.0 |
| **AI 框架** | LangChain 0.3.7 + LangGraph 0.2.45 |
| **数据库** | SQLite + aiosqlite (异步) |
| **模板引擎** | Jinja2 |
| **HTTP 客户端** | httpx |
| **数据验证** | Pydantic v2 |
| **ASGI 服务器** | Uvicorn |

---

## 🚀 启动方法

### 方式一：直接启动（推荐）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 或使用 Python 直接运行
python -m app.main
```

### 方式二：开发模式（热重载）

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器（支持代码热重载）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 方式三：生产环境部署

```bash
# 使用 Gunicorn + Uvicorn Workers
pip install gunicorn

gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

### 访问地址

#### 🌐 在线访问（已部署）

| 地址 | 说明 |
|------|------|
| `http://159.75.23.163:5000` | 主页（Web 界面） |
| `http://159.75.23.163:5000/docs` | API 文档（Swagger UI） |
| `http://159.75.23.163:5000/redoc` | API 文档（ReDoc） |
| `http://159.75.23.163:5000/health` | 健康检查接口 |

> 🎉 **在线体验**：项目已部署在腾讯云 Docker 环境，可直接访问 [http://159.75.23.163:5000](http://159.75.23.163:5000) 体验完整功能！

#### 💻 本地开发访问

启动成功后，可通过以下本地地址访问：

| 地址 | 说明 |
|------|------|
| `http://localhost:8000` | 主页（Web 界面） |
| `http://localhost:8000/docs` | API 文档（Swagger UI） |
| `http://localhost:8000/redoc` | API 文档（ReDoc） |
| `http://localhost:8000/health` | 健康检查接口 |

> 💡 **本地调试**：在本地开发环境中，使用 `http://localhost:8000` 进行接口测试和功能调试。

---

## ⚙️ 配置说明

### 环境变量配置

项目支持通过 `.env` 文件或环境变量进行配置。

#### 创建配置文件

在项目根目录创建 `.env` 文件：

```bash
# 复制示例配置（如果有）
cp .env.example .env

# 或直接创建
touch .env
```

#### 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `API_BASE_URL` | `https://ai-api-prod.qingjiao.art/v1` | AI API 基础地址 |
| `API_KEY` | `1XajEZXRr9YzCW0C2cB5A1B11d03441a8fA32f30F96d5459` | AI API 密钥 |
| `MODEL_NAME` | `deepseek-v3` | 使用的模型名称 |
| `APP_NAME` | `AI 旅行助手` | 应用名称 |
| `APP_VERSION` | `1.0.0` | 应用版本 |
| `DEBUG` | `True` | 调试模式 |
| `DATABASE_URL` | `sqlite+aiosqlite:///./travel_assistant.db` | 数据库连接地址 |
| `HOST` | `0.0.0.0` | 服务监听地址 |
| `PORT` | `8000` | 服务监听端口 |

#### `.env` 文件示例

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

### 配置优先级

配置加载优先级（从高到低）：

1. **环境变量** - 最高优先级
2. **`.env` 文件** - 次优先级
3. **默认值** - 代码中的默认值

### 修改 AI 模型

如需更换 AI 模型，修改以下配置：

```env
# 使用 OpenAI
API_BASE_URL=https://api.openai.com/v1
API_KEY=sk-your-openai-key
MODEL_NAME=gpt-4

# 或使用 DeepSeek
API_BASE_URL=https://api.deepseek.com/v1
API_KEY=sk-your-deepseek-key
MODEL_NAME=deepseek-chat
```

---

## 📁 项目结构

```
travel-assistant/
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
│   ├── templates/           # HTML 模板
│   │   └── index.html       # 主页模板
│   └── static/              # 静态资源
├── tests/                   # 测试文件
├── requirements.txt         # 依赖列表
├── .env                     # 环境配置（需创建）
├── .inscode                 # Inscode 运行配置
└── README.md                # 本文档
```

---

## 📡 API 接口

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

### 数据接口

#### `GET /cities`

获取所有可用城市列表。

#### `GET /health`

健康检查接口。

### 订单接口

#### `GET /api/orders`

获取订单列表。

#### `POST /api/orders`

创建新订单。

---

## 🔧 开发指南

### 安装开发依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 或使用项目提供的测试脚本
python run_tests.py
```

### 代码风格

- 使用 **Black** 格式化代码
- 使用 **isort** 整理导入
- 遵循 **PEP 8** 规范

---

## 🐛 常见问题

### Q: 启动时提示数据库错误？

**A:** 确保项目有写入权限，数据库文件 `travel_assistant.db` 会自动创建。

### Q: AI 对话无响应？

**A:** 检查以下配置：
1. `API_KEY` 是否正确
2. `API_BASE_URL` 是否可访问
3. 网络连接是否正常

### Q: 如何查看日志？

**A:** 日志会输出到控制台，调试模式下日志级别为 DEBUG。

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ by AI Travel Assistant Team**