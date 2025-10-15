"""
模拟知识库系统

用于测试的知识库系统模拟实现
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.knowledge import (
    Knowledge, KnowledgeCategory, KnowledgeStatus,
    KnowledgeSearchResult, KnowledgeQuery
)
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MockKnowledgeBase:
    """模拟知识库系统"""
    
    def __init__(self):
        self.knowledge_items: Dict[str, Knowledge] = {}
        self.vectorizer = TfidfVectorizer()
        self.document_vectors = None
        self.document_ids = []
        self._init_knowledge_data()
        self._build_index()
    
    def _init_knowledge_data(self):
        """初始化知识库数据"""
        knowledge_data = [
            {
                "knowledge_id": "KB001",
                "title": "如何查询订单物流信息",
                "content": """您可以通过以下方式查询订单物流信息:
1. 登录账户后,进入"我的订单"页面
2. 找到您要查询的订单,点击订单号
3. 在订单详情页面可以看到物流跟踪信息
4. 如果订单已发货,会显示快递公司和运单号
5. 点击运单号可以跳转到快递公司官网查看详细物流轨迹

注意:订单发货后24小时内,物流信息可能还未更新,请耐心等待。""",
                "keywords": ["订单", "物流", "查询", "快递", "运单号"],
                "category": KnowledgeCategory.FAQ,
                "tags": ["订单管理", "物流查询"]
            },
            {
                "knowledge_id": "KB002",
                "title": "退货退款流程说明",
                "content": """退货退款流程如下:
1. 在订单详情页点击"申请退货退款"
2. 选择退货原因(质量问题、不喜欢、尺寸不合适等)
3. 上传商品照片(如有质量问题)
4. 等待商家审核(1-2个工作日)
5. 审核通过后,系统会提供退货地址和快递单号
6. 将商品寄回,并在系统中填写退货快递单号
7. 商家收到货并确认后,款项将原路退回

退款到账时间:
- 支付宝/微信: 1-3个工作日
- 银行卡: 3-7个工作日

注意:商品需保持完好,不影响二次销售。""",
                "keywords": ["退货", "退款", "申请", "流程", "售后"],
                "category": KnowledgeCategory.FAQ,
                "tags": ["售后服务", "退货退款"]
            },
            {
                "knowledge_id": "KB003",
                "title": "无线蓝牙耳机使用教程",
                "content": """无线蓝牙耳机使用方法:

配对连接:
1. 打开耳机充电盒,耳机会自动开机
2. 首次使用会自动进入配对模式(指示灯闪烁)
3. 在手机蓝牙设置中搜索设备
4. 选择耳机型号进行连接
5. 连接成功后,指示灯常亮或熄灭

基本操作:
- 单击: 播放/暂停
- 双击: 下一曲
- 三击: 上一曲
- 长按: 激活语音助手

充电说明:
- 将耳机放入充电盒即可充电
- 充电盒可通过USB-C线充电
- 充满电约需2小时,可使用4-6小时

故障排除:
- 无法配对: 长按耳机10秒重置
- 声音小: 检查手机和耳机音量
- 连接不稳定: 清除配对记录后重新连接""",
                "keywords": ["蓝牙耳机", "使用", "配对", "连接", "充电", "操作"],
                "category": KnowledgeCategory.PRODUCT_USAGE,
                "tags": ["产品使用", "耳机"]
            },
            {
                "knowledge_id": "KB004",
                "title": "配送时效说明",
                "content": """我们的配送时效如下:

标准配送:
- 大城市(北上广深等): 2-3个工作日
- 省会城市: 3-5个工作日
- 地级市: 4-7个工作日
- 偏远地区: 7-15个工作日

加急配送(额外收费):
- 大城市: 次日达
- 其他地区: 48小时内送达

影响配送时效的因素:
1. 商品库存情况
2. 天气情况
3. 节假日(春节、国庆等)
4. 收货地址的偏远程度
5. 不可抗力因素

注意:
- 具体时效以实际物流为准
- 预售商品按预售说明发货
- 定制商品制作周期另计""",
                "keywords": ["配送", "物流", "时效", "发货", "送达"],
                "category": KnowledgeCategory.SHIPPING,
                "tags": ["物流配送", "时效说明"]
            },
            {
                "knowledge_id": "KB005",
                "title": "支付方式说明",
                "content": """我们支持以下支付方式:

在线支付:
1. 支付宝
2. 微信支付
3. 银联在线支付
4. 信用卡支付(VISA、MasterCard)
5. Apple Pay
6. 花呗分期

货到付款:
- 支持部分地区
- 需额外支付5元手续费
- 仅支持现金和POS机刷卡

支付安全:
- 所有支付渠道均经过加密
- 不会保存您的支付密码
- 支持7天无理由退款

支付问题:
- 支付失败: 检查余额或联系银行
- 重复支付: 系统会自动退款
- 支付超时: 订单会自动取消,款项原路退回

优惠券使用:
- 在支付页面输入优惠码
- 满足条件的优惠券会自动显示
- 每个订单限用一张优惠券""",
                "keywords": ["支付", "付款", "支付宝", "微信", "货到付款", "优惠券"],
                "category": KnowledgeCategory.PAYMENT,
                "tags": ["支付方式", "付款"]
            },
            {
                "knowledge_id": "KB006",
                "title": "账户安全设置",
                "content": """保护您的账户安全:

密码设置:
- 使用8位以上复杂密码
- 包含字母、数字和符号
- 定期更换密码
- 不要使用生日等容易被猜到的密码

