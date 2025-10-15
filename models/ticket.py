"""
工单数据模型

定义工单系统相关的数据结构
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TicketType(str, Enum):
    """工单类型"""
    ORDER_ISSUE = "order_issue"  # 订单问题
    REFUND = "refund"  # 退款
    RETURN = "return"  # 退货
    EXCHANGE = "exchange"  # 换货
    COMPLAINT = "complaint"  # 投诉
    CONSULTATION = "consultation"  # 咨询
    TECHNICAL_SUPPORT = "technical_support"  # 技术支持
    OTHER = "other"  # 其他


class TicketPriority(str, Enum):
    """工单优先级"""
    URGENT = "urgent"  # 紧急
    HIGH = "high"  # 高
    MEDIUM = "medium"  # 中
    LOW = "low"  # 低


class TicketStatus(str, Enum):
    """工单状态"""
    PENDING = "pending"  # 待处理
    ASSIGNED = "assigned"  # 已分配
    IN_PROGRESS = "in_progress"  # 处理中
    WAITING_USER = "waiting_user"  # 等待用户
    RESOLVED = "resolved"  # 已解决
    CLOSED = "closed"  # 已关闭
    CANCELLED = "cancelled"  # 已取消


class CustomerServiceGroup(str, Enum):
    """客服组"""
    ORDER_TEAM = "order_team"  # 订单处理组
    AFTERSALE_TEAM = "aftersale_team"  # 售后处理组
    GENERAL_TEAM = "general_team"  # 综合处理组
    VIP_TEAM = "vip_team"  # VIP客服组


class Ticket(BaseModel):
    """工单模型"""
    ticket_id: str = Field(..., description="工单ID")
    user_id: str = Field(..., description="用户ID")
    ticket_type: TicketType = Field(..., description="工单类型")
    priority: TicketPriority = Field(default=TicketPriority.MEDIUM, description="优先级")
    title: str = Field(..., description="工单标题")
    description: str = Field(..., description="问题描述")
    related_order_id: Optional[str] = Field(None, description="关联订单ID")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list, description="对话历史")
    assigned_cs: Optional[str] = Field(None, description="分配的客服ID")
    assigned_group: Optional[CustomerServiceGroup] = Field(None, description="分配的客服组")
    status: TicketStatus = Field(default=TicketStatus.PENDING, description="工单状态")
    tags: List[str] = Field(default_factory=list, description="标签")
    attachments: List[str] = Field(default_factory=list, description="附件URL列表")
    internal_notes: List[str] = Field(default_factory=list, description="内部备注")
    resolution: Optional[str] = Field(None, description="解决方案")
    satisfaction_score: Optional[int] = Field(None, description="满意度评分(1-5)")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    resolved_at: Optional[datetime] = Field(None, description="解决时间")
    closed_at: Optional[datetime] = Field(None, description="关闭时间")

    def update_status(self, status: TicketStatus):
        """更新工单状态"""
        self.status = status
        self.updated_at = datetime.now()
        if status == TicketStatus.RESOLVED:
            self.resolved_at = datetime.now()
        elif status == TicketStatus.CLOSED:
            self.closed_at = datetime.now()

    def assign_to(self, cs_id: str, group: CustomerServiceGroup):
        """分配给客服"""
        self.assigned_cs = cs_id
        self.assigned_group = group
        self.status = TicketStatus.ASSIGNED
        self.updated_at = datetime.now()

    def add_note(self, note: str):
        """添加内部备注"""
        self.internal_notes.append(f"[{datetime.now().isoformat()}] {note}")
        self.updated_at = datetime.now()

    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": "TK20241015001",
                "user_id": "user_12345",
                "ticket_type": "order_issue",
                "priority": "high",
                "title": "订单延迟发货",
                "description": "订单ORD123456已下单7天，仍未发货",
                "related_order_id": "ORD123456",
                "status": "pending"
            }
        }


class TicketCreateRequest(BaseModel):
    """创建工单请求"""
    user_id: str = Field(..., description="用户ID")
    ticket_type: TicketType = Field(..., description="工单类型")
    title: str = Field(..., description="工单标题")
    description: str = Field(..., description="问题描述")
    related_order_id: Optional[str] = Field(None, description="关联订单ID")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list, description="对话历史")
    priority: Optional[TicketPriority] = Field(None, description="优先级")
    tags: List[str] = Field(default_factory=list, description="标签")


class TicketAssignment(BaseModel):
    """工单分配信息"""
    ticket_id: str = Field(..., description="工单ID")
    cs_id: str = Field(..., description="客服ID")
    cs_name: str = Field(..., description="客服姓名")
    group: CustomerServiceGroup = Field(..., description="客服组")
    assigned_at: datetime = Field(default_factory=datetime.now, description="分配时间")
    estimated_response_time: int = Field(..., description="预计响应时间(分钟)")


class CustomerServiceAgent(BaseModel):
    """客服人员模型"""
    cs_id: str = Field(..., description="客服ID")
    cs_name: str = Field(..., description="客服姓名")
    group: CustomerServiceGroup = Field(..., description="所属组")
    expertise: List[str] = Field(default_factory=list, description="专长领域")
    current_load: int = Field(default=0, description="当前工单数")
    max_load: int = Field(default=10, description="最大工单数")
    is_online: bool = Field(default=True, description="是否在线")
    avg_response_time: float = Field(default=0.0, description="平均响应时间(分钟)")
    satisfaction_rate: float = Field(default=0.0, description="满意度")

    def can_take_ticket(self) -> bool:
        """是否可以接受新工单"""
        return self.is_online and self.current_load < self.max_load

    class Config:
        json_schema_extra = {
            "example": {
                "cs_id": "CS001",
                "cs_name": "王小明",
                "group": "order_team",
                "expertise": ["订单查询", "物流追踪"],
                "current_load": 3,
                "max_load": 10,
                "is_online": True
            }
        }
