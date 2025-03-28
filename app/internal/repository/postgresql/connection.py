"""Create connection to postgresql."""

from contextlib import asynccontextmanager
from typing import Union
from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.pkg.connectors.postgresql.resource import Sqlalchemy

from app.pkg.connectors import Connectors

__all__ = ["get_connection", "acquire_connection"]


@asynccontextmanager
@inject
async def get_connection(
    engine: Sqlalchemy = Provide[Connectors.postgresql.connector],
    returned_engine: bool = False,
    returned_session: bool = False,
) -> Union[AsyncEngine, AsyncSession]:
    """Get async connection pool to postgresql.

    Args:
        engine:
            Sqlalchimy angine.
        returned_engine:
            if True, return engine.
        returned_session:
            if True, return sessionmaker


    Examples:
        If you have a function that contains a query in postgresql,
        context manager :func:`.get_connection`
        will get async connection to postgresql
        of pool::

            >>> async def exec_some_sql_function() -> None:
            ...     async with get_connection() as c:
            ...         await c.execute("SELECT * FROM users")

    Returns:
        Async connection to postgresql.
    """

    if returned_engine:
        yield engine.get_engine()
        return
    if returned_session:
        yield engine.get_session()
    async with acquire_connection(session=engine.get_session()) as session:
        yield session


@asynccontextmanager
async def acquire_connection(
    session: sessionmaker,
) -> AsyncSession:
    """Acquire connection from pool.

    Args:
        session:
            Getings from :func:`.get_connection` sqlalchemy session.

    Examples:
        If you have a function that contains a query in postgresql,
        context manager :func:`.acquire_connection`
        will get async connection to postgresql
        of pool::

            >>> async def exec_some_sql_function() -> None:
            ...     q = "select * from users;"
            ...     async with get_connection(return_pool=True) as __pool:
            ...         async with acquire_connection(__pool) as _cursor:
            ...             await _cursor.execute(q)
            ...         async with acquire_connection(__pool) as _cursor:
            ...             await _cursor.execute(q)

    Returns:
        Async connection to postgresql.
    """

    async with session() as s:
        yield s
