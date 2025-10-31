"""API request and response models."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """User information model."""
    
    employee_id: str = Field(..., description="Employee ID")
    email: str = Field(..., description="User email")
    full_name_th: str = Field(..., description="Full name in Thai")
    full_name_en: str = Field(..., description="Full name in English")
    nickname: str = Field(..., description="Nickname")
    department: str = Field(..., description="Department")
    position: str = Field(..., description="Job position")
    phone: str = Field(..., description="Phone number")
    office_location: str = Field(..., description="Office location")
    manager: str = Field(..., description="Manager name")
    joined_date: str = Field(..., description="Date joined company")


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    stream_events: bool = Field(True, description="Enable workflow event streaming")


class ChatResponse(BaseModel):
    """Chat response model."""

    message: str = Field(..., description="Assistant's response")
    session_id: str = Field(..., description="Session ID")
    iteration: int = Field(..., description="Current iteration count")
    next_action: str = Field(..., description="Next action (continue, end, escalate)")


class WorkflowEventResponse(BaseModel):
    """Workflow event response model."""
    
    type: str = Field(..., description="Event type")
    timestamp: str = Field(..., description="Event timestamp")
    node_name: Optional[str] = Field(None, description="Node name if applicable")
    tool_name: Optional[str] = Field(None, description="Tool name if applicable")
    message: Optional[str] = Field(None, description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional event data")
    error: Optional[str] = Field(None, description="Error message if applicable")
    iteration: Optional[int] = Field(None, description="Current iteration")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")


class UserSessionResponse(BaseModel):
    """User session response with user info and company info."""
    
    user: UserInfo = Field(..., description="Current user information")
    company: Dict[str, str] = Field(..., description="Company information")
    session_id: Optional[str] = Field(None, description="Session ID")


class TicketCreateRequest(BaseModel):
    """Ticket creation request model."""
    
    subject: str = Field(..., description="Brief summary of the issue")
    description: str = Field(..., description="Detailed description of the problem")
    priority: str = Field("normal", description="Ticket priority (low, normal, high, urgent)")
    requester_email: Optional[str] = Field(None, description="Email of the person reporting the issue")
    requester_name: Optional[str] = Field(None, description="Name of the person reporting the issue")


class TicketUpdateRequest(BaseModel):
    """Ticket update request model."""
    
    status: Optional[str] = Field(None, description="New status")
    priority: Optional[str] = Field(None, description="New priority")
    comment: Optional[str] = Field(None, description="Comment to add")


class AssignTicketRequest(BaseModel):
    """Ticket assignment request model."""
    
    assignee_id: str = Field(..., description="Agent ID to assign the ticket to")


class AddTagsRequest(BaseModel):
    """Add tags to ticket request model."""
    
    tags: list[str] = Field(..., description="List of tags to add")


class SetCategoryRequest(BaseModel):
    """Set ticket category request model."""
    
    category: str = Field(..., description="Category to set")


class BulkUpdateRequest(BaseModel):
    """Bulk ticket update request model."""
    
    ticket_ids: list[int] = Field(..., description="List of ticket IDs to update")
    status: Optional[str] = Field(None, description="New status for all tickets")
    priority: Optional[str] = Field(None, description="New priority for all tickets")
    assignee_id: Optional[str] = Field(None, description="Agent ID to assign tickets to")
    tags: Optional[list[str]] = Field(None, description="Tags to add to all tickets")

