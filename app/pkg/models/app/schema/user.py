import typing

from app.pkg.models.base import BaseModel, BaseEnum
from app.pkg.models.app.schema.auth import JwtType

import pydantic
__all__ = [
	"CreateUserCommand",
	"User",
	"UserWithAccessToken",
	"ReadUserByLoginCommand",
	"UserStatus",
	"ReadUserByIdCommand",
	"UserWithRefreshToken",
]


class UserStatus(BaseEnum):
	ACTIVE = "ACTIVE"
	BLOCKED = "BLOCKED"


class BaseUser(BaseModel):
	"""Base user model."""


class CreateUserCommand(BaseUser):
	login: str
	password: typing.Union[pydantic.SecretStr, pydantic.SecretBytes]
	username: str
	status: UserStatus = UserStatus.ACTIVE
	auth_token: pydantic.SecretStr


class CreateUserDbsCommand(CreateUserCommand):
	password: pydantic.SecretBytes


class User(BaseUser):
	id: pydantic.UUID4
	login: str
	username: str
	password: typing.Union[pydantic.SecretBytes, pydantic.SecretStr]
	auth_token: pydantic.SecretStr
	def to_jwt(self):
		d = self.to_dict(exlcluded=["password"])
		d["id"] = str(d["id"])
		return d


class UserWithAccessToken(BaseUser):
	id: pydantic.UUID4
	login: str
	username: str
	type: JwtType
	exp: int


class ReadUserByLoginCommand(BaseUser):
	login: str
	status: UserStatus


class ReadUserByIdCommand(BaseUser):
	id: pydantic.UUID4
	status: UserStatus = UserStatus.ACTIVE


class UserWithRefreshToken(BaseUser):
	id: pydantic.UUID4
	type: JwtType
