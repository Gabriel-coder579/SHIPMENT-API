"""Database engine and FastAPI session dependency."""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from core.config import settings


# The engine manages connections between the application and the database.
engine = create_async_engine(
    # Database type/dialect and file name.
    url=settings.database_url,
    # Log sql queries
    echo=True,

)


async def create_database_tables() -> None:
    """Create all SQLModel tables that do not already exist."""
    from models.models import Shipment

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    """
    Provide one database session for a request.

    The context manager closes the session automatically after the request,
    which helps prevent connection and resource leaks.
    """
    async with session_maker() as session:
        yield session


# This type alias keeps endpoint function signatures short and readable.
SessionDep = Annotated[AsyncSession, Depends(get_session)]
