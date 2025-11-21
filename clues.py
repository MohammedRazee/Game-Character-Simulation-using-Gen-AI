# clues.py

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Clue:
    """Represents a single clue extracted from a suspect conversation."""
    id: int
    source: str  # e.g. suspect name: "Kabir Rao"
    summary: str  # short, human-readable note


@dataclass
class Notebook:
    """Stores and formats all clues discovered by the player."""
    clues: List[Clue] = field(default_factory=list)

    def add_clue(self, source: str, summary: str) -> Optional[Clue]:
        """Add a new clue if it's non-empty and not already present."""
        if not summary:
            return None

        summary = summary.strip()
        if not summary:
            return None

        # Avoid duplicates based on (source, summary)
        for c in self.clues:
            if c.source == source and c.summary.lower() == summary.lower():
                # Already have this clue
                return None

        clue = Clue(id=len(self.clues) + 1, source=source, summary=summary)
        self.clues.append(clue)
        return clue

    def is_empty(self) -> bool:
        return len(self.clues) == 0

    def format_notes(self) -> str:
        """Return a nicely formatted notebook view to print in the console."""
        if not self.clues:
            return "\n[Notes] You have no clues recorded yet. Keep interrogating.\n"

        lines = ["\n=== Detective Notebook ==="]
        for c in self.clues:
            lines.append(f"{c.id}. ({c.source}) {c.summary}")
        lines.append("==========================\n")
        return "\n".join(lines)
