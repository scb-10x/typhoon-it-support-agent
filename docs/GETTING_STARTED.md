# Getting Started

Complete guide to setting up and running the Typhoon IT Support system.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.12+** installed
- **Node.js 18+** and **pnpm** installed
- **Typhoon API key** from [opentyphoon.ai](https://opentyphoon.ai)
- Basic familiarity with terminal/command line

## Step 1: Get Your Typhoon API Key

1. Visit **https://opentyphoon.ai**
2. Sign up or log in to your account
3. Navigate to the API keys section
4. Generate a new API key
5. Copy and save your API key securely

## Step 2: Clone and Setup

```bash
# Navigate to your project directory
cd typhoon-it-support

# Install backend dependencies
cd agentic-workflow
uv pip install -e ".[dev]"

# Install frontend dependencies
cd ../frontend
pnpm install
```

## Step 3: Configure Backend

### Create Environment File

```bash
cd agentic-workflow
cp .env.example .env
```

### Edit `.env` File

Open `.env` in your text editor and add your configuration:

```bash
# Required: Your Typhoon API key
TYPHOON_API_KEY=your_actual_api_key_here

# API Configuration
TYPHOON_BASE_URL=https://api.opentyphoon.ai/v1
TYPHOON_MODEL=typhoon-v2.5-30b-a3b-instruct

# Agent Settings
TEMPERATURE=0.7          # 0.0-1.0 (higher = more creative)
MAX_TOKENS=1024          # Maximum response length
MAX_ITERATIONS=10        # Max workflow iterations

# Optional: Checkpointer (memory)
CHECKPOINTER_TYPE=memory  # "memory" or "sqlite"
SQLITE_CHECKPOINT_PATH=./checkpoints.db

# Debug Mode
DEBUG=false
```

## Step 4: Initialize Vector Store

The document search feature requires a vector store:

```bash
cd agentic-workflow
python scripts/init_vector_store.py
```

This will:
- Load IT policy documents
- Load troubleshooting guides
- Create FAISS embeddings
- Save to `vector_store/`

## Step 5: Test Your Configuration

### Quick API Test

```bash
cd agentic-workflow
cat > test_connection.py << 'EOF'
import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("TYPHOON_API_KEY"),
    base_url=os.getenv("TYPHOON_BASE_URL")
)

response = client.chat.completions.create(
    model=os.getenv("TYPHOON_MODEL"),
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=50
)

print("✅ Connection successful!")
print(f"Response: {response.choices[0].message.content}")
EOF

uv run python test_connection.py
```

## Step 6: Start the System

You'll need **two separate terminal windows**.

### Terminal 1: Start Backend

```bash
cd typhoon-it-support
./start-backend.sh
```

Wait for the message:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend

```bash
cd typhoon-it-support
./start-frontend.sh
```

Wait for:
```
✓ Ready in 2-3s
Local: http://localhost:3000
```

## Step 7: Access the Application

Open your browser and go to:

**http://localhost:3000**

You should see the IT Support chat interface!

## Try It Out

Try asking these questions:

**English:**
- "I need help resetting my password"
- "My WiFi isn't working"
- "Computer running slowly"

**Thai:**
- "ช่วยแก้ปัญหาคอมพิวเตอร์ช้าหน่อย"
- "ฉันจะรีเซ็ตรหัสผ่านได้อย่างไร"
- "WiFi ของฉันเชื่อมต่อไม่ได้"

## Troubleshooting

### Backend Won't Start

**Check API Key:**
```bash
cd agentic-workflow
cat .env | grep TYPHOON_API_KEY
# Should show: TYPHOON_API_KEY=your_key_here
```

**Reinstall Dependencies:**
```bash
cd agentic-workflow
uv pip install -e ".[dev]"
```

**Free Port 8000:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Frontend Won't Start

**Reinstall Dependencies:**
```bash
cd frontend
rm -rf node_modules
pnpm install
```

**Free Port 3000:**
```bash
lsof -ti:3000 | xargs kill -9
```

### Vector Store Errors

**Rebuild Vector Store:**
```bash
cd agentic-workflow
rm -rf vector_store/
python scripts/init_vector_store.py
```

### API Connection Errors

1. Verify API key is correct
2. Check internet connection
3. Ensure base URL is correct
4. Try the test script again

### No Responses or Errors

**Check Backend Health:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"0.1.0"}
```

**Check Backend Logs:**
```bash
# Look for errors in terminal running backend
# Or check logs/backend.log
```

**Check Browser Console:**
- Open browser DevTools (F12)
- Look for network errors
- Check console for JavaScript errors

## Configuration Options

### Temperature Settings

Controls response creativity:

- **0.0-0.3**: Precise, deterministic (good for technical support)
- **0.4-0.7**: Balanced (default, recommended)
- **0.8-1.0**: Creative, varied responses

### Max Tokens

Controls response length:

- **256-512**: Short, concise answers
- **512-1024**: Detailed explanations (default)
- **1024-2048**: Comprehensive, thorough responses

### Checkpointer Types

**Memory (Development):**
```bash
CHECKPOINTER_TYPE=memory
```
- Fast, in-memory storage
- Lost on restart
- Good for development

**SQLite (Production):**
```bash
CHECKPOINTER_TYPE=sqlite
SQLITE_CHECKPOINT_PATH=./checkpoints.db
```
- Persistent storage
- Survives restarts
- Good for production

## Next Steps

- **[Architecture](ARCHITECTURE.md)** - Understand the system design
- **[Extending](EXTENDING.md)** - Add your own tools and features
- **[Best Practices](BEST_PRACTICES.md)** - Learn agentic system principles
- **[API Reference](API.md)** - Explore REST endpoints

## Development Mode

### Run Tests

```bash
cd agentic-workflow
uv run pytest -v
```

### With Coverage

```bash
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Run Evaluation Suite

```bash
python scripts/run_evaluation.py
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

## Stopping the System

### Stop Both Servers

```bash
./stop-all.sh
```

### Stop Individual Services

**Backend:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Frontend:**
```bash
lsof -ti:3000 | xargs kill -9
```

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review logs in `logs/` directory
3. Verify all prerequisites are installed
4. Ensure API key is valid and active
5. Check [Typhoon documentation](https://docs.opentyphoon.ai)

---

**Ready to build? Start exploring the [Architecture](ARCHITECTURE.md) next!**


