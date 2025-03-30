from app.internal.services.auth_service import AuthService
from dependency_injector.wiring import inject, Provide
from app.internal.services import Services
from fastapi import Security, Depends
from fastapi.security import APIKeyHeader
from app.pkg import models

header = APIKeyHeader(name="AUTH-TOKEN")
__all__ = [
	"jwt_secured",
]


@inject
def jwt_secured(
	api_header_token: str = Security(header),
	auth_service: AuthService = Depends(Provide[Services.auth_service]),
) -> models.app.user_schema.User:
	token = api_header_token
	return auth_service.auth(token)


@inject
def get_vk_api_token(
	api_header_token: str = Security(header),
	auth_service: AuthService = Depends(Provide[Services.auth_service]),
) -> models.vk_api_base.BaseVkApiModelRequest:
	token = api_header_token
	return auth_service.fetch_vk_api_token(token)
