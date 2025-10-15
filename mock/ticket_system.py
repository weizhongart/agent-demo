"""
模拟工单系统

用于测试的工单系统模拟实现
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from models.ticket import (
    Ticket, TicketType, TicketPriority, TicketStatus,
    CustomerServiceGroup, CustomerServiceAgent, TicketAssignment
)
import uuid


class MockTicketSystem:
    """模拟工单系统"""
    
    def __init__(self):
        self.tickets: Dict[str, Ticket] = {}
        self.cs_agents: Dict[str, CustomerServiceAgent] = {}
        self._init_cs_agents()
    
    def _init_cs_agents(self):
        """初始化客服人员"""
        # 订单处理组
        self.cs_agents["CS001"] = CustomerServiceAgent(
            cs_id="CS001",
            cs_name="王小明",
            group=CustomerServiceGroup.ORDER_TEAM,
            expertise=["订单查询", "物流追踪"],
            current_load=2,
            max_load=10,
            is_online=True,
            avg_response_time=5.0,
            satisfaction_rate=0.92
        )
        
        self.cs_agents["CS002"] = CustomerServiceAgent(
            cs_id="CS002",
            cs_name="李华",
            group=CustomerServiceGroup.ORDER_TEAM,
            expertise=["订单处理", "发货管理"],
            current_load=5,
            max_load=10,
            is_online=True,
            avg_response_time=8.0,
            satisfaction_rate=0.88
        )
        
        # 售后处理组
        self.cs_agents["CS003"] = CustomerServiceAgent(
            cs_id="CS003",
            cs_name="张丽",
            group=CustomerServiceGroup.AFTERSALE_TEAM,
            expertise=["退换货", "质量问题处理"],
            current_load=3,
            max_load=8,
            is_online=True,
            avg_response_time=10.0,
            satisfaction_rate=0.90
        )
        
        self.cs_agents["CS004"] = CustomerServiceAgent(
            cs_id="CS004",
            cs_name="刘强",
            group=CustomerServiceGroup.AFTERSALE_TEAM,
            expertise=["投诉处理", "纠纷解决"],
            current_load=1,
            max_load=8,
            is_online=True,
            avg_response_time=15.0,
            satisfaction_rate=0.95
        )
        
        # 综合处理组
        self.cs_agents["CS005"] = CustomerServiceAgent(
            cs_id="CS005",
            cs_name="赵敏",
            group=CustomerServiceGroup.GENERAL_TEAM,
            expertise=["综合咨询", "账户问题"],
            current_load=4,
            max_load=12,
            is_online=True,
            avg_response_time=6.0,
            satisfaction_rate=0.85
        )
    
    def create_ticket(
        self,
        user_id: str,
        ticket_type: TicketType,
        title: str,
        description: str,
        priority: TicketPriority = TicketPriority.MEDIUM,
        related_order_id: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        创建工单
        
        Args:
            user_id: 用户ID
            ticket_type: 工单类型
            title: 标题
            description: 描述
            priority: 优先级
            related_order_id: 关联订单ID
            conversation_history: 对话历史
            
        Returns:
            创建结果
        """
        # 生成工单ID
        ticket_id = f"TK{datetime.now().strftime('%Y%m%d')}{len(self.tickets) + 1:04d}"
        
        # 创建工单
        ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            ticket_type=ticket_type,
            priority=priority,
            title=title,
            description=description,
            related_order_id=related_order_id,
            conversation_history=conversation_history or [],
            status=TicketStatus.PENDING
        )
        
        self.tickets[ticket_id] = ticket
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": ticket.status.value,
            "priority": ticket.priority.value,
            "created_at": ticket.created_at.isoformat()
        }
    
    def assign_customer_service(
        self,
        ticket_id: str,
        priority: TicketPriority,
        ticket_type: TicketType
    ) -> Dict[str, Any]:
        """
        分配客服
        
        Args:
            ticket_id: 工单ID
            priority: 优先级
            ticket_type: 工单类型
            
        Returns:
            分配结果
        """
        if ticket_id not in self.tickets:
            return {
                "success": False,
                "error": f"工单不存在: {ticket_id}"
            }
        
        # 根据工单类型选择客服组
        if ticket_type in [TicketType.ORDER_ISSUE]:
            target_group = CustomerServiceGroup.ORDER_TEAM
        elif ticket_type in [TicketType.REFUND, TicketType.RETURN, 
                            TicketType.EXCHANGE, TicketType.COMPLAINT]:
            target_group = CustomerServiceGroup.AFTERSALE_TEAM
        else:
            target_group = CustomerServiceGroup.GENERAL_TEAM
        
        # 找出该组可用的客服
        available_cs = [
            cs for cs in self.cs_agents.values()
            if cs.group == target_group and cs.can_take_ticket()
        ]
        
        if not available_cs:
            # 没有可用客服,返回等待
            return {
                "success": False,
                "error": "当前没有可用客服,工单将进入等待队列"
            }
        
        # 选择负载最低的客服
        selected_cs = min(available_cs, key=lambda x: x.current_load)
        
        # 更新工单
        ticket = self.tickets[ticket_id]
        ticket.assign_to(selected_cs.cs_id, selected_cs.group)
        
        # 更新客服负载
        selected_cs.current_load += 1
        
        # 根据优先级计算预计响应时间
        response_time_map = {
            TicketPriority.URGENT: 10,
            TicketPriority.HIGH: 30,
            TicketPriority.MEDIUM: 60,
            TicketPriority.LOW: 120
        }
        estimated_time = response_time_map.get(priority, 60)
        
        assignment = TicketAssignment(
            ticket_id=ticket_id,
            cs_id=selected_cs.cs_id,
            cs_name=selected_cs.cs_name,
            group=selected_cs.group,
            estimated_response_time=estimated_time
        )
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "assigned_cs": {
                "cs_id": assignment.cs_id,
                "cs_name": assignment.cs_name,
                "group": assignment.group.value
            },
            "estimated_response_time": estimated_time,
            "message": f"工单已分配给{assignment.cs_name},预计{estimated_time}分钟内响应"
        }
    
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """获取工单详情"""
        return self.tickets.get(ticket_id)
    
    def update_ticket_status(
        self,
        ticket_id: str,
        status: TicketStatus,
        resolution: Optional[str] = None
    ) -> Dict[str, Any]:
        """更新工单状态"""
        if ticket_id not in self.tickets:
            return {
                "success": False,
                "error": f"工单不存在: {ticket_id}"
            }
        
        ticket = self.tickets[ticket_id]
        ticket.update_status(status)
        
        if resolution:
            ticket.resolution = resolution
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": status.value
        }


# 全局单例
_mock_ticket_system = MockTicketSystem()


def get_ticket_system() -> MockTicketSystem:
    """获取工单系统实例"""
    return _mock_ticket_system
