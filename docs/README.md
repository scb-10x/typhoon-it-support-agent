# Documentation

Complete documentation for the Typhoon IT Support agentic workflow example.

## Getting Started

New to this project? Start here:

1. **[Getting Started](GETTING_STARTED.md)** - Complete setup guide
   - Prerequisites and installation
   - Configuration
   - Running the system
   - Troubleshooting

2. **[Main README](../README.md)** - Project overview
   - Quick start
   - Features
   - Technology stack

## Understanding the System

Learn how it works:

3. **[Architecture](ARCHITECTURE.md)** - System design
   - Component overview
   - Workflow pattern
   - Data flow
   - State management

4. **[API Reference](API.md)** - REST endpoints
   - Chat endpoints
   - Ticket management
   - Request/response models
   - Examples

## Extending & Customizing

Build on top of this:

5. **[Extending](EXTENDING.md)** - Add features
   - Creating tools
   - Adding agent nodes
   - Custom state fields
   - Best practices

6. **[Best Practices](BEST_PRACTICES.md)** - Agentic principles
   - Evaluation-driven development
   - Context engineering
   - Prompt engineering
   - Tool design

## Implementation Details

Technical deep-dives:

7. **[Thai Localization](THAI_LOCALIZATION.md)** - Language strategy
   - Design principles
   - Implementation details
   - Best practices

### Backend Documentation

In `agentic-workflow/`:

- **[Typhoon Setup](../agentic-workflow/TYPHOON_SETUP.md)** - Typhoon API configuration
- **[Backend README](../agentic-workflow/README.md)** - Backend overview

In `agentic-workflow/docs/`:

- **[Checkpointer](../agentic-workflow/docs/CHECKPOINTER.md)** - Memory management
- **[Event System](../agentic-workflow/docs/EVENT_SYSTEM.md)** - Streaming implementation
- **[Tools](../agentic-workflow/docs/TOOLS.md)** - Complete tool reference
- **[Usage Examples](../agentic-workflow/docs/USAGE_EXAMPLES.md)** - Practical scenarios

## Quick Reference

### Start the System

```bash
# Terminal 1
./start-backend.sh

# Terminal 2
./start-frontend.sh
```

### Configuration

Key environment variables in `agentic-workflow/.env`:

```bash
TYPHOON_API_KEY=your_key_here
TEMPERATURE=0.7
MAX_TOKENS=1024
```

### Testing

```bash
cd agentic-workflow
uv run pytest -v
```

### Adding a Tool

```python
# In tools/your_tool.py
def your_tool(param: str) -> str:
    """Tool description."""
    return result
```

## Project Structure

```
typhoon-it-support/
├── README.md                    # Main overview
├── docs/                        # User documentation
│   ├── README.md               # This file
│   ├── GETTING_STARTED.md      # Setup guide
│   ├── ARCHITECTURE.md         # System design
│   ├── EXTENDING.md            # How to extend
│   ├── API.md                  # API reference
│   ├── BEST_PRACTICES.md       # Agentic principles
│   └── THAI_LOCALIZATION.md    # Language strategy
│
├── agentic-workflow/            # Backend
│   ├── README.md               # Backend overview
│   ├── TYPHOON_SETUP.md        # Typhoon config
│   ├── src/                    # Source code
│   ├── tests/                  # Tests
│   └── docs/                   # Technical docs
│
└── frontend/                    # Frontend
    └── README.md               # Frontend docs
```

## Learning Path

### For Beginners

1. Read [Main README](../README.md)
2. Follow [Getting Started](GETTING_STARTED.md)
3. Explore the running system
4. Read [Architecture](ARCHITECTURE.md)

### For Developers

1. Understand [Architecture](ARCHITECTURE.md)
2. Study [Best Practices](BEST_PRACTICES.md)
3. Review [API Reference](API.md)
4. Learn [Extending](EXTENDING.md)
5. Explore backend code in `agentic-workflow/src/`

### For Advanced Users

1. Deep dive into agentic-workflow implementation
2. Study [Checkpointer](../agentic-workflow/docs/CHECKPOINTER.md)
3. Understand [Event System](../agentic-workflow/docs/EVENT_SYSTEM.md)
4. Review all [Usage Examples](../agentic-workflow/docs/USAGE_EXAMPLES.md)
5. Implement custom features

## Additional Resources

### External Documentation

- **Typhoon AI**: https://docs.opentyphoon.ai
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **FastAPI**: https://fastapi.tiangolo.com
- **Next.js**: https://nextjs.org/docs

### Example Code

- Tests in `agentic-workflow/tests/`
- Scripts in `agentic-workflow/scripts/`
- Components in `frontend/app/components/`

## Support

Need help?

1. Check [Getting Started](GETTING_STARTED.md) troubleshooting
2. Review [Architecture](ARCHITECTURE.md) for understanding
3. Look at code examples in tests/
4. Check external documentation links

## Contributing

This is a reference implementation. Feel free to:

- Fork and customize
- Add new features
- Share improvements
- Report issues

---

**Ready to start?** Begin with [Getting Started](GETTING_STARTED.md)!


