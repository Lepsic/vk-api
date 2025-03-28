from app.internal.repository.postgresql.user import UserRepository
from app.internal.services.crypto_service import CryptoService
from app.pkg import models

__all__ = [
	"UserService",
]


class UserService:
	__user_service: UserRepository
	__crypto_service: CryptoService

	def __init__(
		self,
		user_repository: UserRepository,
		crypto_service: CryptoService,
	):
		self.__user_repository = user_repository
		self.__crypto_service = crypto_service

	async def create(self, cmd: models.app.user_schema.CreateUserCommand):
		cmd.password = self.__crypto_service.encrypt(cmd.password)

		user = await self.__user_repository.create(cmd=cmd)

		return user

	async def read_by_login(self, cmd: models.app.auth.AuthRequest) -> models.app.user_schema.User:

		user = await self.__user_repository.read_by_login(
			cmd=models.app.user_schema.ReadUserByLoginCommand(
				login=cmd.login,
				status=models.app.user_schema.UserStatus.ACTIVE,
			)
		)
		return user

	async def read_by_id(self, cmd: models.app.user_schema.UserWithRefreshToken) -> models.app.user_schema.User:

		return await self.__user_repository.read_by_id(
			cmd=models.app.user_schema.ReadUserByIdCommand(
				id=cmd.id,
				status=models.app.user_schema.UserStatus.ACTIVE,
			)
		)
