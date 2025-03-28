import jwt
import pydantic
import typing
from app.pkg import models
from app.pkg.settings import settings
import time
from app.internal.services.user_service import UserService
from app.internal.services.crypto_service import CryptoService


class AuthService:

	__user_service: UserService
	__crypto_service: CryptoService

	def __init__(
		self,
		user_service: UserService,
		crypto_service: CryptoService
	):
		self.__user_service = user_service
		self.__crypto_service = crypto_service

	@staticmethod
	def generate_access_token(user: models.app.user_schema.User) -> pydantic.StrictStr:
		return jwt.encode(
			payload={
				**user.to_jwt(),
				"exp": int(time.time() + settings.JWT.EXPIRE_TIME_ACCESS),
				"type": models.app.user_schema.JwtType.ACCESS.value,
			},
			key=settings.JWT.SECRET_KEY.get_secret_value(),
			algorithm="HS256",
		)

	@staticmethod
	def generate_refresh_token(user: models.app.user_schema.User) -> pydantic.StrictStr:
		return jwt.encode(
			payload={
				"id": str(user.id),
				"exp": int(time.time() + settings.JWT.EXPIRE_TIME_REFRESH),
				"type": models.app.user_schema.JwtType.REFRESH.value,
			},
			key=settings.JWT.SECRET_KEY.get_secret_value(),
			algorithm="HS256",
		)

	def auth(self, token: pydantic.StrictStr) -> models.app.user_schema.User:
		try:
			user = self.decode(token=token)
			if user.type != models.app.user_schema.JwtType.ACCESS.value:
				raise models.exceptions.auth.JwtWrongType
			return user
		except jwt.ExpiredSignatureError:
			raise models.exceptions.auth.JwtExpired

	@staticmethod
	def decode(
		token: pydantic.StrictStr
	) -> typing.Union[models.app.user_schema.UserWithAccessToken, models.app.user_schema.UserWithRefreshToken]:
		try:
			data = jwt.decode(
				jwt=token,
				key=settings.JWT.SECRET_KEY.get_secret_value(),
				algorithms=["HS256"],
			)
			if data.get("type", None) == models.app.auth.JwtType.ACCESS.value:
				return models.app.user_schema.UserWithAccessToken(
					**data
				)
			if data.get("type", None) == models.app.auth.JwtType.REFRESH.value:
				return models.app.user_schema.UserWithRefreshToken(
					**data
				)
			raise models.exceptions.auth.JwtIncorrect
		except pydantic.ValidationError as e:
			raise models.exceptions.auth.JwtIncorrect

	async def login(self, cmd: models.app.auth.AuthRequest) -> models.app.auth.AuthResponse:
		user = await self.__user_service.read_by_login(cmd=cmd)
		if cmd.password.get_secret_value() != self.__crypto_service.decrypt(secret_str=user.password):
			raise models.exceptions.auth.CredentialsIncorrect

		return models.app.auth.AuthResponse(
			access_token=self.generate_access_token(user=user),
			refresh_token=self.generate_refresh_token(user=user)
		)

	async def refresh(self, cmd: models.app.auth.RefreshRequest):
		try:
			user: models.app.user_schema.User = await self.__user_service.read_by_id(
				cmd=self.decode(token=cmd.token.get_secret_value())
			)
			return models.app.auth.RefreshResponse(
				access=self.generate_access_token(user=user)
			)
		except jwt.ExpiredSignatureError:
			raise models.exceptions.auth.JwtExpired
