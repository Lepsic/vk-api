from app.pkg.models.base.vk_api_base import BaseVkApiModelRequest
import httpx
import typing
import abc
import inspect

base_request = typing.TypeVar(name="base_request", bound=BaseVkApiModelRequest)

available_methods = typing.Literal["GET"]




class _BaseVkApiClient(abc.ABC):
	__header: typing.Dict
	__params: httpx.QueryParams
	base_url = "https://api.vk.com/method"
	version_api = "5.199"

	def __init__(
		self,
		auth_token: base_request,
	):
		self.__params = httpx.QueryParams({"v": "5.199"})
		self.setup(auth_token)


	async def request(
		self,
		path: str,
		method: available_methods
	) -> typing.Dict:

		async with httpx.AsyncClient() as client:

			r = await client.request(
				method=method,
				params=self.__params,
				url="/".join([self.base_url, path])
			)
			if r.is_success:
				return r.json()
			raise Exception




	def _extend_query_parameters(self, d: dict):
		self.__params.update(**d)


	@abc.abstractmethod
	def 	setup(self, auth_token: base_request):
		pass


vk_api_client = typing.TypeVar("vk_api_client", bound=_BaseVkApiClient)



class VkApiClientFactory:

	def __call__(self, cls: typing.Type[vk_api_client], **kwargs):
		if issubclass(cls, _BaseVkApiClient):
			raise TypeError("Error type factory")
		return cls(**kwargs)



