"""
工单管理工具

提供工单相关的工具函数，供Agent调用
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from mock.ticket_system import get_ticket_system
from models.ticket import TicketType, TicketPriority, TicketStatus
from config.settings import TicketPriorityRules
from utils.logger import logger
from utils.exceptions import TicketCreationException, CustomerServiceAssignException


def create_ticket(
    user_id: str,
    ticket_type: str,
    title: str,
    description: str,
    related_order_id: Optional[str] = None,
    priority: Optional[str] = None,
    conversation_history: Optional[str] = None
) -> str:
    """
    创建工单
    
    Args:
        user_id: 用户ID
        ticket_type: 工单类型，可选值: order_issue, refund, return, exchange, complaint, consultation, technical_support, other
        title: 工单标题
        description: 问题描述
        related_order_id: 关联订单ID（可选）
        priority: 优先级（可选），可选值: urgent, high, medium, low，不提供则自动判断
        conversation_history: 对话历史JSON（可选）
        
    Returns:
        工单创建结果
    """
    try:
        logger.info(f"创建工单: user_id={user_id}, type={ticket_type}, title={title}")
        
        # 转换类型
        try:
            tt = TicketType(ticket_type)
        except ValueError:
            return f"无效的工单类型: {ticket_type}，可选值: order_issue, refund, return, exchange, complaint, consultation, technical_support, other"
        
        # 确定优先级
        if priority:
            try:
                tp = TicketPriority(priority)
            except ValueError:
                return f"无效的优先级: {priority}，可选值: urgent, high, medium, low"
        else:
            # 自动判断优先级
            keywords = [title, description]
            delay_days = 0  # 这里简化处理，实际应该从订单信息中获取
            
            priority_str = TicketPriorityRules.calculate_priority(
                order_amount=0.0,
                delay_days=delay_days,
                keywords=keywords,
                is_vip=False
            )
            tp = TicketPriority(priority_str)
            logger.info(f"自动判断优先级: {priority_str}")
        
        # 转换对话历史
        conv_history = []
        if conversation_history:
            try:
                import json
                conv_history = json.loads(conversation_history) if isinstance(conversation_history, str) else conversation_history
            except:
                logger.warning("对话历史解析失败，使用空列表")
        
        # 创建工单
        ticket_system = get_ticket_system()
        result = ticket_system.create_ticket(
            user_id=user_id,
            ticket_type=tt,
            title=title,
            description=description,
            priority=tp,
            related_order_id=related_order_id,
            conversation_history=conv_history
        )
        
        if not result.get("success"):
            raise TicketCreationException(result.get("error", "未知错误"))
        
        response = (
            f"✓ 工单创建成功\n"
            f"工单号: {result['ticket_id']}\n"
            f"优先级: {result['priority']}\n"
            f"状态: {result['status']}\n"
            f"创建时间: {result['created_at']}"
        )
        
        logger.info(f"工单创建成功: {result['ticket_id']}")
        return response
        
    except TicketCreationException as e:
        logger.error(f"工单创建失败: {e}")
        raise
    except Exception as e:
        logger.error(f"工单创建异常: {e}")
        raise TicketCreationException(str(e))


def assign_customer_service(
    ticket_id: str,
    priority: str,
    ticket_type: str
) -> str:
    """
    分配客服
    
    Args:
        ticket_id: 工单ID
        priority: 优先级，可选值: urgent, high, medium, low
        ticket_type: 工单类型，可选值: order_issue, refund, return, exchange, complaint, consultation, technical_support, other
        
    Returns:
        分配结果
    """
    try:
        logger.info(f"分配客服: ticket_id={ticket_id}, priority={priority}, type={ticket_type}")
        
        # 转换类型
        try:
            tp = TicketPriority(priority)
            tt = TicketType(ticket_type)
        except ValueError as e:
            return f"参数错误: {str(e)}"
        
        ticket_system = get_ticket_system()
        result = ticket_system.assign_customer_service(
            ticket_id=ticket_id,
            priority=tp,
            ticket_type=tt
        )
        
        if not result.get("success"):
            logger.warning(f"客服分配失败: {result.get('error')}")
            return result.get("error", "分配失败")
        
        assigned_cs = result['assigned_cs']
        response = (
            f"✓ 客服分配成功\n"
            f"工单号: {result['ticket_id']}\n"
            f"客服姓名: {assigned_cs['cs_name']}\n"
            f"客服组: {assigned_cs['group']}\n"
            f"预计响应时间: {result['estimated_response_time']} 分钟\n"
            f"{result['message']}"
        )
        
        logger.info(f"客服分配成功: {ticket_id} -> {assigned_cs['cs_name']}")
        return response
        
    except Exception as e:
        logger.error(f"客服分配异常: {e}")
        raise CustomerServiceAssignException(str(e))


def get_ticket_info(ticket_id: str) -> str:
    """
    获取工单详情
    
    Args:
        ticket_id: 工单ID
        
    Returns:
        工单详情
    """
    try:
        logger.info(f"获取工单详情: ticket_id={ticket_id}")
        
        ticket_system = get_ticket_system()
        ticket = ticket_system.get_ticket(ticket_id)
        
        if not ticket:
            return f"工单不存在: {ticket_id}"
        
        response_parts = [
            f"【工单详情】",
            f"工单号: {ticket.ticket_id}",
            f"用户ID: {ticket.user_id}",
            f"工单类型: {ticket.ticket_type.value}",
            f"优先级: {ticket.priority.value}",
            f"状态: {ticket.status.value}",
            f"标题: {ticket.title}",
            f"描述: {ticket.description}",
        ]
        
        if ticket.related_order_id:
            response_parts.append(f"关联订单: {ticket.related_order_id}")
        
        if ticket.assigned_cs:
            response_parts.append(f"分配客服: {ticket.assigned_cs}")
            response_parts.append(f"客服组: {ticket.assigned_group.value if ticket.assigned_group else '未知'}")
        
        if ticket.resolution:
            response_parts.append(f"\n解决方案: {ticket.resolution}")
        
        response_parts.append(f"\n创建时间: {ticket.created_at}")
        response_parts.append(f"更新时间: {ticket.updated_at}")
        
        if ticket.resolved_at:
            response_parts.append(f"解决时间: {ticket.resolved_at}")
        
        response = '\n'.join(response_parts)
        logger.info(f"工单详情获取成功: {ticket_id}")
        return response
        
    except Exception as e:
        logger.error(f"获取工单详情失败: {e}")
        return f"获取工单详情失败: {str(e)}"


def update_ticket_status(
    ticket_id: str,
    status: str,
    resolution: Optional[str] = None
) -> str:
    """
    更新工单状态
    
    Args:
        ticket_id: 工单ID
        status: 新状态，可选值: pending, assigned, in_progress, waiting_user, resolved, closed, cancelled
        resolution: 解决方案（可选）
        
    Returns:
        更新结果
    """
    try:
        logger.info(f"更新工单状态: ticket_id={ticket_id}, status={status}")
        
        try:
            ts = TicketStatus(status)
        except ValueError:
            return f"无效的状态: {status}"
        
        ticket_system = get_ticket_system()
        result = ticket_system.update_ticket_status(
            ticket_id=ticket_id,
            status=ts,
            resolution=resolution
        )
        
        if not result.get("success"):
            return result.get("error", "更新失败")
        
        response = f"✓ 工单状态已更新: {ticket_id} -> {status}"
        if resolution:
            response += f"\n解决方案: {resolution}"
        
        logger.info(f"工单状态更新成功: {ticket_id}")
        return response
        
    except Exception as e:
        logger.error(f"工单状态更新失败: {e}")
        return f"更新失败: {str(e)}"
