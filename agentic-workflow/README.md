# Agentic Workflow - Backend

Backend implementation of the Typhoon IT Support system using LangGraph and FastAPI.

## Overview

This directory contains the core agentic workflow powered by:
- **LangGraph**: Workflow orchestration
- **Typhoon 2.5**: Thai-English bilingual LLM
- **FastAPI**: REST API with streaming
- **FAISS**: Vector store for document search

## Quick Start

### 1. Install Dependencies

```bash
cd agentic-workflow
uv pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your TYPHOON_API_KEY
```

### 3. Initialize Vector Store

```bash
python scripts/init_vector_store.py
```

### 4. Start Server

```bash
cd ..
./start-backend.sh
```

Server will be available at: http://localhost:8000

## Project Structure

```
agentic-workflow/
├── src/typhoon_it_support/
│   ├── agents/            # Agent nodes (think, act, observe)
│   │   ├── agent_node.py  # Main agent logic
│   │   └── tool_node.py   # Tool execution
│   ├── api/               # FastAPI server
│   │   ├── server.py      # API endpoints
│   │   └── models.py      # Request/response models
│   ├── config/            # Configuration
│   │   └── settings.py    # Environment settings
│   ├── events/            # Event system for streaming
│   │   ├── emitter.py     # Event emitter
│   │   └── middleware.py  # Streaming middleware
│   ├── graph/             # LangGraph workflow
│   │   ├── workflow.py    # Workflow definition
│   │   └── checkpointer.py # State persistence
│   ├── models/            # Data models
│   │   └── state.py       # Agent state definition
│   ├── prompts/           # System prompts
│   │   └── agent_prompts.py
│   └── tools/             # Agent tools
│       ├── basic_tools.py        # Utility tools
│       ├── document_search.py    # Vector search
│       └── ticket_tools.py       # Ticket management
├── tests/                 # Unit tests
├── scripts/               # Utility scripts
├── documents/             # IT policy documents
└── vector_store/          # FAISS index
```

## Workflow Pattern

The system implements the **Think → Act → Observe** pattern:

```
START
  ↓
agent (THINK) - Analyze request, decide on tools
  ↓
tools (ACT) - Execute document search, ticket operations
  ↓
observe - Process results
  ↓
router (DECIDE) - Continue, escalate, or end
  ↓
END or loop back to agent
```

## Available Tools

### Document Search
- `search_it_policy` - Search IT policies
- `search_troubleshooting_guide` - Search troubleshooting docs

### Ticket Management
- `create_ticket` - Create new tickets
- `get_ticket` - Retrieve ticket details
- `update_ticket_status` - Update status
- `add_ticket_comment` - Add comments
- `search_tickets` - Search tickets

### Utilities
- `get_current_time` - Get current timestamp

## Configuration

Edit `.env` file:

```bash
# Required
TYPHOON_API_KEY=your_api_key_here

# API Configuration
TYPHOON_BASE_URL=https://api.opentyphoon.ai/v1
TYPHOON_MODEL=typhoon-v2.5-30b-a3b-instruct

# Agent Settings
TEMPERATURE=0.7          # Response creativity
MAX_TOKENS=1024          # Response length
MAX_ITERATIONS=10        # Max workflow loops

# Checkpointer (memory)
CHECKPOINTER_TYPE=memory  # or "sqlite"
SQLITE_CHECKPOINT_PATH=./checkpoints.db
```

See [TYPHOON_SETUP.md](TYPHOON_SETUP.md) for detailed configuration.

## Testing

```bash
# Run all tests
uv run pytest -v

# With coverage
uv run pytest --cov=src --cov-report=html

# Specific test file
uv run pytest tests/test_api.py -v

# Specific test
uv run pytest tests/test_api.py::test_health -v
```

## API Endpoints

- `GET /health` - Health check
- `POST /chat` - Standard chat (JSON response)
- `POST /chat/stream` - Streaming chat (SSE)
- `POST /tickets` - Create ticket
- `GET /tickets/{id}` - Get ticket details

API docs: http://localhost:8000/docs

## Development

### Adding a New Tool

1. Create tool in `src/typhoon_it_support/tools/`
2. Export from `tools/__init__.py`
3. Add tests in `tests/`
4. Document in tool docstring

Example:
```python
def your_tool(param: str) -> str:
    """Brief description.
    
    Args:
        param: Parameter description
        
    Returns:
        Result description
    """
    return process(param)
```

### Running Evaluation

```bash
python scripts/run_evaluation.py
```

### Code Quality

```bash
# Format
uv run black src/ tests/

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

## Documentation

- **[Typhoon Setup](TYPHOON_SETUP.md)** - Typhoon API configuration
- **[Checkpointer](docs/CHECKPOINTER.md)** - Memory management
- **[Event System](docs/EVENT_SYSTEM.md)** - Streaming implementation
- **[Tools](docs/TOOLS.md)** - Complete tool reference
- **[Usage Examples](docs/USAGE_EXAMPLES.md)** - Practical examples

For general documentation, see:
- **[Getting Started](../docs/GETTING_STARTED.md)** - Setup guide
- **[Architecture](../docs/ARCHITECTURE.md)** - System design
- **[Extending](../docs/EXTENDING.md)** - Add features
- **[Best Practices](../docs/BEST_PRACTICES.md)** - Agentic principles

## Performance

- First token: 0.5-1 second
- Full response: 2-5 seconds
- Document search: <200ms
- Ticket operations: <50ms (mock)

## Troubleshooting

### Vector Store Issues
```bash
python scripts/init_vector_store.py
```

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

### API Key Errors
```bash
cat .env | grep TYPHOON_API_KEY
# Verify key is set correctly
```

### Import Errors
```bash
uv pip install -e ".[dev]"
```

## License

MIT

---

**Part of the Typhoon IT Support example project**

See [main README](../README.md) for complete system documentation.