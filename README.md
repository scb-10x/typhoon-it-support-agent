# Typhoon IT Support - Agentic Workflow Example

A **companion example project** demonstrating best practices for building agentic AI systems using **Typhoon 2.5** and **LangGraph**. This project showcases patterns for creating intelligent IT support assistants with real-time streaming, tool usage, and multi-turn conversations.

Please refer to this companion blog post for more details: 🇬🇧 [Mastering Agentic Workflows: 20 Principles That Works](https://opentyphoon.ai/blog/en/agentic-workflows-principles) | 🇹🇭 [20 หลักการเพื่อการออกแบบ Agentic Workflow อย่างมีประสิทธิภาพ](https://opentyphoon.ai/blog/th/agentic-workflows-principles)

> **Note**: This is an educational reference implementation designed to teach best practices. It is **not intended for production use** without significant customization and hardening.

## 🎯 What This Project Demonstrates

- **Agentic Workflows**: Implement Think → Act → Observe patterns with LangGraph
- **Typhoon Integration**: Use Thai-English bilingual AI (Typhoon 2.5) for IT support
- **Tool Orchestration**: Document search, ticket management, and utility tools
- **Event System**: Real-time streaming with Server-Sent Events (SSE)
- **Memory Management**: Session-based conversations with persistent state
- **Production Patterns**: Best practices for error handling, testing, and configuration
- **Demo Mode**: Simulated logged-in experience with pre-configured Thai employee profile

## 💡 Why This Project?

This companion project demonstrates best practices for building agentic AI systems:

✅ **Real-world Architecture**: Not just a toy example—shows proper state management, error handling, and testing patterns  
✅ **Bilingual Support**: Demonstrates Thai-English handling with culturally appropriate responses  
✅ **Streaming First**: Modern UX with token-by-token streaming, not blocking requests  
✅ **Tool Integration**: Shows how to give agents real capabilities (search, tickets, etc.)  
✅ **Production Patterns**: Demonstrates checkpointing, session management, monitoring, and testing approaches  
✅ **Extensible Design**: Easy to understand, modify, and adapt to your domain  

Perfect for developers learning about:
- Multi-agent systems with LangGraph
- Thai language AI applications
- Building IT support automation
- Streaming chat interfaces
- Agentic workflow patterns

## 🏗️ Architecture

The system follows a modern three-tier architecture with event-driven streaming:

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Next.js UI    │ ───► │  FastAPI Server  │ ───► │   LangGraph     │
│  (Port 3000)    │ HTTP │   (Port 8000)    │      │  Agent Workflow │
│  - Streaming    │      │  - Streaming SSE │      │  - Typhoon 2.5  │
│  - Markdown     │      │  - Session Mgmt  │      │  - Tools        │
│  - User Context │      │  - Event System  │      │  - State Mgmt   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

**Flow**: User input → Backend API → LangGraph workflow → Agent (Think) → Tools (Act) → Response streaming → Frontend display

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- pnpm
- Typhoon API key from [opentyphoon.ai](https://opentyphoon.ai)

### 1. Get Typhoon API Key

1. Visit https://opentyphoon.ai
2. Sign up and generate your API key
3. Keep it for the next step

### 2. Configure Backend

Create a `.env` file in the `agentic-workflow` directory:

```bash
cd agentic-workflow
```

Create `.env` file with the following content:
```bash
TYPHOON_API_KEY=your_actual_key_here
TYPHOON_BASE_URL=https://api.opentyphoon.ai/v1
TYPHOON_MODEL=typhoon-v2.5-30b-a3b-instruct
TEMPERATURE=0.7
MAX_TOKENS=1024
MAX_ITERATIONS=10
```

### 3. Install Dependencies

**Backend:**
```bash
cd agentic-workflow
uv pip install -e ".[dev]"
```

**Frontend:**
```bash
cd ../frontend
pnpm install
```

### 4. Initialize Vector Store

The document search requires a vector store. Initialize it with:

```bash
cd ../agentic-workflow
python scripts/init_vector_store.py
```

This will load IT policy documents and create FAISS embeddings.

### 5. Start the System

**Terminal 1 - Backend:**
```bash
./start-backend.sh
# Wait for: "Uvicorn running on http://0.0.0.0:8000"
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
# Wait for: "Ready in 2-3s"
```

### 6. Open Browser

Go to: **http://localhost:3000**

🎭 **Demo Mode**: The application simulates a logged-in employee experience. You'll be automatically logged in as:
- **Name**: Somchai Phimsawat (สมชาย พิมพ์สวัสดิ์)
- **Position**: Digital Marketing Specialist
- **Company**: BlueWave Technology Co., Ltd.
- **Department**: Marketing & Communications

See the profile information in the top-right corner!

**Try asking:**
- "ฉันต้องการใช้ Canva Pro สำหรับทำ campaign" (requesting marketing tools)
- "ช่วยแก้ปัญหาคอมพิวเตอร์ช้าหน่อย" (technical issues)
- "I need help resetting my password"
- "สร้าง ticket เพื่อขออุปกรณ์ใหม่"

## 📚 Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - Detailed setup and configuration
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Extending](docs/EXTENDING.md)** - How to add tools and features
- **[Best Practices](docs/BEST_PRACTICES.md)** - Agentic system principles
- **[API Reference](docs/API.md)** - REST endpoints and usage

## 🎯 Key Features

### Agentic Workflow Pattern
- **Think**: Agent decides what to do next
- **Act**: Execute tools (search docs, manage tickets)
- **Observe**: Process results and respond

### Real-Time Streaming
- Token-by-token streaming responses
- Server-Sent Events (SSE) for real-time updates

### Tool Orchestration
- Document search using FAISS vector store
- Ticket management (create, update, search, comment)
- Utility functions (time, formatting)

### Memory & State
- Session-based conversations
- LangGraph checkpointers for context
- Multi-turn dialogue support

## 📊 Project Structure

```
typhoon-it-support/
├── agentic-workflow/          # Backend - LangGraph + FastAPI
│   ├── src/typhoon_it_support/
│   │   ├── agents/            # Agent nodes (think, act, observe)
│   │   ├── api/               # FastAPI server with streaming
│   │   ├── config/            # Configuration management
│   │   ├── graph/             # LangGraph workflow
│   │   ├── tools/             # Agent tools
│   │   └── prompts/           # System prompts
│   ├── tests/                 # Comprehensive tests
│   └── docs/                  # Technical documentation
│
├── frontend/                  # Next.js + React
│   └── app/components/
│       └── Chat.tsx           # Streaming chat UI
│
├── docs/                      # Developer documentation
└── README.md                  # This file
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
cd agentic-workflow

# Run all tests
uv run pytest -v

# With coverage report
uv run pytest --cov=src --cov-report=html

# Test specific module
uv run pytest tests/test_api.py -v

# Test with verbose output
uv run pytest -vv

# Run fast tests only (exclude slow integration tests)
uv run pytest -m "not slow"
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

## 🔧 Configuration

### Backend Environment Variables

Edit `agentic-workflow/.env`:

```bash
# Required
TYPHOON_API_KEY=your_api_key_here

# API Configuration
TYPHOON_BASE_URL=https://api.opentyphoon.ai/v1
TYPHOON_MODEL=typhoon-v2.5-30b-a3b-instruct

# Agent Settings
TEMPERATURE=0.7          # Response creativity (0.0-1.0)
MAX_TOKENS=1024          # Maximum response length
MAX_ITERATIONS=10        # Max workflow iterations

# Checkpointer (memory management)
CHECKPOINTER_TYPE=memory  # "memory" or "sqlite"
SQLITE_CHECKPOINT_PATH=./checkpoints.db
```

### Configuration Options

- **Temperature**: Controls response creativity (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Maximum length of generated responses
- **Max Iterations**: Maximum workflow loops before stopping
- **Checkpointer**: Use "memory" for development, "sqlite" for production

## 🛠️ Development

### Adding a New Tool

```python
# In src/typhoon_it_support/tools/your_tool.py
def your_tool(param: str) -> str:
    """
    Brief description of what the tool does.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    return result
```

See [docs/EXTENDING.md](docs/EXTENDING.md) for complete examples.

## 🎓 Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Model | Typhoon 2.5 (30B) - Thai LLM |
| Workflow Engine | LangGraph - Agentic workflow orchestration |
| Backend Framework | FastAPI - Modern async Python web framework |
| Frontend | Next.js 16 (App Router) + React 19 |
| Language | Python 3.12+ / TypeScript |
| Styling | Tailwind CSS 4 - Utility-first CSS |
| Vector Store | FAISS - Semantic document search |
| Testing | pytest with coverage |
| Package Management | uv (Python), pnpm (Node.js) |

## 🤝 Using This Project

This is an **educational reference implementation** for learning and experimentation. You're encouraged to:

- **Fork and Learn**: Study the code to understand agentic workflow patterns
- **Customize**: Adapt this project as a starting point for your own applications
- **Experiment**: Try adding new tools, agents, or capabilities
- **Share**: Contribute improvements, examples, or documentation

**Important**: This project demonstrates best practices but requires additional security, scalability, and reliability work before being deployed in production environments.

## 🔍 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**API Key not working:**
- Verify your API key at https://opentyphoon.ai
- Check `.env` file has `TYPHOON_API_KEY=your_key`
- Ensure no extra spaces or quotes around the key

**Vector store errors:**
```bash
cd agentic-workflow
rm -rf vector_store/
python scripts/init_vector_store.py
```

### Frontend Issues

**Port 3000 already in use:**
```bash
lsof -ti:3000 | xargs kill -9
```

**Connection refused errors:**
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend environment
- Verify CORS settings in backend

**Module not found errors:**
```bash
cd frontend
rm -rf node_modules .next
pnpm install
```

### General Issues

**Dependencies not installing:**
- Update uv: `pip install -U uv`
- Update pnpm: `pnpm add -g pnpm`
- Check Python version: `python --version` (need 3.12+)
- Check Node version: `node --version` (need 18+)

**Logs location:**
- Backend logs: `logs/backend.log`
- Frontend logs: `logs/frontend.log`
- Check these for detailed error messages

For more help, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) troubleshooting section.

## 📄 License

[MIT License](LICENSE)

## 📚 Learning Resources

This project is designed as a hands-on companion for learning agentic AI development:

- **Project Documentation**: [docs/](docs/) - Detailed guides and architecture explanations
- **Typhoon AI**: https://opentyphoon.ai - Thai-English LLM platform
- **LangGraph**: https://langchain-ai.github.io/langgraph/ - Agent workflow framework

## 📞 Support & Community

- **Issues**: Report bugs or questions via GitHub Issues
- **Discussions**: Share your learnings and implementations
- **Fork**: Use this as a starting point for your own projects

---

**🌪️ Powered by Typhoon 2.5 - Thai Language AI by SCB 10X**

Built with ❤️ using LangGraph, FastAPI, and Next.js
