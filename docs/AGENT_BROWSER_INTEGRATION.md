# Интеграция agent-browser

## Обзор

[agent-browser](https://agent-browser.dev/) - это инструмент для автоматизации браузера, который использует AI для определения локаторов элементов через accessibility tree с refs. Это позволяет находить элементы без необходимости в `data-testid` атрибутах.

## Установка

```bash
npm install -g agent-browser
```

Проверьте установку:
```bash
agent-browser --version
```

## Архитектура интеграции

Проект включает следующие компоненты:

1. **`tools/agent_browser/client.py`** - Обертка для agent-browser CLI
2. **`tools/agent_browser/snapshot.py`** - Парсер для snapshot (accessibility tree)
3. **`elements/ai_element.py`** - Альтернативные элементы, использующие AI-определяемые refs

## Использование

### 1. Базовое использование с snapshot

```python
from tools.agent_browser.client import AgentBrowserClient
from tools.agent_browser.snapshot import SnapshotParser

def test_with_snapshot(page: Page):
    client = AgentBrowserClient()
    parser = SnapshotParser()
    
    page.goto("https://example.com")
    client.sync_with_playwright(page)
    
    # Получить snapshot страницы
    snapshot = client.snapshot(interactive=True)
    
    # Найти элемент по тексту
    link = parser.find_by_text(snapshot, "More information")
    if link:
        client.click(link.ref)  # Использовать ref для клика
```

### 2. Использование AI элементов

Вместо обычных элементов с `data-testid`:

```python
# Старый способ
from elements.button import Button
login_button = Button(page, "login-button", "Login")

# Новый способ с AI
from elements.ai_element import AIButton
login_button = AIButton(page, "Login", search_text="Login")
```

### 3. Пример компонента с AI элементами

```python
from elements.ai_element import AIInput, AIButton

class LoginFormComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        
        # AI элементы находят себя по тексту или типу
        self.email_input = AIInput(
            page,
            "Email input",
            search_text="Email",
            element_type="input"
        )
        self.password_input = AIInput(
            page,
            "Password input",
            search_text="Password",
            element_type="input"
        )
        self.login_button = AIButton(
            page,
            "Login button",
            search_text="Login"
        )
    
    def fill(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
```

### 4. Использование прямых refs

Если вы уже знаете ref элемента из предыдущего snapshot:

```python
from elements.ai_element import AIButton

# Использовать прямой ref
button = AIButton(page, "Submit", ref="@e5")
button.click()
```

## Преимущества

1. **Не требует data-testid** - элементы находятся по тексту или типу
2. **Более устойчивые тесты** - AI понимает семантику элементов
3. **Быстрая разработка** - не нужно добавлять атрибуты в код приложения
4. **Отладка** - snapshot показывает всю структуру страницы

## Ограничения

1. **Требует установки Node.js** - agent-browser это npm пакет
2. **Дополнительная зависимость** - нужно синхронизировать Playwright и agent-browser
3. **Производительность** - snapshot может быть медленнее, чем прямые локаторы
4. **Не все команды поддерживаются** - некоторые действия могут требовать Playwright

## Гибридный подход

Можно комбинировать оба подхода:

```python
# Использовать agent-browser для поиска элементов
client = AgentBrowserClient()
snapshot = client.snapshot(interactive=True)
parser = SnapshotParser()
element = parser.find_by_text(snapshot, "Submit")

# Затем использовать Playwright для взаимодействия
# (требует маппинга ref на Playwright locator)
```

## Отладка

Для отладки используйте snapshot:

```python
client = AgentBrowserClient()
client.sync_with_playwright(page)
snapshot = client.snapshot(interactive=True)
print(snapshot)  # Показать всю структуру страницы
```

## Сравнение подходов

| Аспект | data-testid | agent-browser |
|--------|-------------|---------------|
| Требует изменения кода приложения | Да | Нет |
| Скорость | Быстро | Средне |
| Устойчивость | Высокая | Очень высокая |
| Отладка | Сложно | Легко (snapshot) |
| Зависимости | Только Playwright | Playwright + Node.js |

## Примеры

См. `examples/agent_browser_example.py` для полных примеров использования.

## Дополнительная информация

- [Документация agent-browser](https://agent-browser.dev/)
- [GitHub agent-browser](https://github.com/agent-browser/agent-browser)
