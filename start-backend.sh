#!/bin/bash
# Start the FastAPI backend server

echo "🚀 Starting IT Support Backend..."
echo "================================"

cd agentic-workflow

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Warning: OPENAI_API_KEY not configured in .env"
    echo "Please edit agentic-workflow/.env and add your OpenAI API key"
    echo ""
fi

echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

uv run python -m src.typhoon_it_support.api.run

