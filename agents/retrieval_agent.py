"""
检索Agent

负责处理知识库检索相关的请求
"""
from agentscope.agents import ReActAgent
from agentscope.models import DashScopeChatWrapper
from agentscope.service import ServiceToolkit
from config.settings import settings, AgentPrompts
from tools.knowledge_tools import (
    search_knowledge,
    get_knowledge_by_id,
    get_related_knowledge,
    feedback_knowledge
)
from utils.logger import logger


def create_retrieval_agent(model_config: dict = None) -> ReActAgent:
    """
    创建检索Agent
    
    Args:
        model_config: 模型配置字典（可选）
        
    Returns:
        ReActAgent实例
    """
    logger.info("创建检索Agent...")
    
    # 使用配置或提供的配置
    if model_config is None:
        model_config = {
            "config_name": "retrieval_agent_model",
            "model_type": "dashscope_chat",
            "model_name": settings.model.model_name,
            "api_key": settings.model.api_key,
            "stream": False,  # 检索Agent不需要流式输出
        }
    
    # 创建工具集
    toolkit = ServiceToolkit()
    
    # 注册知识库相关工具
    toolkit.add(search_knowledge)
    toolkit.add(get_knowledge_by_id)
    toolkit.add(get_related_knowledge)
    toolkit.add(feedback_knowledge)
    
    # 创建Agent
    agent = ReActAgent(
        name="retrieval_agent",
        model_config_name=model_config["config_name"],
        service_toolkit=toolkit,
        sys_prompt=AgentPrompts.RETRIEVAL_AGENT,
        max_iters=5,  # 最多执行5轮ReAct循环
        verbose=True
    )
    
    logger.info("检索Agent创建完成")
    return agent


# 用于测试的函数
if __name__ == "__main__":
    import agentscope
    
    # 初始化AgentScope
    agentscope.init(
        model_configs={
            "config_name": "retrieval_agent_model",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": settings.model.api_key,
        }
    )
    
    # 创建检索Agent
    agent = create_retrieval_agent()
    
    # 测试查询
    from agentscope.message import Msg
    
    test_msg = Msg(
        name="user",
        content="我想知道如何查询订单物流",
        role="user"
    )
    
    response = agent(test_msg)
    print(f"\n检索Agent响应: {response.content}")
