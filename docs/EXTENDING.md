# Extending the System

Learn how to add new tools, agents, and features to the Typhoon IT Support system.

## Adding a New Tool

Tools extend what the agent can do. Here's how to add one.

### Step 1: Create the Tool

Create a new file `src/typhoon_it_support/tools/your_tool.py`:

```python
"""Your custom tool description."""

def your_tool_name(param: str) -> str:
    """Brief description of what the tool does.
    
    Use clear, descriptive language. The LLM reads this docstring
    to understand when and how to use your tool.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of what gets returned
    """
    # Your implementation here
    result = process_data(param)
    return result
```

**Best Practices:**
- Use clear, verb-based names (e.g., `search_knowledge`, `create_ticket`)
- Write comprehensive docstrings
- Return human-readable results
- Handle errors gracefully
- Keep logic deterministic

### Step 2: Export the Tool

Add to `src/typhoon_it_support/tools/__init__.py`:

```python
from .your_tool import your_tool_name

__all__ = [
    # ... existing tools ...
    "your_tool_name",
]
```

### Step 3: Write Tests

Create `tests/test_your_tool.py`:

```python
"""Tests for your custom tool."""

from src.typhoon_it_support.tools.your_tool import your_tool_name


def test_your_tool_basic():
    """Test basic functionality."""
    result = your_tool_name("test input")
    assert result == "expected output"


def test_your_tool_edge_case():
    """Test edge cases."""
    result = your_tool_name("")
    assert "error" in result.lower()
```

### Step 4: Use the Tool

The agent automatically discovers tools exported from `tools/__init__.py`. Just update your prompt if needed to guide usage:

```python
# In prompts/agent_prompts.py

AGENT_SYSTEM_PROMPT = """...

Available tools:
...
- your_tool_name: Use this when you need to [specific use case]
"""
```

## Example: Database Query Tool

Here's a complete example of a database query tool:

```python
# src/typhoon_it_support/tools/database_tools.py
"""Database query tools for IT support."""

import sqlite3
from typing import Optional


def query_user_info(email: str) -> str:
    """Retrieve user information from the database.
    
    Use this tool when you need to look up user account details,
    department, or contact information.
    
    Args:
        email: User's email address
        
    Returns:
        User information including name, department, and role,
        or error message if user not found
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT name, department, role FROM users WHERE email = ?",
        (email,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        name, dept, role = result
        return f"User: {name}\nDepartment: {dept}\nRole: {role}"
    else:
        return f"No user found with email: {email}"
```

## Adding a Specialized Agent Node

For complex workflows, you might want specialized agent nodes.

### Step 1: Create the Node

Create `src/typhoon_it_support/agents/specialist_node.py`:

```python
"""Specialist agent for specific tasks."""

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

from ..config import get_settings
from ..models import AgentState

SPECIALIST_PROMPT = """You are a specialist in [specific domain].

Your role:
- Analyze [specific type of problem]
- Provide [specific type of solution]
- Consider [specific constraints]

Always be concise and actionable.
"""


def specialist_node(state: AgentState) -> AgentState:
    """Process requests requiring specialist knowledge.
    
    Args:
        state: Current workflow state
        
    Returns:
        Updated state with specialist response
    """
    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.typhoon_model,
        temperature=0.5,
        api_key=settings.typhoon_api_key,
        base_url=settings.typhoon_base_url,
    )
    
    messages = [
        {"role": "system", "content": SPECIALIST_PROMPT},
        {"role": "user", "content": state["messages"][-1].content}
    ]
    
    response = llm.invoke(messages)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "iteration": state["iteration"],
    }
```

### Step 2: Update the Workflow

Modify `src/typhoon_it_support/graph/workflow.py`:

```python
from ..agents.specialist_node import specialist_node

def create_workflow():
    workflow = StateGraph(AgentState)
    
    # Add your specialist node
    workflow.add_node("specialist", specialist_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("router", router_node)
    
    # Add routing logic
    workflow.add_edge("agent", "specialist")
    workflow.add_edge("specialist", "router")
    
    # ... rest of workflow setup
```

## Adding Custom State Fields

Extend the state model to track additional information.

### Update State Model

Edit `src/typhoon_it_support/models/state.py`:

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    iteration: int
    
    # Add your custom fields
    user_context: Optional[dict]    # User preferences, history
    active_tickets: list[str]       # Currently working on
    escalation_reason: Optional[str]  # Why escalated
```

### Use in Nodes

```python
def agent_node(state: AgentState) -> AgentState:
    # Access custom state
    user_context = state.get("user_context", {})
    active_tickets = state.get("active_tickets", [])
    
    # ... your logic ...
    
    # Update state
    return {
        "messages": [response],
        "iteration": state["iteration"] + 1,
        "active_tickets": updated_tickets,
    }
