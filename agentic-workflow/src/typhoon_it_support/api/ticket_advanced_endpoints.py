"""Advanced ticket management API endpoints."""

import csv
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..tools.ticket_storage import get_storage
from ..tools.ticket_tools import (
    AVAILABLE_AGENTS,
    TicketCategory,
    TicketPriority,
    TicketStatus,
)
from .models import (
    AddTagsRequest,
    AssignTicketRequest,
    BulkUpdateRequest,
    SetCategoryRequest,
)

router = APIRouter(prefix="/tickets", tags=["tickets-advanced"])


@router.post("/{ticket_id}/assign")
async def assign_ticket_endpoint(ticket_id: int, request: AssignTicketRequest) -> dict:
    """Assign a ticket to an agent.

    Args:
        ticket_id: The ID of the ticket.
        request: Request body containing assignee_id.

    Returns:
        Updated ticket information.
    """
    if not get_storage().get_ticket(ticket_id):
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} not found")

    agent = next((a for a in AVAILABLE_AGENTS if a["id"] == request.assignee_id), None)
    if not agent:
        raise HTTPException(status_code=400, detail="Invalid assignee ID")

    ticket = get_storage().get_ticket(ticket_id)
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
            "changes": {"assignee": {"old": old_assignee, "new": agent["name"]}},
        }
    )

    # Save changes to storage
    get_storage().save_ticket(ticket)

    return {"ticket": ticket, "message": f"Ticket assigned to {agent['name']}"}


@router.post("/{ticket_id}/tags")
async def add_tags_endpoint(ticket_id: int, request: AddTagsRequest) -> dict:
    """Add tags to a ticket.

    Args:
        ticket_id: The ID of the ticket.
        request: Request body containing tags list.

    Returns:
        Updated ticket information.
    """
    if not get_storage().get_ticket(ticket_id):
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} not found")

    ticket = get_storage().get_ticket(ticket_id)
    existing_tags = set(ticket.get("tags", []))
    new_tags = [tag.lower() for tag in request.tags if tag.lower() not in existing_tags]

    if new_tags:
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

        # Save changes to storage
        get_storage().save_ticket(ticket)

    return {
        "ticket": ticket,
        "new_tags": new_tags,
        "message": f"Added {len(new_tags)} tag(s)",
    }


@router.post("/{ticket_id}/category")
async def set_category_endpoint(ticket_id: int, request: SetCategoryRequest) -> dict:
    """Set the category for a ticket.

    Args:
        ticket_id: The ID of the ticket.
        request: Request body containing category.

    Returns:
        Updated ticket information.
    """
    if not get_storage().get_ticket(ticket_id):
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} not found")

    if request.category not in [c.value for c in TicketCategory]:
        raise HTTPException(status_code=400, detail="Invalid category")

    ticket = get_storage().get_ticket(ticket_id)
    old_category = ticket.get("category", "other")
    ticket["category"] = request.category
    ticket["updated_at"] = datetime.now().isoformat()

    # Add to history
    ticket["history"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "action": "category_changed",
            "actor": "IT Support System",
            "changes": {"category": {"old": old_category, "new": request.category}},
        }
    )

    # Save changes to storage
    get_storage().save_ticket(ticket)

    return {"ticket": ticket, "message": f"Category updated to {request.category}"}


@router.get("/search/advanced")
async def advanced_search(
    query: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee_id: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    sla_breached: Optional[bool] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    limit: int = 50,
) -> dict:
    """Advanced ticket search with multiple filters.

    Args:
        query: Search keywords.
        status: Filter by status.
        priority: Filter by priority.
        assignee_id: Filter by assignee.
        category: Filter by category.
        tags: Comma-separated list of tags.
        sla_breached: Filter by SLA breach status.
        created_after: Filter by creation date (after).
        created_before: Filter by creation date (before).
        limit: Maximum results.

    Returns:
        Filtered tickets.
    """
    tickets = list(get_storage().load_all_tickets().values())

    # Apply filters
    if query:
        query_lower = query.lower()
        tickets = [
            t
            for t in tickets
            if query_lower in t["subject"].lower()
            or query_lower in t["description"].lower()
        ]

    if status:
        tickets = [t for t in tickets if t["status"] == status]

    if priority:
        tickets = [t for t in tickets if t["priority"] == priority]

    if assignee_id:
        tickets = [t for t in tickets if t.get("assignee_id") == assignee_id]

    if category:
        tickets = [t for t in tickets if t.get("category") == category]

    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        tickets = [
            t for t in tickets if any(tag in t.get("tags", []) for tag in tag_list)
        ]

    if sla_breached is not None:
        tickets = [
            t
            for t in tickets
            if t.get("sla_breach", {}).get("resolution_breached") == sla_breached
        ]

    if created_after:
        tickets = [t for t in tickets if t["created_at"] >= created_after]

    if created_before:
        tickets = [t for t in tickets if t["created_at"] <= created_before]

    # Sort by creation date (newest first)
    tickets.sort(key=lambda t: t["created_at"], reverse=True)

    # Limit results
    tickets = tickets[:limit]

    return {
        "tickets": tickets,
        "total": len(tickets),
        "filters": {
            "query": query,
            "status": status,
            "priority": priority,
            "assignee_id": assignee_id,
            "category": category,
            "tags": tags,
            "sla_breached": sla_breached,
        },
    }


