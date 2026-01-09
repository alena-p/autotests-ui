import pytest
from _pytest.fixtures import SubRequest
from playwright.sync_api import Playwright
from pages.authentication.registration_page import RegistrationPage
from tools.playwright.page import initialize_playwright_page
from config import settings
from tools.routes import AppRoute


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(base_url=settings.get_base_url())
    page = context.new_page()

    registration_page = RegistrationPage(page=page)
    registration_page.visit(AppRoute.REGISTRATION)
    registration_page.registration_form.fill(
        email=settings.test_user.email,
        username=settings.test_user.username,
        password=settings.test_user.password
    )
    registration_page.click_registration_button()

    context.storage_state(path=settings.browser_state_file)
    browser.close()

@pytest.fixture(params=settings.browsers)
def page(request: SubRequest, playwright: Playwright):
    yield from initialize_playwright_page(
        playwright=playwright,
        browser_type=request.param,
        test_name=request.node.name
    )

@pytest.fixture(scope="function", params=settings.browsers)
def page_with_state(request: SubRequest, playwright: Playwright, initialize_browser_state):
    yield from initialize_playwright_page(
        playwright=playwright,
        test_name=request.node.name,
        browser_type=request.param,
        storage_state=settings.browser_state_file
    )
