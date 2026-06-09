import sys
import os
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')

print("=== Testing Template Loading ===")
print("Current directory:", os.getcwd())

# 检查模板文件
import os.path
template_path = os.path.join("app/templates", "index.html")
print("Template path:", template_path)
print("Template exists:", os.path.exists(template_path))

# 列出模板目录
print("\nTemplates directory contents:")
if os.path.exists("app/templates"):
    for f in os.listdir("app/templates"):
        print(f"  - {f}")
else:
    print("  ERROR: Templates directory does not exist!")

try:
    from fastapi import FastAPI, Request
    from fastapi.templating import Jinja2Templates
    import uvicorn
    
    app = FastAPI()
    
    # 尝试加载模板
    print("\nLoading templates...")
    templates = Jinja2Templates(directory="app/templates")
    print("Templates loaded successfully!")
    
    # 测试模板响应
    @app.get("/")
    async def root(request: Request):
        print("Rendering template...")
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            print(f"ERROR rendering template: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    print("\n=== Starting Server on Port 8003 ===")
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="debug")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
