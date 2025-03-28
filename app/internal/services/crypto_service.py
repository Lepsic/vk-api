import typing
import pydantic
from cryptography.fernet import Fernet

__all__ = [
	"CryptoService"
]


class CryptoService:
	__secret_key: str
	__fernet: Fernet

	def __init__(
		self,
		secret_key: pydantic.SecretStr
	):
		self.__secret_key = secret_key.get_secret_value()
		self.__fernet = Fernet(key=self.__secret_key)

	def encrypt(
		self,
		secret_str: typing.Union[str, pydantic.SecretStr],
	) -> str:
		if isinstance(secret_str, pydantic.SecretStr):
			secret_str = secret_str.get_secret_value()
		return self.__fernet.encrypt(secret_str.encode())

	def decrypt(
		self,
		secret_str: typing.Union[str, pydantic.SecretStr, pydantic.SecretBytes, bytes],
	) -> str:
		if isinstance(secret_str, pydantic.SecretStr) or isinstance(secret_str, pydantic.SecretBytes):
			secret_str = secret_str.get_secret_value()

		return self.__fernet.decrypt(secret_str).decode()
