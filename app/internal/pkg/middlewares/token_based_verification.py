"""Authentication middleware for token-based authentication."""

from fastapi import Security
from fastapi.security import APIKeyHeader

from app.pkg.models.exceptions.token_verification import InvalidCredentials
from app.pkg.settings import settings

__all__ = ["token_based_verification"]

x_api_key_header = APIKeyHeader(name="X-ACCESS-TOKEN")


async def token_based_verification(
    api_key_header: str = Security(x_api_key_header),
):

    value = settings.API.X_ACCESS_TOKEN.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials


