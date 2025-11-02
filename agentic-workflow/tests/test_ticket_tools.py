"""Tests for ticket management tools."""


import pytest

from src.typhoon_it_support.tools.ticket_storage import get_storage, reset_storage
from src.typhoon_it_support.tools.ticket_tools import (
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


@pytest.fixture(autouse=True)
def reset_tickets(tmp_path):
    """Reset ticket storage before each test."""
    # Use a temporary file for testing
    test_file = tmp_path / "test_tickets.jsonl"
    reset_storage(test_file)
    yield
    # Cleanup
    get_storage().clear()


class TestCreateTicket:
    """Tests for ticket creation."""

    def test_create_basic_ticket(self):
        """Test creating a basic ticket."""
        result = create_ticket.invoke(
            {
                "subject": "Test Issue",
                "description": "Test description",
            }
        )

        assert "✅ Ticket Created Successfully!" in result
        assert "#1000" in result
        assert "Test Issue" in result
        assert len(get_storage().load_all_tickets()) == 1
        assert get_storage().get_ticket(1000) is not None

    def test_create_ticket_with_priority(self):
        """Test creating ticket with priority."""
        result = create_ticket.invoke(
            {
                "subject": "Urgent Issue",
                "description": "Critical bug",
                "priority": "urgent",
            }
        )

        assert "URGENT" in result
        assert get_storage().get_ticket(1000)["priority"] == "urgent"

    def test_create_ticket_with_requester_info(self):
        """Test creating ticket with requester information."""
        result = create_ticket.invoke(
            {
                "subject": "My Issue",
                "description": "Help needed",
                "requester_email": "test@example.com",
                "requester_name": "Test User",
            }
        )

        assert "test@example.com" in result
        assert "Test User" in result
        assert get_storage().get_ticket(1000)["requester_email"] == "test@example.com"

    def test_create_ticket_invalid_priority(self):
        """Test creating ticket with invalid priority defaults to normal."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
                "priority": "invalid",
            }
        )

        assert get_storage().get_ticket(1000)["priority"] == "normal"

    def test_create_multiple_tickets(self):
        """Test creating multiple tickets increments ID."""
        create_ticket.invoke({"subject": "First", "description": "First ticket"})
        create_ticket.invoke({"subject": "Second", "description": "Second ticket"})
        create_ticket.invoke({"subject": "Third", "description": "Third ticket"})

        assert len(get_storage().load_all_tickets()) == 3
        assert get_storage().get_ticket(1000) is not None
        assert get_storage().get_ticket(1001) is not None
        assert get_storage().get_ticket(1002) is not None


class TestGetTicket:
    """Tests for retrieving ticket details."""

    def test_get_existing_ticket(self):
        """Test retrieving an existing ticket."""
        create_ticket.invoke(
            {
                "subject": "Test Ticket",
                "description": "Test description",
            }
        )

        result = get_ticket.invoke({"ticket_id": 1000})

        assert "Ticket Details - #1000" in result
        assert "Test Ticket" in result
        assert "Test description" in result

    def test_get_nonexistent_ticket(self):
        """Test retrieving a non-existent ticket."""
        result = get_ticket.invoke({"ticket_id": 9999})

        assert "❌" in result
        assert "not found" in result

    def test_get_ticket_with_comments(self):
        """Test retrieving ticket with comments."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )
        add_ticket_comment.invoke(
            {
                "ticket_id": 1000,
                "comment": "This is a comment",
            }
        )

        result = get_ticket.invoke({"ticket_id": 1000})

        assert "Comments/Updates" in result
        assert "This is a comment" in result


class TestUpdateTicketStatus:
    """Tests for updating ticket status."""

    def test_update_status_to_open(self):
        """Test updating ticket status to open."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = update_ticket_status.invoke(
            {
                "ticket_id": 1000,
                "status": "open",
            }
        )

        assert "✅ Ticket Status Updated!" in result
        assert "NEW" in result
        assert "OPEN" in result
        assert get_storage().get_ticket(1000)["status"] == "open"

    def test_update_status_to_solved(self):
        """Test updating ticket status to solved."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        update_ticket_status.invoke(
            {
                "ticket_id": 1000,
                "status": "solved",
            }
        )

        assert get_storage().get_ticket(1000)["status"] == "solved"
        assert get_storage().get_ticket(1000)["resolved_at"] is not None

    def test_update_status_with_comment(self):
        """Test updating status with a comment."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = update_ticket_status.invoke(
            {
                "ticket_id": 1000,
                "status": "pending",
                "comment": "Waiting for user response",
            }
        )

        assert "Comment Added" in result
        assert "Waiting for user response" in result
        assert len(get_storage().get_ticket(1000)["comments"]) == 1

    def test_update_status_invalid(self):
        """Test updating with invalid status."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = update_ticket_status.invoke(
            {
                "ticket_id": 1000,
                "status": "invalid_status",
            }
        )

        assert "❌" in result
        assert "Invalid status" in result

    def test_update_nonexistent_ticket(self):
        """Test updating non-existent ticket."""
        result = update_ticket_status.invoke(
            {
                "ticket_id": 9999,
                "status": "open",
            }
        )

        assert "❌" in result
        assert "not found" in result