```

## Adding Evaluation Test Cases

Add test cases to measure performance.

### Create Test Case

Edit `src/typhoon_it_support/evaluation/test_cases.py`:

```python
TEST_CASES = [
    # ... existing cases ...
    {
        "test_id": "your_test_001",
        "category": "your_category",
        "query": "Test user query",
        "expected_tools": ["tool_name"],
        "expected_keywords": ["keyword1", "keyword2"],
        "description": "Test description",
    },
]
```

### Run Evaluation

```bash
python scripts/run_evaluation.py --test-ids your_test_001
```

## Customizing Prompts

### Modify Agent Behavior

Edit `src/typhoon_it_support/prompts/agent_prompts.py`:

```python
AGENT_SYSTEM_PROMPT = """คุณเป็นผู้ช่วย IT Support ที่เชี่ยวชาญ

<role>
บทบาทและความรับผิดชอบของคุณ:
- ช่วยเหลือผู้ใช้แก้ปัญหาด้านไอที
- ใช้เครื่องมือที่มีอย่างเหมาะสม
- [Add your custom responsibilities]
</role>

<guidelines>
- [Add your custom guidelines]
- อธิบายอย่างชัดเจนและเข้าใจง่าย
- ใช้ภาษาไทยที่สุภาพ
</guidelines>

<tools>
Available tools:
- [Document your tools]
</tools>

ตอบคำถามเป็นภาษาไทยเสมอ
"""
```

### Version Control

Always version control prompt changes:

```bash
git add src/typhoon_it_support/prompts/agent_prompts.py
git commit -m "feat(prompts): add custom guidelines for [feature]"
```

## Adding API Endpoints

### Create Endpoint

Add to `src/typhoon_it_support/api/server.py`:

```python
@app.post("/your-endpoint")
async def your_endpoint(request: YourRequest):
    """Your endpoint description."""
    try:
        result = process_request(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Define Request Model

```python
from pydantic import BaseModel

class YourRequest(BaseModel):
    field1: str
    field2: int
    field3: Optional[str] = None
```

## Best Practices

### Tool Design

1. **Clear Names**: Use descriptive verbs
2. **Good Docs**: Write comprehensive docstrings
3. **Error Handling**: Return human-readable errors
4. **Deterministic**: Same input → same output
5. **Tested**: Write unit tests

### Prompt Engineering

1. **Version Control**: Track all changes
2. **Keep Simple**: Concise, structured
3. **English Internal**: Better LLM reasoning
4. **Thai Output**: Natural user experience
5. **Test Changes**: Use evaluation suite

### State Management

1. **Minimal State**: Only essential data
2. **Clear Types**: Type hints everywhere
3. **Document Fields**: Explain each field
4. **Preserve History**: Don't lose context

### Testing

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test workflows
3. **Evaluation**: Measure real performance
4. **Edge Cases**: Test error scenarios

## Common Patterns

### Pattern 1: Conditional Tool Execution

```python
def smart_search(query: str, force: bool = False) -> str:
    """Search only if not already in context.
    
    Args:
        query: Search query
        force: Force search even if already searched
        
    Returns:
        Search results or cached results
    """
    if not force and query in _search_cache:
        return _search_cache[query]
    
    results = perform_search(query)
    _search_cache[query] = results
    return results
```

### Pattern 2: Multi-Step Tool

```python
def complex_operation(param: str) -> str:
    """Perform multi-step operation.
    
    This tool handles multiple steps internally, returning
    a summary of all actions taken.
    """
    step1_result = step_one(param)
    if "error" in step1_result:
        return step1_result
    
    step2_result = step_two(step1_result)
    step3_result = step_three(step2_result)
    
    return f"Completed: {step3_result}"
```

### Pattern 3: Async Tool

```python
import asyncio

async def async_tool(param: str) -> str:
    """Asynchronous tool for concurrent execution."""
    results = await asyncio.gather(
        async_operation_1(param),
        async_operation_2(param),
    )
    return combine_results(results)
```

## Debugging Tips

### Enable Debug Mode

```bash
# In .env
DEBUG=true
```

### Add Logging

```python
import logging

logger = logging.getLogger(__name__)

def your_tool(param: str) -> str:
    logger.debug(f"Tool called with: {param}")
    result = process(param)
    logger.debug(f"Tool returning: {result}")
    return result
```

### Test Isolated

```python
# Test tool in isolation
from src.typhoon_it_support.tools.your_tool import your_tool

result = your_tool("test")
print(result)
```

## Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Typhoon Docs**: https://docs.opentyphoon.ai
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Project Tests**: See `tests/` for examples

---

**Ready to build?** Check the [Best Practices](BEST_PRACTICES.md) for agentic system principles.


