#!/usr/bin/env python3
"""
多智能体客服系统主程序

基于AgentScope框架的电商客服系统
"""
import sys
from typing import Optional
from core.initializer import initialize_system
from core.collaboration import create_collaboration_manager
from utils.logger import logger


def print_welcome():
    """打印欢迎信息"""
    welcome_msg = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          欢迎使用多智能体客服系统 (AgentScope版)              ║
║                                                                ║
║  本系统由3个智能Agent协作提供服务:                            ║
║  • 接待Agent (Friday): 接待用户并识别意图                     ║
║  • 检索Agent: 提供知识库查询服务                              ║
║  • 工单Agent: 处理订单查询和售后问题                          ║
║                                                                ║
║  输入 'help' 查看帮助                                          ║
║  输入 'quit' 或 'exit' 退出系统                                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(welcome_msg)


def print_help():
    """打印帮助信息"""
    help_msg = """
【使用指南】

1. 知识咨询类问题:
   - "蓝牙耳机怎么使用？"
   - "退货流程是什么？"
   - "支付方式有哪些？"

2. 订单相关问题:
   - "查询订单ORD001的物流"
   - "我的订单还没发货"
   - "订单什么时候能到？"

3. 售后问题:
   - "我要退货"
   - "申请退款"
   - "商品有质量问题"

【测试订单号】
- ORD001: 正常发货中的订单
- ORD002: 延迟发货的订单
- ORD003: 高价值订单
- ORD004: 已送达订单

【系统命令】
- help: 显示此帮助信息
- quit/exit: 退出系统
- clear: 清空屏幕
"""
    print(help_msg)


def main():
    """主函数"""
    try:
        # 初始化系统
        reception_agent, retrieval_agent, ticket_agent = initialize_system()
        
        # 创建协作管理器
        collaboration = create_collaboration_manager(
            reception_agent=reception_agent,
            retrieval_agent=retrieval_agent,
            ticket_agent=ticket_agent
        )
        
        # 打印欢迎信息
        print_welcome()
        
        # 对话历史
        conversation_history = []
        
        # 主循环
        while True:
            try:
                # 获取用户输入
                user_input = input("\n👤 您: ").strip()
                
                # 检查退出命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("\n感谢使用！再见！👋\n")
                    logger.info("用户退出系统")
                    break
                
                # 检查帮助命令
                if user_input.lower() in ['help', '帮助']:
                    print_help()
                    continue
                
                # 检查清屏命令
                if user_input.lower() == 'clear':
                    import os
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print_welcome()
                    continue
                
                # 忽略空输入
                if not user_input:
                    continue
                
                # 处理用户消息
                print("\n🤖 客服 Friday: ", end="", flush=True)
                
                response = collaboration.handle_user_message(user_input)
                print(response)
                
                # 更新对话历史
                conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
            except KeyboardInterrupt:
                print("\n\n检测到中断信号，正在退出...")
                logger.info("用户通过Ctrl+C退出系统")
                break
            except Exception as e:
                logger.error(f"处理用户输入时出错: {e}", exc_info=True)
                print(f"\n❌ 抱歉，出现了一些问题: {str(e)}")
                print("请重试或输入 'help' 查看帮助\n")
    
    except KeyboardInterrupt:
        print("\n\n系统启动被中断\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"系统启动失败: {e}", exc_info=True)
        print(f"\n❌ 系统启动失败: {str(e)}")
        print("\n请检查:")
        print("1. 是否已配置 DASHSCOPE_API_KEY")
        print("2. 是否已安装所有依赖: pip install -r requirements.txt")
        print("3. 查看日志文件了解详细错误信息\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
