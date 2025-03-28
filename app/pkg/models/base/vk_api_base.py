from app.pkg.models.base.model import BaseModel
from pydantic import SecretStr

__all__ = [
	"BaseVkApiModelRequest",
]


class BaseVkApiModelRequest(BaseModel):

	token: SecretStr


class BaseVkApiUser(BaseVkApiModelRequest):
	user_id: str
