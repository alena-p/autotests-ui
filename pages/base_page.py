import allure
from playwright.sync_api import Page, expect
from typing import Pattern

from tools.logger import get_logger

logger = get_logger("BASE_PAGE")

class BasePage:
    def __init__(self, page: Page):
        self.page = page


    def visit(self, url: str):
        step = f"Opening the {url}"

        with allure.step(step):
            logger.info(step)
            self.page.goto(url, wait_until="networkidle")

    def reload(self):
        step = f"Reload page with {self.page.url}"

        with allure.step(step):
            logger.info(step)
            self.page.reload(wait_until="networkidle")

    def check_current_url(self, expected_url: Pattern[str]):
        step = f"Checking that current page have url {expected_url.pattern}"

        with allure.step(step):
            logger.info(step)
            expect(self.page).to_have_url(expected_url)