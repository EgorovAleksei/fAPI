from typing import AsyncGenerator

from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    AsyncEngine,
)

from core.config import settings


class DBEngine:
    """https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine"""

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    def get_scope_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            # await session.close()

    async def scope_session_dependency(self) -> AsyncSession:
        session = self.get_scope_session()
        yield session
        await session.close()


db = DBEngine(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
