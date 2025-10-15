"""
知识库数据模型

定义知识库相关的数据结构
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
import numpy as np


class KnowledgeCategory(str, Enum):
    """知识分类"""
    PRODUCT_USAGE = "product_usage"  # 产品使用
    POLICY = "policy"  # 政策说明
    FAQ = "faq"  # 常见问题
    TROUBLESHOOTING = "troubleshooting"  # 故障排除
    SHIPPING = "shipping"  # 物流配送
    PAYMENT = "payment"  # 支付相关
    ACCOUNT = "account"  # 账户相关
    OTHER = "other"  # 其他


class KnowledgeStatus(str, Enum):
    """知识状态"""
    DRAFT = "draft"  # 草稿
    PUBLISHED = "published"  # 已发布
    ARCHIVED = "archived"  # 已归档


class Knowledge(BaseModel):
    """知识条目模型"""
    knowledge_id: str = Field(..., description="知识ID")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    keywords: List[str] = Field(default_factory=list, description="关键词")
    category: KnowledgeCategory = Field(..., description="分类")
    tags: List[str] = Field(default_factory=list, description="标签")
    status: KnowledgeStatus = Field(default=KnowledgeStatus.PUBLISHED, description="状态")
    view_count: int = Field(default=0, description="查看次数")
    helpful_count: int = Field(default=0, description="有用次数")
    unhelpful_count: int = Field(default=0, description="无用次数")
    related_knowledge_ids: List[str] = Field(default_factory=list, description="相关知识ID")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    created_by: Optional[str] = Field(None, description="创建者")
    
    # 向量嵌入(用于语义检索,存储为列表以支持序列化)
    embedding: Optional[List[float]] = Field(None, description="向量嵌入")

    def mark_helpful(self, is_helpful: bool = True):
        """标记是否有用"""
        if is_helpful:
            self.helpful_count += 1
        else:
            self.unhelpful_count += 1
        self.updated_at = datetime.now()

    def increment_view(self):
        """增加查看次数"""
        self.view_count += 1
        self.updated_at = datetime.now()

    def get_helpfulness_rate(self) -> float:
        """获取有用率"""
        total = self.helpful_count + self.unhelpful_count
        if total == 0:
            return 0.0
        return self.helpful_count / total

    class Config:
        json_schema_extra = {
            "example": {
                "knowledge_id": "KB001",
                "title": "如何查询订单物流信息",
                "content": "登录账户后，进入'我的订单'页面，点击订单号即可查看详细物流信息...",
                "keywords": ["订单", "物流", "查询"],
                "category": "faq",
                "tags": ["订单管理", "物流"]
            }
        }


class KnowledgeSearchResult(BaseModel):
    """知识检索结果"""
    knowledge_id: str = Field(..., description="知识ID")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    category: KnowledgeCategory = Field(..., description="分类")
    similarity_score: float = Field(..., description="相似度分数")
    matched_keywords: List[str] = Field(default_factory=list, description="匹配的关键词")

    class Config:
        json_schema_extra = {
            "example": {
                "knowledge_id": "KB001",
                "title": "如何查询订单物流信息",
                "content": "登录账户后...",
                "category": "faq",
                "similarity_score": 0.92,
                "matched_keywords": ["订单", "物流"]
            }
        }


class KnowledgeQuery(BaseModel):
    """知识检索查询"""
    query: str = Field(..., description="查询文本")
    top_k: int = Field(default=5, description="返回结果数量")
    threshold: float = Field(default=0.6, description="相似度阈值")
    category: Optional[KnowledgeCategory] = Field(None, description="限定分类")
    include_archived: bool = Field(default=False, description="是否包含已归档")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "怎么查物流",
                "top_k": 5,
                "threshold": 0.6,
                "category": "faq"
            }
        }


class KnowledgeFeedback(BaseModel):
    """知识反馈"""
    knowledge_id: str = Field(..., description="知识ID")
    user_id: str = Field(..., description="用户ID")
    is_helpful: bool = Field(..., description="是否有用")
    comment: Optional[str] = Field(None, description="反馈评论")
    timestamp: datetime = Field(default_factory=datetime.now, description="反馈时间")

    class Config:
        json_schema_extra = {
            "example": {
                "knowledge_id": "KB001",
                "user_id": "user_12345",
                "is_helpful": True,
                "comment": "很清楚，解决了我的问题"
            }
        }


class KnowledgeBase:
    """知识库管理类"""
    
    def __init__(self):
        self.knowledge_items: Dict[str, Knowledge] = {}
        self.embeddings_cache: Dict[str, np.ndarray] = {}

    def add_knowledge(self, knowledge: Knowledge):
        """添加知识"""
        self.knowledge_items[knowledge.knowledge_id] = knowledge
        if knowledge.embedding:
            self.embeddings_cache[knowledge.knowledge_id] = np.array(knowledge.embedding)

    def get_knowledge(self, knowledge_id: str) -> Optional[Knowledge]:
        """获取知识"""
        return self.knowledge_items.get(knowledge_id)

    def search_by_keyword(self, keywords: List[str], limit: int = 5) -> List[Knowledge]:
        """关键词搜索"""
        results = []
        for knowledge in self.knowledge_items.values():
            if knowledge.status != KnowledgeStatus.PUBLISHED:
                continue
            
            # 计算关键词匹配度
            matched = set(keywords) & set(knowledge.keywords)
            if matched:
                results.append((knowledge, len(matched)))
        
        # 按匹配度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [k for k, _ in results[:limit]]

    def get_all_published(self) -> List[Knowledge]:
        """获取所有已发布的知识"""
        return [
            k for k in self.knowledge_items.values() 
            if k.status == KnowledgeStatus.PUBLISHED
        ]
