"""
消息数据模型

定义系统中使用的各类消息结构
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ChannelType(str, Enum):
    """渠道类型"""
    WEB = "web"
    APP = "app"
    MINIAPP = "miniapp"
    WECHAT = "wechat"


class MessageRole(str, Enum):
    """消息角色"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class IntentType(str, Enum):
    """意图类型"""
    ORDER_QUERY = "order_query"  # 订单查询
    AFTER_SALE = "after_sale"  # 售后服务
    KNOWLEDGE = "knowledge"  # 知识咨询
    GREETING = "greeting"  # 简单问候
    COMPLEX = "complex"  # 复杂问题
    UNKNOWN = "unknown"  # 未知意图


class ConversationState(str, Enum):
    """对话状态"""
    IDLE = "idle"  # 空闲
    PROCESSING = "processing"  # 处理中
    WAITING_AGENT = "waiting_agent"  # 等待Agent响应
    RESPONDING = "responding"  # 响应中
    CLARIFYING = "clarifying"  # 澄清中
    COMPLETED = "completed"  # 已完成


class UserMessage(BaseModel):
    """用户消息模型"""
    user_id: str = Field(..., description="用户ID")
    session_id: str = Field(..., description="会话ID")
    message: str = Field(..., description="消息内容")
    timestamp: datetime = Field(default_factory=datetime.now, description="发送时间")
    channel: ChannelType = Field(default=ChannelType.WEB, description="渠道类型")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "session_id": "session_67890",
                "message": "我的订单什么时候发货？",
                "channel": "web",
                "metadata": {
                    "ip": "192.168.1.1",
                    "user_agent": "Mozilla/5.0"
                }
            }
        }


class AgentResponse(BaseModel):
    """Agent响应模型"""
    session_id: str = Field(..., description="会话ID")
    response: str = Field(..., description="响应内容")
    status: str = Field(default="success", description="处理状态")
    intent: Optional[IntentType] = Field(None, description="识别的意图")
    suggestions: List[str] = Field(default_factory=list, description="建议操作")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="响应时间")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_67890",
                "response": "您的订单预计明天发货",
                "status": "success",
                "intent": "order_query",
                "suggestions": ["查看物流", "联系客服"]
            }
        }


class ConversationContext(BaseModel):
    """对话上下文模型"""
    session_id: str = Field(..., description="会话ID")
    user_id: str = Field(..., description="用户ID")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="消息历史")
    entities: Dict[str, Any] = Field(default_factory=dict, description="提取的实体")
    intent_sequence: List[IntentType] = Field(default_factory=list, description="意图序列")
    state: ConversationState = Field(default=ConversationState.IDLE, description="对话状态")
    temp_data: Dict[str, Any] = Field(default_factory=dict, description="临时数据")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

    def add_message(self, role: MessageRole, content: str, metadata: Optional[Dict] = None):
        """添加消息到历史"""
        message = {
            "role": role.value,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        self.updated_at = datetime.now()

    def add_entity(self, key: str, value: Any):
        """添加实体"""
        self.entities[key] = value
        self.updated_at = datetime.now()

    def add_intent(self, intent: IntentType):
        """添加意图"""
        self.intent_sequence.append(intent)
        self.updated_at = datetime.now()

    def update_state(self, state: ConversationState):
        """更新对话状态"""
        self.state = state
        self.updated_at = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_67890",
                "user_id": "user_12345",
                "state": "processing",
                "entities": {
                    "order_id": "ORD123456"
                },
                "intent_sequence": ["order_query"]
            }
        }
