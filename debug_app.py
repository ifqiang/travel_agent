import sys
import os

print("=" * 60)
print("DEBUGGING APPLICATION STARTUP")
print("=" * 60)

# 设置路径
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'

print("\n1. Python Version: " + sys.version)
print("2. Python Executable: " + sys.executable)
print("3. Working Directory: " + os.getcwd())
print("4. PYTHONPATH: " + os.environ.get('PYTHONPATH', 'Not set'))

# 测试依赖导入
print("\n5. Testing Dependencies...")
try:
    import fastapi
    print("   OK fastapi: " + fastapi.__version__)
except Exception as e:
    print("   ERR fastapi: " + str(e))

try:
    import uvicorn
    print("   OK uvicorn: " + uvicorn.__version__)
except Exception as e:
    print("   ERR uvicorn: " + str(e))

try:
    import langchain
    print("   OK langchain: " + langchain.__version__)
except Exception as e:
    print("   ERR langchain: " + str(e))

try:
    import langgraph
    print("   OK langgraph: " + langgraph.__version__)
except Exception as e:
    print("   ERR langgraph: " + str(e))

try:
    import aiosqlite
    print("   OK aiosqlite: " + aiosqlite.__version__)
except Exception as e:
    print("   ERR aiosqlite: " + str(e))

try:
    import jinja2
    print("   OK jinja2: " + jinja2.__version__)
except Exception as e:
    print("   ERR jinja2: " + str(e))

# 测试应用导入
print("\n6. Testing App Import...")
try:
    from app.main import app
    print("   OK App imported successfully")
    print("   App title: " + app.title)
except Exception as e:
    print("   ERR Failed to import app: " + str(e))
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)