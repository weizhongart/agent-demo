"""
系统初始化模块

负责初始化AgentScope和创建所有Agent实例
"""
import agentscope
from typing import Dict, Any, Tuple
from config.settings import settings
from agents.reception_agent import create_reception_agent
from agents.retrieval_agent import create_retrieval_agent
from agents.ticket_agent import create_ticket_agent
from utils.logger import logger
from utils.exceptions import ConfigurationException


def initialize_agentscope() -> None:
    """
    初始化AgentScope框架
    """
    logger.info("初始化AgentScope...")
    
    # 验证配置
    if not settings.validate():
        raise ConfigurationException(
            "DASHSCOPE_API_KEY",
            "未设置API密钥，请在.env文件中配置DASHSCOPE_API_KEY"
        )
    
    # 定义模型配置
    model_configs = [
        {
            "config_name": "reception_agent_model",
            "model_type": "dashscope_chat",
            "model_name": settings.model.model_name,
            "api_key": settings.model.api_key,
            "stream": settings.model.stream,
            "temperature": settings.model.temperature,
            "max_tokens": settings.model.max_tokens,
        },
        {
            "config_name": "retrieval_agent_model",
            "model_type": "dashscope_chat",
            "model_name": settings.model.model_name,
            "api_key": settings.model.api_key,
            "stream": False,  # 检索Agent不需要流式
            "temperature": settings.model.temperature,
            "max_tokens": settings.model.max_tokens,
        },
        {
            "config_name": "ticket_agent_model",
            "model_type": "dashscope_chat",
            "model_name": settings.model.model_name,
            "api_key": settings.model.api_key,
            "stream": False,  # 工单Agent不需要流式
            "temperature": settings.model.temperature,
            "max_tokens": settings.model.max_tokens,
        },
    ]
    
    # 初始化AgentScope
    agentscope.init(
        model_configs=model_configs,
        project="customer_service_system",
        name="multi_agent_demo",
        save_code=False,
        save_api_invoke=False,
        use_monitor=False,
    )
    
    logger.info("AgentScope初始化完成")


def create_agents() -> Tuple[Any, Any, Any]:
    """
    创建所有Agent实例
    
    Returns:
        (reception_agent, retrieval_agent, ticket_agent) 三元组
    """
    logger.info("创建Agent实例...")
    
    try:
        # 创建检索Agent
        retrieval_agent = create_retrieval_agent()
        
        # 创建工单Agent
        ticket_agent = create_ticket_agent()
        
        # 创建接待Agent
        reception_agent = create_reception_agent()
        
        logger.info("所有Agent创建完成")
        return reception_agent, retrieval_agent, ticket_agent
        
    except Exception as e:
        logger.error(f"创建Agent失败: {e}")
        raise


def initialize_system() -> Tuple[Any, Any, Any]:
    """
    初始化整个系统
    
    Returns:
        (reception_agent, retrieval_agent, ticket_agent) 三元组
    """
    logger.info("=" * 60)
    logger.info("多智能体客服系统启动中...")
    logger.info("=" * 60)
    
    # 初始化AgentScope
    initialize_agentscope()
    
    # 创建Agent
    reception_agent, retrieval_agent, ticket_agent = create_agents()
    
    logger.info("系统初始化完成，准备就绪！")
    logger.info("=" * 60)
    
    return reception_agent, retrieval_agent, ticket_agent


if __name__ == "__main__":
    # 测试初始化
    try:
        reception, retrieval, ticket = initialize_system()
        print(f"\n✓ 接待Agent: {reception.name}")
        print(f"✓ 检索Agent: {retrieval.name}")
        print(f"✓ 工单Agent: {ticket.name}")
        print("\n系统初始化测试通过！")
    except Exception as e:
        print(f"\n✗ 系统初始化失败: {e}")
