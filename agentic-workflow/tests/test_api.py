"""Tests for FastAPI endpoints."""

from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from langchain_core.messages import AIMessage

from src.typhoon_it_support.api.server import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns health status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@patch("src.typhoon_it_support.api.chat_endpoints.create_workflow")
def test_chat_endpoint_basic(mock_workflow):
    """Test basic chat endpoint functionality."""
    # Mock workflow response
    mock_workflow_instance = Mock()
    mock_workflow.return_value = mock_workflow_instance
    mock_workflow_instance.invoke.return_value = {
        "messages": [AIMessage(content="I can help you with that!")],
        "iteration": 1,
        "next_action": "continue",
    }
    
    response = client.post(
        "/chat",
        json={"message": "Hello, I need help"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "session_id" in data
    assert "iteration" in data
    assert "next_action" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0


@patch("src.typhoon_it_support.api.chat_endpoints.create_workflow")
def test_chat_endpoint_with_session(mock_workflow):
    """Test chat endpoint with existing session."""
    # Mock workflow response
    mock_workflow_instance = Mock()
    mock_workflow.return_value = mock_workflow_instance
    mock_workflow_instance.invoke.return_value = {
        "messages": [AIMessage(content="Response to your message")],
        "iteration": 1,
        "next_action": "continue",
    }
    
    # First request
    response1 = client.post(
        "/chat",
        json={"message": "First message"}
    )
    session_id = response1.json()["session_id"]
    
    # Second request with same session
    response2 = client.post(
        "/chat",
        json={
            "message": "Second message",
            "session_id": session_id
        }
    )
    assert response2.status_code == 200
    data = response2.json()
    assert data["session_id"] == session_id


def test_get_session_not_found():
    """Test getting non-existent session."""
    response = client.get("/chat/nonexistent-session-id")
    assert response.status_code == 404


@patch("src.typhoon_it_support.api.chat_endpoints.create_workflow")
def test_clear_session(mock_workflow):
    """Test clearing a session."""
    # Mock workflow response
    mock_workflow_instance = Mock()
    mock_workflow.return_value = mock_workflow_instance
    mock_workflow_instance.invoke.return_value = {
        "messages": [AIMessage(content="Test response")],
        "iteration": 1,
        "next_action": "continue",
    }
    
    # Create a session
    response1 = client.post(
        "/chat",
        json={"message": "Test message"}
    )
    session_id = response1.json()["session_id"]
    
    # Clear the session
    response2 = client.delete(f"/chat/{session_id}")
    assert response2.status_code == 200
    data = response2.json()
    assert data["status"] == "success"

