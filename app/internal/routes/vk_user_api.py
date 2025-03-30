from app.pkg import models
from fastapi import APIRouter, Depends, status, Query
from dependency_injector.wiring import Provide, inject
from app.internal.services.vk_service import VkUserService
from app.internal.services import Services
from app.internal.pkg.middlewares.jwt_auth_midleware import get_vk_api_token

router = APIRouter(
	prefix="/user-api",
	tags=["vk user api"]
)



@router.get(
	path="",
	response_model=models.app.vk_api.user_api.ResponseUserInfoClient,
	status_code=status.HTTP_200_OK,

)
@inject
async def read_user_info(
	username: str = Query(
		description="vk username",
	),
	api_token: models.vk_api_base.BaseVkApiModelRequest = Depends(get_vk_api_token),
	vk_user_service: VkUserService = Depends(Provide[Services.vk_user_service])
):
	return await vk_user_service.read_user_info(
		cmd=models.app.vk_api.user_api.ReadUserInfoCommand(
			user_id=username
		),
		api_token=api_token
	)


@router.get(
	path="/walls",
	response_model=models.app.vk_api.user_api.ResponseUserInfoClient,
	status_code=status.HTTP_200_OK,
)
@inject
async def read_user_info(
	username: str = Query(
		description="vk username",
	),
	api_token: models.vk_api_base.BaseVkApiModelRequest = Depends(get_vk_api_token),
	vk_user_service: VkUserService = Depends(Provide[Services.vk_user_service])
):
	return await vk_user_service.read_wall_count(
		cmd=models.app.vk_api.user_api.ReadUserInfoCommand(
			user_id=username,
		),
		api_token=api_token
	)
