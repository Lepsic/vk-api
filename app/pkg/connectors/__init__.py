"""All connectors in declarative container."""

from dependency_injector import containers, providers

from app.pkg.connectors.postgresql import SqlAlchemy

__all__ = ["Connectors", "SqlAlchemy"]


class Connectors(containers.DeclarativeContainer):
    """Declarative container with all connectors."""

    postgresql: SqlAlchemy = providers.Container(SqlAlchemy)
