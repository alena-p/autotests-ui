"""
Пример теста с интеграцией Applitools Eyes для визуального тестирования.

Этот файл демонстрирует, как интегрировать Applitools в существующие тесты.
Для использования Applitools необходимо:
1. Установить пакет: pip install eyes-playwright
2. Установить переменную окружения APPLITOOLS_API_KEY или настроить в коде
3. Использовать фикстуру eyes в тестах
"""
import pytest
from applitools.playwright import Eyes

from pages.base_page import BasePage
from pages.login_page import LoginPage


# @pytest.mark.flaky(reruns=5)
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.parametrize(
    "email, password",
    [
        ("user.name@gmail.com", "password"),
        ("user.name@gmail.com", "  "),
        ("  ", "password")
    ]
)
def test_wrong_email_or_password_authorization_with_applitools(
    login_page: LoginPage, 
    eyes: Eyes, 
    email: str, 
    password: str
):
    """
    Тест авторизации с визуальными проверками через Applitools.
    
    Args:
        login_page: Фикстура страницы логина
        eyes: Фикстура Applitools Eyes для визуальных проверок
        email: Email для входа (параметризовано)
        password: Пароль для входа (параметризовано)
    """
    # Переход на страницу логина
    login_page.visit(url="https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    
    # Визуальная проверка начального состояния страницы
    eyes.check_window("Login Page - Initial State")
    
    # Заполнение формы логина
    login_page.login_form.fill(email=email, password=password)
    
    # Визуальная проверка формы после заполнения
    eyes.check_window(f"Login Page - After Filling Form (email={email})")
    
    # Нажатие кнопки логина
    login_page.click_login_button()
    
    # Визуальная проверка страницы после попытки входа
    eyes.check_window(f"Login Page - After Login Attempt (email={email})")
    
    # Функциональная проверка (существующая логика)
    login_page.check_visible_wrong_email_or_password_alert()
    
    # Визуальная проверка с фокусом на алерт
    # Вариант 1: Проверка конкретного элемента через target
    # alert_element = login_page.page.get_by_test_id("login-page-wrong-email-or-password-alert")
    # eyes.check(
    #     name=f"Login Page - Error Alert (email={email})",
    #     target=eyes.target.locator(alert_element)
    # )
    
    # Вариант 2: Простая проверка всей страницы (более надежный вариант)
    eyes.check_window(f"Login Page - Error Alert Visible (email={email})")


@pytest.mark.regression
@pytest.mark.authorization
def test_login_page_visual_regression(login_page: LoginPage, eyes: Eyes):
    """
    Пример простого визуального регрессионного теста для страницы логина.
    Проверяет весь вид страницы без взаимодействия.
    """
    login_page.visit(url="https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    
    # Полная визуальная проверка страницы
    eyes.check_window("Login Page - Full Page Check")


@pytest.mark.regression
@pytest.mark.authorization
def test_login_form_interaction_visual(login_page: LoginPage, eyes: Eyes):
    """
    Пример визуального теста с проверкой различных состояний формы.
    """
    login_page.visit(url="https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    
    # Проверка пустой формы
    eyes.check_window("Login Form - Empty State")
    
    # Заполнение email
    login_page.login_form.fill(email="test@example.com", password="")
    eyes.check_window("Login Form - Email Filled")
    
    # Заполнение пароля
    login_page.login_form.fill(email="test@example.com", password="password123")
    eyes.check_window("Login Form - Both Fields Filled")
    
    # Проверка с фокусом на форму
    # Альтернативный вариант для проверки конкретного элемента:
    # form_element = login_page.page.get_by_test_id("login-form")
    # eyes.check(
    #     name="Login Form - Focused View",
    #     target=eyes.target.locator(form_element)
    # )
    
    # Простая проверка всей страницы после заполнения
    eyes.check_window("Login Form - Final State")

def test_get_listing(login_page: LoginPage, eyes: Eyes):
    login_page.visit("https://shop-fe-qa02.befree.ru/zhenskaya/platia")
    eyes.check_window("Listing page")

