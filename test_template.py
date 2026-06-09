import sys
import os

os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')

print("=== Testing Template Loading ===")

try:
    from fastapi import FastAPI, Request
    from fastapi.templating import Jinja2Templates
    
    app = FastAPI()
    
    # 尝试加载模板
    templates = Jinja2Templates(directory="app/templates")
    
    # 检查模板文件
    import os.path
    template_path = os.path.join("app/templates", "index.html")
    print("Template path:", template_path)
    print("Template exists:", os.path.exists(template_path))
    
    # 列出模板目录
    print("\nTemplates directory contents:")
    for f in os.listdir("app/templates"):
        print(f"  - {f}")
    
    # 测试模板响应
    @app.get("/")
    async def root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    
    print("\n=== Starting Server on Port 8002 ===")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
