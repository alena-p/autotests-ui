"""
Example of using agent-browser for AI-powered element selection.

This example demonstrates how to use agent-browser instead of data-testid
for finding and interacting with elements.
"""

import pytest
from playwright.sync_api import Page

from tools.agent_browser.client import AgentBrowserClient
from tools.agent_browser.snapshot import SnapshotParser
from elements.ai_element import AIButton, AIInput, AILink, AIElement


def test_example_with_snapshot(page: Page):
    """Example: Using snapshot to understand page structure."""
    client = AgentBrowserClient()
    
    # Navigate to page
    page.goto("https://example.com")
    client.sync_with_playwright(page)
    
    # Get snapshot to see all available elements
    snapshot = client.snapshot(interactive=True)
    print("Page snapshot:")
    print(snapshot)
    
    # Parse snapshot
    parser = SnapshotParser()
    elements = parser.parse(snapshot)
    
    # Find specific elements
    link = parser.find_by_text(snapshot, "More information")
    if link:
        print(f"Found link: {link.ref} - {link.text}")
        client.click(link.ref)


def test_example_with_ai_elements(page: Page):
    """Example: Using AI elements instead of data-testid."""
    page.goto("https://example.com")
    
    # Create AI elements - they will find themselves by text
    more_info_link = AILink(page, "More information link", search_text="More information")
    
    # Use them like regular elements
    more_info_link.check_visible()
    more_info_link.click()


def test_example_hybrid_approach(page: Page):
    """
    Example: Hybrid approach - use agent-browser for discovery,
    then use Playwright for interaction.
    """
    client = AgentBrowserClient()
    parser = SnapshotParser()
    
    page.goto("https://example.com")
    client.sync_with_playwright(page)
    
    # Get snapshot to find element ref
    snapshot = client.snapshot(interactive=True)
    heading = parser.find_by_text(snapshot, "Example Domain")
    
    if heading:
        # Now use Playwright to interact with the element
        # (You would need to map ref back to Playwright locator)
        print(f"Found heading with ref: {heading.ref}")


class ExamplePageWithAI:
    """Example page object using AI elements."""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Instead of: Button(page, "login-button", "Login")
        # Use: AIButton(page, "Login", search_text="Login")
        self.login_button = AIButton(page, "Login", search_text="Login")
        
        # Instead of: Input(page, "email-input", "Email")
        # Use: AIInput(page, "Email", search_text="Email")
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
        
        # Link with direct ref (if you know it from previous snapshot)
        self.registration_link = AILink(
            page,
            "Registration link",
            search_text="Register"
        )


def test_example_page_object(page: Page):
    """Example: Using AI elements in page objects."""
    example_page = ExamplePageWithAI(page)
    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    
    # Use AI elements just like regular elements
    example_page.email_input.fill("test@example.com")
    example_page.password_input.fill("123456")
    example_page.login_button.click()
    example_page.registration_link.check_visible()


if __name__ == "__main__":
    # This is just for demonstration
    # In real tests, use pytest fixtures
    pytest.main([__file__, "-v"])
