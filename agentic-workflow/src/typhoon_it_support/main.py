"""Main entry point for the IT support workflow."""

from langchain_core.messages import HumanMessage

from .config import get_settings
from .graph import create_workflow
from .models import AgentState


def run_workflow(user_message: str) -> dict:
    """Run the IT support workflow with a user message.
    
    Args:
        user_message: The user's support request.
        
    Returns:
        Final state after workflow completion.
    """
    settings = get_settings()
    
    # Create workflow
    workflow = create_workflow()
    
    # Initialize state
    initial_state: AgentState = {
        "messages": [HumanMessage(content=user_message)],
        "iteration": 0,
        "next_action": "start",
    }
    
    # Run workflow
    final_state = workflow.invoke(initial_state)
    
    if settings.debug:
        print(f"\nFinal iteration count: {final_state.get('iteration', 0)}")
        print(f"Next action: {final_state.get('next_action', 'unknown')}")
    
    return final_state


def main() -> None:
    """Main function for running the workflow."""
    print("IT Support Agent - Basic Demo")
    print("=" * 50)
    
    # Example usage
    user_query = "I need help resetting my password"
    print(f"\nUser: {user_query}")
    
    result = run_workflow(user_query)
    
    # Display conversation
    print("\nConversation History:")
    print("-" * 50)
    for message in result["messages"]:
        if hasattr(message, "type"):
            role = "User" if message.type == "human" else "Agent"
            print(f"\n{role}: {message.content}")


if __name__ == "__main__":
    main()

