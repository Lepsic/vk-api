"""Async resource for PostgresSQL connector."""


from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.pkg.connectors import resources

__all__ = ["Sqlalchemy"]


class Sqlalchemy(resources.BaseResource):

    """PostgresSQL connector using aiopg."""
    __engine: AsyncEngine = None
    __session: sessionmaker = None
    dsn: str

    def get_engine(self) -> AsyncEngine:
        if self.__engine is None:
            self.__engine = create_async_engine(url=self.dsn)
        return self.__engine

    def get_session(self) -> sessionmaker:
        if self.__session is None:
            self.__session = sessionmaker(
                bind=self.get_engine(),
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return self.__session

    def __init__(self, dsn: str):
        """Getting connection pool in asynchronous.

        Args:
            dsn: D.S.N - Data Source Name.

        Returns:
            Created connection pool.
        """
        self.dsn = dsn
        self.get_engine()

    async def shutdown(self):
        """Close connection.

        Args:
            resource: Resource returned by :meth:`.Postgresql.init()` method.

        Notes:
            This method is called automatically
            when the application is stopped
            or
            ``Closing`` provider is used.
        """
        await self.__engine.dispose()
