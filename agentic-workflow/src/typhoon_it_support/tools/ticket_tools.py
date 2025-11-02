"""Ticket handling tools for IT support system."""

import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

import requests
from langchain_core.tools import tool

from .ticket_storage import get_storage


class TicketPriority(str, Enum):
    """Ticket priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(str, Enum):
    """Ticket status values."""

    NEW = "new"
    OPEN = "open"
    PENDING = "pending"
    SOLVED = "solved"
    CLOSED = "closed"


class TicketCategory(str, Enum):
    """Ticket categories."""

    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    ACCOUNT_ACCESS = "account_access"
    EMAIL = "email"
    PRINTER = "printer"
    VPN = "vpn"
    SECURITY = "security"
    OTHER = "other"


# SLA targets in minutes based on priority
SLA_TARGETS = {
    "urgent": {"first_response": 15, "resolution": 240},  # 15 min, 4 hours
    "high": {"first_response": 60, "resolution": 480},  # 1 hour, 8 hours
    "normal": {"first_response": 240, "resolution": 1440},  # 4 hours, 24 hours
    "low": {"first_response": 480, "resolution": 2880},  # 8 hours, 48 hours
}

# Available agents
AVAILABLE_AGENTS = [
    {
        "id": "agent_1",
        "name": "น้องเทค (IT Support)",
        "email": "techsupport@bluewave-tech.co.th",
    },
    {"id": "agent_2", "name": "พี่แอดมิน (Admin)", "email": "admin@bluewave-tech.co.th"},
    {"id": "agent_3", "name": "พี่เน็ต (Network)", "email": "network@bluewave-tech.co.th"},
    {
        "id": "agent_4",
        "name": "พี่ซีเคียว (Security)",
        "email": "security@bluewave-tech.co.th",
    },
]


# Mock ticketing system configuration - replace with real API credentials if using external system
TICKET_API_SUBDOMAIN = os.getenv("TICKET_API_SUBDOMAIN", "your-subdomain")
TICKET_API_EMAIL = os.getenv("TICKET_API_EMAIL", "support@company.com")
TICKET_API_TOKEN = os.getenv("TICKET_API_TOKEN", "your-api-token")
TICKET_API_BASE_URL = f"https://{TICKET_API_SUBDOMAIN}.ticketsystem.com/api/v2"


# JSONL-based storage (persisted to disk)
def _get_tickets() -> Dict[int, Dict]:
    """Get all tickets from storage."""
    return get_storage().load_all_tickets()


def _get_ticket(ticket_id: int) -> Optional[Dict]:
    """Get a single ticket from storage."""
    return get_storage().get_ticket(ticket_id)


def _save_ticket(ticket: Dict) -> None:
    """Save a ticket to storage."""
    get_storage().save_ticket(ticket)


def _delete_ticket(ticket_id: int) -> bool:
    """Delete a ticket from storage."""
    return get_storage().delete_ticket(ticket_id)


def _get_next_ticket_id() -> int:
    """Get the next available ticket ID."""
    return get_storage().get_next_id()


# Legacy compatibility - these are now backed by JSONL
# Note: These are kept for backward compatibility with init_demo_tickets.py
# but should be accessed as properties that return current state
class _TicketsAccessor:
    """Accessor for backward compatibility with old _mock_tickets code."""

    @staticmethod
    def clear():
        """Clear all tickets from storage."""
        get_storage().clear()

    def __getitem__(self, key):
        """Get a ticket by ID."""
        return _get_ticket(key)

    def __setitem__(self, key, value):
        """Set a ticket by ID."""
        _save_ticket(value)

    def __len__(self):
        """Get number of tickets."""
        return len(_get_tickets())

    def items(self):
        """Get all tickets as items."""
        return _get_tickets().items()

    def values(self):
        """Get all ticket values."""
        return _get_tickets().values()

    def keys(self):
        """Get all ticket IDs."""
        return _get_tickets().keys()

    def get(self, key, default=None):
        """Get a ticket with default."""
        ticket = _get_ticket(key)
        return ticket if ticket is not None else default


class _CounterAccessor:
    """Accessor for backward compatibility with old _ticket_counter code."""

    def __getitem__(self, key):
        """Get counter value."""
        if key == "value":
            return _get_next_ticket_id()
        raise KeyError(key)

    def __setitem__(self, key, value):
        """Set counter value (no-op for JSONL-based storage)."""
        # Counter is derived from max ticket ID, so setting is a no-op
        pass


_mock_tickets = _TicketsAccessor()
_ticket_counter = _CounterAccessor()


def _get_api_headers() -> Dict[str, str]:
    """Get headers for ticket API requests.

    Returns:
        Dictionary of HTTP headers.
    """
    import base64

    credentials = f"{TICKET_API_EMAIL}/token:{TICKET_API_TOKEN}"
    encoded = base64.b64encode(credentials.encode()).decode()

    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
    }


def _call_ticket_api(
    endpoint: str, method: str = "GET", data: Optional[Dict] = None
) -> Dict:
    """Call ticket API (mock implementation).

    Args:
        endpoint: API endpoint path.
        method: HTTP method.
        data: Request payload.

    Returns:
        API response data.
    """
    # Mock implementation - replace with real API calls
    # For production: use requests.request(method, f"{TICKET_API_BASE_URL}{endpoint}", ...)

    if (
        "TICKET_API_TOKEN" in os.environ
        and os.getenv("TICKET_API_TOKEN") != "your-api-token"
    ):
        # Real API call
        headers = _get_api_headers()
        response = requests.request(
            method,
            f"{TICKET_API_BASE_URL}{endpoint}",
            headers=headers,
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    else:
        # Mock implementation
        return {"mock": True, "endpoint": endpoint, "method": method}


def _calculate_sla_targets(priority: str, created_at) -> Dict:
    """Calculate SLA target times based on priority.

    Args:
        priority: Ticket priority.
        created_at: Creation timestamp (str or datetime).

    Returns:
        Dictionary with SLA target times.
    """
    created = (
        datetime.fromisoformat(created_at)
        if isinstance(created_at, str)
        else created_at
    )
    targets = SLA_TARGETS.get(priority, SLA_TARGETS["normal"])

    return {
        "first_response_due": (
            created + timedelta(minutes=targets["first_response"])
        ).isoformat(),
        "resolution_due": (
            created + timedelta(minutes=targets["resolution"])
        ).isoformat(),
    }


def _check_sla_breach(
    created_at, priority: str, first_response_at=None, resolved_at=None
) -> Dict:
    """Check if SLA has been breached.

    Args:
        created_at: Creation timestamp (str or datetime).
        priority: Ticket priority.
        first_response_at: First response timestamp (str or datetime).
        resolved_at: Resolution timestamp (str or datetime).

    Returns:
        Dictionary with breach status.
    """
    created = (
        datetime.fromisoformat(created_at)
        if isinstance(created_at, str)
        else created_at
    )
    targets = SLA_TARGETS.get(priority, SLA_TARGETS["normal"])
    now = datetime.now()

    breach = {
        "first_response_breached": False,
        "resolution_breached": False,
    }

    # Check first response SLA
    first_response_due = created + timedelta(minutes=targets["first_response"])
    if first_response_at:
        first_response = (
            datetime.fromisoformat(first_response_at)
            if isinstance(first_response_at, str)
            else first_response_at
        )
        breach["first_response_breached"] = first_response > first_response_due
    else:
        breach["first_response_breached"] = now > first_response_due

    # Check resolution SLA
    resolution_due = created + timedelta(minutes=targets["resolution"])
    if resolved_at:
        resolved = (
            datetime.fromisoformat(resolved_at)
            if isinstance(resolved_at, str)
            else resolved_at
        )
        breach["resolution_breached"] = resolved > resolution_due
    else:
        breach["resolution_breached"] = now > resolution_due

    return breach


@tool
def create_ticket(
    subject: str,
    description: str,
    priority: str = "normal",
    requester_email: Optional[str] = None,
    requester_name: Optional[str] = None,
) -> str:
    """Create a new support ticket.

    Use this tool when the user wants to:
    - Report a new IT issue
    - Create a formal support request
    - Escalate an issue that needs tracking

    Args:
        subject: Brief summary of the issue (required).
        description: Detailed description of the problem (required).
        priority: Ticket priority - "low", "normal", "high", or "urgent". Default: "normal".
        requester_email: Email of the person reporting the issue.
        requester_name: Name of the person reporting the issue.

    Returns:
        Ticket creation confirmation with ticket ID.
    """
    # Validate priority
    if priority not in [p.value for p in TicketPriority]:
        priority = "normal"

    # Get next ticket ID
    ticket_id = _get_next_ticket_id()
    created_at = datetime.now().isoformat()

    # Calculate SLA targets
    sla_targets = _calculate_sla_targets(priority, created_at)

    ticket = {
        "id": ticket_id,
        "subject": subject,
        "description": description,
        "priority": priority,
        "status": "new",
        "requester_email": requester_email or "unknown@company.com",
        "requester_name": requester_name or "Unknown User",
        "created_at": created_at,
        "updated_at": created_at,
        "comments": [],
        "assignee_id": None,
        "assignee_name": None,
        "tags": [],
        "category": "other",
        "due_date": None,
        "first_response_at": None,
        "resolved_at": None,
        "sla_first_response_due": sla_targets["first_response_due"],
        "sla_resolution_due": sla_targets["resolution_due"],
        "sla_breach": _check_sla_breach(created_at, priority),
        "history": [
            {
                "timestamp": created_at,
                "action": "created",
                "actor": requester_name or "System",
                "changes": {"status": "new", "priority": priority},
            }
        ],
    }

    # Save to storage
    _save_ticket(ticket)

    result = f"""✅ Ticket Created Successfully!

