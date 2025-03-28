from app.pkg import models
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject
from app.internal.services.vk_service import VkUserService
from app.internal.services import Services
from app.internal.pkg.middlewares.jwt_auth_midleware import jwt_secured

router = APIRouter(
	prefix="/user-api",
	tags=["User"]
)



@router.get(
	path="",
	response_model=models.app.vk_api.user_api.ResponseUserInfoClient,
	status_code=status.HTTP_200_OK,

)
@inject
async def read_user_info(
	cmd: models.app.vk_api.user_api.ReadUserInfoCommand,
	user: models.app.user_schema.User = Depends(jwt_secured),
	vk_user_service: VkUserService = Depends(Provide[Services.vk_user_service])
):
	return await vk_user_service.read_user_info(cmd=cmd, user=user)
