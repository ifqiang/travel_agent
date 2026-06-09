"""
AI 旅行助手 - FastAPI 主应用
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from jinja2 import Environment, FileSystemLoader
import logging
import os

from .core.config import settings
from .db.connection import init_db
from .routers import chat, orders

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    logger.info("🚀 启动 AI 旅行助手...")
    await init_db()
    logger.info("✅ 数据库初始化完成")
    yield
    # 关闭时清理资源
    logger.info("👋 关闭 AI 旅行助手")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于 LangChain + LangGraph 的智能旅行助手",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 模板引擎
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(templates_dir))

# 注册路由
app.include_router(chat.router)
app.include_router(orders.router)


@app.get("/", tags=["page"], response_class=HTMLResponse)
async def index(request: Request):
    """主页"""
    try:
        logger.info("Rendering index.html template")
        template = jinja_env.get_template("index.html")
        return template.render(request=request)
    except Exception as e:
        logger.error(f"Error rendering template: {e}", exc_info=True)
        return f"Error: {e}"


@app.get("/health", tags=["health"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/cities", tags=["data"])
async def get_cities():
    """获取所有可用城市列表"""
    from .db.connection import get_db
    
    cities = set()
    
    async with get_db() as db:
        # 从航班数据获取城市
        cursor = await db.execute("SELECT DISTINCT departure_city FROM flights")
        for row in await cursor.fetchall():
            cities.add(row['departure_city'])
        
        cursor = await db.execute("SELECT DISTINCT arrival_city FROM flights")
        for row in await cursor.fetchall():
            cities.add(row['arrival_city'])
        
        # 从酒店数据获取城市
        cursor = await db.execute("SELECT DISTINCT city FROM hotels")
        for row in await cursor.fetchall():
            cities.add(row['city'])
        
        # 从旅游产品数据获取目的地
        cursor = await db.execute("SELECT DISTINCT destination FROM products")
        for row in await cursor.fetchall():
            cities.add(row['destination'])
    
    # 按拼音排序返回
    sorted_cities = sorted(list(cities))
    return {"cities": sorted_cities}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )