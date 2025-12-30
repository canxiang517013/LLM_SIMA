"""FastAPI主程序"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.database import init_database
from backend.utils.config import settings
from backend.utils.logger import logger
from backend.api import chat, database, chart

# 创建FastAPI应用
app = FastAPI(
    title="学生信息管理助手",
    description="基于大语言模型的学生信息管理智能助手",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router)
app.include_router(database.router)
app.include_router(chart.router)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("=" * 50)
    logger.info("学生信息管理助手启动中...")
    logger.info("=" * 50)
    
    # 初始化数据库表
    init_database()
    
    logger.info(f"后端服务地址: http://localhost:8000")
    logger.info(f"API文档地址: http://localhost:8000/docs")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("学生信息管理助手已停止")
    logger.info("=" * 50)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "学生信息管理助手API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "student-management-assistant"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
