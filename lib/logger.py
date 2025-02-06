import logging
import os
from lib.data import OUTPUT_PATHS

def setup_logger(name='ipcsuite', log_level=logging.INFO):
    # 创建日志目录
    log_dir = os.path.join(OUTPUT_PATHS, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 设置日志文件路径
    log_file = os.path.join(log_dir, 'ipcsuite.log')

    # 创建logger实例
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# 创建全局logger实例
logger = setup_logger()