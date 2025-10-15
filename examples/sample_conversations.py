"""
示例对话脚本

演示系统的各种使用场景
"""
from core.initializer import initialize_system
from core.collaboration import create_collaboration_manager
from utils.logger import logger


def print_separator():
    """打印分隔线"""
    print("\n" + "=" * 70 + "\n")


def scenario_knowledge_query():
    """场景1: 知识咨询"""
    print("📚 场景1: 知识咨询 - 用户询问产品使用方法")
    print_separator()
    
    queries = [
        "蓝牙耳机怎么使用？",
        "退货流程是什么？",
        "支持哪些支付方式？"
    ]
    
    return queries


def scenario_order_query():
    """场景2: 订单查询"""
    print("📦 场景2: 订单查询 - 用户查询订单状态")
    print_separator()
    
    queries = [
        "查询订单ORD001的物流信息",
        "我的订单ORD002什么时候发货？"
    ]
    
    return queries


def scenario_after_sale():
    """场景3: 售后处理"""
    print("🔄 场景3: 售后处理 - 用户申请退货")
    print_separator()
    
    queries = [
        "我想退货，订单号是ORD003",
        "商品有质量问题，要求退款"
    ]
    
    return queries


def scenario_complex_conversation():
    """场景4: 复杂对话"""
    print("💬 场景4: 复杂多轮对话")
    print_separator()
    
    queries = [
        "你好",
        "我的订单ORD002还没发货，帮我查一下",
        "为什么这么慢？",
        "那我要退款"
    ]
    
    return queries


def run_scenario(collaboration, scenario_name, queries):
    """
    运行场景
    
    Args:
        collaboration: 协作管理器
        scenario_name: 场景名称
        queries: 查询列表
    """
    print(f"\n🎬 开始执行: {scenario_name}\n")
    
    for i, query in enumerate(queries, 1):
        print(f"步骤 {i}:")
        print(f"👤 用户: {query}")
        
        try:
            response = collaboration.handle_user_message(query)
            print(f"🤖 Friday: {response}")
        except Exception as e:
            print(f"❌ 错误: {e}")
            logger.error(f"场景执行失败: {e}", exc_info=True)
        
        print("-" * 70)
    
    print(f"\n✅ 场景完成: {scenario_name}")
    print_separator()


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              多智能体客服系统 - 示例对话演示                     ║
║                                                                  ║
║  本脚本演示系统在不同场景下的使用效果                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # 初始化系统
        print("正在初始化系统...\n")
        reception_agent, retrieval_agent, ticket_agent = initialize_system()
        
        # 创建协作管理器
        collaboration = create_collaboration_manager(
            reception_agent=reception_agent,
            retrieval_agent=retrieval_agent,
            ticket_agent=ticket_agent
        )
        
        print("\n系统初始化完成！开始演示...\n")
        print_separator()
        
        # 场景1: 知识咨询
        queries_1 = scenario_knowledge_query()
        run_scenario(collaboration, "知识咨询", queries_1)
        
        # 场景2: 订单查询
        queries_2 = scenario_order_query()
        run_scenario(collaboration, "订单查询", queries_2)
        
        # 场景3: 售后处理
        queries_3 = scenario_after_sale()
        run_scenario(collaboration, "售后处理", queries_3)
        
        # 场景4: 复杂对话
        queries_4 = scenario_complex_conversation()
        run_scenario(collaboration, "复杂多轮对话", queries_4)
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                      所有示例场景演示完成！                      ║
║                                                                  ║
║  您可以查看日志文件了解详细的执行过程                            ║
║  日志文件: logs/customer_service.log                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
    except KeyboardInterrupt:
        print("\n\n演示被中断\n")
    except Exception as e:
        print(f"\n❌ 演示执行失败: {e}\n")
        logger.error(f"示例脚本执行失败: {e}", exc_info=True)


if __name__ == "__main__":
    main()
