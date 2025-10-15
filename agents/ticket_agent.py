"""
工单Agent

负责处理订单查询、工单创建和客服分配相关的请求
"""
from agentscope.agents import ReActAgent
from agentscope.models import DashScopeChatWrapper
from agentscope.service import ServiceToolkit
from config.settings import settings, AgentPrompts
from tools.order_tools import (
    query_order_status,
    query_orders_by_user,
    check_inventory
)
from tools.ticket_tools import (
    create_ticket,
    assign_customer_service,
    get_ticket_info,
    update_ticket_status
)
from utils.logger import logger


def create_ticket_agent(model_config: dict = None) -> ReActAgent:
    """
    创建工单Agent
    
    Args:
        model_config: 模型配置字典（可选）
        
    Returns:
        ReActAgent实例
    """
    logger.info("创建工单Agent...")
    
    # 使用配置或提供的配置
    if model_config is None:
        model_config = {
            "config_name": "ticket_agent_model",
            "model_type": "dashscope_chat",
            "model_name": settings.model.model_name,
            "api_key": settings.model.api_key,
            "stream": False,  # 工单Agent不需要流式输出
        }
    
    # 创建工具集
    toolkit = ServiceToolkit()
    
    # 注册订单相关工具
    toolkit.add(query_order_status)
    toolkit.add(query_orders_by_user)
    toolkit.add(check_inventory)
    
    # 注册工单相关工具
    toolkit.add(create_ticket)
    toolkit.add(assign_customer_service)
    toolkit.add(get_ticket_info)
    toolkit.add(update_ticket_status)
    
    # 创建Agent
    agent = ReActAgent(
        name="ticket_agent",
        model_config_name=model_config["config_name"],
        service_toolkit=toolkit,
        sys_prompt=AgentPrompts.TICKET_AGENT,
        max_iters=5,  # 最多执行5轮ReAct循环
        verbose=True
    )
    
    logger.info("工单Agent创建完成")
    return agent


# 用于测试的函数
if __name__ == "__main__":
    import agentscope
    
    # 初始化AgentScope
    agentscope.init(
        model_configs={
            "config_name": "ticket_agent_model",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": settings.model.api_key,
        }
    )
    
    # 创建工单Agent
    agent = create_ticket_agent()
    
    # 测试查询
    from agentscope.message import Msg
    
    test_msg = Msg(
        name="user",
        content="我的订单ORD001还没发货，帮我查一下",
        role="user"
    )
    
    response = agent(test_msg)
    print(f"\n工单Agent响应: {response.content}")
