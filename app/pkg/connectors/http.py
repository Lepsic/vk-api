import typing

import httpx
import pydantic
from typing import TypeVar
from app.pkg.models.base import BaseModel
from logging import Logger
from app.pkg.logger import get_logger
from app.pkg.models.base import BaseClientException
Command = TypeVar("Command", bound=BaseModel)


class HttpRequest:
	access_token: typing.Optional[pydantic.SecretStr]
	url: pydantic.AnyUrl
	client_name: pydantic.StrictStr
	logger: Logger

	def __init__(
		self,
		url: pydantic.AnyUrl,
		client_name: pydantic.StrictStr,
		access_token: typing.Optional[pydantic.StrictStr],
	):
		self.access_token = access_token
		self.client_name = client_name,
		self.url = url
		self.logger = get_logger(name=client_name)

	async def request(
		self,
		cmd: Command,
		path: str,
		method: typing.Literal["GET", "POST", "DELETE", "PATCH", "PUT"]
	) -> httpx.Response:

		async with httpx.AsyncClient() as client:
			try:
				headers = None
				if self.access_token is not None:
					headers = {"ACCESS-TOKEN": self.access_token.get_secret_value()}
				response = await client.request(
					method=method,
					url="".join([str(self.url), path]),
					json=cmd.to_dict(),
					headers=headers,
				)

				if response.is_success:
					return response
				self.logger.exception("Request isn't success %s", response.text)
				raise BaseClientException(
					client_name=self.client_name,
					status_code=response.status_code,
					message=response.text,
				)
			except httpx.HTTPError as exception:
				self.logger.error(
					msg=f"Http client error {exception}",
				)
