import logging
from base import BaseAction

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)


class SearchVacancy(BaseAction):
    """
    Поиск по запросу.
    """
    
    def execute(self, vacancy_query: str) -> None:
        """
        - Нажатие на строку поиска.
        - Ввод запроса в строку.

        Args:
            vacancy_query (str): Запрос по которому ищем вакансии.
        """
        search_input = WebDriverWait(self._driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-qa="search-input"]')))
        search_input.click()
        search_input.send_keys(vacancy_query)
        search_input.send_keys(Keys.ENTER)