**Ticket ID**: #{ticket_id}
**Subject**: {subject}
**Priority**: {priority.upper()}
**Status**: NEW
**Requester**: {requester_name or "Unknown"} ({requester_email or "unknown@company.com"})

The ticket has been created and assigned to the IT support team.
You will receive updates via email at {requester_email or "your registered email"}.

Reference this ticket ID (#${ticket_id}) for any follow-ups."""

    return result


@tool
def get_ticket(ticket_id: int) -> str:
    """Retrieve details of an existing ticket.

    Use this tool to:
    - Check the status of a ticket
    - View ticket details and history
    - See what updates have been made

    Args:
        ticket_id: The ID of the ticket to retrieve.

    Returns:
        Ticket details including status, description, and comments.
    """
    # Get ticket from storage
    ticket = _get_ticket(ticket_id)

    if ticket:
        # Format comments
        comments_text = ""
        if ticket["comments"]:
            comments_text = "\n\n**Comments/Updates:**\n"
            for i, comment in enumerate(ticket["comments"], 1):
                comments_text += f"\n{i}. [{comment['created_at']}] {comment['author']}:\n   {comment['body']}\n"

        result = f"""**Ticket Details - #{ticket_id}**

**Subject**: {ticket["subject"]}
**Status**: {ticket["status"].upper()}
**Priority**: {ticket["priority"].upper()}
**Requester**: {ticket["requester_name"]} ({ticket["requester_email"]})
**Created**: {ticket["created_at"]}
**Last Updated**: {ticket["updated_at"]}

**Description**:
{ticket["description"]}
{comments_text}"""

        return result

    return (
        f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."
    )


@tool
def update_ticket_status(
    ticket_id: int, status: str, comment: Optional[str] = None
) -> str:
    """Update the status of an existing ticket.

    Use this tool to:
    - Mark a ticket as solved
    - Change ticket status (open, pending, solved, closed)
    - Add a comment when updating status

    Args:
        ticket_id: The ID of the ticket to update.
        status: New status - "new", "open", "pending", "solved", or "closed".
        comment: Optional comment to add with the status update.

    Returns:
        Confirmation of the status update.
    """
    # Validate status
    if status not in [s.value for s in TicketStatus]:
        return f"❌ Invalid status '{status}'. Valid options: new, open, pending, solved, closed"

    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Update ticket
    # ticket already loaded above
    old_status = ticket["status"]
    now = datetime.now().isoformat()
    ticket["status"] = status
    ticket["updated_at"] = now

    # Update SLA tracking
    if status == "solved" or status == "closed":
        if not ticket.get("resolved_at"):
            ticket["resolved_at"] = now

    # Update SLA breach status
    ticket["sla_breach"] = _check_sla_breach(
        ticket["created_at"],
        ticket["priority"],
        ticket.get("first_response_at"),
        ticket.get("resolved_at"),
    )

    # Add comment if provided
    if comment:
        # Track first response time
        if not ticket.get("first_response_at") and len(ticket["comments"]) == 0:
            ticket["first_response_at"] = now

        ticket["comments"].append(
            {
                "author": "IT Support Agent",
                "body": comment,
                "public": True,
                "created_at": now,
            }
        )

    # Add to history
    ticket["history"].append(
        {
            "timestamp": now,
            "action": "status_changed",
            "actor": "IT Support Agent",
            "changes": {"status": {"old": old_status, "new": status}},
        }
    )

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Ticket Status Updated!

**Ticket ID**: #{ticket_id}
**Previous Status**: {old_status.upper()}
**New Status**: {status.upper()}
**Updated**: {ticket["updated_at"]}
"""

    if comment:
        result += f"\n**Comment Added**:\n{comment}"

    return result


@tool
def add_ticket_comment(ticket_id: int, comment: str, is_public: bool = True) -> str:
    """Add a comment to an existing ticket.

    Use this tool to:
    - Provide updates to the user
    - Ask for more information
    - Document troubleshooting steps taken
    - Communicate status changes

    Args:
        ticket_id: The ID of the ticket.
        comment: The comment text to add.
        is_public: Whether the comment is visible to the requester (default: True).

    Returns:
        Confirmation that the comment was added.
    """
    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Add comment
    # ticket already loaded above
    now = datetime.now().isoformat()

    # Track first response time
    if not ticket.get("first_response_at") and len(ticket["comments"]) == 0:
        ticket["first_response_at"] = now
        # Update SLA breach status
        ticket["sla_breach"] = _check_sla_breach(
            ticket["created_at"],
            ticket["priority"],
            ticket.get("first_response_at"),
            ticket.get("resolved_at"),
        )

    ticket["comments"].append(
        {
            "author": "IT Support Agent",
            "body": comment,
            "public": is_public,
            "created_at": now,
        }
    )
    ticket["updated_at"] = now

    # Add to history
    ticket["history"].append(
        {
            "timestamp": now,
            "action": "comment_added",
            "actor": "IT Support Agent",
            "changes": {
                "comment": {
                    "public": is_public,
                    "preview": comment[:50] + "..." if len(comment) > 50 else comment,
                }
            },
        }
    )

    visibility = "Public" if is_public else "Internal"

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Comment Added to Ticket!

**Ticket ID**: #{ticket_id}
**Visibility**: {visibility}
**Added**: {now}

**Comment**:
{comment}

The requester {"will" if is_public else "will NOT"} be notified of this update."""

    return result


@tool
def update_ticket_priority(ticket_id: int, priority: str) -> str:
    """Update the priority level of a ticket.

    Use this tool when:
    - Issue severity changes
    - Need to escalate or de-escalate urgency
    - Business impact assessment changes

    Args:
        ticket_id: The ID of the ticket.
        priority: New priority level - "low", "normal", "high", or "urgent".

    Returns:
        Confirmation of the priority update.
    """
    # Validate priority
    if priority not in [p.value for p in TicketPriority]:
        return f"❌ Invalid priority '{priority}'. Valid options: low, normal, high, urgent"

    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Update priority
    # ticket already loaded above
    old_priority = ticket["priority"]
    now = datetime.now().isoformat()
    ticket["priority"] = priority
    ticket["updated_at"] = now

    # Recalculate SLA targets based on new priority
    sla_targets = _calculate_sla_targets(priority, ticket["created_at"])
    ticket["sla_first_response_due"] = sla_targets["first_response_due"]
    ticket["sla_resolution_due"] = sla_targets["resolution_due"]

    # Update SLA breach status
    ticket["sla_breach"] = _check_sla_breach(
        ticket["created_at"],
        priority,
        ticket.get("first_response_at"),
        ticket.get("resolved_at"),
    )

    # Add automatic comment
    ticket["comments"].append(
        {
            "author": "IT Support System",
            "body": f"Priority changed from {old_priority.upper()} to {priority.upper()}",
            "public": False,
            "created_at": now,
        }
    )

    # Add to history
    ticket["history"].append(
        {
            "timestamp": now,
            "action": "priority_changed",
            "actor": "IT Support System",
            "changes": {"priority": {"old": old_priority, "new": priority}},
        }
    )

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Ticket Priority Updated!

**Ticket ID**: #{ticket_id}
**Previous Priority**: {old_priority.upper()}
**New Priority**: {priority.upper()}
**Updated**: {ticket["updated_at"]}

Priority change has been logged and relevant teams have been notified."""

    return result


@tool
def search_tickets(query: str, status: Optional[str] = None, limit: int = 5) -> str:
    """Search for tickets by subject or description.

    Use this tool to:
    - Find related tickets
    - Check if similar issues exist
    - Look up tickets by keywords

    Args:
        query: Search keywords.
        status: Optional status filter (new, open, pending, solved, closed).
        limit: Maximum number of results to return (default: 5).

    Returns:
        List of matching tickets.
    """
    query_lower = query.lower()
    results = []

    for ticket_id, ticket in _get_tickets().items():
        # Filter by status if provided
        if status and ticket["status"] != status:
            continue

        # Search in subject and description
        if (
            query_lower in ticket["subject"].lower()
            or query_lower in ticket["description"].lower()
        ):
            results.append(ticket)

        if len(results) >= limit:
            break

    if not results:
        filter_text = f" with status '{status}'" if status else ""
        return f"No tickets found matching '{query}'{filter_text}."

    # Format results
    output = f"**Found {len(results)} ticket(s) matching '{query}':**\n\n"

    for ticket in results:
        output += f"""**#{ticket["id"]}** - {ticket["subject"]}
  Status: {ticket["status"].upper()} | Priority: {ticket["priority"].upper()}
  Created: {ticket["created_at"]}
  Requester: {ticket["requester_name"]}

"""

    return output


@tool
def get_my_open_tickets(limit: int = 10) -> str:
    """Get a list of currently open tickets assigned to you.

    Use this tool to:
    - Check your current workload
    - Review pending tickets
    - Find tickets that need attention

    Args:
        limit: Maximum number of tickets to return (default: 10).

    Returns:
        List of open tickets.
    """
    open_tickets = [
        ticket
        for ticket in _get_tickets().values()
        if ticket["status"] in ["new", "open", "pending"]
    ]

    if not open_tickets:
        return "✅ No open tickets found. All tickets are either solved or closed."

    # Sort by priority (urgent first) and creation date (oldest first)
    priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
    open_tickets.sort(
        key=lambda t: (priority_order.get(t["priority"], 2), t["created_at"])
    )

    # Limit results
    open_tickets = open_tickets[:limit]

    # Format output
    output = f"**Open Tickets ({len(open_tickets)}):**\n\n"

    for ticket in open_tickets:
        output += f"""**#{ticket["id"]}** - {ticket["subject"]}
  Status: {ticket["status"].upper()} | Priority: {ticket["priority"].upper()}
  Created: {ticket["created_at"]}
  Requester: {ticket["requester_name"]} ({ticket["requester_email"]})

"""

    return output


@tool
def assign_ticket(ticket_id: int, assignee_id: str) -> str:
    """Assign a ticket to a specific agent.

    Use this tool to:
    - Assign tickets to specialized agents
    - Distribute workload among team members
    - Route tickets to the appropriate person

    Args:
        ticket_id: The ID of the ticket to assign.
        assignee_id: The ID of the agent to assign (agent_1, agent_2, agent_3, agent_4).

    Returns:
        Confirmation of the assignment.
    """
    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Find agent
    agent = next((a for a in AVAILABLE_AGENTS if a["id"] == assignee_id), None)
    if not agent:
        available = ", ".join([a["id"] for a in AVAILABLE_AGENTS])
        return f"❌ Invalid assignee ID. Available agents: {available}"

    # Assign ticket
    # ticket already loaded above
    old_assignee = ticket.get("assignee_name")
    ticket["assignee_id"] = agent["id"]
    ticket["assignee_name"] = agent["name"]
    ticket["updated_at"] = datetime.now().isoformat()

    # Add to history
    ticket["history"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "action": "assigned",
            "actor": "IT Support System",
            "changes": {
                "assignee": {"old": old_assignee, "new": agent["name"]},
            },
        }
    )

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Ticket Assigned Successfully!

**Ticket ID**: #{ticket_id}
**Assigned To**: {agent["name"]} ({agent["email"]})
**Previous Assignee**: {old_assignee or "Unassigned"}

The assignee will be notified about this ticket."""

    return result


@tool
def add_tags_to_ticket(ticket_id: int, tags: List[str]) -> str:
    """Add tags to a ticket for better organization.

    Use this tool to:
    - Categorize tickets
    - Add relevant keywords
    - Improve searchability

    Args:
        ticket_id: The ID of the ticket.
        tags: List of tags to add (e.g., ["wifi", "network", "urgent"]).

    Returns:
        Confirmation with updated tags.
    """
    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Add tags (avoid duplicates)
    # ticket already loaded above
    existing_tags = set(ticket.get("tags", []))
    new_tags = [tag.lower() for tag in tags if tag.lower() not in existing_tags]

    if not new_tags:
        return f"ℹ️ All tags already exist on ticket #{ticket_id}."

    ticket["tags"].extend(new_tags)
    ticket["updated_at"] = datetime.now().isoformat()

    # Add to history
    ticket["history"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "action": "tags_added",
            "actor": "IT Support System",
            "changes": {"tags_added": new_tags},
        }
    )

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Tags Added Successfully!

