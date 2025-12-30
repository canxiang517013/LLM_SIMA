"""日志配置模块"""
import logging
import sys
from pathlib import Path
from backend.utils.config import settings


def setup_logger(name: str = "student_assistant") -> logging.Logger:
    """配置日志记录器"""
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level))
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level))
    
    # 文件handler
    file_handler = logging.FileHandler(
        log_dir / "app.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# 创建全局logger实例
logger = setup_logger()
