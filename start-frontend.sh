#!/bin/bash
# Start the Next.js frontend server

echo "🎨 Starting IT Support Frontend..."
echo "=================================="

cd frontend

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo "✅ Created .env.local with default backend URL"
    echo ""
fi

# Check if node_modules exists
if [ ! -d node_modules ]; then
    echo "📦 Installing dependencies..."
    pnpm install
    echo ""
fi

echo "Starting frontend on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""

pnpm dev

