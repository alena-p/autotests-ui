"""Parser for agent-browser snapshot output."""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass

from tools.logger import get_logger

logger = get_logger("SNAPSHOT_PARSER")


@dataclass
class SnapshotElement:
    """Represents an element from snapshot."""
    ref: str
    element_type: str
    text: Optional[str] = None
    role: Optional[str] = None
    attributes: Dict[str, str] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


class SnapshotParser:
    """Parser for agent-browser snapshot accessibility tree."""

    # Pattern to match snapshot lines like: "- heading "Example Domain" [ref=e1]"
    ELEMENT_PATTERN = re.compile(
        r'^[\s-]*(\w+)\s+"([^"]*)"\s+\[ref=(\w+)\]'
    )

    def parse(self, snapshot_text: str) -> List[SnapshotElement]:
        """
        Parse snapshot text into list of elements.
        
        Args:
            snapshot_text: Raw snapshot output from agent-browser
            
        Returns:
            List of SnapshotElement objects
        """
        elements = []
        lines = snapshot_text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = self.ELEMENT_PATTERN.match(line)
            if match:
                element_type = match.group(1)
                text = match.group(2) if match.group(2) else None
                ref = f"@{match.group(3)}"

                element = SnapshotElement(
                    ref=ref,
                    element_type=element_type,
                    text=text
                )
                elements.append(element)
                logger.debug(f"Parsed element: {ref} - {element_type} - {text}")

        return elements

    def find_by_text(self, snapshot_text: str, search_text: str, partial: bool = True) -> Optional[SnapshotElement]:
        """
        Find element by text content.
        
        Args:
            snapshot_text: Raw snapshot output
            search_text: Text to search for
            partial: If True, matches partial text
            
        Returns:
            SnapshotElement if found, None otherwise
        """
        elements = self.parse(snapshot_text)
        
        for element in elements:
            if element.text:
                if partial and search_text.lower() in element.text.lower():
                    return element
                elif not partial and element.text == search_text:
                    return element

        return None

    def find_by_type(self, snapshot_text: str, element_type: str) -> List[SnapshotElement]:
        """
        Find all elements of a specific type.
        
        Args:
            snapshot_text: Raw snapshot output
            element_type: Type to search for (e.g., "button", "input", "link")
            
        Returns:
            List of matching SnapshotElement objects
        """
        elements = self.parse(snapshot_text)
        return [e for e in elements if e.element_type.lower() == element_type.lower()]

    def find_by_ref(self, snapshot_text: str, ref: str) -> Optional[SnapshotElement]:
        """
        Find element by ref.
        
        Args:
            snapshot_text: Raw snapshot output
            ref: Element ref (e.g., "@e1")
            
        Returns:
            SnapshotElement if found, None otherwise
        """
        elements = self.parse(snapshot_text)
        for element in elements:
            if element.ref == ref:
                return element
        return None

    def get_all_refs(self, snapshot_text: str) -> List[str]:
        """
        Get all refs from snapshot.
        
        Args:
            snapshot_text: Raw snapshot output
            
        Returns:
            List of all refs
        """
        elements = self.parse(snapshot_text)
        return [e.ref for e in elements]
