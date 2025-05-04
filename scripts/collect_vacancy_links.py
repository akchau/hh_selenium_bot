import logging
from base import BaseAction

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)


class CollectVacancyLinks(BaseAction):
    
    def execute(self) -> list[str]:
        """Собирает ссылки на вакансии со страницы"""
        links = []
        cards = WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]'))
        )
        logger.debug(f"Найдено карточек {len(cards)}. Проверим, какие из них содержат ссылку на вакансию.")
        for card in cards:
            href = card.get_attribute("href")
            if href and "hh.ru/vacancy" in href:
                links.append(href)
        logger.info(f"На данной странице {len(cards)} ссылкок на вакансии.")
        return links