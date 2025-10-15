"""
模拟订单系统

用于测试的订单系统模拟实现
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import random
from models.message import IntentType


class OrderStatus:
    """订单状态"""
    PENDING_PAYMENT = "pending_payment"  # 待支付
    PENDING_SHIP = "pending_ship"  # 待发货
    SHIPPED = "shipped"  # 已发货
    DELIVERED = "delivered"  # 已送达
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消


class MockOrderSystem:
    """模拟订单系统"""
    
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}
        self._init_mock_data()
    
    def _init_mock_data(self):
        """初始化模拟数据"""
        # 正常订单
        self.orders["ORD001"] = {
            "order_id": "ORD001",
            "user_id": "user_001",
            "status": OrderStatus.SHIPPED,
            "amount": 299.00,
            "products": [
                {"name": "无线蓝牙耳机", "quantity": 1, "price": 299.00}
            ],
            "created_at": (datetime.now() - timedelta(days=3)).isoformat(),
            "shipped_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "tracking_number": "SF1234567890",
            "carrier": "顺丰快递",
            "current_location": "北京市朝阳区分拨中心",
            "estimated_delivery": (datetime.now() + timedelta(days=1)).isoformat(),
            "is_delayed": False,
            "delay_reason": None
        }
        
        # 延迟订单
        self.orders["ORD002"] = {
            "order_id": "ORD002",
            "user_id": "user_002",
            "status": OrderStatus.PENDING_SHIP,
            "amount": 1599.00,
            "products": [
                {"name": "智能手环", "quantity": 2, "price": 799.00}
            ],
            "created_at": (datetime.now() - timedelta(days=8)).isoformat(),
            "shipped_at": None,
            "tracking_number": None,
            "carrier": None,
            "current_location": "仓库",
            "estimated_delivery": None,
            "is_delayed": True,
            "delay_reason": "库存不足,正在紧急调货"
        }
        
        # 高价值订单
        self.orders["ORD003"] = {
            "order_id": "ORD003",
            "user_id": "user_003",
            "status": OrderStatus.SHIPPED,
            "amount": 5999.00,
            "products": [
                {"name": "笔记本电脑", "quantity": 1, "price": 5999.00}
            ],
            "created_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "shipped_at": (datetime.now() - timedelta(hours=12)).isoformat(),
            "tracking_number": "JD9876543210",
            "carrier": "京东物流",
            "current_location": "上海市浦东新区配送中心",
            "estimated_delivery": datetime.now().isoformat(),
            "is_delayed": False,
            "delay_reason": None
        }
        
        # 已送达订单
        self.orders["ORD004"] = {
            "order_id": "ORD004",
            "user_id": "user_001",
            "status": OrderStatus.DELIVERED,
            "amount": 199.00,
            "products": [
                {"name": "鼠标垫", "quantity": 1, "price": 199.00}
            ],
            "created_at": (datetime.now() - timedelta(days=10)).isoformat(),
            "shipped_at": (datetime.now() - timedelta(days=8)).isoformat(),
            "tracking_number": "YTO1122334455",
            "carrier": "圆通快递",
            "current_location": "已签收",
            "estimated_delivery": (datetime.now() - timedelta(days=5)).isoformat(),
            "is_delayed": False,
            "delay_reason": None,
            "delivered_at": (datetime.now() - timedelta(days=5)).isoformat()
        }
    
    def query_order_status(self, order_id: str) -> Dict[str, Any]:
        """
        查询订单状态
        
        Args:
            order_id: 订单ID
            
        Returns:
            订单信息字典
        """
        if order_id not in self.orders:
            return {
                "success": False,
                "error": f"订单不存在: {order_id}",
                "order_id": order_id
            }
        
        order = self.orders[order_id]
        return {
            "success": True,
            "order_id": order["order_id"],
            "status": order["status"],
            "amount": order["amount"],
            "products": order["products"],
            "created_at": order["created_at"],
            "tracking_info": {
                "tracking_number": order.get("tracking_number"),
                "carrier": order.get("carrier"),
                "current_location": order.get("current_location"),
                "estimated_delivery": order.get("estimated_delivery")
            } if order["status"] in [OrderStatus.SHIPPED, OrderStatus.DELIVERED] else None,
            "is_delayed": order.get("is_delayed", False),
            "delay_reason": order.get("delay_reason"),
            "delivered_at": order.get("delivered_at")
        }
    
    def query_orders_by_user(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        查询用户的订单列表
        
        Args:
            user_id: 用户ID
            limit: 返回数量限制
            
        Returns:
            订单列表
        """
        user_orders = [
            order for order in self.orders.values()
            if order["user_id"] == user_id
        ]
        
        # 按创建时间倒序
        user_orders.sort(key=lambda x: x["created_at"], reverse=True)
        
        return [
            {
                "order_id": order["order_id"],
                "status": order["status"],
                "amount": order["amount"],
                "created_at": order["created_at"],
                "product_count": len(order["products"])
            }
            for order in user_orders[:limit]
        ]
    
    def check_inventory(self, product_id: str) -> Dict[str, Any]:
        """
        检查库存
        
        Args:
            product_id: 产品ID
            
        Returns:
            库存信息
        """
        # 模拟库存查询
        inventory_data = {
            "PROD001": {"available": 100, "reserved": 20},
            "PROD002": {"available": 5, "reserved": 3},
            "PROD003": {"available": 0, "reserved": 0},
        }
        
        if product_id in inventory_data:
            data = inventory_data[product_id]
            return {
                "success": True,
                "product_id": product_id,
                "available": data["available"],
                "reserved": data["reserved"],
                "in_stock": data["available"] > 0
            }
        else:
            return {
                "success": True,
                "product_id": product_id,
                "available": random.randint(10, 100),
                "reserved": random.randint(0, 10),
                "in_stock": True
            }


# 全局单例
_mock_order_system = MockOrderSystem()


def get_order_system() -> MockOrderSystem:
    """获取订单系统实例"""
    return _mock_order_system
