"""AI-powered element using agent-browser refs instead of data-testid."""

import allure
from playwright.sync_api import Page, Locator, expect
from typing import Optional

from tools.agent_browser.client import AgentBrowserClient
from tools.agent_browser.snapshot import SnapshotParser
from elements.ui_coverage import tracker
from ui_coverage_tool import ActionType, SelectorType
from tools.logger import get_logger

logger = get_logger("AI_ELEMENT")


class AIElement:
    """
    Element that uses agent-browser AI-determined refs instead of data-testid.
    
    This element gets its ref from snapshot by searching for text or element type.
    """

    def __init__(
        self,
        page: Page,
        name: str,
        search_text: Optional[str] = None,
        element_type: Optional[str] = None,
        ref: Optional[str] = None
    ):
        """
        Initialize AI element.
        
        Args:
            page: Playwright Page object
            name: Human-readable name for logging
            search_text: Text to search for in snapshot (used to find ref)
            element_type: Type of element (e.g., "button", "input", "link")
            ref: Direct ref to use (e.g., "@e1"). If provided, search_text and element_type are ignored.
        """
        self.page = page
        self.name = name
        self.search_text = search_text
        self.element_type = element_type
        self._ref: Optional[str] = ref
        self._client: Optional[AgentBrowserClient] = None
        self._snapshot_parser: Optional[SnapshotParser] = None

    @property
    def type_of(self) -> str:
        return "ai element"

    @property
    def client(self) -> AgentBrowserClient:
        """Lazy initialization of agent-browser client."""
        if self._client is None:
            self._client = AgentBrowserClient()
            # Sync with current Playwright page
            self._client.sync_with_playwright(self.page)
        return self._client

    @property
    def snapshot_parser(self) -> SnapshotParser:
        """Lazy initialization of snapshot parser."""
        if self._snapshot_parser is None:
            self._snapshot_parser = SnapshotParser()
        return self._snapshot_parser

    def _get_ref(self) -> str:
        """
        Get element ref from snapshot.
        
        Returns:
            Element ref (e.g., "@e1")
        """
        if self._ref:
            return self._ref

        if not self.search_text and not self.element_type:
            raise ValueError(
                f"AIElement '{self.name}' requires either ref, search_text, or element_type"
            )

        # Get snapshot
        snapshot_text = self.client.snapshot(interactive=True)
        
        # Find element
        element = None
        if self.search_text:
            element = self.snapshot_parser.find_by_text(snapshot_text, self.search_text)
        
        if not element and self.element_type:
            elements = self.snapshot_parser.find_by_type(snapshot_text, self.element_type)
            if elements:
                element = elements[0]  # Take first match

        if not element:
            raise ValueError(
                f"Could not find element '{self.name}' in snapshot. "
                f"Search text: {self.search_text}, Type: {self.element_type}"
            )

        self._ref = element.ref
        logger.info(f"Found ref {self._ref} for element '{self.name}'")
        return self._ref

    def get_ref(self) -> str:
        """Get or resolve element ref."""
        return self._get_ref()

    def get_locator(self) -> Locator:
        """
        Get Playwright locator using ref.
        
        Note: This converts agent-browser ref to Playwright locator.
        The ref format is @e1, @e2, etc. We need to find the element
        by its position in the accessibility tree or use a different approach.
        
        For now, we'll use agent-browser commands directly instead of Playwright locators.
        """
        # Since agent-browser uses refs that don't directly map to Playwright locators,
        # we'll use a hybrid approach: use agent-browser for interaction but
        # try to find equivalent Playwright locator for compatibility
        ref = self.get_ref()
        
        # Try to find element by accessible name or role
        if self.search_text:
            # Try to find by accessible name
            return self.page.get_by_role(self.element_type or "generic", name=self.search_text)
        
        # Fallback: use agent-browser directly
        logger.warning(
            f"Using agent-browser directly for '{self.name}'. "
            "Playwright locator may not be available."
        )
        # Return a dummy locator - actual interaction will use agent-browser
        return self.page.locator("body")  # Placeholder

    def click(self):
        """Click element using agent-browser ref."""
        step = f"Clicking {self.type_of} '{self.name}'"

        with allure.step(step):
            ref = self.get_ref()
            logger.info(f"{step} using ref {ref}")
            self.client.click(ref)

        # Track coverage if possible
        try:
            tracker.track_coverage(
                selector=f"agent-browser:{ref}",
                action_type=ActionType.CLICK,
                selector_type=SelectorType.XPATH  # Using as fallback
            )
        except Exception as e:
            logger.warning(f"Could not track coverage: {e}")

    def fill(self, value: str):
        """Fill input element using agent-browser ref."""
        step = f"Filling {self.type_of} '{self.name}' with '{value}'"

        with allure.step(step):
            ref = self.get_ref()
            logger.info(f"{step} using ref {ref}")
            self.client.fill(ref, value)

        # Track coverage if possible
        try:
            tracker.track_coverage(
                selector=f"agent-browser:{ref}",
                action_type=ActionType.FILL,
                selector_type=SelectorType.XPATH
            )
        except Exception as e:
            logger.warning(f"Could not track coverage: {e}")

    def check_visible(self):
        """Check that element is visible using snapshot."""
        step = f"Check that {self.type_of} '{self.name}' is visible"

        with allure.step(step):
            ref = self.get_ref()
            logger.info(f"{step} using ref {ref}")
            # Wait for element to appear in snapshot
            self.client.wait_for(ref, timeout=5000)

        # Track coverage if possible
        try:
            tracker.track_coverage(
                selector=f"agent-browser:{ref}",
                action_type=ActionType.VISIBLE,
                selector_type=SelectorType.XPATH
            )
        except Exception as e:
            logger.warning(f"Could not track coverage: {e}")

    def check_have_text(self, text: str):
        """Check that element has specific text."""
        step = f"Check that {self.type_of} '{self.name}' has text '{text}'"

        with allure.step(step):
            ref = self.get_ref()
            logger.info(f"{step} using ref {ref}")
            element_text = self.client.get_text(ref)
            
            if text not in element_text:
                raise AssertionError(
                    f"Element '{self.name}' text '{element_text}' does not contain '{text}'"
                )

        # Track coverage if possible
        try:
            tracker.track_coverage(
                selector=f"agent-browser:{ref}",
                action_type=ActionType.TEXT,
                selector_type=SelectorType.XPATH
            )
        except Exception as e:
            logger.warning(f"Could not track coverage: {e}")

    def get_text(self) -> str:
        """Get text content of element."""
        ref = self.get_ref()
        return self.client.get_text(ref)


class AIInput(AIElement):
    """AI-powered input element."""

    @property
    def type_of(self) -> str:
        return "ai input"

    def check_have_value(self, value: str):
        """Check that input has specific value."""
        step = f"Checking that {self.type_of} '{self.name}' has value '{value}'"

        with allure.step(step):
            ref = self.get_ref()
            logger.info(f"{step} using ref {ref}")
            # Get current value and compare
            current_value = self.client.get_text(ref)
            
            if current_value != value:
                raise AssertionError(
                    f"Input '{self.name}' value '{current_value}' does not equal '{value}'"
                )


class AIButton(AIElement):
    """AI-powered button element."""

    def __init__(self, page: Page, name: str, search_text: Optional[str] = None, ref: Optional[str] = None):
        super().__init__(page, name, search_text=search_text, element_type="button", ref=ref)

    @property
    def type_of(self) -> str:
        return "ai button"


class AILink(AIElement):
    """AI-powered link element."""

    def __init__(self, page: Page, name: str, search_text: Optional[str] = None, ref: Optional[str] = None):
        super().__init__(page, name, search_text=search_text, element_type="link", ref=ref)

    @property
    def type_of(self) -> str:
        return "ai link"