**Ticket ID**: #{ticket_id}
**New Tags**: {", ".join(new_tags)}
**All Tags**: {", ".join(ticket["tags"])}

Tags have been updated for better organization."""

    return result


@tool
def set_ticket_category(ticket_id: int, category: str) -> str:
    """Set the category for a ticket.

    Use this tool to:
    - Categorize tickets by type
    - Route to specialized teams
    - Generate category-based reports

    Args:
        ticket_id: The ID of the ticket.
        category: Category (hardware, software, network, account_access, email, printer, vpn, security, other).

    Returns:
        Confirmation with the updated category.
    """
    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Validate category
    if category not in [c.value for c in TicketCategory]:
        valid_categories = ", ".join([c.value for c in TicketCategory])
        return f"❌ Invalid category. Valid options: {valid_categories}"

    # Set category
    # ticket already loaded above
    old_category = ticket.get("category", "other")
    ticket["category"] = category
    ticket["updated_at"] = datetime.now().isoformat()

    # Add to history
    ticket["history"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "action": "category_changed",
            "actor": "IT Support System",
            "changes": {"category": {"old": old_category, "new": category}},
        }
    )

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Category Updated Successfully!

**Ticket ID**: #{ticket_id}
**Previous Category**: {old_category}
**New Category**: {category}

Category has been updated for better tracking."""

    return result


