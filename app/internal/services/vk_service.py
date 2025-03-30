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
			api_token: models.vk_api_base.BaseVkApiModelRequest,
	):
		self.vk_api_client.auth(auth_token=api_token)
		return await self.vk_api_client.read_user_info(cmd=cmd)

	async def read_wall_count(
			self,
			cmd: models.app.vk_api.user_api.ReadUserInfoCommand,
			api_token: models.vk_api_base.BaseVkApiModelRequest,
	):
		user_info = await self.read_user_info(
			cmd=models.app.vk_api.user_api.ReadUserInfoCommand(
				user_id=cmd.user_id
			),
			api_token=api_token,
		)

		return await self.vk_api_client.read_user_walls(
			cmd=models.app.vk_api.user_api.ReadWallsCommand(
				owner_id=user_info.id,
			)
		)

