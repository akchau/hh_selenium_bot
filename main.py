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
import settings

# Параметры поиска
search_query = "Python разработчик"
max_pages = 5  # Максимальное количество страниц для парсинга

# Настройка драйвера
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Безголовый режим
driver = webdriver.Chrome(options=options)


init_logger()


logger = logging.getLogger(__name__)

# Сбор данных
vacancies = []

try:
    # Переход на главную страницу
    driver.get("https://hh.ru")
    
    # Клик на "Войти"
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'account/login')]"))
    )
    login_button.click()

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//span[contains(text(), "Войти")]]'))
    )
    
    submit_button.click()

    label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//label[.//input[@data-qa="credential-type-EMAIL"]]'))
    )
    label.click()

    email_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-qa="applicant-login-input-email"]'))
)

    # Очистка поля и ввод пароля
    email_input.clear()
    email_input.send_keys(settings.settings.HH_EMAIL)

    submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="expand-login-by-password"]'))
)
    submit_button.click()
    
    password_field = driver.find_element(By.CSS_SELECTOR, "input[data-qa='applicant-login-input-password']")
    password_field.send_keys(settings.settings.HH_PASSWORD)
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="submit-button"]'))
    )
    submit_button.click()
    
    search_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[data-qa="search-input"]'))
    )
    search_input.click()
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.ENTER)
    
    vacancy_card = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa*="vacancy-serp__vacancy"]'))
)
    vacancy_card.click()
    
    # Переключаемся на новую вкладку (если открывается в новом окне)
    driver.switch_to.window(driver.window_handles[1])
    
    # Ждем загрузки страницы вакансии
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-title"]'))
    )
    
    
    company_name_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-company-name"]'))
)

# Извлекаем текст из элемента
    company_name = company_name_element.text

    # Выводим название компании в консоль
    logger.info(f"Название компании: {company_name}")

    # Если нужно сохранить данные, добавляем их в список vacancies
    vacancies.append({
        "company_name": company_name,
    })

    # Закрываем текущую вкладку и возвращаемся к предыдущей
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    vacancy_cards = driver.find_elements(By.CSS_SELECTOR, '[data-qa*="vacancy-serp__vacancy"]')
    print(vacancy_cards[10])
    
    for index, card in enumerate(vacancy_cards):
        # Кликаем по карточке вакансии
        card.click()
        
        # Переключаемся на новую вкладку (если открывается в новом окне)
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        
        # Ждем загрузки страницы вакансии и извлекаем название компании
        company_name_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-company-name"]'))
        )
        company_name = company_name_element.text
        
        # Извлекаем заголовок вакансии
        vacancy_title_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-title"]'))
        )
        vacancy_title = vacancy_title_element.text
        
        # Логируем данные
        logger.info(f"Вакансия {index + 1}: {vacancy_title} - {company_name}")
        
        # Сохраняем данные
        vacancies.append({
            "title": vacancy_title,
            "company": company_name,
        })
        
        # Закрываем текущую вкладку и возвращаемся к предыдущей
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        # Ждем немного перед переходом к следующей вакансии
        time.sleep(1)

except Exception as e:
    logger.error(f"Произошла ошибка: {e}")

finally:
    driver.quit()

# Сохранение в Excel
df = pd.DataFrame(vacancies)
df.to_excel(f"{search_query}_вакансии.xlsx", index=False)

print(f"Сохранено {len(vacancies)} вакансий")