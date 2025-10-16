"""Database connection and session management."""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)

# Global engine and session maker
engine = None
async_session_maker = None


def init_database(database_url: str, echo: bool = False) -> None:
    """Initialize database engine and session maker."""
    global engine, async_session_maker

    logger.info(f"Initializing database connection: {database_url.split('@')[-1]}")
    engine = create_async_engine(database_url, echo=echo, pool_pre_ping=True)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    logger.info("Database initialized successfully")


async def close_database() -> None:
    """Close database connections."""
    global engine

    if engine:
        logger.info("Closing database connections")
        await engine.dispose()
        logger.info("Database connections closed")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session.

    Usage:
        async with get_session() as session:
            # use session
    """
    if async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
