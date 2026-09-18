
"""Main entry point for the FastAPI Shipment Management application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.router import router
from core.config import settings
from database.session import create_database_tables

# Configure application logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shipment_api")

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    """
    Run startup and shutdown tasks for the FastAPI application.

    Creates database tables before accepting incoming requests.
    """
    logger.info("Creating database tables...")
    await create_database_tables()
    logger.info("Application startup complete.")

    yield

    logger.info("Application shutdown complete.")


# Initialize the FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan_handler,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register rate-limit state and error handler on the FastAPI app instance
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

# Configure CORS middleware on the main app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach the modular API router
app.include_router(router)