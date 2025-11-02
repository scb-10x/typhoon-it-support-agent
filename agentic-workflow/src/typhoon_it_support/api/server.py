"""FastAPI server implementation."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config.user_context import get_current_user, get_company_info
from .models import HealthResponse, UserInfo, UserSessionResponse
from .chat_endpoints import router as chat_router
from .ticket_endpoints import router as ticket_router
from .ticket_advanced_endpoints import router as ticket_advanced_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events.
    
    Args:
        app: FastAPI application instance.
        
    Yields:
        None during application runtime.
    """
    # Startup
    from .init_demo_tickets import initialize_demo_tickets
    count = initialize_demo_tickets()
    print(f"✅ Initialized {count} demo tickets")
    
    yield
    
    # Shutdown (if needed)
    pass


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title="Typhoon IT Support API",
        description="API for IT support agentic workflow",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS configuration for frontend - allow all origins in development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://0.0.0.0:3000",
            "http://0.0.0.0:3001",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )

    # Include routers
    app.include_router(chat_router)
    app.include_router(ticket_router)
    app.include_router(ticket_advanced_router)

    return app


# Create the application instance
app = create_app()


@app.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """Root endpoint with health check."""
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@app.get("/user/session", response_model=UserSessionResponse)
async def get_user_session() -> UserSessionResponse:
    """Get current user session information.
    
    Returns the logged-in user's profile and company information.
    In this hypothetical scenario, we always return the mock user.
    """
    user_profile = get_current_user()
    company_info = get_company_info()
    
    return UserSessionResponse(
        user=UserInfo(**user_profile.to_dict()),
        company=company_info,
        session_id=None
    )

