#!/usr/bin/env python3
"""
系统验证脚本

快速验证系统各模块是否正常工作
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """测试所有模块导入"""
    print("1. 测试模块导入...")
    
    try:
        from config.settings import settings
        from models.message import UserMessage, ConversationContext
        from models.ticket import Ticket, TicketType
        from models.knowledge import Knowledge, KnowledgeBase
        from mock.order_system import get_order_system
        from mock.ticket_system import get_ticket_system
        from mock.knowledge_base import get_knowledge_base
        from tools import knowledge_tools, order_tools, ticket_tools
        from utils.logger import logger
        from utils.exceptions import CustomerServiceException
        
        print("   ✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"   ✗ 模块导入失败: {e}")
        return False


def test_mock_systems():
    """测试模拟系统"""
    print("\n2. 测试模拟系统...")
    
    try:
        from mock.order_system import get_order_system
        from mock.ticket_system import get_ticket_system
        from mock.knowledge_base import get_knowledge_base
        
        # 测试订单系统
        order_sys = get_order_system()
        order = order_sys.query_order_status("ORD001")
        assert order["success"], "订单查询失败"
        print("   ✓ 订单系统正常")
        
        # 测试工单系统
        ticket_sys = get_ticket_system()
        assert len(ticket_sys.cs_agents) > 0, "客服人员为空"
        print("   ✓ 工单系统正常")
        
        # 测试知识库
        kb = get_knowledge_base()
        results = kb.search_knowledge("蓝牙耳机", top_k=3, threshold=0.3)
        assert len(results) > 0, "知识检索失败"
        print("   ✓ 知识库系统正常")
        
        return True
    except Exception as e:
        print(f"   ✗ 模拟系统测试失败: {e}")
        return False


def test_tools():
    """测试工具函数"""
    print("\n3. 测试工具函数...")
    
    try:
        from tools.knowledge_tools import search_knowledge
        from tools.order_tools import query_order_status
        from tools.ticket_tools import create_ticket
        
        # 测试知识检索
        result = search_knowledge("蓝牙耳机")
        assert "知识" in result or "未找到" in result, "知识检索异常"
        print("   ✓ 知识检索工具正常")
        
        # 测试订单查询
        result = query_order_status("ORD001")
        assert "订单" in result, "订单查询异常"
        print("   ✓ 订单查询工具正常")
        
        # 测试工单创建
        result = create_ticket(
            user_id="test_user",
            ticket_type="order_issue",
            title="测试工单",
            description="这是一个测试"
        )
        assert "工单" in result, "工单创建异常"
        print("   ✓ 工单创建工具正常")
        
        return True
    except Exception as e:
        print(f"   ✗ 工具函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """测试配置"""
    print("\n4. 测试配置...")
    
    try:
        from config.settings import settings, AgentPrompts
        
        # 检查API密钥配置
        if not settings.model.api_key:
            print("   ⚠️  DASHSCOPE_API_KEY未配置")
            print("   提示: 在.env文件中设置API密钥")
            return False
        
        print("   ✓ API密钥已配置")
        print(f"   ✓ 模型: {settings.model.model_name}")
        print(f"   ✓ 温度: {settings.model.temperature}")
        
        # 检查提示词
        assert len(AgentPrompts.RECEPTION_AGENT) > 0, "接待Agent提示词为空"
        assert len(AgentPrompts.RETRIEVAL_AGENT) > 0, "检索Agent提示词为空"
        assert len(AgentPrompts.TICKET_AGENT) > 0, "工单Agent提示词为空"
        print("   ✓ Agent提示词配置正常")
        
        return True
    except Exception as e:
        print(f"   ✗ 配置测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("  多智能体客服系统 - 系统验证")
    print("=" * 60)
    print()
    
    results = []
    
    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("模拟系统", test_mock_systems()))
    results.append(("工具函数", test_tools()))
    results.append(("配置检查", test_configuration()))
    
    # 统计结果
    print("\n" + "=" * 60)
    print("  验证结果")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:12s} : {status}")
    
    print("-" * 60)
    print(f"总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n✅ 所有测试通过！系统准备就绪。")
        print("\n运行系统:")
        print("  python main.py")
        print("\n运行示例:")
        print("  python examples/sample_conversations.py")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查配置和依赖。")
        if not results[3][1]:  # 配置测试失败
            print("\n配置提示:")
            print("  1. 复制环境变量模板: cp .env.example .env")
            print("  2. 编辑.env文件，设置DASHSCOPE_API_KEY")
        return 1


if __name__ == "__main__":
    sys.exit(main())
