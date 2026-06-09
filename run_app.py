import sys
import os
import io
import traceback

# 设置环境变量
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')

print("Step 1: Setting up environment...")
print("Python:", sys.executable)
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))

try:
    print("\nStep 2: Testing basic imports...")
    import fastapi
    print("fastapi OK")
    
    import uvicorn
    print("uvicorn OK")
    
    import langchain
    print("langchain OK")
    
    import langgraph
    print("langgraph OK")
    
    import aiosqlite
    print("aiosqlite OK")
    
    import jinja2
    print("jinja2 OK")
    
    print("\nStep 3: Importing app...")
    from app.main import app
    print("App imported successfully!")
    
    print("\nStep 4: Starting server...")
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
    
except Exception as e:
    print("\nERROR:", str(e))
    print("\nTraceback:")
    traceback.print_exc()
    
    # 写入错误日志
    with open('server_error.log', 'w', encoding='utf-8') as f:
        f.write(str(e) + '\n\n')
        traceback.print_exc(file=f)
    
    print("\nError logged to server_error.log")
    input("Press Enter to exit...")