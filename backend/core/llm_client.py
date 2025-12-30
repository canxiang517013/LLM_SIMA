"""大语言模型客户端模块"""
from typing import List, Dict, Any, Optional
from openai import OpenAI
from backend.utils.config import settings
from backend.utils.logger import logger


class LLMClient:
    """大语言模型客户端类"""
    
    def __init__(self):
        """初始化LLM客户端"""
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            timeout=settings.llm_timeout,
            max_retries=settings.llm_max_retries
        )
        self.model = settings.deepseek_model
        
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        调用大语言模型进行对话
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否流式输出
            
        Returns:
            响应结果
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.llm_temperature,
                max_tokens=max_tokens or settings.llm_max_tokens,
                stream=stream
            )
            
            if stream:
                return {"stream": response}
            else:
                return {
                    "content": response.choices[0].message.content,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            raise
    
    def simple_chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        简单对话
        
        Args:
            user_message: 用户消息
            system_prompt: 系统提示词
            conversation_history: 对话历史
            
        Returns:
            AI回复
        """
        messages = []
        
        # 添加系统提示词
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加对话历史
        if conversation_history:
            messages.extend(conversation_history)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.chat_completion(messages)
            return response["content"]
        except Exception as e:
            logger.error(f"对话失败: {e}")
            return f"抱歉，我遇到了一些问题：{str(e)}"
    
    def text2sql(
        self,
        natural_language: str,
        database_schema: str,
        examples: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        将自然语言转换为SQL查询
        
        Args:
            natural_language: 自然语言查询
            database_schema: 数据库schema
            examples: Few-shot examples
            
        Returns:
            生成的SQL查询
        """
        system_prompt = """你是一个SQL查询生成专家。请根据用户的自然语言描述，生成准确的SQL查询语句。

数据库Schema:
students表字段:
- id: 主键
- name: 学生姓名
- student_id: 学号（唯一）
- class_name: 班级
- college: 学院
- major: 专业
- grade: 年级
- gender: 性别（'男' 或 '女'）
- phone: 手机号
- created_at: 创建时间
- updated_at: 更新时间

注意事项:
1. 只输出SQL语句，不要有任何解释或额外内容
2. 使用中文值时用单引号包裹
3. 对于INSERT/UPDATE/DELETE操作，确保 WHERE 条件准确
4. 查询时如果涉及统计，使用 COUNT, SUM, AVG 等聚合函数
5. 按照字段名准确拼写
"""
        
        examples_text = ""
        if examples:
            examples_text = "\n\n示例:\n"
            for example in examples:
                examples_text += f"Q: {example['question']}\nA: {example['sql']}\n\n"
        
        user_message = f"请将以下自然语言转换为SQL查询：\n{natural_language}\n{examples_text}"
        
        try:
            response = self.simple_chat(user_message, system_prompt)
            # 清理SQL语句
            sql = response.strip()
            # 移除可能的markdown代码块标记
            if sql.startswith("```sql"):
                sql = sql[6:]
            elif sql.startswith("```"):
                sql = sql[3:]
            if sql.endswith("```"):
                sql = sql[:-3]
            return sql.strip()
        except Exception as e:
            logger.error(f"Text2SQL转换失败: {e}")
            raise
    
    def determine_chart_type(
        self,
        query_result: List[Dict[str, Any]],
        query_description: str
    ) -> Dict[str, str]:
        """
        判断适合的图表类型
        
        Args:
            query_result: 查询结果
            query_description: 查询描述
            
        Returns:
            包含图表类型和配置的字典
        """
        if not query_result:
            return {"chart_type": "none", "reason": "没有数据"}
        
        system_prompt = """你是一个数据可视化专家。请根据查询结果和描述，判断最适合的图表类型。

可选图表类型:
- bar: 柱状图（适合比较不同类别的数值）
- pie: 饼图（适合展示占比）
- line: 折线图（适合展示趋势）
- none: 不需要图表（适合简单的列表或单条记录）

请以JSON格式返回，格式为:
{
    "chart_type": "bar/pie/line/none",
    "reason": "选择该图表的原因",
    "title": "图表标题",
    "x_column": "X轴字段名",
    "y_column": "Y轴字段名"
}

只返回JSON，不要有其他内容。"""
        
        # 分析查询结果结构
        columns = list(query_result[0].keys()) if query_result else []
        columns_info = "查询结果列: " + ", ".join(columns)
        row_count = len(query_result)
        
        user_message = f"""查询描述: {query_description}
{columns_info}
数据行数: {row_count}

请判断最适合的图表类型。"""
        
        try:
            response = self.simple_chat(user_message, system_prompt)
            # 尝试解析JSON
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回默认配置
            return {
                "chart_type": "bar",
                "reason": "默认使用柱状图",
                "title": "查询结果",
                "x_column": columns[0] if columns else "",
                "y_column": columns[1] if len(columns) > 1 else ""
            }
        except Exception as e:
            logger.error(f"图表类型判断失败: {e}")
            return {"chart_type": "none", "reason": str(e)}


# 创建全局LLM客户端实例
llm_client = LLMClient()