@tool
def set_ticket_due_date(ticket_id: int, due_date: str) -> str:
    """Set a due date for a ticket.

    Use this tool to:
    - Set deadlines for ticket resolution
    - Prioritize work
    - Track time-sensitive issues

    Args:
        ticket_id: The ID of the ticket.
        due_date: Due date in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS).

    Returns:
        Confirmation with the due date.
    """
    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Set due date
    # ticket already loaded above
    old_due_date = ticket.get("due_date")
    ticket["due_date"] = due_date
    ticket["updated_at"] = datetime.now().isoformat()

    # Add to history
    ticket["history"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "action": "due_date_set",
            "actor": "IT Support System",
            "changes": {"due_date": {"old": old_due_date, "new": due_date}},
        }
    )

    # Save updated ticket
    _save_ticket(ticket)

    result = f"""✅ Due Date Set Successfully!

**Ticket ID**: #{ticket_id}
**Due Date**: {due_date}
**Previous Due Date**: {old_due_date or "Not set"}

Due date has been set for this ticket."""

    return result


@tool
def delete_ticket(ticket_id: int) -> str:
    """Delete a ticket from the system.

    Use this tool when:
    - A ticket was created by mistake
    - A ticket is a duplicate
    - User explicitly requests ticket deletion

    WARNING: This action cannot be undone. Use with caution.

    Args:
        ticket_id: The ID of the ticket to delete.

    Returns:
        Confirmation of deletion.
    """
    # Check if ticket exists
    ticket = _get_ticket(ticket_id)
    if not ticket:
        return f"❌ Ticket #{ticket_id} not found. Please verify the ticket ID and try again."

    # Store ticket info before deletion
    subject = ticket["subject"]

    # Delete ticket from storage
    success = _delete_ticket(ticket_id)

    if not success:
        return f"❌ Failed to delete ticket #{ticket_id}. Please try again."

    result = f"""✅ Ticket Deleted Successfully!

**Ticket ID**: #{ticket_id}
**Subject**: {subject}

The ticket has been permanently deleted from the system.
This action cannot be undone."""

    return result


def get_available_agents() -> List[Dict]:
    """Get list of available agents for assignment.

    Returns:
        List of agent dictionaries.
    """
    return AVAILABLE_AGENTS