class TestAddTicketComment:
    """Tests for adding comments to tickets."""

    def test_add_public_comment(self):
        """Test adding a public comment."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = add_ticket_comment.invoke(
            {
                "ticket_id": 1000,
                "comment": "This is a public comment",
            }
        )

        assert "✅ Comment Added" in result
        assert "This is a public comment" in result
        assert get_storage().get_ticket(1000)["comments"][0]["public"] is True

    def test_add_internal_comment(self):
        """Test adding an internal comment."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = add_ticket_comment.invoke(
            {
                "ticket_id": 1000,
                "comment": "Internal note",
                "is_public": False,
            }
        )

        assert "Internal" in result
        assert get_storage().get_ticket(1000)["comments"][0]["public"] is False

    def test_add_multiple_comments(self):
        """Test adding multiple comments."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        add_ticket_comment.invoke({"ticket_id": 1000, "comment": "First comment"})
        add_ticket_comment.invoke({"ticket_id": 1000, "comment": "Second comment"})
        add_ticket_comment.invoke({"ticket_id": 1000, "comment": "Third comment"})

        assert len(get_storage().get_ticket(1000)["comments"]) == 3


class TestUpdateTicketPriority:
    """Tests for updating ticket priority."""

    def test_update_priority_to_urgent(self):
        """Test updating priority to urgent."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
                "priority": "normal",
            }
        )

        result = update_ticket_priority.invoke(
            {
                "ticket_id": 1000,
                "priority": "urgent",
            }
        )

        assert "✅ Ticket Priority Updated!" in result
        assert "NORMAL" in result
        assert "URGENT" in result
        assert get_storage().get_ticket(1000)["priority"] == "urgent"

    def test_update_priority_invalid(self):
        """Test updating with invalid priority."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = update_ticket_priority.invoke(
            {
                "ticket_id": 1000,
                "priority": "super_urgent",
            }
        )

        assert "❌" in result
        assert "Invalid priority" in result


class TestSearchTickets:
    """Tests for searching tickets."""

    def test_search_by_subject(self):
        """Test searching tickets by subject."""
        create_ticket.invoke(
            {
                "subject": "Password Reset Issue",
                "description": "Cannot reset password",
            }
        )
        create_ticket.invoke(
            {
                "subject": "WiFi Connection Problem",
                "description": "WiFi not working",
            }
        )

        result = search_tickets.invoke({"query": "password"})

        assert "Password Reset Issue" in result
        assert "WiFi" not in result

    def test_search_by_description(self):
        """Test searching tickets by description."""
        create_ticket.invoke(
            {
                "subject": "Issue A",
                "description": "Network connectivity problem",
            }
        )
        create_ticket.invoke(
            {
                "subject": "Issue B",
                "description": "Printer setup",
            }
        )

        result = search_tickets.invoke({"query": "network"})

        assert "Issue A" in result

    def test_search_with_status_filter(self):
        """Test searching with status filter."""
        create_ticket.invoke(
            {
                "subject": "Open Ticket",
                "description": "Test",
            }
        )
        update_ticket_status.invoke({"ticket_id": 1000, "status": "open"})

        create_ticket.invoke(
            {
                "subject": "Solved Ticket",
                "description": "Test",
            }
        )
        update_ticket_status.invoke({"ticket_id": 1001, "status": "solved"})

        result = search_tickets.invoke(
            {
                "query": "Ticket",
                "status": "open",
            }
        )

        assert "Open Ticket" in result
        assert "Solved Ticket" not in result

    def test_search_no_results(self):
        """Test searching with no matching results."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = search_tickets.invoke({"query": "nonexistent"})

        assert "No tickets found" in result

    def test_search_with_limit(self):
        """Test searching with limit."""
        for i in range(10):
            create_ticket.invoke(
                {
                    "subject": f"Test Issue {i}",
                    "description": "Test description",
                }
            )

        result = search_tickets.invoke(
            {
                "query": "Test",
                "limit": 3,
            }
        )

        # Should find only 3 tickets due to limit
        assert result.count("Test Issue") == 3