二次验证:
1. 绑定手机号
2. 开启登录验证
3. 设置支付密码
4. 绑定邮箱作为备用

防范提醒:
- 不要将密码告诉他人
- 不要在公共设备上保存密码
- 警惕钓鱼网站和诈骗短信
- 官方不会索要验证码

账户异常:
- 收到异常登录提醒立即修改密码
- 发现未知订单立即联系客服
- 可以查看登录记录
- 支持远程登出所有设备

找回密码:
1. 点击"忘记密码"
2. 通过手机验证码找回
3. 或通过邮箱找回
4. 设置新密码""",
                "keywords": ["账户", "安全", "密码", "登录", "验证", "找回"],
                "category": KnowledgeCategory.ACCOUNT,
                "tags": ["账户安全", "密码管理"]
            },
        ]
        
        for data in knowledge_data:
            knowledge = Knowledge(**data)
            self.knowledge_items[knowledge.knowledge_id] = knowledge
    
    def _build_index(self):
        """构建索引"""
        if not self.knowledge_items:
            return
        
        # 收集所有文档
        documents = []
        self.document_ids = []
        
        for knowledge in self.knowledge_items.values():
            if knowledge.status == KnowledgeStatus.PUBLISHED:
                # 组合标题、内容和关键词用于检索
                text = f"{knowledge.title} {knowledge.content} {' '.join(knowledge.keywords)}"
                documents.append(text)
                self.document_ids.append(knowledge.knowledge_id)
        
        # 构建TF-IDF向量
        if documents:
            self.document_vectors = self.vectorizer.fit_transform(documents)
    
    def search_knowledge(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.6,
        category: Optional[KnowledgeCategory] = None
    ) -> List[KnowledgeSearchResult]:
        """
        语义检索知识
        
        Args:
            query: 查询文本
            top_k: 返回数量
            threshold: 相似度阈值
            category: 限定分类
            
        Returns:
            检索结果列表
        """
        if not self.document_vectors or not self.document_ids:
            return []
        
        # 将查询转换为向量
        query_vector = self.vectorizer.transform([query])
        
        # 计算相似度
        similarities = cosine_similarity(query_vector, self.document_vectors)[0]
        
        # 获取排序后的索引
        ranked_indices = np.argsort(similarities)[::-1]
        
        # 构建结果
        results = []
        for idx in ranked_indices:
            if len(results) >= top_k:
                break
            
            similarity = float(similarities[idx])
            if similarity < threshold:
                continue
            
            knowledge_id = self.document_ids[idx]
            knowledge = self.knowledge_items[knowledge_id]
            
            # 类别过滤
            if category and knowledge.category != category:
                continue
            
            # 提取匹配的关键词
            query_words = set(query.lower().split())
            matched_keywords = [
                kw for kw in knowledge.keywords
                if kw.lower() in query.lower() or any(qw in kw.lower() for qw in query_words)
            ]
            
            # 增加查看次数
            knowledge.increment_view()
            
            result = KnowledgeSearchResult(
                knowledge_id=knowledge.knowledge_id,
                title=knowledge.title,
                content=knowledge.content,
                category=knowledge.category,
                similarity_score=similarity,
                matched_keywords=matched_keywords
            )
            results.append(result)
        
        return results
    
    def get_knowledge_by_id(self, knowledge_id: str) -> Optional[Knowledge]:
        """
        获取知识详情
        
        Args:
            knowledge_id: 知识ID
            
        Returns:
            知识对象
        """
        knowledge = self.knowledge_items.get(knowledge_id)
        if knowledge:
            knowledge.increment_view()
        return knowledge
    
    def get_related_knowledge(
        self,
        knowledge_id: str,
        limit: int = 3
    ) -> List[Knowledge]:
        """
        获取相关知识
        
        Args:
            knowledge_id: 知识ID
            limit: 返回数量
            
        Returns:
            相关知识列表
        """
        knowledge = self.knowledge_items.get(knowledge_id)
        if not knowledge:
            return []
        
        # 使用相同分类或相同标签的知识作为相关知识
        related = []
        for k in self.knowledge_items.values():
            if k.knowledge_id == knowledge_id:
                continue
            if k.status != KnowledgeStatus.PUBLISHED:
                continue
            
            # 计算相关性分数
            score = 0
            if k.category == knowledge.category:
                score += 2
            
            common_tags = set(k.tags) & set(knowledge.tags)
            score += len(common_tags)
            
            if score > 0:
                related.append((k, score))
        
        # 按分数排序
        related.sort(key=lambda x: x[1], reverse=True)
        
        return [k for k, _ in related[:limit]]
    
    def feedback_knowledge(
        self,
        knowledge_id: str,
        is_helpful: bool
    ) -> Dict[str, Any]:
        """
        反馈知识是否有用
        
        Args:
            knowledge_id: 知识ID
            is_helpful: 是否有用
            
        Returns:
            反馈结果
        """
        knowledge = self.knowledge_items.get(knowledge_id)
        if not knowledge:
            return {
                "success": False,
                "error": f"知识不存在: {knowledge_id}"
            }
        
        knowledge.mark_helpful(is_helpful)
        
        return {
            "success": True,
            "knowledge_id": knowledge_id,
            "helpfulness_rate": knowledge.get_helpfulness_rate()
        }


# 全局单例
_mock_knowledge_base = MockKnowledgeBase()


def get_knowledge_base() -> MockKnowledgeBase:
    """获取知识库实例"""
    return _mock_knowledge_base
