import os
import pytest
from dotenv import load_dotenv
from applitools.playwright import Eyes
from playwright.sync_api import Page

# Загрузка переменных окружения из .env файла
load_dotenv()


@pytest.fixture(scope="function")
def eyes(chromium_page: Page, request) -> Eyes:
    """
    Фикстура для инициализации Applitools Eyes.
    Настраивает Eyes и открывает тест перед каждым тестом.
    
    Для использования необходимо установить переменную окружения APPLITOOLS_API_KEY
    или установить API ключ в коде.
    
    Usage:
        def test_example(login_page: LoginPage, eyes: Eyes):
            login_page.visit(url="...")
            eyes.check_window("Page Title")
    """
    eyes = Eyes()
    
    # Установка API ключа из переменной окружения
    # Можно также установить напрямую: eyes.api_key = "your-api-key"
    api_key = os.getenv("APPLITOOLS_API_KEY")
    if api_key:
        eyes.api_key = api_key
    else:
        # Если ключ не установлен, выводим предупреждение
        pytest.skip("APPLITOOLS_API_KEY не установлен. Установите переменную окружения для использования Applitools.")
    
    # Получение имени теста из request
    test_name = request.node.name if hasattr(request, 'node') else "Test"
    
    # Открытие Eyes с указанием приложения и теста
    eyes.open(
        driver=chromium_page,
        app_name="QA Automation Engineer UI Course",
        test_name=test_name,
        viewport_size={"width": None, "height": None}
    )
    
    yield eyes
    
    # Закрытие Eyes после теста
    try:
        eyes.close()
    except Exception as e:
        # Если произошла ошибка при закрытии, пытаемся прервать сессию
        eyes.abort_if_not_closed()
        raise e

