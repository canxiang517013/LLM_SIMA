"""Text2SQL转换模块"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.core.llm_client import llm_client
from backend.core.database_manager import database_manager
from backend.utils.logger import logger


class Text2SQL:
    """Text2SQL转换类"""
    
    def __init__(self):
        """初始化Text2SQL转换器"""
        self.database_schema = """
表名: students
字段:
- id (BIGINT, 主键)
- name (VARCHAR(50)): 学生姓名
- student_id (VARCHAR(20)): 学号，唯一
- class_name (VARCHAR(50)): 班级
- college (VARCHAR(100)): 学院
- major (VARCHAR(100)): 专业
- grade (VARCHAR(10)): 年级
- gender (ENUM('男', '女')): 性别
- phone (VARCHAR(20)): 手机号
- created_at (TIMESTAMP): 创建时间
- updated_at (TIMESTAMP): 更新时间
"""
        
        # Few-shot examples
        self.examples = [
            {
                "question": "查询所有学生的信息",
                "sql": "SELECT * FROM students"
            },
            {
                "question": "查询计算机学院的所有学生",
                "sql": "SELECT * FROM students WHERE college = '计算机学院'"
            },
            {
                "question": "统计每个年级的学生人数",
                "sql": "SELECT grade, COUNT(*) as count FROM students GROUP BY grade"
            },
            {
                "question": "查询男女生的人数",
                "sql": "SELECT gender, COUNT(*) as count FROM students GROUP BY gender"
            },
            {
                "question": "添加学生：张三，学号2025001，计算机1班，计算机学院，计算机科学与技术专业，2025级，男，手机13800138001",
                "sql": "INSERT INTO students (name, student_id, class_name, college, major, grade, gender, phone) VALUES ('张三', '2025001', '计算机1班', '计算机学院', '计算机科学与技术', '2025级', '男', '13800138001')"
            },
            {
                "question": "更新学号2024001的学生的手机号为13900139001",
                "sql": "UPDATE students SET phone = '13900139001' WHERE student_id = '2024001'"
            },
            {
                "question": "删除学号2024001的学生",
                "sql": "DELETE FROM students WHERE student_id = '2024001'"
            }
        ]
    
    def convert(
        self,
        natural_language: str,
        db: Session,
        admin_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        将自然语言转换为SQL并执行
        
        Args:
            natural_language: 自然语言查询
            db: 数据库会话
            admin_token: 管理员令牌
            
        Returns:
            执行结果
        """
        try:
            # 判断是否是数据库查询请求
            if not self._is_database_query(natural_language):
                return {
                    "success": False,
                    "message": "这不是一个数据库查询请求"
                }
            
            # 转换为SQL
            sql = llm_client.text2sql(
                natural_language,
                self.database_schema,
                self.examples
            )
            
            logger.info(f"生成的SQL: {sql}")
            
            # 执行SQL
            result = database_manager.execute_query(
                db,
                sql,
                admin_token
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Text2SQL转换失败: {e}")
            return {
                "success": False,
                "message": f"Text2SQL转换失败: {str(e)}"
            }
    
    def _is_database_query(self, text: str) -> bool:
        """
        判断是否是数据库查询请求
        
        Args:
            text: 用户输入文本
            
        Returns:
            True表示是数据库查询
        """
        # 数据库查询相关的关键词
        db_keywords = [
            "查询", "统计", "搜索", "查找", "列出",
            "添加", "插入", "新增", "创建",
            "更新", "修改", "改变", "编辑",
            "删除", "移除", "去掉",
            "学生", "学号", "学院", "专业", "班级", "年级",
            "多少", "几个", "数量", "人数"
        ]
        
        for keyword in db_keywords:
            if keyword in text:
                return True
        
        return False


# 创建全局Text2SQL实例
text2sql = Text2SQL()
