from fastapi import APIRouter, Depends, status
from app.pkg import models
from dependency_injector.wiring import Provide, inject
from app.internal.services.user_service import UserService
from app.internal.services import Services
from app.internal.pkg.middlewares.jwt_auth_midleware import jwt_secured

router = APIRouter(
	prefix="/user",
	tags=["User"]
)


@router.post(
	"",
	response_model=models.app.user_schema.User,
	status_code=status.HTTP_201_CREATED,
)
@inject
async def create_user(
		cmd: models.app.user_schema.CreateUserCommand,
		user_service: UserService = Depends(Provide[Services.user_service]),
		_=Depends(jwt_secured)
):
	return await user_service.create(cmd=cmd)
