"""Tools available to the agents."""

from .basic_tools import get_current_time
from .document_search import (
    search_it_policy,
    search_troubleshooting_guide,
    search_all_documents,
)
from .ticket_tools import (
    create_ticket,
    get_ticket,
    update_ticket_status,
    add_ticket_comment,
    update_ticket_priority,
    search_tickets,
    get_my_open_tickets,
    assign_ticket,
    add_tags_to_ticket,
    set_ticket_category,
    set_ticket_due_date,
    delete_ticket,
)

__all__ = [
    # Basic tools
    "get_current_time",
    # Document search tools
    "search_it_policy",
    "search_troubleshooting_guide",
    "search_all_documents",
    # Ticket tools
    "create_ticket",
    "get_ticket",
    "update_ticket_status",
    "add_ticket_comment",
    "update_ticket_priority",
    "search_tickets",
    "get_my_open_tickets",
    "assign_ticket",
    "add_tags_to_ticket",
    "set_ticket_category",
    "set_ticket_due_date",
    "delete_ticket",
]

