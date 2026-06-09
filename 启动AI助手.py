#!/usr/bin/env python
import subprocess
import sys
import os

# 切换到项目目录
os.chdir('d:\\大数据专业综合课程设计\\travel_agent')
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'

print("=== Starting AI Travel Assistant ===")
print("Working Directory:", os.getcwd())
print("Python:", sys.executable)
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))

# 启动服务器
cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']
print("\nRunning command:", ' '.join(cmd))
print("\nServer should be available at: http://localhost:8000")
print("Press Ctrl+C to stop the server\n")

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                          text=True, bufsize=1)

for line in iter(process.stdout.readline, ''):
    if line:
        print(line.rstrip())
