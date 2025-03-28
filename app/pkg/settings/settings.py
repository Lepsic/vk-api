"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic_settings import BaseSettings



__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables.

    Examples:
        `.env` file should look like::

            TELEGRAM__TOKEN=...
            TELEGRAM__WEBHOOK_DOMAIN_URL=...

            LOGGER__PATH_TO_LOG="./src/logs"
            LOGGER__LEVEL="DEBUG"

            API_SERVER__HOST="127.0.0.1"
            API_SERVER__PORT=9191

    Warnings:
        In the case where a value is specified for the same Settings field in multiple
        ways, the selected value is determined as follows
        (in descending order of priority):

        1. Arguments passed to the Settings class initializer.
        2. Environment variables, e.g., my_prefix_special_function as described above.
        3. Variables loaded from a dotenv (.env) file.
        4. Variables loaded from the secrets directory.
        5. The default field values for the Settings model.

    See Also:
        https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True
        #: Literal['allow', 'ignore', 'forbid'] ignore extra
        extra = "ignore"
        #: bool: case-sensitive for env variables.
        case_sensitive = True
        #: str: delimiter for nested env variables.
        env_nested_delimiter = "__"


class Jwt(_Settings):
    SECRET_KEY: pydantic.SecretStr
    EXPIRE_TIME_ACCESS: pydantic.PositiveInt
    EXPIRE_TIME_REFRESH: pydantic.PositiveInt


class TransactionService(_Settings):
    URL: pydantic.AnyUrl
    TOKEN: pydantic.SecretStr


class Secret(_Settings):
    PASSWORD_CRYPTO_KEY: pydantic.SecretStr


class Postgresql(_Settings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: pydantic.StrictStr
    DATABASE: str
    SCHEMA: str
    DRIVER: str = "asyncpg"

    def get_alchemy_dsn(self) -> str:
        return f"{self.SCHEMA}+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    def get_migration_dsn(self) -> str:
        return f"{self.SCHEMA}+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev` if server running with parameter
    `dev`.
    """
    POSTGRES_AUTH: Postgresql
    JWT: Jwt
    SECRET: Secret
    TRANSACTION: TransactionService



@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
