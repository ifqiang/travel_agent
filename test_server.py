import sys
import os

# 设置环境变量
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')

print("=== Test Server ===")
print("Python:", sys.executable)
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))

try:
    from fastapi import FastAPI
    from fastapi.templating import Jinja2Templates
    import uvicorn
    
    app = FastAPI()
    templates = Jinja2Templates(directory="app/templates")
    
    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    print("\nStarting test server on http://127.0.0.1:8080")
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()