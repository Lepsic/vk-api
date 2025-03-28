from app.pkg.models.base import BaseAPIException
from fastapi import status

__all__ = [
	"JwtExpired",
	"JwtWrongType",
	"JwtIncorrect",
	"CredentialsIncorrect"
]


class JwtWrongType(BaseAPIException):

	message = "Jwt is not correct."
	status_code = status.HTTP_403_FORBIDDEN


class JwtExpired(BaseAPIException):
	message = "Token expired."
	status_code = status.HTTP_401_UNAUTHORIZED


class JwtIncorrect(BaseAPIException):

	message = "Jwt payload incorrect"
	status_code = status.HTTP_401_UNAUTHORIZED


class CredentialsIncorrect(BaseAPIException):

	message = "Incorrect username or password."
	status_code = status.HTTP_403_FORBIDDEN
