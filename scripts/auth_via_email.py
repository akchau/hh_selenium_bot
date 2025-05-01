
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger = logging.getLogger(__name__)

def auth(driver, email, password) -> None:
    logger.debug("Авторизуемся через email и пароль")
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
    
    logger.debug("Вводим email")
    
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-qa="applicant-login-input-email"]'))
    )
    # Очистка поля и ввод пароля
    email_input.clear()
    email_input.send_keys(email)

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="expand-login-by-password"]'))
    )
    submit_button.click()
    
    logger.debug("Вводим пароль")
    
    password_field = driver.find_element(By.CSS_SELECTOR, "input[data-qa='applicant-login-input-password']")
    password_field.send_keys(password)
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="submit-button"]'))
    )
    submit_button.click()
    logger.debug("Авторизация успешна")