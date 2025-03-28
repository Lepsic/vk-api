import pydantic
from app.pkg.models.base import BaseModel, BaseEnum

__all__ = [
	"JwtType",
	"AuthRequest",
	"AuthResponse",
]


class JwtType(BaseEnum):
	ACCESS = "access"
	REFRESH = "refresh"


class BaseAuthModel(BaseModel):
	pass


class AuthRequest(BaseModel):
	login: str
	password: pydantic.SecretStr


class AuthResponse(BaseAuthModel):
	access_token: pydantic.StrictStr
	refresh_token: pydantic.StrictStr


class RefreshRequest(BaseAuthModel):
	token: pydantic.SecretStr


class RefreshResponse(BaseAuthModel):
	access: pydantic.SecretStr
