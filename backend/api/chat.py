"""聊天API路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.models.database import get_db
from backend.models.schemas import ChatRequest, ChatResponse
from backend.core.llm_client import llm_client
from backend.core.text2sql import text2sql
from backend.core.chart_generator import chart_generator
from backend.utils.logger import logger


router = APIRouter(prefix="/api/chat", tags=["聊天"])


# 系统提示词
SYSTEM_PROMPT = """你是一个智能学生信息管理助手。你可以帮助用户：
1. 回答关于学生信息管理的问题
2. 处理数据库查询请求（通过text2sql）
3. 生成图表展示查询结果

数据库表结构：
- students表包含学生信息：姓名、学号、班级、学院、专业、年级、性别、手机号等

当用户询问关于学生信息的查询、统计、增删改等操作时，请礼貌地回复，说明你会处理这个请求。
"""

# 会话历史存储（简化版，生产环境应使用Redis等）
conversation_history: Dict[str, List[Dict[str, str]]] = {}


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    聊天接口
    
    处理用户消息，判断是普通对话还是数据库操作请求
    """
    try:
        user_message = request.message
        admin_token = request.admin_token
        
        logger.info(f"用户消息: {user_message}")
        
        # 判断是否是数据库查询请求
        if text2sql._is_database_query(user_message):
            # 使用text2sql处理数据库查询
            db_result = text2sql.convert(user_message, db, admin_token)
            
            if db_result["success"]:
                # 查询成功
                if db_result["operation"] == "SELECT":
                    # 查询操作，检查是否需要生成图表
                    result_data = db_result["result"]
                    
                    ai_message = db_result["message"]
                    data_type = "table"
                    response_data = {"table": result_data}
                    
                    # 判断是否需要生成图表
                    if chart_generator.should_generate_chart(result_data, user_message):
                        chart_result = chart_generator.generate(result_data, user_message)
                        if chart_result["success"]:
                            # 同时保留表格数据和图表数据
                            response_data["chart"] = {
                                "type": chart_result["chart_type"],
                                "data": chart_result["chart_data"]
                            }
                            data_type = "table_and_chart"
                            ai_message += "\n\n我已为您生成图表展示结果。"
                
                else:
                    # 增删改操作
                    ai_message = db_result["message"]
                    data_type = "text"
                    response_data = {"operation": db_result["operation"]}
                
                return ChatResponse(
                    success=True,
                    message=ai_message,
                    data=response_data,
                    data_type=data_type
                )
            
            else:
                # 数据库操作失败
                return ChatResponse(
                    success=False,
                    message=db_result["message"],
                    data_type="text"
                )
        
        else:
            # 普通对话
            history = request.conversation_history or []
            ai_response = llm_client.simple_chat(
                user_message,
                SYSTEM_PROMPT,
                history
            )
            
            return ChatResponse(
                success=True,
                message=ai_response,
                data_type="text"
            )
    
    except Exception as e:
        logger.error(f"聊天处理失败: {e}")
        return ChatResponse(
            success=False,
            message=f"处理失败: {str(e)}",
            data_type="text"
        )
