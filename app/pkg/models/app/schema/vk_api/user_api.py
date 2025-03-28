from app.pkg.models.base import BaseModel
import typing
import pydantic
__all__ = [
	"ReadUserInfoCommand",
	"ReadUserInfoCommandClient",
	"ResponseUserInfoClient",
]


class UserCounters(BaseModel):
	albums: typing.Optional[int] = None
	videos: typing.Optional[int] = None
	audios: typing.Optional[int] = None
	photos: typing.Optional[int] = None
	friends: typing.Optional[int] = None
	online_friends: typing.Optional[int] = None
	mutual_friends: typing.Optional[int] = None
	followers: typing.Optional[int] = None
	subscriptions: typing.Optional[int] = None


class ReadUserInfoCommand(BaseModel):
	user_id: str


class ReadUserInfoCommandClient(BaseModel):
	user_ids: str
	fields:  typing.List[str] = ["first_name", "last_name", "counters"]


class ResponseUserInfoClient(BaseModel):
	first_name: str
	last_name: str
	id: int
	status: str
	counters: typing.Optional[UserCounters]

