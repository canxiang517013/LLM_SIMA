"""数据库模型定义"""
from sqlalchemy import create_engine, Column, BigInteger, String, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.utils.config import settings
from backend.utils.logger import logger

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
    echo=settings.enable_sql_log,
    pool_pre_ping=True  # 连接健康检查
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


class Student(Base):
    """学生信息表模型"""
    __tablename__ = "students"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(50), nullable=False, comment="学生姓名")
    student_id = Column(String(20), nullable=False, unique=True, comment="学号（唯一）")
    class_name = Column(String(50), nullable=False, comment="班级")
    college = Column(String(100), nullable=False, comment="学院")
    major = Column(String(100), nullable=False, comment="专业")
    grade = Column(String(10), nullable=False, comment="年级")
    gender = Column(Enum("男", "女"), nullable=False, comment="性别")
    phone = Column(String(20), comment="手机号")
    created_at = Column(TIMESTAMP, comment="创建时间")
    updated_at = Column(TIMESTAMP, comment="更新时间")
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "student_id": self.student_id,
            "class_name": self.class_name,
            "college": self.college,
            "major": self.major,
            "grade": self.grade,
            "gender": self.gender,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """初始化数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表初始化成功")
    except Exception as e:
        logger.error(f"数据库表初始化失败: {e}")
        raise
