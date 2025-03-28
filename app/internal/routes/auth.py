from fastapi import APIRouter, Depends, status
from app.pkg import models
from dependency_injector.wiring import Provide, inject
from app.internal.services.auth_service import AuthService
from app.internal.services import Services

__all__ = [
	"router",
]

router = APIRouter(
	prefix="/auth",
	tags=["Auth"]
)


@router.post(
	"/login",
	response_model=models.app.auth.AuthResponse,
	status_code=status.HTTP_200_OK,
)
@inject
async def login(
	cmd: models.app.auth.AuthRequest,
	auth_service: AuthService = Depends(Provide[Services.auth_service])
):
	return await auth_service.login(cmd=cmd)


@router.post(
	"/refresh",
	response_model=models.app.auth.RefreshResponse,
	status_code=status.HTTP_200_OK,
)
@inject
async def refresh(
	cmd: models.app.auth.RefreshRequest,
	auth_service: AuthService = Depends(Provide[Services.auth_service])
):
	return await auth_service.refresh(cmd=cmd)
