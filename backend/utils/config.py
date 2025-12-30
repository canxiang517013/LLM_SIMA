"""配置管理模块"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """应用配置类"""
    
    # ==================== DeepSeek API配置 ====================
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # LLM参数
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    llm_timeout: int = int(os.getenv("LLM_TIMEOUT", "30"))
    llm_max_retries: int = int(os.getenv("LLM_MAX_RETRIES", "3"))
    llm_retry_delay: int = int(os.getenv("LLM_RETRY_DELAY", "1"))
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # ==================== 数据库配置 ====================
    db_type: str = os.getenv("DB_TYPE", "mysql")
    mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "")
    mysql_database: str = os.getenv("MYSQL_DATABASE", "student_db")
    
    # 连接池配置
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    db_pool_recycle: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    enable_sql_log: bool = os.getenv("ENABLE_SQL_LOG", "false").lower() == "true"
    
    # ==================== 安全配置 ====================
    admin_token: str = os.getenv("ADMIN_TOKEN", "student_project_2024")
    max_affected_rows: int = int(os.getenv("MAX_AFFECTED_ROWS", "100"))
    max_query_rows: int = int(os.getenv("MAX_QUERY_ROWS", "1000"))
    
    # ==================== 应用配置 ====================
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    
    # ==================== 前端配置 ====================
    backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # ==================== 图表配置 ====================
    chart_width: int = int(os.getenv("CHART_WIDTH", "800"))
    chart_height: int = int(os.getenv("CHART_HEIGHT", "600"))
    chart_dpi: int = int(os.getenv("CHART_DPI", "100"))
    
    # ==================== 缓存配置 ====================
    use_redis: bool = os.getenv("USE_REDIS", "false").lower() == "true"
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_database: int = int(os.getenv("REDIS_DATABASE", "0"))
    cache_ttl: int = int(os.getenv("CACHE_TTL", "300"))
    
    @property
    def database_url(self) -> str:
        """获取数据库连接URL"""
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset=utf8mb4"
        )
    
    @property
    def cors_origins_list(self) -> list:
        """获取CORS允许的源列表"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 创建全局配置实例
settings = Settings()
