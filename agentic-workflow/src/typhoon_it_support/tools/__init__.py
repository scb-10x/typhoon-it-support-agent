"""Tools available to the agents."""

from .basic_tools import get_current_time
from .document_search import (
    search_all_documents,
    search_it_policy,
    search_troubleshooting_guide,
)
from .ticket_tools import (
    add_tags_to_ticket,
    add_ticket_comment,
    assign_ticket,
    create_ticket,
    delete_ticket,
    get_my_open_tickets,
    get_ticket,
    search_tickets,
    set_ticket_category,
    set_ticket_due_date,
    update_ticket_priority,
    update_ticket_status,
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
