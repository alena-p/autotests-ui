"""
Minimal conftest for examples directory.

This conftest provides only the essential fixtures needed for examples
without loading the full project configuration.
"""

import pytest
from playwright.sync_api import Playwright, Page


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    """Provide Playwright instance."""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture
def page(playwright: Playwright) -> Page:
    """
    Provide a Playwright page for testing.
    
    This is a minimal implementation that doesn't require project configuration.
    """
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    browser.close()
