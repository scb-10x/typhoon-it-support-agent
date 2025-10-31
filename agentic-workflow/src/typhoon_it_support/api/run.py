"""Run the FastAPI server."""

import uvicorn

from ..config import get_settings


def main() -> None:
    """Start the FastAPI server."""
    settings = get_settings()
    
    uvicorn.run(
        "typhoon_it_support.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )


if __name__ == "__main__":
    main()

