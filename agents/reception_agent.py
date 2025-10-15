"""
接待Agent

负责接收用户咨询、识别意图、协调其他Agent、返回结果
"""
from agentscope.agents import ReActAgent
from agentscope.models import DashScopeChatWrapper  
from agentscope.service import ServiceToolkit
from config.settings import settings, AgentPrompts
from utils.logger import logger


def create_reception_agent(model_config: dict = None) -> ReActAgent:
    """
    创建接待Agent
    
    Args:
        model_config: 模型配置字典（可选）
        
    Returns:
        ReActAgent实例
    """
    logger.info("创建接待Agent...")
    
    # 使用配置或提供的配置
    if model_config is None:
        model_config = {
            "config_name": "reception_agent_model",
            "model_type": "dashscope_chat",
            "model_name": settings.model.model_name,
            "api_key": settings.model.api_key,
            "stream": settings.model.stream,  # 接待Agent使用流式输出提升体验
        }
    
    # 创建工具集（接待Agent主要通过协作来完成任务，不需要太多工具）
    toolkit = ServiceToolkit()
    
    # 创建Agent
    agent = ReActAgent(
        name="reception_agent",
        model_config_name=model_config["config_name"],
        service_toolkit=toolkit,
        sys_prompt=AgentPrompts.RECEPTION_AGENT,
        max_iters=3,  # 接待Agent执行较少的迭代，主要是意图识别和路由
        verbose=True
    )
    
    logger.info("接待Agent创建完成")
    return agent


# 用于测试的函数
if __name__ == "__main__":
    import agentscope
    
    # 初始化AgentScope
    agentscope.init(
        model_configs={
            "config_name": "reception_agent_model",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": settings.model.api_key,
            "stream": True,
        }
    )
    
    # 创建接待Agent
    agent = create_reception_agent()
    
    # 测试对话
    from agentscope.message import Msg
    
    test_messages = [
        "你好",
        "我想查一下订单ORD001的物流",
        "蓝牙耳机怎么用？"
    ]
    
    for msg_content in test_messages:
        print(f"\n用户: {msg_content}")
        test_msg = Msg(
            name="user",
            content=msg_content,
            role="user"
        )
        response = agent(test_msg)
        print(f"接待Agent: {response.content}")
