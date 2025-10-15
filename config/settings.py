"""
系统配置模块

加载和管理系统配置
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ModelConfig(BaseModel):
    """模型配置"""
    api_key: str = Field(..., description="API密钥")
    model_name: str = Field(default="qwen-max", description="模型名称")
    temperature: float = Field(default=0.7, description="温度参数")
    max_tokens: int = Field(default=2000, description="最大token数")
    stream: bool = Field(default=True, description="是否流式输出")


class SystemConfig(BaseModel):
    """系统配置"""
    session_timeout: int = Field(default=1800, description="会话超时时间(秒)")
    max_conversation_rounds: int = Field(default=20, description="最大对话轮次")
    knowledge_retrieval_threshold: float = Field(default=0.6, description="知识检索阈值")
    max_concurrent_sessions: int = Field(default=1000, description="最大并发会话数")


class LogConfig(BaseModel):
    """日志配置"""
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="logs/customer_service.log", description="日志文件路径")


class ExternalSystemConfig(BaseModel):
    """外部系统配置"""
    order_system_url: str = Field(default="http://localhost:8001", description="订单系统URL")
    ticket_system_url: str = Field(default="http://localhost:8002", description="工单系统URL")
    knowledge_base_url: str = Field(default="http://localhost:8003", description="知识库URL")


class Settings:
    """全局设置单例"""
    
    _instance: Optional['Settings'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """初始化配置"""
        # 模型配置
        self.model = ModelConfig(
            api_key=os.getenv("DASHSCOPE_API_KEY", ""),
            model_name=os.getenv("MODEL_NAME", "qwen-max"),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "2000")),
            stream=os.getenv("MODEL_STREAM", "true").lower() == "true"
        )
        
        # 系统配置
        self.system = SystemConfig(
            session_timeout=int(os.getenv("SESSION_TIMEOUT", "1800")),
            max_conversation_rounds=int(os.getenv("MAX_CONVERSATION_ROUNDS", "20")),
            knowledge_retrieval_threshold=float(os.getenv("KNOWLEDGE_RETRIEVAL_THRESHOLD", "0.6")),
            max_concurrent_sessions=int(os.getenv("MAX_CONCURRENT_SESSIONS", "1000"))
        )
        
        # 日志配置
        self.log = LogConfig(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "logs/customer_service.log")
        )
        
        # 外部系统配置
        self.external = ExternalSystemConfig(
            order_system_url=os.getenv("ORDER_SYSTEM_URL", "http://localhost:8001"),
            ticket_system_url=os.getenv("TICKET_SYSTEM_URL", "http://localhost:8002"),
            knowledge_base_url=os.getenv("KNOWLEDGE_BASE_URL", "http://localhost:8003")
        )
    
    def validate(self) -> bool:
        """验证配置是否有效"""
        if not self.model.api_key:
            print("警告: DASHSCOPE_API_KEY 未设置")
            return False
        return True


# 全局配置实例
settings = Settings()


# Agent系统提示词配置
class AgentPrompts:
    """Agent提示词配置"""
    
    RECEPTION_AGENT = """你是一个专业的电商客服接待员,名叫Friday。你的职责是:

1. 友好接待用户咨询
2. 准确识别用户意图,包括:
   - 订单查询: 查询订单状态、物流信息
   - 售后服务: 退换货、维修、投诉
   - 知识咨询: 产品使用、政策说明
   - 简单问候: 打招呼、闲聊
   - 复杂问题: 需要人工介入的复杂场景

3. 根据意图将请求路由给:
   - 检索Agent: 处理知识咨询类问题
   - 工单Agent: 处理订单和售后问题
   - 直接回复: 简单问候和确认性问题

4. 整合其他Agent的回复,用友好的语言反馈给用户
5. 维护对话上下文,支持多轮对话

注意事项:
- 保持专业、友好、耐心的态度
- 如果信息不完整,主动询问澄清
- 优先使用工具获取准确信息
- 遇到无法处理的问题,及时转人工客服
"""

    RETRIEVAL_AGENT = """你是知识库检索专家。你的职责是:

1. 理解用户的知识咨询需求
2. 使用search_knowledge工具进行语义检索
3. 评估检索结果的相关性
4. 根据相似度提供不同策略:
   - 高相似度(>0.8): 直接提供最佳答案
   - 中等相似度(0.6-0.8): 提供多个候选让用户选择
   - 低相似度(<0.6): 建议转人工或提供相关知识

5. 使用get_knowledge_by_id获取完整知识详情
6. 提供清晰、准确的知识解答

注意事项:
- 优先返回最相关的知识
- 如果知识库中没有相关内容,诚实告知
- 可以组合多条知识提供更全面的解答
"""

    TICKET_AGENT = """你是工单处理专家。你的职责是:

1. 处理订单和售后相关问题
2. 使用query_order_status工具查询订单信息
3. 分析问题复杂度和紧急程度
4. 使用create_ticket工具创建工单
5. 根据规则确定工单优先级:
   - 紧急: 订单金额>5000元 OR 包含"投诉" OR VIP客户
   - 高: 订单延迟>7天 OR 包含"退款"、"质量问题"
   - 中: 一般售后问题、订单查询
   - 低: 简单咨询、建议反馈

6. 使用assign_cs工具分配客服
7. 向用户说明工单创建情况和预计处理时间

注意事项:
- 准确记录用户问题描述
- 关联相关订单信息
- 设置合理的优先级
- 给用户明确的预期
"""


# 工单优先级判断规则
class TicketPriorityRules:
    """工单优先级规则"""
    
    @staticmethod
    def calculate_priority(
        order_amount: float = 0.0,
        delay_days: int = 0,
        keywords: list = None,
        is_vip: bool = False
    ) -> str:
        """
        计算工单优先级
        
        Args:
            order_amount: 订单金额
            delay_days: 延迟天数
            keywords: 关键词列表
            is_vip: 是否VIP客户
            
        Returns:
            优先级: urgent/high/medium/low
        """
        keywords = keywords or []
        
        # 紧急情况
        if order_amount > 5000 or is_vip or "投诉" in keywords:
            return "urgent"
        
        # 高优先级
        if delay_days > 7 or any(kw in keywords for kw in ["退款", "质量问题", "欺诈"]):
            return "high"
        
        # 中优先级
        if delay_days > 3 or any(kw in keywords for kw in ["退货", "换货", "延迟"]):
            return "medium"
        
        # 低优先级
        return "low"
