"""Tests for ticket API endpoints - Real user scenarios and edge cases."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from src.typhoon_it_support.api.server import app
from src.typhoon_it_support.tools.ticket_storage import get_storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tickets():
    """Reset ticket storage before each test."""
    storage = get_storage()
    # Clear all tickets
    for ticket_id in list(storage.load_all_tickets().keys()):
        storage.delete_ticket(ticket_id)
    # Reset counter
    storage._next_id = 1000
    yield
    # Clear after test
    for ticket_id in list(storage.load_all_tickets().keys()):
        storage.delete_ticket(ticket_id)


# ============= Real User API Scenarios =============

class TestRealUserAPIScenarios:
    """Test real-world API usage scenarios."""
    
    def test_user_creates_ticket_via_api(self):
        """Scenario: User creates ticket through web interface."""
        response = client.post(
            "/tickets",
            json={
                "subject": "Laptop running very slow",
                "description": "My laptop takes 10 minutes to boot and applications freeze frequently.",
                "priority": "high",
                "requester_email": "john.doe@company.com",
                "requester_name": "John Doe"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "ticket" in data
        assert data["ticket"]["id"] == 1000
        assert data["ticket"]["subject"] == "Laptop running very slow"
        assert data["ticket"]["priority"] == "high"
        assert data["ticket"]["status"] == "new"
        assert "sla_first_response_due" in data["ticket"]
        assert "sla_resolution_due" in data["ticket"]
    
    def test_admin_views_all_tickets(self):
        """Scenario: Admin views ticket dashboard."""
        # Create several tickets
        for i in range(5):
            client.post(
                "/tickets",
                json={
                    "subject": f"Issue {i+1}",
                    "description": f"Description {i+1}",
                    "priority": ["low", "normal", "high"][i % 3]
                }
            )
        
        # Get all tickets
        response = client.get("/tickets")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["tickets"]) == 5
    
    def test_filter_tickets_by_status(self):
        """Scenario: Admin filters tickets by status."""
        # Create tickets with different statuses
        client.post("/tickets", json={"subject": "Issue 1", "description": "Desc 1"})
        client.post("/tickets", json={"subject": "Issue 2", "description": "Desc 2"})
        
        # Update one to solved
        client.patch("/tickets/1000", json={"status": "solved"})
        
        # Filter by status
        response = client.get("/tickets?status=solved")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["tickets"][0]["status"] == "solved"
        
        response = client.get("/tickets?status=new")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["tickets"][0]["status"] == "new"
    
    def test_get_ticket_details(self):
        """Scenario: User checks their ticket details."""
        # Create ticket
        create_response = client.post(
            "/tickets",
            json={
                "subject": "Password reset needed",
                "description": "Forgot my password",
                "priority": "normal"
            }
        )
        ticket_id = create_response.json()["ticket"]["id"]
        
        # Get ticket details
        response = client.get(f"/tickets/{ticket_id}")
        assert response.status_code == 200
        data = response.json()
        assert "ticket" in data
        assert data["ticket"]["id"] == ticket_id
        assert data["ticket"]["subject"] == "Password reset needed"
    
    def test_update_ticket_status_workflow(self):
        """Scenario: Agent updates ticket through workflow."""
        # Create ticket
        create_response = client.post(
            "/tickets",
            json={
                "subject": "VPN not connecting",
                "description": "Cannot connect to VPN from home"
            }
        )
        ticket_id = create_response.json()["ticket"]["id"]
        
        # Agent opens ticket
        response = client.patch(
            f"/tickets/{ticket_id}",
            json={"status": "open", "comment": "Investigating the issue"}
        )
        assert response.status_code == 200
        assert response.json()["ticket"]["status"] == "open"
        
        # Agent marks as pending
        response = client.patch(
            f"/tickets/{ticket_id}",
            json={"status": "pending", "comment": "Waiting for user response"}
        )
        assert response.status_code == 200
        assert response.json()["ticket"]["status"] == "pending"
        
        # Agent solves ticket
        response = client.patch(
            f"/tickets/{ticket_id}",
            json={"status": "solved", "comment": "Issue resolved"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["ticket"]["status"] == "solved"
        assert data["ticket"]["resolved_at"] is not None
    
    def test_assign_ticket_to_agent(self):
        """Scenario: Supervisor assigns ticket to specialist."""
        # Create ticket
        create_response = client.post(
            "/tickets",
            json={
                "subject": "Network outage in Building B",
                "description": "Complete network failure"
            }
        )
        ticket_id = create_response.json()["ticket"]["id"]
        
        # Assign to network specialist
        response = client.post(
            f"/tickets/{ticket_id}/assign",
            json={"assignee_id": "agent_3"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticket"]["assignee_id"] == "agent_3"
        assert data["ticket"]["assignee_name"] == "พี่เน็ต (Network)"
    
    def test_add_tags_to_ticket(self):
        """Scenario: Agent categorizes ticket with tags."""
        # Create ticket
        create_response = client.post(
            "/tickets",
            json={"subject": "Printer jam", "description": "Paper stuck"}
        )
        ticket_id = create_response.json()["ticket"]["id"]
        
        # Add tags
        response = client.post(
            f"/tickets/{ticket_id}/tags",
            json={"tags": ["printer", "hardware", "floor-3"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "printer" in data["ticket"]["tags"]
        assert "hardware" in data["ticket"]["tags"]
    
    def test_set_ticket_category(self):
        """Scenario: Admin sets category for reporting."""
        # Create ticket
        create_response = client.post(
            "/tickets",
            json={"subject": "Software license request", "description": "Need Adobe"}
        )
        ticket_id = create_response.json()["ticket"]["id"]
        
        # Set category
        response = client.post(
            f"/tickets/{ticket_id}/category",
            json={"category": "software"}
        )
        
        assert response.status_code == 200
        assert response.json()["ticket"]["category"] == "software"
    
    def test_advanced_search(self):
        """Scenario: Admin searches with multiple filters."""
        # Create diverse tickets
        client.post("/tickets", json={
            "subject": "VPN issue",
            "description": "Cannot connect",
            "priority": "high"
        })
        client.patch("/tickets/1000", json={"status": "open"})
        client.post("/tickets/1000/category", json={"category": "vpn"})
        
        client.post("/tickets", json={
            "subject": "Printer problem",
            "description": "Not printing",
            "priority": "low"
        })
        client.post("/tickets/1001/category", json={"category": "printer"})
        
        # Search with multiple filters
        response = client.get(
            "/tickets/search/advanced?"
            "query=VPN&"
            "priority=high&"
            "status=open&"
            "category=vpn"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert any("VPN" in t["subject"] for t in data["tickets"])
    
    def test_bulk_update_tickets(self):
        """Scenario: Admin bulk updates related tickets."""
        # Create multiple related tickets
        ticket_ids = []
        for i in range(3):
            response = client.post(
                "/tickets",
                json={
                    "subject": f"Email issue {i+1}",
                    "description": "Cannot send emails"
                }
            )
            ticket_ids.append(response.json()["ticket"]["id"])
        
        # Bulk update all
        response = client.post(
            "/tickets/bulk/update",
            json={
                "ticket_ids": ticket_ids,
                "status": "solved",
                "tags": ["email-outage-resolved"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["updated"] == 3
        assert data["total"] == 3
        
        # Verify all updated
        for ticket_id in ticket_ids:
            response = client.get(f"/tickets/{ticket_id}")
            ticket = response.json()["ticket"]
            assert ticket["status"] == "solved"
            assert "email-outage-resolved" in ticket["tags"]
    
    def test_export_tickets_csv(self):
        """Scenario: Admin exports tickets for reporting."""
        # Create tickets
        for i in range(3):
            client.post(
                "/tickets",
                json={
                    "subject": f"Issue {i+1}",
                    "description": f"Desc {i+1}",
                    "priority": "normal"
                }
            )
        
        # Export as CSV
        response = client.get("/tickets/export/csv")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        
        # Verify CSV content
        csv_content = response.text
        assert "ID" in csv_content  # Header
        assert "Subject" in csv_content
        assert "Issue 1" in csv_content or "Issue 2" in csv_content
    
    def test_get_ticket_statistics(self):
        """Scenario: Dashboard loads statistics."""
        # Create varied tickets
        statuses = ["new", "open", "pending", "solved", "closed"]
        priorities = ["low", "normal", "high", "urgent"]
        
        for i, status in enumerate(statuses):
            response = client.post(
                "/tickets",
                json={
                    "subject": f"Ticket {i}",
                    "description": "Test",
                    "priority": priorities[i % len(priorities)]
                }
            )
            ticket_id = response.json()["ticket"]["id"]
            client.patch(f"/tickets/{ticket_id}", json={"status": status})
        
        # Get statistics
        response = client.get("/tickets/stats/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert "by_status" in data
        assert "by_priority" in data
        assert data["by_status"]["open"] >= 1
        assert data["by_status"]["solved"] >= 1
    
    def test_get_available_agents(self):
        """Scenario: UI loads agent list for assignment."""
        response = client.get("/tickets/agents")
        
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) > 0
        
        # Verify agent structure
        agent = data["agents"][0]
        assert "id" in agent
        assert "name" in agent
        assert "email" in agent


# ============= Edge Cases API Tests =============

class TestEdgeCasesAPI:
    """Test API edge cases and error handling."""
    
    def test_create_ticket_missing_required_fields(self):
        """Edge case: Missing required fields."""
        response = client.post(
            "/tickets",
            json={"subject": "Only subject"}  # Missing description
        )
        # Should still work or return appropriate error
        assert response.status_code in [200, 422]
    
    def test_get_nonexistent_ticket(self):
        """Edge case: Get ticket that doesn't exist."""
        response = client.get("/tickets/9999")
        assert response.status_code == 404
    
    def test_update_nonexistent_ticket(self):
        """Edge case: Update non-existent ticket."""
        response = client.patch(
            "/tickets/9999",
            json={"status": "open"}
        )
        assert response.status_code == 404
    
    def test_delete_nonexistent_ticket(self):
        """Edge case: Delete non-existent ticket."""
        response = client.delete("/tickets/9999")
        assert response.status_code == 404
    
    def test_assign_invalid_agent(self):
        """Edge case: Assign to non-existent agent."""
        response = client.post("/tickets", json={"subject": "Test", "description": "Test"})
        ticket_id = response.json()["ticket"]["id"]
        
        response = client.post(
            f"/tickets/{ticket_id}/assign",
            json={"assignee_id": "invalid_agent"}
        )
        assert response.status_code == 400
    
    def test_set_invalid_status(self):
        """Edge case: Invalid status value."""
        response = client.post("/tickets", json={"subject": "Test", "description": "Test"})
        ticket_id = response.json()["ticket"]["id"]
        
        response = client.patch(
            f"/tickets/{ticket_id}",
            json={"status": "super_duper_closed"}
        )
        assert response.status_code == 400
    
    def test_set_invalid_priority(self):
        """Edge case: Invalid priority value."""
        response = client.post("/tickets", json={"subject": "Test", "description": "Test"})
        ticket_id = response.json()["ticket"]["id"]
        
        response = client.patch(
            f"/tickets/{ticket_id}",
            json={"priority": "extremely_urgent"}
        )
        assert response.status_code == 400
    
    def test_set_invalid_category(self):
        """Edge case: Invalid category value."""
        response = client.post("/tickets", json={"subject": "Test", "description": "Test"})
        ticket_id = response.json()["ticket"]["id"]
        
        response = client.post(
            f"/tickets/{ticket_id}/category",
            json={"category": "invalid_category"}
        )
        assert response.status_code == 400
    
    def test_bulk_update_empty_list(self):
        """Edge case: Bulk update with empty ticket list."""
        response = client.post(
            "/tickets/bulk/update",
            json={"ticket_ids": [], "status": "open"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["updated"] == 0
    
    def test_bulk_update_partial_failure(self):
        """Edge case: Bulk update with some invalid IDs."""
        # Create one valid ticket
        response = client.post("/tickets", json={"subject": "Test", "description": "Test"})
        valid_id = response.json()["ticket"]["id"]
        
        # Try to update valid and invalid tickets
        response = client.post(
            "/tickets/bulk/update",
            json={
                "ticket_ids": [valid_id, 9999, 8888],
                "status": "open"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["updated"] == 1
        assert data["total"] == 3
        assert len(data["errors"]) == 2
    
    def test_search_with_no_results(self):
        """Edge case: Search returns no results."""
        response = client.get("/tickets/search/advanced?query=nonexistent_keyword")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
    
    def test_filter_invalid_status(self):
        """Edge case: Filter with invalid status."""
        response = client.get("/tickets?status=invalid_status")
        assert response.status_code == 400
    
    def test_very_long_subject(self):
        """Edge case: Very long ticket subject."""
        long_subject = "A" * 1000
        response = client.post(
            "/tickets",
            json={
                "subject": long_subject,
                "description": "Test description"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["ticket"]["subject"]) == 1000
    
    def test_unicode_and_special_characters(self):
        """Edge case: Unicode and special characters."""
        response = client.post(
            "/tickets",
            json={
                "subject": "ปัญหา WiFi ไม่เชื่อมต่อ 🔧💻",
                "description": "อักขระพิเศษ: @#$%^&*()",
                "requester_name": "ผู้ใช้ ทดสอบ",
                "requester_email": "ผู้ใช้@example.co.th"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "🔧" in data["ticket"]["subject"]
        assert "อักขระพิเศษ" in data["ticket"]["description"]
    
    def test_concurrent_updates_same_ticket(self):
        """Edge case: Multiple concurrent updates."""
        # Create ticket
        response = client.post("/tickets", json={"subject": "Test", "description": "Test"})
        ticket_id = response.json()["ticket"]["id"]
        
        # Make multiple updates rapidly
        responses = []
        responses.append(client.patch(f"/tickets/{ticket_id}", json={"status": "open"}))
        responses.append(client.post(f"/tickets/{ticket_id}/assign", json={"assignee_id": "agent_1"}))
        responses.append(client.patch(f"/tickets/{ticket_id}", json={"priority": "high"}))
        responses.append(client.post(f"/tickets/{ticket_id}/tags", json={"tags": ["urgent"]}))
        
        # All should succeed
        for r in responses:
            assert r.status_code == 200
        
        # Final state should have all updates
        response = client.get(f"/tickets/{ticket_id}")
        ticket = response.json()["ticket"]
        assert ticket["status"] == "open"
        assert ticket["assignee_id"] == "agent_1"
        assert ticket["priority"] == "high"
        assert "urgent" in ticket["tags"]


# ============= Integration API Tests =============

class TestIntegrationAPI:
    """Integration tests for complete API workflows."""
    
    def test_full_ticket_lifecycle_via_api(self):
        """Integration: Complete ticket lifecycle through API."""
        # 1. Create ticket
        create_response = client.post(
            "/tickets",
            json={
                "subject": "Cannot access shared folder",
                "description": "Getting permission denied error",
                "priority": "high",
                "requester_email": "user@company.com",
                "requester_name": "Test User"
            }
        )
        assert create_response.status_code == 200
        ticket_id = create_response.json()["ticket"]["id"]
        
        # 2. Assign to agent
        assign_response = client.post(
            f"/tickets/{ticket_id}/assign",
            json={"assignee_id": "agent_2"}
        )
        assert assign_response.status_code == 200
        
        # 3. Set category
        category_response = client.post(
            f"/tickets/{ticket_id}/category",
            json={"category": "account_access"}
        )
        assert category_response.status_code == 200
        
        # 4. Add tags
        tags_response = client.post(
            f"/tickets/{ticket_id}/tags",
            json={"tags": ["permissions", "file-share"]}
        )
        assert tags_response.status_code == 200
        
        # 5. Update status with comment
        status_response = client.patch(
            f"/tickets/{ticket_id}",
            json={
                "status": "open",
                "comment": "Investigating permissions issue"
            }
        )
        assert status_response.status_code == 200
        
        # 6. Resolve ticket
        resolve_response = client.patch(
            f"/tickets/{ticket_id}",
            json={
                "status": "solved",
                "comment": "Permissions fixed - user can now access folder"
            }
        )
        assert resolve_response.status_code == 200
        
        # 7. Verify final state
        final_response = client.get(f"/tickets/{ticket_id}")
        ticket = final_response.json()["ticket"]
        
        assert ticket["status"] == "solved"
        assert ticket["assignee_id"] == "agent_2"
        assert ticket["category"] == "account_access"
        assert "permissions" in ticket["tags"]
        assert "file-share" in ticket["tags"]
        assert ticket["resolved_at"] is not None
        assert ticket["first_response_at"] is not None
        assert len(ticket["comments"]) >= 2
        assert len(ticket["history"]) >= 6
    
    def test_multi_ticket_incident_via_api(self):
        """Integration: Handle incident with multiple tickets."""
        # Create multiple tickets for same incident
        ticket_ids = []
        for i in range(5):
            response = client.post(
                "/tickets",
                json={
                    "subject": f"Network outage - Floor {i+1}",
                    "description": "Cannot access internet",
                    "priority": "urgent"
                }
            )
            ticket_ids.append(response.json()["ticket"]["id"])
        
        # Tag all as part of incident
        for tid in ticket_ids:
            client.post(
                f"/tickets/{tid}/tags",
                json={"tags": ["incident-network-outage", "building-a"]}
            )
        
        # Bulk assign to network team
        bulk_response = client.post(
            "/tickets/bulk/update",
            json={
                "ticket_ids": ticket_ids,
                "assignee_id": "agent_3"
            }
        )
        assert bulk_response.status_code == 200
        assert bulk_response.json()["updated"] == 5
        
        # Search for incident tickets
        search_response = client.get(
            "/tickets/search/advanced?tags=incident-network-outage"
        )
        assert search_response.status_code == 200
        assert search_response.json()["total"] >= 5
        
        # Bulk resolve
        bulk_resolve = client.post(
            "/tickets/bulk/update",
            json={
                "ticket_ids": ticket_ids,
                "status": "solved"
            }
        )
        assert bulk_resolve.status_code == 200
        
        # Verify all resolved
        stats_response = client.get("/tickets/stats/summary")
        stats = stats_response.json()
        assert stats["by_status"]["solved"] >= 5

