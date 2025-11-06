# Интеграция Applitools Eyes

Этот документ описывает, как использовать Applitools Eyes для визуального тестирования в проекте.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Установите Playwright браузеры (если еще не установлены):
```bash
playwright install
```

## Настройка API ключа

Для работы с Applitools необходимо получить API ключ:

1. Зарегистрируйтесь на [Applitools](https://applitools.com/)
2. Получите API ключ из личного кабинета
3. Установите API ключ одним из способов:

### Способ 1: Использование .env файла (рекомендуется)

Создайте файл `.env` в корне проекта:
```bash
APPLITOOLS_API_KEY=your-api-key-here
```

Переменные из `.env` файла автоматически загружаются при запуске тестов благодаря `python-dotenv`.

**Важно:** Добавьте `.env` в `.gitignore`, чтобы не коммитить секретные ключи в репозиторий!

### Способ 2: Переменные окружения системы

#### Linux/macOS:
```bash
export APPLITOOLS_API_KEY="your-api-key-here"
```

#### Windows:
```cmd
set APPLITOOLS_API_KEY=your-api-key-here
```

### Способ 3: Прямая установка в коде (не рекомендуется)
Отредактируйте `fixtures/applitools.py` и установите ключ напрямую:
```python
eyes.api_key = "your-api-key-here"
```

## Использование

### Базовый пример

Добавьте фикстуру `eyes` в параметры вашего теста:

```python
import pytest
from applitools.playwright import Eyes
from pages.login_page import LoginPage

def test_example(login_page: LoginPage, eyes: Eyes):
    login_page.visit(url="https://example.com")
    
    # Визуальная проверка всей страницы
    eyes.check_window("Page Title")
```

### Проверка конкретного элемента

```python
def test_element(login_page: LoginPage, eyes: Eyes):
    login_page.visit(url="https://example.com")
    
    # Проверка конкретного элемента
    form_element = login_page.page.get_by_test_id("login-form")
    eyes.check(
        name="Login Form",
        target=eyes.target.locator(form_element)
    )
```

### Проверка нескольких состояний

```python
def test_multiple_states(login_page: LoginPage, eyes: Eyes):
    login_page.visit(url="https://example.com")
    
    # Начальное состояние
    eyes.check_window("Initial State")
    
    # После взаимодействия
    login_page.login_form.fill(email="test@example.com", password="password")
    eyes.check_window("After Filling Form")
    
    # После действия
    login_page.click_login_button()
    eyes.check_window("After Click")
```

## Примеры тестов

Смотрите файл `tests/test_authorization_applitools.py` для полных примеров интеграции.

## Запуск тестов

Запуск всех тестов с Applitools:
```bash
pytest tests/test_authorization_applitools.py
```

Запуск конкретного теста:
```bash
pytest tests/test_authorization_applitools.py::test_login_page_visual_regression
```

## Просмотр результатов

После запуска тестов результаты визуальных проверок доступны в [Applitools Dashboard](https://eyes.applitools.com/).

## Дополнительные возможности

- **Batch тестирование**: Группировка тестов в батчи
- **Baseline управление**: Управление базовыми снимками
- **Ignore regions**: Игнорирование динамических областей
- **Match levels**: Настройка уровня сравнения (Exact, Strict, Content, Layout)

Подробнее в [официальной документации Applitools](https://applitools.com/docs/).

