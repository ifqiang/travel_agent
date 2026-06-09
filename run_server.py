import subprocess
import os
import sys

# 设置环境变量
os.chdir('d:\\大数据专业综合课程设计\\travel_agent')
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'

print("=== Starting Server ===")
print("Python:", sys.executable)
print("Working Directory:", os.getcwd())

# 启动服务器
process = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    cwd='d:\\大数据专业综合课程设计\\travel_agent'
)

print("Server starting...")
print("PID:", process.pid)

# 实时输出
for line in iter(process.stdout.readline, ''):
    if line:
        print(line.rstrip())
