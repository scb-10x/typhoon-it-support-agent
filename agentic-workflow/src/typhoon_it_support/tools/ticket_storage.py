"""JSONL-based ticket storage system."""

import json
from pathlib import Path
from threading import Lock
from typing import Dict, Optional

TICKETS_FILE = Path(__file__).parent.parent.parent.parent / "tickets.jsonl"
_storage_lock = Lock()


class TicketStorage:
    """Thread-safe JSONL-based ticket storage."""

    def __init__(self, file_path: Optional[Path] = None):
        """Initialize ticket storage.

        Args:
            file_path: Path to JSONL file. Defaults to tickets.jsonl in project root.
        """
        self.file_path = file_path or TICKETS_FILE
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize file if it doesn't exist
        if not self.file_path.exists():
            self.file_path.touch()

    def load_all_tickets(self) -> Dict[int, Dict]:
        """Load all tickets from JSONL file.

        Returns:
            Dictionary mapping ticket_id to ticket data.
        """
        tickets = {}

        with _storage_lock:
            if not self.file_path.exists() or self.file_path.stat().st_size == 0:
                return tickets

            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    ticket = json.loads(line)
                    ticket_id = ticket.get("id")
                    if ticket_id is not None:
                        tickets[ticket_id] = ticket

        return tickets

    def save_ticket(self, ticket: Dict) -> None:
        """Save or update a ticket.

        This appends the ticket to the file. For updates, the most recent
        entry takes precedence when loading.

        Args:
            ticket: Ticket dictionary to save.
        """
        with _storage_lock:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(ticket, ensure_ascii=False) + "\n")

    def delete_ticket(self, ticket_id: int) -> bool:
        """Delete a ticket from storage.

        This rewrites the entire file without the deleted ticket.

        Args:
            ticket_id: ID of ticket to delete.

        Returns:
            True if ticket was deleted, False if not found.
        """
        tickets = self.load_all_tickets()

        if ticket_id not in tickets:
            return False

        del tickets[ticket_id]

        # Rewrite file
        with _storage_lock:
            with open(self.file_path, "w", encoding="utf-8") as f:
                for ticket in tickets.values():
                    f.write(json.dumps(ticket, ensure_ascii=False) + "\n")

        return True

    def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        """Get a specific ticket.

        Args:
            ticket_id: ID of ticket to retrieve.

        Returns:
            Ticket dictionary or None if not found.
        """
        tickets = self.load_all_tickets()
        return tickets.get(ticket_id)

    def compact(self) -> int:
        """Compact the JSONL file by removing duplicate entries.

        Keeps only the most recent version of each ticket.

        Returns:
            Number of duplicate entries removed.
        """
        tickets = self.load_all_tickets()
        original_lines = 0

        # Count original lines
        with _storage_lock:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    original_lines = sum(1 for line in f if line.strip())

            # Rewrite with unique entries
            with open(self.file_path, "w", encoding="utf-8") as f:
                for ticket in tickets.values():
                    f.write(json.dumps(ticket, ensure_ascii=False) + "\n")

        removed = original_lines - len(tickets)
        return removed

    def clear(self) -> None:
        """Clear all tickets from storage."""
        with _storage_lock:
            with open(self.file_path, "w", encoding="utf-8"):
                pass  # Truncate file

    def get_next_id(self) -> int:
        """Get the next available ticket ID.

        Returns:
            Next ticket ID to use.
        """
        tickets = self.load_all_tickets()
        if not tickets:
            return 1000
        return max(tickets.keys()) + 1


# Global storage instance
_storage = TicketStorage()


def get_storage() -> TicketStorage:
    """Get the global ticket storage instance.

    Returns:
        Global TicketStorage instance.
    """
    return _storage


def reset_storage(file_path: Optional[Path] = None) -> None:
    """Reset storage to use a different file path.

    Useful for testing.

    Args:
        file_path: New file path to use.
    """
    global _storage
    _storage = TicketStorage(file_path)
