from app.pkg.vk_executor.base import _BaseVkApiClient
from app.pkg import models



class UserExecutor(_BaseVkApiClient):

	# noinspection PyTypeChecker
	async def read_user_info(
		self,
		cmd: models.app.vk_api.user_api.ReadUserInfoCommand,
	) -> models.app.vk_api.user_api.ResponseUserInfoClient:

		response = await self.request(
			method="GET",
			path="users.get",
			params=models.app.vk_api.user_api.ReadUserInfoCommandClient.to_query(
				data=models.app.vk_api.user_api.ReadUserInfoCommandClient(
					user_ids=cmd.user_id,
				)
			)
		)
		return response

	# noinspection PyTypeChecker
	async def read_user_walls(
		self,
		cmd: models.app.vk_api.user_api.ReadWallsCommand
	) -> models.app.vk_api.user_api.ResponseWallsClient:
		response = await self.request(
			method="GET",
			path="wall.get",
			params=cmd.to_dict()
		)
		return response.json().get("response")


