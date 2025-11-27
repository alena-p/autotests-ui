import pytest
from playwright.sync_api import Playwright
from _pytest.fixtures import SubRequest
from pages.authentication.registration_page import RegistrationPage
from tools.playwright.page import initialize_playwright_page, initialize_agentql_page


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    registration_page = RegistrationPage(page=page)
    registration_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")
    registration_page.registration_form.fill("user.name@gmail.com", "username", "password")
    registration_page.click_registration_button()

    context.storage_state(path="browser-context.json")
    browser.close()

@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright):
    yield from initialize_playwright_page(playwright=playwright, test_name=request.node.name)

@pytest.fixture(scope="function")
def chromium_page_with_state(request: SubRequest, playwright: Playwright, initialize_browser_state):
    yield from initialize_playwright_page(
        playwright=playwright,
        test_name=request.node.name,
        storage_state="browser-context.json"
    )

@pytest.fixture
def agentql_chromium_page(request: SubRequest, playwright: Playwright):
    yield from initialize_agentql_page(playwright=playwright, test_name=request.node.name)
