#!/bin/bash

# Test runner script for Typhoon IT Support

set -e

echo "🧪 Typhoon IT Support Test Runner"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    uv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if needed
if ! python -m pytest --version > /dev/null 2>&1; then
    echo "📥 Installing dependencies..."
    uv pip install -e ".[dev]"
fi

echo ""
echo "Running tests..."
echo ""

# Parse command line arguments
if [ "$1" == "all" ]; then
    echo "🔍 Running all tests..."
    python -m pytest tests/ -v
elif [ "$1" == "ticket-tools" ]; then
    echo "🎫 Running ticket tools tests..."
    python -m pytest tests/test_ticket_tools.py -v
elif [ "$1" == "ticket-api" ]; then
    echo "🌐 Running ticket API tests..."
    python -m pytest tests/test_ticket_api.py -v
elif [ "$1" == "coverage" ]; then
    echo "📊 Running tests with coverage..."
    python -m pytest tests/ --cov=src.typhoon_it_support --cov-report=html --cov-report=term
    echo ""
    echo "✅ Coverage report generated in htmlcov/index.html"
elif [ "$1" == "fast" ]; then
    echo "⚡ Running fast tests (unit tests only)..."
    python -m pytest tests/test_ticket_tools.py::TestRealUserScenarios -v
elif [ "$1" == "edge-cases" ]; then
    echo "🔬 Running edge case tests..."
    python -m pytest tests/test_ticket_tools.py::TestEdgeCases -v
elif [ "$1" == "integration" ]; then
    echo "🔗 Running integration tests..."
    python -m pytest tests/test_ticket_tools.py::TestIntegration tests/test_ticket_api.py::TestIntegrationAPI -v
elif [ "$1" == "performance" ]; then
    echo "🚀 Running performance tests..."
    python -m pytest tests/test_ticket_tools.py::TestPerformance -v
elif [ "$1" == "watch" ]; then
    echo "👀 Running tests in watch mode..."
    python -m pytest tests/ -v --looponfail
else
    echo "Usage: ./run_tests.sh [option]"
    echo ""
    echo "Options:"
    echo "  all           - Run all tests"
    echo "  ticket-tools  - Run ticket tools tests only"
    echo "  ticket-api    - Run ticket API tests only"
    echo "  coverage      - Run tests with coverage report"
    echo "  fast          - Run fast unit tests only"
    echo "  edge-cases    - Run edge case tests only"
    echo "  integration   - Run integration tests only"
    echo "  performance   - Run performance tests only"
    echo "  watch         - Run tests in watch mode"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh all"
    echo "  ./run_tests.sh ticket-tools"
    echo "  ./run_tests.sh coverage"
    exit 1
fi

echo ""
echo "✅ Tests completed!"

