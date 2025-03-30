import functools

import pydantic
from app.pkg.models.base.vk_api_base import BaseVkApiModelRequest
import httpx
import typing
import inspect
from app.pkg.models.base import BaseModel

base_request = typing.TypeVar(name="base_request", bound=BaseVkApiModelRequest)
model = typing.TypeVar(name="model", bound=BaseModel)
available_methods = typing.Literal["GET"]


def collect_response(fn: typing.Callable[..., typing.Awaitable[httpx.Response]]):
	@functools.wraps(fn)
	async def wrapper(*args, **kwargs):
		annotation = inspect.getfullargspec(fn)
		return_annotation = annotation.annotations.get("return")
		adapter = pydantic.TypeAdapter(return_annotation)
		try:

			response: typing.Union[httpx.Response] = await fn(*args, **kwargs)
			if isinstance(response, httpx.Response):
				if response.json().get("error"):
					print(response.json().get("error"))
					raise ValueError
				response: dict | list = response.json().get("response")
				if len(response) == 1:
					return adapter.validate_python(response[0])
			return adapter.validate_python(response)
		except pydantic.ValidationError as error:
			print(f"Validation Error in collect response {error}")
			raise error

	return wrapper


class _MetaBaseVkApiClient(type):
	__skip_method_validate = {"request"}
	request_methods = set()

	def __new__(cls, name, bases, dct):
		for attr_name, attr_value in dct.items():
			if not callable(attr_value):
				continue
			if "".join(attr_name[0:2]) == "__":
				continue
			if not inspect.iscoroutinefunction(attr_value):
				continue
			if attr_name in cls.__skip_method_validate:
				continue
			dct[attr_name] = collect_response(attr_value)
			cls.request_methods.add(attr_name)
		dct["request_methods"] = cls.request_methods.copy()
		cls.request_methods.clear()
		return super().__new__(cls, name, bases, dct)







class _BaseVkApiClient(metaclass=_MetaBaseVkApiClient):
	__header: typing.Dict
	__params: httpx.QueryParams
	base_url = "https://api.vk.com/method"
	version_api = "5.199"
	__base_params = httpx.QueryParams
	request_methods: int
	def __init__(
		self,
		auth_token: typing.Optional[base_request] = None,
	):
		self.__params = httpx.QueryParams({"v": "5.199"})
		if auth_token:
			self.auth(auth_token=auth_token)


	async def request(
		self,
		path: str,
		method: available_methods,
		body: typing.Optional[typing.Dict] = None,
		params: typing.Optional[typing.Dict] = None,
		expected_status_code: typing.List = None
	) -> httpx.Response:

		async with httpx.AsyncClient() as client:
			if self.__params.get("auth_token"):
				raise ValueError("Not auth")
			if params:
				params = self._extend_query_parameters(params)
			if method == "GET" and body is not None:
				raise TypeError("Get request not have payload.")

			r = await client.request(
				method=method,
				params=params if params else self.__params,
				url="/".join([self.base_url, path])
			)
			if expected_status_code and r.status_code in expected_status_code:
				return r
			if r.is_success:
				return r
			raise Exception




	def _extend_query_parameters(self, d: dict) -> httpx.QueryParams:
		# query params type is immutable object.
		return self.__params.merge(d)


	def auth(self, auth_token: base_request):
		self.__params = self.__params.merge({"access_token": auth_token.token.get_secret_value()})



vk_api_client = typing.TypeVar("vk_api_client", bound=_BaseVkApiClient)



class VkApiClientFactory:

	def __call__(self, cls: typing.Type[vk_api_client], **kwargs):
		if not issubclass(cls, _BaseVkApiClient):
			raise TypeError("Error type factory")
		return cls(**kwargs)

