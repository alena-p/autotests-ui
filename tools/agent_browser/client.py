"""Client wrapper for agent-browser CLI tool."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.sync_api import Page

from tools.logger import get_logger

logger = get_logger("AGENT_BROWSER")


class AgentBrowserClient:
    """Wrapper for agent-browser CLI commands."""

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize agent-browser client.
        
        Args:
            session_id: Optional session ID for isolated browser instances
        """
        self.session_id = session_id or "default"
        self._check_installation()

    def _check_installation(self):
        """Check if agent-browser is installed."""
        try:
            result = subprocess.run(
                ["agent-browser", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                logger.warning("agent-browser may not be properly installed")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning(
                "agent-browser not found. Install it with: npm install -g agent-browser"
            )

    def _run_command(self, command: list[str], input_data: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute agent-browser command.
        
        Args:
            command: List of command arguments
            input_data: Optional input data for stdin
            
        Returns:
            Command output as dictionary
        """
        full_command = ["agent-browser"] + command
        if self.session_id:
            full_command.extend(["--session", self.session_id])

        logger.debug(f"Executing: {' '.join(full_command)}")

        try:
            result = subprocess.run(
                full_command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                logger.error(f"Command failed: {result.stderr}")
                raise RuntimeError(f"agent-browser command failed: {result.stderr}")

            # Try to parse JSON output
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"output": result.stdout, "stderr": result.stderr}

        except subprocess.TimeoutExpired:
            logger.error("Command timed out")
            raise RuntimeError("agent-browser command timed out")

    def open(self, url: str) -> Dict[str, Any]:
        """
        Open a URL in the browser.
        
        Args:
            url: URL to open
            
        Returns:
            Command result
        """
        return self._run_command(["open", url])

    def snapshot(self, interactive: bool = False) -> str:
        """
        Get accessibility tree snapshot of the current page.
        
        Args:
            interactive: If True, returns interactive snapshot with refs
            
        Returns:
            Snapshot text with accessibility tree
        """
        command = ["snapshot"]
        if interactive:
            command.append("-i")
        
        result = self._run_command(command)
        return result.get("output", "")

    def click(self, ref: str) -> Dict[str, Any]:
        """
        Click an element by ref.
        
        Args:
            ref: Element ref (e.g., "@e1")
            
        Returns:
            Command result
        """
        return self._run_command(["click", ref])

    def fill(self, ref: str, text: str) -> Dict[str, Any]:
        """
        Fill an input element by ref.
        
        Args:
            ref: Element ref (e.g., "@e1")
            text: Text to fill
            
        Returns:
            Command result
        """
        return self._run_command(["fill", ref, text])

    def screenshot(self, path: str) -> Dict[str, Any]:
        """
        Take a screenshot.
        
        Args:
            path: Path to save screenshot
            
        Returns:
            Command result
        """
        return self._run_command(["screenshot", path])

    def close(self) -> Dict[str, Any]:
        """
        Close the browser.
        
        Returns:
            Command result
        """
        return self._run_command(["close"])

    def get_text(self, ref: str) -> str:
        """
        Get text content of an element by ref.
        
        Args:
            ref: Element ref (e.g., "@e1")
            
        Returns:
            Element text content
        """
        result = self._run_command(["get-text", ref])
        return result.get("output", "")

    def wait_for(self, ref: str, timeout: int = 5000) -> Dict[str, Any]:
        """
        Wait for an element to appear.
        
        Args:
            ref: Element ref (e.g., "@e1")
            timeout: Timeout in milliseconds
            
        Returns:
            Command result
        """
        return self._run_command(["wait-for", ref, "--timeout", str(timeout)])

    def sync_with_playwright(self, page: Page, url: Optional[str] = None):
        """
        Sync agent-browser session with Playwright page.
        
        This opens the same URL in agent-browser that Playwright has open.
        
        Args:
            page: Playwright Page object
            url: Optional URL to open (uses page.url if not provided)
        """
        target_url = url or page.url
        if target_url and target_url != "about:blank":
            logger.info(f"Syncing agent-browser with Playwright page: {target_url}")
            self.open(target_url)
        else:
            logger.warning("Cannot sync: page URL is not available")
