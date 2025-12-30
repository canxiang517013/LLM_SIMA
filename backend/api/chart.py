"""图表生成API路由"""
from fastapi import APIRouter
from typing import List, Dict, Any
from backend.models.schemas import ChartGenerateRequest, ChartGenerateResponse
from backend.core.chart_generator import chart_generator
from backend.utils.logger import logger


router = APIRouter(prefix="/api/chart", tags=["图表生成"])


@router.post("/generate", response_model=ChartGenerateResponse)
async def generate_chart(request: ChartGenerateRequest):
    """
    生成图表
    
    根据查询结果和描述，自动判断图表类型并生成
    """
    try:
        result = chart_generator.generate(
            request.query_result,
            request.query_description
        )
        
        return ChartGenerateResponse(
            success=result["success"],
            chart_type=result.get("chart_type", "none"),
            chart_data=result.get("chart_data"),
            message=result["message"]
        )
    
    except Exception as e:
        logger.error(f"图表生成失败: {e}")
        return ChartGenerateResponse(
            success=False,
            chart_type="none",
            message=f"图表生成失败: {str(e)}"
        )
