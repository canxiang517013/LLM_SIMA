"""图表生成模块"""
from typing import List, Dict, Any, Optional
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import pandas as pd
import base64
import io
from pathlib import Path
from backend.core.llm_client import llm_client
from backend.utils.config import settings
from backend.utils.logger import logger


class ChartGenerator:
    """图表生成器类"""
    
    def __init__(self):
        """初始化图表生成器"""
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图表保存目录
        self.chart_dir = Path("charts")
        self.chart_dir.mkdir(exist_ok=True)
    
    def generate(
        self,
        query_result: List[Dict[str, Any]],
        query_description: str
    ) -> Dict[str, Any]:
        """
        生成图表
        
        Args:
            query_result: 查询结果数据
            query_description: 查询描述
            
        Returns:
            图表生成结果
        """
        if not query_result:
            return {
                "success": False,
                "chart_type": "none",
                "message": "没有数据可以生成图表"
            }
        
        try:
            # 使用LLM判断图表类型
            chart_config = llm_client.determine_chart_type(
                query_result,
                query_description
            )
            
            logger.info(f"图表配置: {chart_config}")
            
            chart_type = chart_config.get("chart_type", "none")
            
            if chart_type == "none":
                return {
                    "success": False,
                    "chart_type": "none",
                    "message": chart_config.get("reason", "不需要生成图表")
                }
            
            # 生成图表
            chart_base64 = self._create_chart(
                chart_type,
                query_result,
                chart_config
            )
            
            return {
                "success": True,
                "chart_type": chart_type,
                "chart_data": chart_base64,
                "message": f"成功生成{chart_type}图表",
                "config": chart_config
            }
            
        except Exception as e:
            logger.error(f"图表生成失败: {e}")
            return {
                "success": False,
                "chart_type": "none",
                "message": f"图表生成失败: {str(e)}"
            }
    
    def _create_chart(
        self,
        chart_type: str,
        data: List[Dict[str, Any]],
        config: Dict[str, str]
    ) -> str:
        """
        创建图表并返回base64编码
        
        Args:
            chart_type: 图表类型
            data: 数据
            config: 图表配置
            
        Returns:
            base64编码的图表
        """
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 创建图表
        fig, ax = plt.subplots(
            figsize=(settings.chart_width / 100, settings.chart_height / 100),
            dpi=settings.chart_dpi
        )
        
        # 获取列名
        columns = list(df.columns)
        x_col = config.get("x_column", columns[0] if columns else "")
        y_col = config.get("y_column", columns[1] if len(columns) > 1 else "")
        title = config.get("title", "查询结果")
        
        if chart_type == "bar":
            # 柱状图
            if x_col in df.columns and y_col in df.columns:
                ax.bar(df[x_col], df[y_col], color='steelblue', alpha=0.8)
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
            else:
                # 如果指定的列不存在，使用前两列
                if len(columns) >= 2:
                    ax.bar(df[columns[0]], df[columns[1]], color='steelblue', alpha=0.8)
                    ax.set_xlabel(columns[0])
                    ax.set_ylabel(columns[1])
        
        elif chart_type == "pie":
            # 饼图
            if len(columns) >= 2:
                labels = df[columns[0]]
                values = df[columns[1]]
                ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
            else:
                ax.text(0.5, 0.5, '数据不足', ha='center', va='center', transform=ax.transAxes)
        
        elif chart_type == "line":
            # 折线图
            if x_col in df.columns and y_col in df.columns:
                ax.plot(df[x_col], df[y_col], marker='o', linewidth=2, markersize=8)
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
            else:
                # 如果指定的列不存在，使用前两列
                if len(columns) >= 2:
                    ax.plot(df[columns[0]], df[columns[1]], marker='o', linewidth=2, markersize=8)
                    ax.set_xlabel(columns[0])
                    ax.set_ylabel(columns[1])
        
        else:
            ax.text(0.5, 0.5, f'不支持的图表类型: {chart_type}', 
                   ha='center', va='center', transform=ax.transAxes)
        
        # 设置标题
        ax.set_title(title, fontsize=14, pad=20)
        
        # 调整布局
        plt.tight_layout()
        
        # 转换为base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=settings.chart_dpi)
        plt.close()
        buf.seek(0)
        
        chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        return chart_base64
    
    def should_generate_chart(
        self,
        query_result: List[Dict[str, Any]],
        query_description: str
    ) -> bool:
        """
        判断是否应该生成图表
        
        Args:
            query_result: 查询结果
            query_description: 查询描述
            
        Returns:
            True表示应该生成图表
        """
        # 没有数据不生成图表
        if not query_result:
            return False
        
        # 只有一条记录通常不生成图表
        if len(query_result) <= 1:
            return False
        
        # 检查查询描述中是否包含统计相关关键词
        chart_keywords = ["统计", "数量", "人数", "分布", "比例", "占比", "趋势"]
        for keyword in chart_keywords:
            if keyword in query_description:
                return True
        
        return False


# 创建全局图表生成器实例
chart_generator = ChartGenerator()
