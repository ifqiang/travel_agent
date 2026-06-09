FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app ./app

# 复制数据库文件（如果存在）
COPY travel_assistant.db .

# 暴露端口（与配置文件一致）
EXPOSE 8000

# 使用uvicorn启动（生产环境禁用reload）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