@router.post("/bulk/update")
async def bulk_update_tickets(request: BulkUpdateRequest) -> dict:
    """Bulk update multiple tickets.

    Args:
        request: Request body containing ticket IDs and update fields.

    Returns:
        Summary of updates.
    """
    updated_count = 0
    errors = []

    for ticket_id in request.ticket_ids:
        if not get_storage().get_ticket(ticket_id):
            errors.append(f"Ticket #{ticket_id} not found")
            continue

        ticket = get_storage().get_ticket(ticket_id)
        changes = {}

        # Update status
        if request.status:
            if request.status not in [s.value for s in TicketStatus]:
                errors.append(f"Invalid status for ticket #{ticket_id}")
                continue
            old_status = ticket["status"]
            ticket["status"] = request.status
            changes["status"] = {"old": old_status, "new": request.status}

        # Update priority
        if request.priority:
            if request.priority not in [p.value for p in TicketPriority]:
                errors.append(f"Invalid priority for ticket #{ticket_id}")
                continue
            old_priority = ticket["priority"]
            ticket["priority"] = request.priority
            changes["priority"] = {"old": old_priority, "new": request.priority}

        # Update assignee
        if request.assignee_id:
            agent = next(
                (a for a in AVAILABLE_AGENTS if a["id"] == request.assignee_id), None
            )
            if not agent:
                errors.append(f"Invalid assignee for ticket #{ticket_id}")
                continue
            old_assignee = ticket.get("assignee_name")
            ticket["assignee_id"] = agent["id"]
            ticket["assignee_name"] = agent["name"]
            changes["assignee"] = {"old": old_assignee, "new": agent["name"]}

        # Add tags
        if request.tags:
            existing_tags = set(ticket.get("tags", []))
            new_tags = [
                tag.lower() for tag in request.tags if tag.lower() not in existing_tags
            ]
            if new_tags:
                ticket["tags"].extend(new_tags)
                changes["tags_added"] = new_tags

        # Update timestamp
        now = datetime.now().isoformat()
        ticket["updated_at"] = now

        # Add to history
        if changes:
            ticket["history"].append(
                {
                    "timestamp": now,
                    "action": "bulk_updated",
                    "actor": "IT Support System",
                    "changes": changes,
                }
            )
            # Save changes to storage
            get_storage().save_ticket(ticket)
            updated_count += 1

    return {
        "updated": updated_count,
        "total": len(request.ticket_ids),
        "errors": errors,
        "message": f"Successfully updated {updated_count} ticket(s)",
    }


@router.get("/export/csv")
async def export_tickets_csv(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
) -> StreamingResponse:
    """Export tickets to CSV format.

    Args:
        status: Filter by status.
        priority: Filter by priority.
        category: Filter by category.

    Returns:
        CSV file with ticket data.
    """
    tickets = list(get_storage().load_all_tickets().values())

    # Apply filters
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    if priority:
        tickets = [t for t in tickets if t["priority"] == priority]
    if category:
        tickets = [t for t in tickets if t.get("category") == category]

    # Sort by creation date
    tickets.sort(key=lambda t: t["created_at"], reverse=True)

    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(
        [
            "ID",
            "Subject",
            "Status",
            "Priority",
            "Category",
            "Assignee",
            "Requester Name",
            "Requester Email",
            "Created At",
            "Updated At",
            "Due Date",
            "First Response At",
            "Resolved At",
            "SLA First Response Breached",
            "SLA Resolution Breached",
            "Tags",
            "Description",
        ]
    )

    # Write data
    for ticket in tickets:
        writer.writerow(
            [
                ticket["id"],
                ticket["subject"],
                ticket["status"],
                ticket["priority"],
                ticket.get("category", "other"),
                ticket.get("assignee_name", "Unassigned"),
                ticket["requester_name"],
                ticket["requester_email"],
                ticket["created_at"],
                ticket["updated_at"],
                ticket.get("due_date", ""),
                ticket.get("first_response_at", ""),
                ticket.get("resolved_at", ""),
                ticket.get("sla_breach", {}).get("first_response_breached", False),
                ticket.get("sla_breach", {}).get("resolution_breached", False),
                ", ".join(ticket.get("tags", [])),
                ticket["description"],
            ]
        )

    # Return as streaming response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=tickets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        },
    )
