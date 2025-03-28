from app.pkg.models.base import BaseModel
import pydantic

__all__ = [
	"CreateBalance",
]


class BaseTransaction(BaseModel):
	pass


class CreateBalance(BaseTransaction):
	user_id: pydantic.UUID4
