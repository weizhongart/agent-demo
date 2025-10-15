"""
订单查询工具

提供订单相关的工具函数，供Agent调用
"""
from typing import Dict, Any, List
from mock.order_system import get_order_system
from utils.logger import logger
from utils.exceptions import OrderQueryException, OrderNotFoundException


def query_order_status(order_id: str) -> str:
    """
    查询订单状态
    
    Args:
        order_id: 订单ID，例如"ORD001"
        
    Returns:
        订单状态信息的文本描述
    """
    try:
        logger.info(f"查询订单状态: order_id={order_id}")
        
        order_system = get_order_system()
        result = order_system.query_order_status(order_id)
        
        if not result.get("success"):
            logger.warning(f"订单不存在: {order_id}")
            return f"订单不存在: {order_id}，请检查订单号是否正确"
        
        # 格式化订单信息
        response_parts = [f"【订单信息】"]
        response_parts.append(f"订单号: {result['order_id']}")
        response_parts.append(f"订单状态: {result['status']}")
        response_parts.append(f"订单金额: ¥{result['amount']:.2f}")
        
        # 商品信息
        products = result.get('products', [])
        if products:
            response_parts.append(f"\n商品信息:")
            for p in products:
                response_parts.append(f"  - {p['name']} x {p['quantity']} (¥{p['price']:.2f})")
        
        response_parts.append(f"\n下单时间: {result['created_at']}")
        
        # 物流信息
        tracking_info = result.get('tracking_info')
        if tracking_info:
            response_parts.append(f"\n【物流信息】")
            response_parts.append(f"快递公司: {tracking_info.get('carrier', '未知')}")
            response_parts.append(f"运单号: {tracking_info.get('tracking_number', '无')}")
            response_parts.append(f"当前位置: {tracking_info.get('current_location', '未知')}")
            if tracking_info.get('estimated_delivery'):
                response_parts.append(f"预计送达: {tracking_info['estimated_delivery']}")
        
        # 延迟信息
        if result.get('is_delayed'):
            response_parts.append(f"\n⚠️ 延迟提醒: {result.get('delay_reason', '订单发货延迟')}")
        
        # 已送达信息
        if result.get('delivered_at'):
            response_parts.append(f"\n✓ 已于 {result['delivered_at']} 送达")
        
        response = '\n'.join(response_parts)
        logger.info(f"订单查询成功: {order_id}")
        return response
        
    except Exception as e:
        logger.error(f"订单查询失败: {e}")
        raise OrderQueryException(str(e))


def query_orders_by_user(user_id: str, limit: int = 10) -> str:
    """
    查询用户的订单列表
    
    Args:
        user_id: 用户ID
        limit: 返回数量限制，默认10条
        
    Returns:
        订单列表的文本描述
    """
    try:
        logger.info(f"查询用户订单: user_id={user_id}, limit={limit}")
        
        order_system = get_order_system()
        orders = order_system.query_orders_by_user(user_id, limit)
        
        if not orders:
            logger.info(f"用户暂无订单: {user_id}")
            return f"您还没有订单记录"
        
        response_parts = [f"您有 {len(orders)} 个订单：\n"]
        
        for i, order in enumerate(orders, 1):
            response_parts.append(
                f"{i}. 订单号: {order['order_id']}\n"
                f"   状态: {order['status']}\n"
                f"   金额: ¥{order['amount']:.2f}\n"
                f"   下单时间: {order['created_at']}\n"
            )
        
        response = '\n'.join(response_parts)
        logger.info(f"找到{len(orders)}个订单")
        return response
        
    except Exception as e:
        logger.error(f"查询用户订单失败: {e}")
        return f"查询订单列表失败: {str(e)}"


def check_inventory(product_id: str) -> str:
    """
    检查商品库存
    
    Args:
        product_id: 商品ID
        
    Returns:
        库存信息
    """
    try:
        logger.info(f"查询库存: product_id={product_id}")
        
        order_system = get_order_system()
        result = order_system.check_inventory(product_id)
        
        if not result.get("success"):
            return f"查询库存失败: {product_id}"
        
        in_stock_text = "有货" if result['in_stock'] else "缺货"
        response = (
            f"商品库存信息:\n"
            f"商品ID: {result['product_id']}\n"
            f"可用库存: {result['available']} 件\n"
            f"预留库存: {result['reserved']} 件\n"
            f"状态: {in_stock_text}"
        )
        
        logger.info(f"库存查询成功: {product_id}")
        return response
        
    except Exception as e:
        logger.error(f"库存查询失败: {e}")
        return f"查询库存失败: {str(e)}"
