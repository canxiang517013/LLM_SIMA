"""Pydantic数据模型定义"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str = Field(..., description="用户消息")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None, 
        description="对话历史"
    )
    admin_token: Optional[str] = Field(default=None, description="管理员令牌")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="AI回复消息")
    data: Optional[Dict[str, Any]] = Field(default=None, description="附加数据（表格、图表等）")
    data_type: Optional[str] = Field(default=None, description="数据类型：text/table/chart")


class StudentCreate(BaseModel):
    """创建学生信息模型"""
    name: str = Field(..., min_length=1, max_length=50, description="学生姓名")
    student_id: str = Field(..., min_length=1, max_length=20, description="学号")
    class_name: str = Field(..., min_length=1, max_length=50, description="班级")
    college: str = Field(..., min_length=1, max_length=100, description="学院")
    major: str = Field(..., min_length=1, max_length=100, description="专业")
    grade: str = Field(..., min_length=1, max_length=10, description="年级")
    gender: str = Field(..., pattern="^(男|女)$", description="性别")
    phone: Optional[str] = Field(default=None, max_length=20, description="手机号")


class StudentUpdate(BaseModel):
    """更新学生信息模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="学生姓名")
    student_id: Optional[str] = Field(None, min_length=1, max_length=20, description="学号")
    class_name: Optional[str] = Field(None, min_length=1, max_length=50, description="班级")
    college: Optional[str] = Field(None, min_length=1, max_length=100, description="学院")
    major: Optional[str] = Field(None, min_length=1, max_length=100, description="专业")
    grade: Optional[str] = Field(None, min_length=1, max_length=10, description="年级")
    gender: Optional[str] = Field(None, pattern="^(男|女)$", description="性别")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class StudentResponse(BaseModel):
    """学生信息响应模型"""
    id: int
    name: str
    student_id: str
    class_name: str
    college: str
    major: str
    grade: str
    gender: str
    phone: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class SQLQueryRequest(BaseModel):
    """SQL查询请求模型"""
    natural_language: str = Field(..., description="自然语言查询")
    admin_token: Optional[str] = Field(default=None, description="管理员令牌")


class SQLQueryResponse(BaseModel):
    """SQL查询响应模型"""
    success: bool
    sql: Optional[str] = None
    result: Optional[List[Dict[str, Any]]] = None
    affected_rows: Optional[int] = None
    message: str
    operation: Optional[str] = None  # SELECT/INSERT/UPDATE/DELETE


class ChartGenerateRequest(BaseModel):
    """图表生成请求模型"""
    query_result: List[Dict[str, Any]] = Field(..., description="查询结果数据")
    query_description: str = Field(..., description="查询描述")


class ChartGenerateResponse(BaseModel):
    """图表生成响应模型"""
    success: bool
    chart_type: str = Field(..., description="图表类型")
    chart_data: Optional[str] = Field(None, description="图表base64数据")
    message: str


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    message: str = Field(..., description="错误信息")
    error_type: Optional[str] = Field(None, description="错误类型")
