"""Basic tools for the IT support agent."""

from datetime import datetime
from langchain_core.tools import tool


@tool
def get_current_time() -> str:
    """Get the current time.
    
    Returns:
        Current time as a formatted string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

