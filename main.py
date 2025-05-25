import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from file_savers.excel_saver import ExcelSaver
from logger import init_logger
from scripts.auth_via_email import AuthViaEmailPasssword
from scripts.collect_vacancy_links import CollectVacancyLinks
from scripts.go_to_next_page import GoToNextPageScript
from scripts.parse_vacancy import ParseVacancyScript
from scripts.search_vacancy import SearchVacancy
from settings import settings

search_query = "Python разработчик"
max_pages = 50

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


init_logger()


logger = logging.getLogger(__name__)


try:
    vacancies = []
    # Переход на главную страницу
    driver.get("https://hh.ru")

    AuthViaEmailPasssword(driver).execute(email=settings.HH_EMAIL, password=settings.HH_PASSWORD)

    SearchVacancy(driver).execute(search_query)

    for page in range(max_pages):

        logger.info(f"Обрабатываем страницу {page}")

        links = CollectVacancyLinks(driver).execute()

        logger.debug(f"Найдено {len(links)} вакансий на странице {page+1}")
        for link in links:
            logger.info(f"Пытаемся получить данные по ссылке вакансии {link}")
            parsed_vacancy = ParseVacancyScript(driver).execute(link)
            if parsed_vacancy:
                logger.info(f"Вакансия {parsed_vacancy.company} - {parsed_vacancy.title} успешно сохранена!")
                vacancies.append(parsed_vacancy)
            else:
                logger.info(f"При парсинге вакансии по ссылке {link} произошла ошибка.")
            break
        # Переходим на следующую страницу
        if not GoToNextPageScript(driver).execute(page):
            break
    logger.info(f"Страницы закончились или достигли предельного значения.")

except Exception as e:
    logger.error(f"Произошла ошибка: {e}")

finally:
    driver.quit()


ExcelSaver(base_path=".").save_to(filename="Python разработчик_вакансии", list_data=vacancies)