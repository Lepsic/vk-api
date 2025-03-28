from app.pkg.vk_executor.base import _BaseVkApiClient
from app.pkg.models.base.vk_api_base import BaseVkApiUser
from app.pkg import models



class UserExecutor(_BaseVkApiClient):


	async def read_user_info(
		self,
		cmd: models.app.vk_api.user_api.ReadUserInfoCommand,
	) -> models.app.vk_api.user_api.ResponseUserInfoClient:
		self._extend_query_parameters(models.app.vk_api.user_api.ReadUserInfoCommandClient(
			user_ids=cmd.user_id,
		).to_dict())
		r = await self.request(
			method="GET",
			path="users.get",
		)
		return models.app.vk_api.user_api.ResponseUserInfoClient(**r)

	async def read_user_post(self):
		"""TODO по аналогии"""

	async def read_user_video(self):
		"""TODO по аналогии"""

	async def read_video_info(self):
		"""TODO по аналогии"""



	def setup(self, auth_token: str):
		self._extend_query_parameters(d={"access_token": auth_token})
