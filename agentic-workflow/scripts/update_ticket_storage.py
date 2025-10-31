#!/usr/bin/env python3
"""Script to update ticket_tools.py to use JSONL storage."""

import re
from pathlib import Path

TICKET_TOOLS_PATH = Path(__file__).parent.parent / "src" / "typhoon_it_support" / "tools" / "ticket_tools.py"

def update_ticket_tools():
    """Update ticket_tools.py to use storage functions."""
    
    with open(TICKET_TOOLS_PATH, 'r') as f:
        content = f.read()
    
    # Pattern 1: Replace _mock_tickets[ticket_id] access with _get_ticket and later save
    # We need to be careful here as we'll need to save after modifications
    
    # Pattern 2: Replace _mock_tickets.items() and .values()
    content = re.sub(r'_mock_tickets\.items\(\)', r'_get_tickets().items()', content)
    content = re.sub(r'_mock_tickets\.values\(\)', r'_get_tickets().values()', content)
    
    # Pattern 3: Update get_ticket function
    content = re.sub(
        r'# Check mock storage\s+if ticket_id in _mock_tickets:\s+ticket = _mock_tickets\[ticket_id\]',
        r'# Get ticket from storage\n    ticket = _get_ticket(ticket_id)\n    if ticket:',
        content,
        flags=re.DOTALL
    )
    
    with open(TICKET_TOOLS_PATH, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated {TICKET_TOOLS_PATH}")

if __name__ == "__main__":
    update_ticket_tools()