class TestGetMyOpenTickets:
    """Tests for getting open tickets."""

    def test_get_open_tickets(self):
        """Test getting list of open tickets."""
        create_ticket.invoke(
            {
                "subject": "Open 1",
                "description": "Test",
            }
        )
        update_ticket_status.invoke({"ticket_id": 1000, "status": "open"})

        create_ticket.invoke(
            {
                "subject": "Open 2",
                "description": "Test",
            }
        )
        update_ticket_status.invoke({"ticket_id": 1001, "status": "pending"})

        create_ticket.invoke(
            {
                "subject": "Closed",
                "description": "Test",
            }
        )
        update_ticket_status.invoke({"ticket_id": 1002, "status": "closed"})

        result = get_my_open_tickets.invoke({})

        assert "Open 1" in result
        assert "Open 2" in result
        assert "Closed" not in result

    def test_get_open_tickets_empty(self):
        """Test getting open tickets when none exist."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )
        update_ticket_status.invoke({"ticket_id": 1000, "status": "solved"})

        result = get_my_open_tickets.invoke({})

        assert "No open tickets" in result

    def test_get_open_tickets_priority_order(self):
        """Test that open tickets are ordered by priority."""
        create_ticket.invoke(
            {
                "subject": "Low Priority",
                "description": "Test",
                "priority": "low",
            }
        )

        create_ticket.invoke(
            {
                "subject": "Urgent Priority",
                "description": "Test",
                "priority": "urgent",
            }
        )

        create_ticket.invoke(
            {
                "subject": "Normal Priority",
                "description": "Test",
                "priority": "normal",
            }
        )

        result = get_my_open_tickets.invoke({})

        # Urgent should appear first
        urgent_pos = result.find("Urgent Priority")
        normal_pos = result.find("Normal Priority")
        low_pos = result.find("Low Priority")

        assert urgent_pos < normal_pos < low_pos


class TestAssignTicket:
    """Tests for assigning tickets to agents."""

    def test_assign_to_valid_agent(self):
        """Test assigning ticket to a valid agent."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = assign_ticket.invoke(
            {
                "ticket_id": 1000,
                "assignee_id": "agent_1",
            }
        )

        assert "✅ Ticket Assigned Successfully!" in result
        assert get_storage().get_ticket(1000)["assignee_id"] == "agent_1"
        assert get_storage().get_ticket(1000)["assignee_name"] is not None

    def test_assign_to_invalid_agent(self):
        """Test assigning to invalid agent."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = assign_ticket.invoke(
            {
                "ticket_id": 1000,
                "assignee_id": "invalid_agent",
            }
        )

        assert "❌" in result
        assert "Invalid assignee" in result

    def test_reassign_ticket(self):
        """Test reassigning ticket to different agent."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        assign_ticket.invoke({"ticket_id": 1000, "assignee_id": "agent_1"})
        result = assign_ticket.invoke({"ticket_id": 1000, "assignee_id": "agent_2"})

        assert get_storage().get_ticket(1000)["assignee_id"] == "agent_2"
        assert "Previous Assignee" in result


