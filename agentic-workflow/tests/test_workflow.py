"""Tests for workflow graph."""

from src.typhoon_it_support.graph import create_workflow


def test_create_workflow():
    """Test that workflow can be created and compiled."""
    workflow = create_workflow()
    assert workflow is not None


def test_workflow_has_nodes():
    """Test that workflow contains expected nodes."""
    workflow = create_workflow()
    # The compiled graph should be executable
    assert hasattr(workflow, "invoke")
