"""数据库管理模块"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.models.database import Student
from backend.utils.config import settings
from backend.utils.logger import logger
import re


class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self):
        """初始化数据库管理器"""
        pass
    
    def is_write_operation(self, sql: str) -> bool:
        """
        判断是否为写操作（INSERT/UPDATE/DELETE）
        
        Args:
            sql: SQL语句
            
        Returns:
            True表示是写操作
        """
        sql_upper = sql.strip().upper()
        return any(sql_upper.startswith(op) for op in ["INSERT", "UPDATE", "DELETE"])
    
    def validate_sql(self, sql: str) -> bool:
        """
        验证SQL语句的安全性
        
        Args:
            sql: SQL语句
            
        Returns:
            True表示SQL安全
        """
        sql_upper = sql.upper()
        
        # 检查危险关键字
        dangerous_keywords = ["DROP", "TRUNCATE", "ALTER", "CREATE", "GRANT", "REVOKE"]
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                logger.warning(f"检测到危险关键字: {keyword}")
                return False
        
        # 检查是否只包含允许的操作
        allowed_operations = ["SELECT", "INSERT", "UPDATE", "DELETE"]
        if not any(sql_upper.startswith(op) for op in allowed_operations):
            logger.warning(f"不允许的SQL操作: {sql[:20]}...")
            return False
        
        return True
    
    def execute_query(
        self,
        db: Session,
        sql: str,
        admin_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行SQL查询
        
        Args:
            db: 数据库会话
            sql: SQL语句
            admin_token: 管理员令牌（写操作需要）
            
        Returns:
            执行结果
        """
        # 验证SQL安全性
        if not self.validate_sql(sql):
            return {
                "success": False,
                "message": "SQL语句包含不安全的操作",
                "sql": sql
            }
        
        # 判断操作类型
        is_write = self.is_write_operation(sql)
        
        # 写操作需要验证管理员令牌
        if is_write:
            if admin_token != settings.admin_token:
                return {
                    "success": False,
                    "message": "写操作需要管理员权限",
                    "sql": sql
                }
        
        try:
            # 执行SQL
            result = db.execute(text(sql))
            
            if sql.strip().upper().startswith("SELECT"):
                # 查询操作
                rows = result.fetchall()
                columns = list(result.keys())
                
                # 转换为字典列表
                data = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        # 处理datetime类型
                        if hasattr(value, "isoformat"):
                            value = value.isoformat()
                        row_dict[col] = value
                    data.append(row_dict)
                
                # 限制返回行数
                if len(data) > settings.max_query_rows:
                    logger.warning(f"查询结果超过最大行数限制: {len(data)}")
                    data = data[:settings.max_query_rows]
                
                operation = "SELECT"
                db.commit()
                
                return {
                    "success": True,
                    "sql": sql,
                    "result": data,
                    "affected_rows": len(data),
                    "message": f"查询成功，共 {len(data)} 条记录",
                    "operation": operation
                }
            
            else:
                # 写操作
                affected_rows = result.rowcount
                
                # 限制影响行数
                if affected_rows > settings.max_affected_rows:
                    db.rollback()
                    return {
                        "success": False,
                        "message": f"影响行数超过限制 ({settings.max_affected_rows})，操作已回滚",
                        "sql": sql
                    }
                
                db.commit()
                
                if sql.strip().upper().startswith("INSERT"):
                    operation = "INSERT"
                    message = f"成功插入 {affected_rows} 条记录"
                elif sql.strip().upper().startswith("UPDATE"):
                    operation = "UPDATE"
                    message = f"成功更新 {affected_rows} 条记录"
                else:
                    operation = "DELETE"
                    message = f"成功删除 {affected_rows} 条记录"
                
                return {
                    "success": True,
                    "sql": sql,
                    "result": None,
                    "affected_rows": affected_rows,
                    "message": message,
                    "operation": operation
                }
                
        except Exception as e:
            db.rollback()
            logger.error(f"SQL执行失败: {e}\nSQL: {sql}")
            return {
                "success": False,
                "message": f"SQL执行失败: {str(e)}",
                "sql": sql
            }
    
    def create_student(self, db: Session, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建学生信息
        
        Args:
            db: 数据库会话
            student_data: 学生数据
            
        Returns:
            创建结果
        """
        try:
            # 检查学号是否已存在
            existing = db.query(Student).filter(
                Student.student_id == student_data["student_id"]
            ).first()
            
            if existing:
                return {
                    "success": False,
                    "message": f"学号 {student_data['student_id']} 已存在"
                }
            
            # 创建新学生
            student = Student(**student_data)
            db.add(student)
            db.commit()
            db.refresh(student)
            
            return {
                "success": True,
                "message": "学生信息创建成功",
                "data": student.to_dict()
            }
        except Exception as e:
            db.rollback()
            logger.error(f"创建学生失败: {e}")
            return {
                "success": False,
                "message": f"创建学生失败: {str(e)}"
            }
    
    def get_students(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        获取学生列表
        
        Args:
            db: 数据库会话
            skip: 跳过记录数
            limit: 返回记录数
            filters: 过滤条件
            
        Returns:
            学生列表
        """
        try:
            query = db.query(Student)
            
            # 应用过滤条件
            if filters:
                for key, value in filters.items():
                    if hasattr(Student, key):
                        query = query.filter(getattr(Student, key) == value)
            
            students = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "data": [student.to_dict() for student in students],
                "total": len(students)
            }
        except Exception as e:
            logger.error(f"获取学生列表失败: {e}")
            return {
                "success": False,
                "message": f"获取学生列表失败: {str(e)}"
            }
    
    def update_student(
        self,
        db: Session,
        student_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新学生信息
        
        Args:
            db: 数据库会话
            student_id: 学号
            update_data: 更新数据
            
        Returns:
            更新结果
        """
        try:
            student = db.query(Student).filter(
                Student.student_id == student_id
            ).first()
            
            if not student:
                return {
                    "success": False,
                    "message": f"学号 {student_id} 不存在"
                }
            
            # 更新字段
            for key, value in update_data.items():
                if hasattr(student, key) and value is not None:
                    setattr(student, key, value)
            
            db.commit()
            db.refresh(student)
            
            return {
                "success": True,
                "message": "学生信息更新成功",
                "data": student.to_dict()
            }
        except Exception as e:
            db.rollback()
            logger.error(f"更新学生失败: {e}")
            return {
                "success": False,
                "message": f"更新学生失败: {str(e)}"
            }
    
    def delete_student(
        self,
        db: Session,
        student_id: str
    ) -> Dict[str, Any]:
        """
        删除学生信息
        
        Args:
            db: 数据库会话
            student_id: 学号
            
        Returns:
            删除结果
        """
        try:
            student = db.query(Student).filter(
                Student.student_id == student_id
            ).first()
            
            if not student:
                return {
                    "success": False,
                    "message": f"学号 {student_id} 不存在"
                }
            
            db.delete(student)
            db.commit()
            
            return {
                "success": True,
                "message": "学生信息删除成功"
            }
        except Exception as e:
            db.rollback()
            logger.error(f"删除学生失败: {e}")
            return {
                "success": False,
                "message": f"删除学生失败: {str(e)}"
            }


# 创建全局数据库管理器实例
database_manager = DatabaseManager()
