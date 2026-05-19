"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # API 配置
    API_BASE_URL: str = "https://ai-api-prod.qingjiao.art/v1"
    API_KEY: str = "1XajEZXRr9YzCW0C2cB5A1B11d03441a8fA32f30F96d5459"
    MODEL_NAME: str = "deepseek-v3"
    
    # 应用配置
    APP_NAME: str = "AI 旅行助手"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./travel_assistant.db"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings()