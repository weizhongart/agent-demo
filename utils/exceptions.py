"""
异常处理模块

定义系统中使用的自定义异常
"""


class CustomerServiceException(Exception):
    """客服系统基础异常"""
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class AgentException(CustomerServiceException):
    """Agent相关异常"""
    pass


class AgentTimeoutException(AgentException):
    """Agent超时异常"""
    def __init__(self, agent_name: str, timeout: int):
        message = f"Agent '{agent_name}' 响应超时 ({timeout}秒)"
        super().__init__(message, "AGENT_TIMEOUT")


class AgentNotAvailableException(AgentException):
    """Agent不可用异常"""
    def __init__(self, agent_name: str):
        message = f"Agent '{agent_name}' 当前不可用"
        super().__init__(message, "AGENT_NOT_AVAILABLE")


class KnowledgeBaseException(CustomerServiceException):
    """知识库相关异常"""
    pass


class KnowledgeNotFoundException(KnowledgeBaseException):
    """知识未找到异常"""
    def __init__(self, query: str):
        message = f"未找到相关知识: {query}"
        super().__init__(message, "KNOWLEDGE_NOT_FOUND")


class KnowledgeRetrievalException(KnowledgeBaseException):
    """知识检索异常"""
    def __init__(self, error_detail: str):
        message = f"知识检索失败: {error_detail}"
        super().__init__(message, "KNOWLEDGE_RETRIEVAL_ERROR")


class OrderSystemException(CustomerServiceException):
    """订单系统相关异常"""
    pass


class OrderNotFoundException(OrderSystemException):
    """订单未找到异常"""
    def __init__(self, order_id: str):
        message = f"订单不存在: {order_id}"
        super().__init__(message, "ORDER_NOT_FOUND")


class OrderQueryException(OrderSystemException):
    """订单查询异常"""
    def __init__(self, error_detail: str):
        message = f"订单查询失败: {error_detail}"
        super().__init__(message, "ORDER_QUERY_ERROR")


class TicketSystemException(CustomerServiceException):
    """工单系统相关异常"""
    pass


class TicketCreationException(TicketSystemException):
    """工单创建异常"""
    def __init__(self, error_detail: str):
        message = f"工单创建失败: {error_detail}"
        super().__init__(message, "TICKET_CREATION_ERROR")


class CustomerServiceAssignException(TicketSystemException):
    """客服分配异常"""
    def __init__(self, error_detail: str):
        message = f"客服分配失败: {error_detail}"
        super().__init__(message, "CS_ASSIGN_ERROR")


class ModelException(CustomerServiceException):
    """模型相关异常"""
    pass


class ModelAPIException(ModelException):
    """模型API异常"""
    def __init__(self, error_detail: str):
        message = f"模型API调用失败: {error_detail}"
        super().__init__(message, "MODEL_API_ERROR")


class ModelTimeoutException(ModelException):
    """模型超时异常"""
    def __init__(self, timeout: int):
        message = f"模型响应超时 ({timeout}秒)"
        super().__init__(message, "MODEL_TIMEOUT")


class SessionException(CustomerServiceException):
    """会话相关异常"""
    pass


class SessionNotFoundException(SessionException):
    """会话未找到异常"""
    def __init__(self, session_id: str):
        message = f"会话不存在: {session_id}"
        super().__init__(message, "SESSION_NOT_FOUND")


class SessionExpiredException(SessionException):
    """会话过期异常"""
    def __init__(self, session_id: str):
        message = f"会话已过期: {session_id}"
        super().__init__(message, "SESSION_EXPIRED")


class ConfigurationException(CustomerServiceException):
    """配置异常"""
    def __init__(self, config_name: str, error_detail: str):
        message = f"配置错误 '{config_name}': {error_detail}"
        super().__init__(message, "CONFIGURATION_ERROR")
