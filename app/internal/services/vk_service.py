from app.pkg import models
from app.pkg.vk_executor import vk_api_client_factory
from app.pkg.vk_executor.vk_user_executor import UserExecutor


class VkUserService:
	vk_api_client: UserExecutor

	def __init__(
		self,
	):
		self.vk_api_client = vk_api_client_factory(cls=UserExecutor)


	async def read_user_info(
		self,
		cmd: models.app.vk_api.user_api.ReadUserInfoCommand,
		user: models.app.user_schema.User
	):
		self.vk_api_client.setup(auth_token=user.auth_token.get_secret_value())
		return await self.vk_api_client.read_user_info(cmd=cmd)
