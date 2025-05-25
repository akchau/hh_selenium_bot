import logging
import time

from selenium.webdriver.common.by import By
from base import BaseAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tps import VacancyType



logger = logging.getLogger(__name__)



class ElementParser:
    """
    Парсер элемента на странице вакансии.
    """

    def __init__(self, driver, css_selector: str, default_value: str):
        self.__driver = driver
        self.__css_selector = css_selector
        self.__default_value = default_value
    
    
    def parse(self) -> str:
        try:
            salary_element = WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.__css_selector))
            )
            return salary_element.text.strip()
        except Exception as e:
            return self.__default_value



class ParseVacancyScript(BaseAction):
    
    def execute(self, link) -> VacancyType | None:
        """
        Открывает вакансию по ссылке и парсит данные
        """

        logger.debug(f"Открываем вакансию по ссылке: {link}")

        self._driver.execute_script("window.open();")
        self._driver.switch_to.window(self._driver.window_handles[1])
        self._driver.get(link)

        try:

            company_name = ElementParser(driver=self._driver, css_selector='[data-qa="vacancy-company-name"]', default_value="Не указано").parse()
            vacancy_title = ElementParser(driver=self._driver, css_selector='[data-qa="vacancy-title"]', default_value="Не указан").parse()
            vct = VacancyType(
                title=vacancy_title,
                company=company_name,
                salary=ElementParser(driver=self._driver, css_selector='[data-qa="vacancy-salary-compensation-type-net"]', default_value="Не указанa").parse(),
                required_work_experience=ElementParser(driver=self._driver, css_selector='p[data-qa="work-experience-text"]', default_value="Не указан").parse(),
                work_format=ElementParser(driver=self._driver, css_selector='p[data-qa="work-formats-text"]', default_value="Не указан").parse(),
                link=link
            )
            logger.debug(f"Вакансия: {vacancy_title} — {company_name} распареша.")
            return vct

        except Exception as e:
            logger.error(f"Ошибка при парсинге вакансии {link}: {e}")

        finally:
            # Закрываем вкладку
            self._driver.close()
            self._driver.switch_to.window(self._driver.window_handles[0])
            time.sleep(1)