class TestAddTagsToTicket:
    """Tests for adding tags to tickets."""

    def test_add_single_tag(self):
        """Test adding a single tag."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = add_tags_to_ticket.invoke(
            {
                "ticket_id": 1000,
                "tags": ["urgent"],
            }
        )

        assert "✅ Tags Added Successfully!" in result
        assert "urgent" in get_storage().get_ticket(1000)["tags"]

    def test_add_multiple_tags(self):
        """Test adding multiple tags."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        add_tags_to_ticket.invoke(
            {
                "ticket_id": 1000,
                "tags": ["wifi", "network", "urgent"],
            }
        )

        assert len(get_storage().get_ticket(1000)["tags"]) == 3
        assert "wifi" in get_storage().get_ticket(1000)["tags"]
        assert "network" in get_storage().get_ticket(1000)["tags"]

    def test_add_duplicate_tags(self):
        """Test that duplicate tags are not added."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        add_tags_to_ticket.invoke({"ticket_id": 1000, "tags": ["wifi"]})
        result = add_tags_to_ticket.invoke({"ticket_id": 1000, "tags": ["wifi"]})

        assert "already exist" in result
        assert get_storage().get_ticket(1000)["tags"].count("wifi") == 1

    def test_tags_case_insensitive(self):
        """Test that tags are case insensitive."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        add_tags_to_ticket.invoke(
            {
                "ticket_id": 1000,
                "tags": ["WiFi", "URGENT"],
            }
        )

        # Tags should be lowercased
        assert "wifi" in get_storage().get_ticket(1000)["tags"]
        assert "urgent" in get_storage().get_ticket(1000)["tags"]


