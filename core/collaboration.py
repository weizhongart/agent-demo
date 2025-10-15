"""
多智能体协作模块

实现多个Agent之间的协作和消息传递
"""
from typing import Any, List, Dict
from agentscope.message import Msg
from agentscope.msghub import msghub
from utils.logger import logger


class AgentCollaboration:
    """Agent协作管理器"""
    
    def __init__(
        self,
        reception_agent: Any,
        retrieval_agent: Any,
        ticket_agent: Any
    ):
        """
        初始化协作管理器
        
        Args:
            reception_agent: 接待Agent
            retrieval_agent: 检索Agent
            ticket_agent: 工单Agent
        """
        self.reception_agent = reception_agent
        self.retrieval_agent = retrieval_agent
        self.ticket_agent = ticket_agent
        
        logger.info("Agent协作管理器初始化完成")
    
    def route_to_agent(self, user_msg: Msg, intent: str) -> Msg:
        """
        根据意图路由到相应的Agent
        
        Args:
            user_msg: 用户消息
            intent: 意图类型
            
        Returns:
            Agent的响应消息
        """
        logger.info(f"路由消息到Agent: intent={intent}")
        
        # 根据意图选择Agent
        if "知识" in intent or "咨询" in intent or "怎么" in intent or "如何" in intent:
            logger.info("路由到检索Agent")
            return self.retrieval_agent(user_msg)
        elif "订单" in intent or "物流" in intent or "售后" in intent or "退" in intent or "换" in intent:
            logger.info("路由到工单Agent")
            return self.ticket_agent(user_msg)
        else:
            # 简单问候或其他,由接待Agent直接处理
            logger.info("由接待Agent直接处理")
            return self.reception_agent(user_msg)
    
    def handle_user_message(self, user_input: str, user_id: str = "user") -> str:
        """
        处理用户消息的主流程
        
        Args:
            user_input: 用户输入
            user_id: 用户ID
            
        Returns:
            系统响应
        """
        logger.info(f"处理用户消息: user_id={user_id}, input='{user_input}'")
        
        try:
            # 创建用户消息
            user_msg = Msg(
                name=user_id,
                content=user_input,
                role="user"
            )
            
            # 第一步: 接待Agent进行意图识别
            logger.info("步骤1: 接待Agent识别意图")
            reception_response = self.reception_agent(user_msg)
            
            # 简单的意图识别逻辑(在实际系统中,这应该由LLM来判断)
            content = user_input.lower()
            
            # 判断是否需要路由到专业Agent
            needs_routing = False
            target_agent = None
            
            if any(kw in content for kw in ["怎么", "如何", "是什么", "什么是", "使用", "教程"]):
                needs_routing = True
                target_agent = "retrieval"
                logger.info("检测到知识咨询意图")
            elif any(kw in content for kw in ["订单", "物流", "快递", "发货", "退货", "退款", "换货", "投诉"]):
                needs_routing = True
                target_agent = "ticket"
                logger.info("检测到订单/售后意图")
            
            # 如果需要路由,调用专业Agent
            if needs_routing:
                logger.info(f"步骤2: 路由到专业Agent - {target_agent}")
                
                if target_agent == "retrieval":
                    specialist_response = self.retrieval_agent(user_msg)
                else:
                    specialist_response = self.ticket_agent(user_msg)
                
                # 返回专业Agent的响应
                final_response = specialist_response.content
            else:
                # 接待Agent直接处理
                logger.info("接待Agent直接处理(简单问候或其他)")
                final_response = reception_response.content
            
            logger.info("消息处理完成")
            return final_response
            
        except Exception as e:
            logger.error(f"处理用户消息时出错: {e}", exc_info=True)
            return f"抱歉，处理您的请求时出现了问题: {str(e)}"
    
    def handle_conversation(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        处理多轮对话
        
        Args:
            messages: 对话历史 [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            更新后的对话历史
        """
        conversation_history = messages.copy()
        
        # 获取最后一条用户消息
        last_user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_message = msg.get("content")
                break
        
        if not last_user_message:
            logger.warning("对话历史中没有找到用户消息")
            return conversation_history
        
        # 处理消息
        response = self.handle_user_message(last_user_message)
        
        # 添加助手响应
        conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return conversation_history


def create_collaboration_manager(
    reception_agent: Any,
    retrieval_agent: Any,
    ticket_agent: Any
) -> AgentCollaboration:
    """
    创建协作管理器
    
    Args:
        reception_agent: 接待Agent
        retrieval_agent: 检索Agent
        ticket_agent: 工单Agent
        
    Returns:
        AgentCollaboration实例
    """
    return AgentCollaboration(
        reception_agent=reception_agent,
        retrieval_agent=retrieval_agent,
        ticket_agent=ticket_agent
    )
