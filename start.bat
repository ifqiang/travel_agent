@echo off
cd /d "d:\大数据专业综合课程设计\travel_agent"
set PYTHONPATH=d:\大数据专业综合课程设计\travel_agent
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info
pause