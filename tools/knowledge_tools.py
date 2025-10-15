"""
知识库检索工具

提供知识库相关的工具函数，供Agent调用
"""
from typing import List, Dict, Any, Optional
from mock.knowledge_base import get_knowledge_base
from models.knowledge import KnowledgeCategory
from utils.logger import logger
from utils.exceptions import KnowledgeRetrievalException


def search_knowledge(
    query: str,
    top_k: int = 5,
    threshold: float = 0.6
) -> str:
    """
    搜索知识库
    
    Args:
        query: 查询文本，用户的问题描述
        top_k: 返回结果数量，默认5条
        threshold: 相似度阈值，默认0.6
        
    Returns:
        JSON格式的检索结果字符串
    """
    try:
        logger.info(f"知识库检索: query='{query}', top_k={top_k}, threshold={threshold}")
        
        kb = get_knowledge_base()
        results = kb.search_knowledge(
            query=query,
            top_k=top_k,
            threshold=threshold
        )
        
        if not results:
            logger.info(f"未找到相关知识: {query}")
            return "未找到相关知识，建议转人工客服处理"
        
        # 格式化结果
        response_parts = []
        response_parts.append(f"找到 {len(results)} 条相关知识：\n")
        
        for i, result in enumerate(results, 1):
            similarity_pct = result.similarity_score * 100
            response_parts.append(
                f"\n【知识{i}】(相似度: {similarity_pct:.1f}%)\n"
                f"标题: {result.title}\n"
                f"分类: {result.category.value}\n"
                f"内容: {result.content[:200]}{'...' if len(result.content) > 200 else ''}\n"
                f"知识ID: {result.knowledge_id}"
            )
            
            if result.matched_keywords:
                response_parts.append(f"匹配关键词: {', '.join(result.matched_keywords)}")
        
        response = '\n'.join(response_parts)
        logger.info(f"知识检索成功，返回{len(results)}条结果")
        return response
        
    except Exception as e:
        logger.error(f"知识检索失败: {e}")
        raise KnowledgeRetrievalException(str(e))


def get_knowledge_by_id(knowledge_id: str) -> str:
    """
    根据ID获取知识详情
    
    Args:
        knowledge_id: 知识ID
        
    Returns:
        知识详细内容
    """
    try:
        logger.info(f"获取知识详情: knowledge_id={knowledge_id}")
        
        kb = get_knowledge_base()
        knowledge = kb.get_knowledge_by_id(knowledge_id)
        
        if not knowledge:
            logger.warning(f"知识不存在: {knowledge_id}")
            return f"知识不存在: {knowledge_id}"
        
        response = (
            f"【{knowledge.title}】\n\n"
            f"{knowledge.content}\n\n"
            f"分类: {knowledge.category.value}\n"
            f"标签: {', '.join(knowledge.tags)}\n"
            f"查看次数: {knowledge.view_count}\n"
            f"有用率: {knowledge.get_helpfulness_rate() * 100:.1f}%"
        )
        
        logger.info(f"成功获取知识: {knowledge_id}")
        return response
        
    except Exception as e:
        logger.error(f"获取知识详情失败: {e}")
        return f"获取知识失败: {str(e)}"


def get_related_knowledge(knowledge_id: str, limit: int = 3) -> str:
    """
    获取相关知识
    
    Args:
        knowledge_id: 知识ID
        limit: 返回数量
        
    Returns:
        相关知识列表
    """
    try:
        logger.info(f"获取相关知识: knowledge_id={knowledge_id}, limit={limit}")
        
        kb = get_knowledge_base()
        related = kb.get_related_knowledge(knowledge_id, limit)
        
        if not related:
            return "暂无相关知识"
        
        response_parts = ["相关知识推荐：\n"]
        for i, k in enumerate(related, 1):
            response_parts.append(
                f"\n{i}. {k.title} (ID: {k.knowledge_id})\n"
                f"   {k.content[:100]}..."
            )
        
        logger.info(f"找到{len(related)}条相关知识")
        return '\n'.join(response_parts)
        
    except Exception as e:
        logger.error(f"获取相关知识失败: {e}")
        return f"获取相关知识失败: {str(e)}"


def feedback_knowledge(knowledge_id: str, is_helpful: bool) -> str:
    """
    反馈知识是否有用
    
    Args:
        knowledge_id: 知识ID
        is_helpful: 是否有用
        
    Returns:
        反馈结果
    """
    try:
        logger.info(f"知识反馈: knowledge_id={knowledge_id}, is_helpful={is_helpful}")
        
        kb = get_knowledge_base()
        result = kb.feedback_knowledge(knowledge_id, is_helpful)
        
        if result["success"]:
            return f"感谢您的反馈！当前有用率: {result['helpfulness_rate'] * 100:.1f}%"
        else:
            return result.get("error", "反馈失败")
            
    except Exception as e:
        logger.error(f"知识反馈失败: {e}")
        return f"反馈失败: {str(e)}"
