from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла при запуске pytest
load_dotenv()

pytest_plugins = (
    "fixtures.browsers",
    "fixtures.pages",
    "fixtures.applitools"
)