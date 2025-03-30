from app.pkg.models.base import BaseModel
import typing
import pydantic
__all__ = [
	"ReadUserInfoCommand",
	"ReadUserInfoCommandClient",
	"ResponseUserInfoClient",
	"ReadWallsCommand",
	"ResponseWallsClient"
]


class UserCounters(BaseModel):
	videos: typing.Optional[int] = None
	followers: typing.Optional[int] = None


class ReadUserInfoCommand(BaseModel):
	user_id: str


class ReadUserInfoCommandClient(BaseModel):
	user_ids: str
	fields:  typing.List[str] = ["first_name", "last_name", "counters", "online"]

	@classmethod
	def to_query(cls, data: "ReadUserInfoCommandClient"):
		return {"user_ids": data.user_ids, "fields": ",".join(data.fields)}



class ResponseUserInfoClient(BaseModel):
	first_name: str
	last_name: str
	id: int
	online: bool
	counters: typing.Optional[UserCounters]


class ReadWallsCommand(BaseModel):
	owner_id: int
	count: int = 1


class ResponseWallsClient(BaseModel):
	count: int

