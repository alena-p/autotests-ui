import allure
from playwright.sync_api import Page, Playwright
import agentql
import os
from pathlib import Path

# Загрузка .env файла, если установлен python-dotenv
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def initialize_playwright_page(playwright: Playwright, test_name: str, storage_state: str | None = None) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir="./videos", storage_state=storage_state)

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    page = context.new_page()

    yield page

    context.tracing.stop(path=f"./tracing/{test_name}.zip")
    browser.close()

    allure.attach.file(source=f"./tracing/{test_name}.zip", name="tracing", extension="zip")
    allure.attach.file(source=f"{page.video.path()}", name="video", attachment_type=allure.attachment_type.WEBM)


def initialize_agentql_page(playwright: Playwright, test_name: str, storage_state: str | None = None) -> Page:
    # Проверка наличия API ключа AgentQL
    # Ключ должен быть в переменной окружения или в .env файле (загружается выше)
    api_key = os.getenv("AGENTQL_API_KEY")
    if not api_key:
        raise ValueError(
            "AGENTQL_API_KEY не установлен.\n"
            "Добавьте ключ в файл .env в корне проекта:\n"
            "  AGENTQL_API_KEY=ваш-ключ\n"
            "Или установите переменную окружения:\n"
            "  export AGENTQL_API_KEY=ваш-ключ"
        )
    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir="./videos", storage_state=storage_state)

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    page = agentql.wrap(context.new_page())

    yield page

    context.tracing.stop(path=f"./tracing/{test_name}.zip")
    browser.close()

    allure.attach.file(source=f"./tracing/{test_name}.zip", name="tracing", extension="zip")
    allure.attach.file(source=f"{page.video.path()}", name="video", attachment_type=allure.attachment_type.WEBM)