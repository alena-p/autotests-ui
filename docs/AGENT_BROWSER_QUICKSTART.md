# Быстрый старт с agent-browser

## Установка

```bash
# Установить agent-browser глобально
npm install -g agent-browser

# Проверить установку
agent-browser --version
```

## Минимальный пример

```python
import pytest
from playwright.sync_api import Page
from elements.ai_element import AIButton, AIInput

def test_login_with_ai(page: Page):
    page.goto("https://your-app.com/login")
    
    # Создать AI элементы - они найдут себя автоматически
    email = AIInput(page, "Email", search_text="Email")
    password = AIInput(page, "Password", search_text="Password")
    login_btn = AIButton(page, "Login", search_text="Login")
    
    # Использовать как обычные элементы
    email.fill("user@example.com")
    password.fill("password123")
    login_btn.click()
```

## Получение snapshot для отладки

```python
from tools.agent_browser.client import AgentBrowserClient
from tools.agent_browser.snapshot import SnapshotParser

def test_debug_snapshot(page: Page):
    client = AgentBrowserClient()
    parser = SnapshotParser()
    
    page.goto("https://your-app.com")
    client.sync_with_playwright(page)
    
    # Получить snapshot
    snapshot = client.snapshot(interactive=True)
    print(snapshot)
    
    # Найти все кнопки
    buttons = parser.find_by_type(snapshot, "button")
    for btn in buttons:
        print(f"Button: {btn.text} - ref: {btn.ref}")
```

## Миграция существующих тестов

### До (с data-testid):
```python
from elements.button import Button
from elements.input import Input

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = Input(page, "login-email-input", "Email")
        self.password_input = Input(page, "login-password-input", "Password")
        self.login_button = Button(page, "login-button", "Login")
```

### После (с agent-browser):
```python
from elements.ai_element import AIInput, AIButton

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = AIInput(page, "Email", search_text="Email", element_type="input")
        self.password_input = AIInput(page, "Password", search_text="Password", element_type="input")
        self.login_button = AIButton(page, "Login", search_text="Login")
```

## Когда использовать agent-browser

✅ **Используйте когда:**
- Нет доступа к коду приложения для добавления data-testid
- Нужна быстрая разработка тестов
- Элементы часто меняются, но текст остается
- Нужна отладка структуры страницы

❌ **Не используйте когда:**
- Критична производительность
- Нет Node.js в окружении
- Нужна полная совместимость с Playwright locators
- Элементы не имеют уникального текста

## Следующие шаги

- Прочитайте полную документацию: [AGENT_BROWSER_INTEGRATION.md](./AGENT_BROWSER_INTEGRATION.md)
- Посмотрите примеры: [examples/agent_browser_example.py](../examples/agent_browser_example.py)
- Официальная документация: https://agent-browser.dev/