class TestSetTicketCategory:
    """Tests for setting ticket category."""

    def test_set_valid_category(self):
        """Test setting a valid category."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = set_ticket_category.invoke(
            {
                "ticket_id": 1000,
                "category": "network",
            }
        )

        assert "✅ Category Updated Successfully!" in result
        assert get_storage().get_ticket(1000)["category"] == "network"

    def test_set_invalid_category(self):
        """Test setting invalid category."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        result = set_ticket_category.invoke(
            {
                "ticket_id": 1000,
                "category": "invalid_category",
            }
        )

        assert "❌" in result
        assert "Invalid category" in result

    def test_change_category(self):
        """Test changing category."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        set_ticket_category.invoke({"ticket_id": 1000, "category": "hardware"})
        result = set_ticket_category.invoke({"ticket_id": 1000, "category": "software"})

        assert get_storage().get_ticket(1000)["category"] == "software"
        assert "hardware" in result
        assert "software" in result


class TestSetTicketDueDate:
    """Tests for setting ticket due date."""

    def test_set_due_date(self):
        """Test setting a due date."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        due_date = "2025-12-31T23:59:59"
        result = set_ticket_due_date.invoke(
            {
                "ticket_id": 1000,
                "due_date": due_date,
            }
        )

        assert "✅ Due Date Set Successfully!" in result
        assert get_storage().get_ticket(1000)["due_date"] == due_date

    def test_update_due_date(self):
        """Test updating an existing due date."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        set_ticket_due_date.invoke({"ticket_id": 1000, "due_date": "2025-12-31"})
        result = set_ticket_due_date.invoke(
            {"ticket_id": 1000, "due_date": "2026-01-15"}
        )

        assert get_storage().get_ticket(1000)["due_date"] == "2026-01-15"
        assert "2025-12-31" in result


class TestDeleteTicket:
    """Tests for deleting tickets."""

    def test_delete_existing_ticket(self):
        """Test deleting an existing ticket."""
        create_ticket.invoke(
            {
                "subject": "To Be Deleted",
                "description": "Test",
            }
        )

        assert get_storage().get_ticket(1000) is not None

        result = delete_ticket.invoke({"ticket_id": 1000})

        assert "✅ Ticket Deleted Successfully!" in result
        assert "To Be Deleted" in result
        assert get_storage().get_ticket(1000) is None

    def test_delete_nonexistent_ticket(self):
        """Test deleting non-existent ticket."""
        result = delete_ticket.invoke({"ticket_id": 9999})

        assert "❌" in result
        assert "not found" in result

    def test_delete_ticket_permanent(self):
        """Test that deletion is permanent."""
        create_ticket.invoke(
            {
                "subject": "Test",
                "description": "Test",
            }
        )

        delete_ticket.invoke({"ticket_id": 1000})

        # Try to get deleted ticket
        result = get_ticket.invoke({"ticket_id": 1000})
        assert "not found" in result

    def test_delete_multiple_tickets(self):
        """Test deleting multiple tickets."""
        create_ticket.invoke({"subject": "Test 1", "description": "Test"})
        create_ticket.invoke({"subject": "Test 2", "description": "Test"})
        create_ticket.invoke({"subject": "Test 3", "description": "Test"})

        assert len(get_storage().load_all_tickets()) == 3

        delete_ticket.invoke({"ticket_id": 1000})
        delete_ticket.invoke({"ticket_id": 1002})

        assert len(get_storage().load_all_tickets()) == 1
        assert get_storage().get_ticket(1001) is not None
        assert get_storage().get_ticket(1000) is None
        assert get_storage().get_ticket(1002) is None


class TestTicketWorkflow:
    """Integration tests for complete ticket workflows."""

    def test_complete_ticket_lifecycle(self):
        """Test complete ticket lifecycle from creation to resolution."""
        # Create ticket
        create_result = create_ticket.invoke(
            {
                "subject": "Computer won't start",
                "description": "My computer displays a black screen",
                "priority": "high",
                "requester_email": "user@example.com",
                "requester_name": "John Doe",
            }
        )
        assert "#1000" in create_result

        # Get ticket details
        get_result = get_ticket.invoke({"ticket_id": 1000})
        assert "Computer won't start" in get_result

        # Assign to agent
        assign_result = assign_ticket.invoke(
            {
                "ticket_id": 1000,
                "assignee_id": "agent_1",
            }
        )
        assert "✅" in assign_result

        # Add tags
        add_tags_to_ticket.invoke(
            {
                "ticket_id": 1000,
                "tags": ["hardware", "urgent"],
            }
        )

        # Set category
        set_ticket_category.invoke(
            {
                "ticket_id": 1000,
                "category": "hardware",
            }
        )

        # Update status to open
        update_ticket_status.invoke(
            {
                "ticket_id": 1000,
                "status": "open",
                "comment": "Investigating the issue",
            }
        )

        # Add comment
        add_ticket_comment.invoke(
            {
                "ticket_id": 1000,
                "comment": "Please check if the power cable is connected",
            }
        )

        # Update status to solved
        update_result = update_ticket_status.invoke(
            {
                "ticket_id": 1000,
                "status": "solved",
                "comment": "Issue resolved: power cable was loose",
            }
        )
        assert "SOLVED" in update_result

        # Verify final state
        final_ticket = get_storage().get_ticket(1000)
        assert final_ticket["status"] == "solved"
        assert final_ticket["assignee_id"] == "agent_1"
        assert "hardware" in final_ticket["tags"]
        assert final_ticket["category"] == "hardware"
        assert len(final_ticket["comments"]) >= 2
        assert final_ticket["resolved_at"] is not None

    def test_duplicate_ticket_deletion(self):
        """Test workflow for handling duplicate tickets."""
        # Create original ticket
        create_ticket.invoke(
            {
                "subject": "Password Reset",
                "description": "Need to reset my password",
            }
        )

        # Create duplicate
        create_ticket.invoke(
            {
                "subject": "Password Reset",
                "description": "Cannot access my account",
            }
        )

        # Search for duplicates
        search_result = search_tickets.invoke({"query": "Password Reset"})
        assert "#1000" in search_result
        assert "#1001" in search_result

        # Delete duplicate
        delete_result = delete_ticket.invoke({"ticket_id": 1001})
        assert "✅" in delete_result

        # Verify only one remains
        assert len(get_storage().load_all_tickets()) == 1
        assert get_storage().get_ticket(1000) is not None

    def test_escalation_workflow(self):
        """Test ticket escalation workflow."""
        # Create normal priority ticket
        create_ticket.invoke(
            {
                "subject": "Minor issue",
                "description": "Small problem",
                "priority": "normal",
            }
        )

        # Escalate priority
        update_ticket_priority.invoke(
            {
                "ticket_id": 1000,
                "priority": "urgent",
            }
        )

        # Reassign to specialized agent
        assign_ticket.invoke(
            {
                "ticket_id": 1000,
                "assignee_id": "agent_4",  # Security agent
            }
        )

        # Add escalation tag
        add_tags_to_ticket.invoke(
            {
                "ticket_id": 1000,
                "tags": ["escalated", "urgent"],
            }
        )

        # Verify escalation
        ticket = get_storage().get_ticket(1000)
        assert ticket["priority"] == "urgent"
        assert ticket["assignee_id"] == "agent_4"
        assert "escalated" in ticket["tags"]
