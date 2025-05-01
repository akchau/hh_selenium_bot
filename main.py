import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

from logger import init_logger
from scripts.auth_via_email import auth
import settings
from tps import VacancyType

search_query = "Python разработчик"
max_pages = 5

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


init_logger()


logger = logging.getLogger(__name__)

# Сбор данных
vacancies = []


def parse_vacancy(link):
    """Открывает вакансию по ссылке и парсит данные"""
    logger.debug(f"Открываем вакансию: {link}")
    
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)

    try:
        # Ждём загрузки названия компании и вакансии
        company_name_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-company-name"]'))
        )
        vacancy_title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-title"]'))
        )
        
        try:
            salary_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-salary-compensation-type-net"]'))
            )
            salary = salary_element.text.strip()
        except Exception as e:
            salary = "Не указана"
        
        company_name = company_name_element.text
        vacancy_title = vacancy_title_element.text

        logger.debug(f"Получена вакансия: {vacancy_title} — {company_name}")

        vacancies.append(VacancyType(
            title=vacancy_title,
            company=company_name,
            salary=salary
        ))

    except Exception as e:
        logger.error(f"Ошибка при парсинге вакансии {link}: {e}")

    finally:
        # Закрываем вкладку
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)


def get_vacancy_links():
    """Собирает ссылки на вакансии со страницы"""
    links = []
    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]'))
    )
    logger.debug(f"Найдено карточек {len(cards)}")
    for card in cards:
        href = card.get_attribute("href")
        if href and "hh.ru/vacancy" in href:
            links.append(href)
    return links


def go_to_next_page(page):
    """Переход на следующую страницу"""
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(0.5)  # небольшая пауза для прогрузки после скролла
        next_button.click()
        logger.debug(f"Перешли на страницу {page + 1}")
        time.sleep(2)  # Ждём прогрузки страницы
        return True
    except Exception as e:
        logger.info("Больше нет страниц.")
        raise e
        # return False


try:
    # Переход на главную страницу
    driver.get("https://hh.ru")

    # Авторизация
    auth(driver, settings.settings.HH_EMAIL, settings.settings.HH_PASSWORD)

    # Поиск вакансий
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-qa="search-input"]'))
    )
    search_input.click()
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.ENTER)

    for page in range(max_pages):
        logger.debug(f"Обрабатываем страницу {page + 1}")

        # # Собираем ссылки на вакансии
        links = get_vacancy_links()
        logger.debug(f"Найдено {len(links)} вакансий на странице {page + 1}")

        # Парсим каждую вакансию
        for link in links:
            parse_vacancy(link)

        # Переходим на следующую страницу
        if not go_to_next_page(page):
            break

except Exception as e:
    logger.error(f"Произошла ошибка: {e}")

finally:
    driver.quit()

# Сохранение в Excel
df = pd.DataFrame([model.dict() for model in vacancies])
filename = f"{search_query}_вакансии.xlsx"
df.to_excel(filename, index=False)

print(f"Сохранено {len(vacancies)} вакансий в файл {filename}")