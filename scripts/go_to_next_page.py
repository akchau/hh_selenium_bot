import logging
import time
from selenium.webdriver.support.wait import WebDriverWait
from scripts.auth_via_email import BaseAction
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


logger = logging.getLogger(__name__)


class GoToNextPageScript(BaseAction):
    
    def execute(self, page):
        """
        Переход на следующую страницу на странице списка вакансий.

        Находит кнопку перехода на следующую страницу.
        Нажимает ее.
        Ждет загрузки страницы.
        """
        try:
            next_button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]'))
            )
            self._driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            next_button.click()
            logger.debug(f"Перешли на страницу {page + 2}")
            time.sleep(2)
            return True
        except Exception as e:
            logger.debug("Больше нет страниц.")
            raise e