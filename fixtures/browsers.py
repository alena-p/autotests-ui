import allure
import pytest
from playwright.sync_api import Playwright, Page
from _pytest.fixtures import SubRequest
from pages.authentication.registration_page import RegistrationPage


@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    yield context.new_page()

    context.tracing.stop(path=f"./tracing/{request.node.name}.zip")
    browser.close()

    allure.attach.file(source=f"./tracing/{request.node.name}.zip", name="tracing", extension="zip")


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

@pytest.fixture(scope="function")
def chromium_page_with_state(request: SubRequest, initialize_browser_state, playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-context.json")
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    yield context.new_page()

    context.tracing.stop(path=f"./tracing/{request.node.name}.zip")
    browser.close()

    allure.attach.file(source=f"./tracing/{request.node.name}.zip", name="tracing", extension="zip")
