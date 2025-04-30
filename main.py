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
    time.sleep(10)
    # Получаем контейнер с полем для ввода электронной почты
    # parent_container = email_radio_button.find_element(By.XPATH, "./parent::*/following-sibling::div")

    # # Находим само поле ввода почты
    # email_input_field = parent_container.find_element(By.TAG_NAME, "input")

    # # Заполняем электронная почту
    # email_input_field.send_keys(settings.settings.HH_EMAIL)

    # time.sleep(10)
    # # Ввод email
    # email_input = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.NAME, "username"))
    # )
    # email_input.send_keys(settings.settings.HH_EMAIL)

    # # Переход к следующему полю
    # next_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    # next_button.click()

    # # Ввод пароля
    # password_input = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.NAME, "password"))
    # )
    # password_input.send_keys(settings.settings.HH_PASSWORD)

    # # Вход
    # login_submit = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='account-login-submit']"))
    # )
    # login_submit.click()

    # # Ожидание успешной авторизации
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "bloko-header-section-2"))
    # )
    
    # # Ожидание загрузки поля поиска
    # search_input = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "a11y-search-input"))
    # )
    
    # # Ввод поискового запроса
    # search_input.send_keys(search_query)
    # search_input.submit()
    
    # # Ожидание загрузки результатов
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "vacancy-serp-item"))
    # )
    
    # for page in range(max_pages):
    #     # Получение содержимого текущей страницы
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')
        
    #     # Парсинг вакансий
    #     for item in soup.find_all('div', class_='vacancy-serp-item'):
    #         title = item.find('h3')
    #         company = item.find('div', class_='vacancy-serp-item__meta-info-company')
    #         salary = item.find('span', class_='bloko-header-section-3')
            
    #         vacancies.append({
    #             'Должность': title.text.strip() if title else '',
    #             'Компания': company.text.strip() if company else '',
    #             'Зарплата': salary.text.strip() if salary else 'Не указана',
    #             'Ссылка': title.find('a')['href'] if title and title.find('a') else ''
    #         })
        
    #     # Переход на следующую страницу
    #     try:
    #         next_button = WebDriverWait(driver, 10).until(
    #             EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Дальше')]"))
    #         )
    #         next_button.click()
    #         time.sleep(2)  # Пауза для загрузки страницы
    #     except Exception as e:
    #         print(f"Не удалось перейти на следующую страницу: {e}")
    #         break
            
finally:
    driver.quit()

# Сохранение в Excel
df = pd.DataFrame(vacancies)
df.to_excel(f"{search_query}_вакансии.xlsx", index=False)

print(f"Сохранено {len(vacancies)} вакансий")