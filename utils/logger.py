"""
日志模块

配置和管理系统日志
"""
import os
import sys
from loguru import logger
from config.settings import settings


def setup_logger():
    """配置日志系统"""
    
    # 移除默认处理器
    logger.remove()
    
    # 确保日志目录存在
    log_dir = os.path.dirname(settings.log.log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 控制台输出 - 彩色格式
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log.log_level,
        colorize=True
    )
    
    # 文件输出 - 详细格式
    logger.add(
        settings.log.log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log.log_level,
        rotation="500 MB",  # 文件大小达到500MB时轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8"
    )
    
    # 错误日志单独输出
    if log_dir:
        error_log = os.path.join(log_dir, "error.log")
        logger.add(
            error_log,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="ERROR",
            rotation="100 MB",
            retention="60 days",
            compression="zip",
            encoding="utf-8"
        )
    
    logger.info("日志系统初始化完成")
    return logger


# 初始化日志
setup_logger()


# 导出logger供其他模块使用
__all__ = ['logger']
