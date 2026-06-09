import sys
import os

os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
