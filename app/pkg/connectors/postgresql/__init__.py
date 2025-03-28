"""Container with PostgresSQL connector."""

from dependency_injector import containers, providers

from app.pkg.connectors.postgresql.resource import Sqlalchemy
from app.pkg.settings import settings

__all__ = ["SqlAlchemy"]


class SqlAlchemy(containers.DeclarativeContainer):
    """Declarative container with PostgresSQL connector."""

    configuration = providers.Configuration(
        name="settings",
        pydantic_settings=[settings],
    )

    connector = providers.Singleton(
        Sqlalchemy,
        dsn=settings.POSTGRES_AUTH.get_alchemy_dsn(),
    )
