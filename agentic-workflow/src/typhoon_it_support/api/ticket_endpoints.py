"""Basic ticket CRUD API endpoints."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from ..tools.ticket_storage import get_storage
from ..tools.ticket_tools import (
    AVAILABLE_AGENTS,
    TicketPriority,
    TicketStatus,
    _calculate_sla_targets,
    _check_sla_breach,
)
from ..config.user_context import get_current_user
from .models import TicketCreateRequest, TicketUpdateRequest

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("")
async def list_tickets(
    status: Optional[str] = None,
    limit: int = 50
) -> dict:
    """List all tickets with optional status filter.
    
    Args:
        status: Optional status filter (new, open, pending, solved, closed).
        limit: Maximum number of tickets to return.
        
    Returns:
        List of tickets.
    """
    tickets = list(get_storage().load_all_tickets().values())
    
    # Filter by status if provided
    if status:
        if status not in [s.value for s in TicketStatus]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Valid options: {', '.join([s.value for s in TicketStatus])}"
            )
        tickets = [t for t in tickets if t["status"] == status]
    
    # Sort by creation date (newest first)
    tickets.sort(key=lambda t: t["created_at"], reverse=True)
    
    # Limit results
    tickets = tickets[:limit]
    
    return {
        "tickets": tickets,
        "total": len(tickets),
        "status_filter": status,
    }


@router.get("/agents")
async def get_agents() -> dict:
    """Get list of available agents for assignment.
    
    Returns:
        List of available agents.
    """
    return {"agents": AVAILABLE_AGENTS}


@router.get("/{ticket_id}")
async def get_ticket_detail(ticket_id: int) -> dict:
    """Get detailed information about a specific ticket.
    
    Args:
        ticket_id: The ID of the ticket.
        
    Returns:
        Ticket details.
        
    Raises:
        HTTPException: If ticket not found.
    """
    ticket = get_storage().get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} not found")
    
    return {"ticket": ticket}


@router.post("")
async def create_new_ticket(request: TicketCreateRequest) -> dict:
    """Create a new support ticket.
    
    Args:
        request: Ticket creation request.
        
    Returns:
        Created ticket information.
    """
    # Get current user if not provided
    user_profile = get_current_user()
    requester_email = request.requester_email or user_profile.email
    requester_name = request.requester_name or user_profile.display_name
    
    subject = request.subject
    description = request.description
    priority = request.priority
    
    # Validate priority
    if priority not in [p.value for p in TicketPriority]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid priority. Valid options: {', '.join([p.value for p in TicketPriority])}"
        )
    
    # Create ticket
    ticket_id = get_storage().get_next_id()
    created_at = datetime.now().isoformat()
    
    # Calculate SLA targets
    sla_targets = _calculate_sla_targets(priority, created_at)
    
    ticket = {
        "id": ticket_id,
        "subject": subject,
        "description": description,
        "priority": priority,
        "status": "new",
        "requester_email": requester_email,
        "requester_name": requester_name,
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
                "actor": requester_name,
                "changes": {"status": "new", "priority": priority},
            }
        ],
    }
    
    get_storage().save_ticket(ticket)
    
    return {
        "ticket": ticket,
        "message": f"Ticket #{ticket_id} created successfully"
    }


@router.patch("/{ticket_id}")
async def update_ticket(ticket_id: int, request: TicketUpdateRequest) -> dict:
    """Update a ticket's status, priority, or add a comment.
    
    Args:
        ticket_id: The ID of the ticket to update.
        request: Update request with status, priority, and/or comment.
        
    Returns:
        Updated ticket information.
        
    Raises:
        HTTPException: If ticket not found or invalid parameters.
    """
    if not get_storage().get_ticket(ticket_id):
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} not found")
    
    ticket = get_storage().get_ticket(ticket_id)
    changes = []
    
    # Update status
    if request.status:
        if request.status not in [s.value for s in TicketStatus]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Valid options: {', '.join([s.value for s in TicketStatus])}"
            )
        old_status = ticket["status"]
        ticket["status"] = request.status
        changes.append(f"Status changed from {old_status} to {request.status}")
        
        # Track SLA milestones
        now_str = datetime.now().isoformat()
        # First response is when ticket moves from "new" to any active status
        if request.status in ["open", "pending"] and not ticket.get("first_response_at"):
            ticket["first_response_at"] = now_str
        # Resolution is when ticket is marked as solved or closed
        elif request.status in ["solved", "closed"] and not ticket.get("resolved_at"):
            ticket["resolved_at"] = now_str
        
        # Check for SLA breach
        created_at_str = ticket["created_at"]
        created_at = datetime.fromisoformat(created_at_str) if isinstance(created_at_str, str) else created_at_str
        
        first_response_str = ticket.get("first_response_at")
        first_response = datetime.fromisoformat(first_response_str) if first_response_str and isinstance(first_response_str, str) else first_response_str
        
        resolved_str = ticket.get("resolved_at")
        resolved = datetime.fromisoformat(resolved_str) if resolved_str and isinstance(resolved_str, str) else resolved_str
        
        ticket["sla_breach"] = _check_sla_breach(
            created_at,
            ticket["priority"],
            first_response,
            resolved
        )
    
    # Update priority
    if request.priority:
        if request.priority not in [p.value for p in TicketPriority]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid priority. Valid options: {', '.join([p.value for p in TicketPriority])}"
            )
        old_priority = ticket["priority"]
        ticket["priority"] = request.priority
        changes.append(f"Priority changed from {old_priority} to {request.priority}")
    
    # Add comment
    if request.comment:
        ticket["comments"].append({
            "author": "IT Support Agent",
            "body": request.comment,
            "public": True,
            "created_at": datetime.now().isoformat(),
        })
        changes.append("Comment added")
    
    # Update timestamp
    now = datetime.now().isoformat()
    ticket["updated_at"] = now
    
    # Add to history if any changes were made
    if request.status or request.priority or request.comment:
        history_changes = {}
        if request.status:
            history_changes["status"] = {"old": old_status, "new": request.status}
        if request.priority:
            history_changes["priority"] = {"old": old_priority, "new": request.priority}
        if request.comment:
            history_changes["comment_added"] = True
        
        ticket["history"].append({
            "timestamp": now,
            "action": "updated",
            "actor": "IT Support Agent",
            "changes": history_changes,
        })
    
    # Save changes to storage
    get_storage().save_ticket(ticket)
    
    return {
        "ticket": ticket,
        "changes": changes,
        "message": f"Ticket #{ticket_id} updated successfully"
    }


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int) -> dict:
    """Delete a ticket (for demo purposes only).
    
    Args:
        ticket_id: The ID of the ticket to delete.
        
    Returns:
        Deletion confirmation.
        
    Raises:
        HTTPException: If ticket not found.
    """
    if not get_storage().get_ticket(ticket_id):
        raise HTTPException(status_code=404, detail=f"Ticket #{ticket_id} not found")
    
    get_storage().delete_ticket(ticket_id)
    
    return {
        "message": f"Ticket #{ticket_id} deleted successfully"
    }


@router.get("/stats/summary")
async def get_ticket_stats() -> dict:
    """Get summary statistics about tickets.
    
    Returns:
        Ticket statistics grouped by status and priority.
    """
    from collections import defaultdict
    
    stats = {
        "total": len(get_storage().load_all_tickets()),
        "by_status": defaultdict(int),
        "by_priority": defaultdict(int),
    }
    
    for ticket in get_storage().load_all_tickets().values():
        stats["by_status"][ticket["status"]] += 1
        stats["by_priority"][ticket["priority"]] += 1
    
    return {
        "total": stats["total"],
        "by_status": dict(stats["by_status"]),
        "by_priority": dict(stats["by_priority"]),
    }


@router.post("/demo/initialize")
async def initialize_demo_data() -> dict:
    """Initialize demo tickets for showcase (for demo purposes only).
    
    Returns:
        Confirmation with number of tickets created.
    """
    from .init_demo_tickets import initialize_demo_tickets
    
    count = initialize_demo_tickets()
    
    return {
        "message": f"Demo tickets initialized successfully",
        "count": count
    }

