"""数据库管理API路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.database import get_db, Student
from backend.models.schemas import (
    StudentCreate, StudentUpdate, StudentResponse,
    SQLQueryRequest, SQLQueryResponse
)
from backend.core.database_manager import database_manager
from backend.utils.logger import logger


router = APIRouter(prefix="/api/database", tags=["数据库管理"])


@router.post("/students", response_model=dict)
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """
    创建学生信息
    
    需要验证：学号唯一
    """
    result = database_manager.create_student(db, student.dict())
    return result


@router.get("/students", response_model=dict)
async def get_students(
    skip: int = 0,
    limit: int = 100,
    college: Optional[str] = None,
    grade: Optional[str] = None,
    class_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取学生列表
    
    支持按学院、年级、班级过滤
    """
    filters = {}
    if college:
        filters["college"] = college
    if grade:
        filters["grade"] = grade
    if class_name:
        filters["class_name"] = class_name
    
    result = database_manager.get_students(db, skip, limit, filters)
    return result


@router.get("/students/{student_id}", response_model=dict)
async def get_student_by_id(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    根据学号获取学生信息
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        return {
            "success": False,
            "message": f"学号 {student_id} 不存在"
        }
    return {
        "success": True,
        "data": student.to_dict()
    }


@router.put("/students/{student_id}", response_model=dict)
async def update_student(
    student_id: str,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    更新学生信息
    
    需要提供学号
    """
    # 只包含非None的字段
    update_data = {k: v for k, v in student_update.dict().items() if v is not None}
    result = database_manager.update_student(db, student_id, update_data)
    return result


@router.delete("/students/{student_id}", response_model=dict)
async def delete_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    删除学生信息
    
    需要提供学号
    """
    result = database_manager.delete_student(db, student_id)
    return result


@router.post("/query", response_model=SQLQueryResponse)
async def execute_sql_query(
    request: SQLQueryRequest,
    db: Session = Depends(get_db)
):
    """
    执行SQL查询（通过text2sql）
    
    需要提供自然语言查询
    写操作需要管理员令牌
    """
    from backend.core.text2sql import text2sql
    
    result = text2sql.convert(
        request.natural_language,
        db,
        request.admin_token
    )
    
    return SQLQueryResponse(
        success=result.get("success", False),
        sql=result.get("sql"),
        result=result.get("result"),
        affected_rows=result.get("affected_rows"),
        message=result.get("message", ""),
        operation=result.get("operation")
    )
