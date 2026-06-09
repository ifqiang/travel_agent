$env:PYTHONPATH = 'd:\大数据专业综合课程设计\travel_agent'
cd d:\大数据专业综合课程设计\travel_agent
Write-Host "Starting server..."
py -3.13 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info