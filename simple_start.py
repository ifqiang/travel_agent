import sys
import os

# 设置环境变量
os.chdir('d:\\大数据专业综合课程设计\\travel_agent')
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'

print("=== Starting Server ===")
print("Python:", sys.executable)
print("Working Directory:", os.getcwd())

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from jinja2 import Environment, FileSystemLoader
    import uvicorn
    
    # 创建应用
    app = FastAPI()
    
    # 创建Jinja2环境
    template_dir = "app/templates"
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    
    # 简单路由 - 直接使用Jinja2渲染
    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        template = jinja_env.get_template("index.html")
        return template.render(request=request)
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    # 启动服务器
    print("Starting server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")