import logging
import time

from selenium.webdriver.common.by import By
from base import BaseAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tps import VacancyType



logger = logging.getLogger(__name__)


class ParseVacancyScript(BaseAction):

    
    def execute(self, link) -> VacancyType | None:
        """Открывает вакансию по ссылке и парсит данные"""
        logger.debug(f"Открываем вакансию по ссылке: {link}")

        self._driver.execute_script("window.open();")
        self._driver.switch_to.window(self._driver.window_handles[1])
        self._driver.get(link)

        try:
            # Ждём загрузки названия компании и вакансии
            company_name_element = WebDriverWait(self._driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-company-name"]'))
            )
            vacancy_title_element = WebDriverWait(self._driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-title"]'))
            )

            required_work_experience_element = WebDriverWait(self._driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-qa="work-experience-text"]'))
            )
            required_work_experience = required_work_experience_element.text.strip()

            
            
            try:
                salary_element = WebDriverWait(self._driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-salary-compensation-type-net"]'))
                )
                salary = salary_element.text.strip()
            except Exception as e:
                salary = "Не указанa"

            try:
                work_format_element = WebDriverWait(self._driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'p[data-qa="work-formats-text"]'))
                )
                work_format = work_format_element.text.strip()
            except Exception as e:
                work_format = "Не указан"

            company_name = company_name_element.text
            vacancy_title = vacancy_title_element.text

            logger.debug(f"Вакансия: {vacancy_title} — {company_name} распареша.")

            return VacancyType(
                title=vacancy_title,
                company=company_name,
                salary=salary,
                required_work_experience=required_work_experience,
                work_format=work_format,
                link=link
            )

        except Exception as e:
            logger.error(f"Ошибка при парсинге вакансии {link}: {e}")

        finally:
            # Закрываем вкладку
            self._driver.close()
            self._driver.switch_to.window(self._driver.window_handles[0])
            time.sleep(1)