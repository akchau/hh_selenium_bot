from abc import ABC, abstractmethod
import logging
import os

from pydantic import BaseModel
from selenium import webdriver


logger = logging.getLogger(__name__)


class BaseElementParser(ABC):
    """
    Заготовка под парсер элемента.
    """

    def __init__(self) -> None:
        pass

    def parse_element(self) -> None:
        pass



class BaseAction(ABC):
    """
    Базовое действие на сайте.
    """
    
    def __init__(self, driver: webdriver.Chrome) -> None:
        """
        Инициализация класса.

        Args:
            driver (webdriver.Chrome): web-драйвер для работы 
        """
        self._driver = driver
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        В данном методе реализуйте скрипт реализующий действие.
        """
        raise NotImplementedError


class BaseFileSaver(ABC):
    """
    Базовый класс для сохранения.
    """
    
    _extension: str = None
    
    def __init__(self, base_path: str) -> None:
        self.__base_path = base_path

    @abstractmethod
    def _save(self, filepath: str, list_data: list[BaseModel]) -> None:
        """
        Реализация сохранения.

        Args:
            filepath (str): Путь для сохранения.
            list_data (list[BaseModel]): Список данных для сохранения.
        """
        raise NotImplementedError

    def save_to(self, filename: str, list_data: list[BaseModel]) -> None:
        """
        Шаблонный метод сохранителя.

        Args:
            filename (str): Имя файла.
            list_data (list[BaseModel]): Список данных для сохранения в таблицу.
        """
        full_filename = f"{filename}.{self._extension}"
        
        logger.info(f"Сохраняем результат парсинга в файл {full_filename}")
        filepath = os.path.join(self.__base_path, full_filename)
        self._save(filepath, list_data)
        logger.info(f"Сохранено {len(list_data)} вакансий в файл {filepath}")