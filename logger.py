import logging
from logging.handlers import RotatingFileHandler
import os

import coloredlogs

from settings import settings

logger = logging.getLogger()
debug_level = logging.DEBUG
production_level = logging.INFO
LOG_LEVEL = debug_level if debug_level else production_level

max_rotate_file_bytes = 1024 * 1024 * 300


def create_base_log_path() -> None:
    """
    Метод создающий директорию в которой будут лежать логги.
    """
    if not os.path.exists(settings.BASE_LOG_PATH):
        logger.debug("Базовый пути логов не существует. Создадим.")
        os.makedirs(settings.BASE_LOG_PATH, exist_ok=True)
    else:
        logger.debug("Базовый путь логов существует.")


def disable_bad_loggers() -> None:
    """
    В данном методе указаны все логгеры которые требуется отключить.
    """
    pass


def init_logger() -> None:
    """
    Метод инициализации логгера для работы приложения.
    """
    create_base_log_path()
    
    logger.setLevel(LOG_LEVEL)
    
    c_handler = logging.StreamHandler()
    f_handler = RotatingFileHandler(
        os.path.join(settings.BASE_LOG_PATH, 'debug.log'),
        maxBytes=max_rotate_file_bytes, 
        backupCount=3
    )

    c_handler.setLevel(LOG_LEVEL)
    f_handler.setLevel(LOG_LEVEL)

    c_format = coloredlogs.ColoredFormatter(
        '%(name)s - %(levelname)s - [%(threadName)s] - %(asctime)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    f_format = logging.Formatter(
        '%(name)s - %(levelname)s - %(asctime)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    disable_bad_loggers()


def init_test_logger() -> None:
    """
    Метод инициализации логгера для работы приложения.
    """
    logger.setLevel(LOG_LEVEL)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(LOG_LEVEL)
    c_format = coloredlogs.ColoredFormatter(
        '%(name)s - %(levelname)s - [%(threadName)s] - %(asctime)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)
    disable_bad_loggers()