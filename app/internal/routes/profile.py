from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security, status

from app.internal.services import Services
from app.internal.services.user import UserService
from app.pkg import models
from app.pkg.jwt import JwtAuthorizationCredentials, access_security

router = APIRouter(prefix="/user/me", tags=["User profile"])


@router.post(
    "/",
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
    response_model_exclude={"password"},
)
@inject
async def create_user_profile(
    cmd: models.CreateUserProfileCommand,
    user_service: UserService = Depends(Provide[Services.user_service]),
):
    return await user_service.create_user(
        cmd=models.CreateUserCommand(
            username=cmd.username,
            password=cmd.password.get_secret_value(),
            phone_number=cmd.phone_number,
        ),
    )


@router.get(
    "/",
    response_model=models.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Read specific user without password field",
)
@inject
async def read_user_profile(
    user_service: UserService = Depends(Provide[Services.user_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get('user_id')

    return await user_service.read_specific_user_by_id(
        query=models.ReadUserByIdQuery(id=user_id),
    )


@router.put(
    "/",
    response_model=models.User,
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Update specific user",
)
@inject
async def update_user(
    cmd: models.UpdateUserProfileCommand,
    user_service: UserService = Depends(Provide[Services.user_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get('user_id')
    user = await user_service.read_specific_user_by_id(
        query=models.ReadUserByIdQuery(id=user_id),
    )

    return await user_service.update_specific_user(
        cmd=models.UpdateUserCommand(
            id=user_id,
            username=cmd.username,
            password=user.password.get_secret_value(),
            phone_number=cmd.phone_number,
        ),
    )


@router.delete(
    "/",
    response_model=List[models.User],
    status_code=status.HTTP_200_OK,
    response_model_exclude={"password"},
    description="Delete specific user",
)
@inject
async def delete_user(
    user_service: UserService = Depends(Provide[Services.user_service]),
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    user_id = credentials.subject.get('user_id')

    return await user_service.delete_specific_user(
        cmd=models.DeleteUserCommand(id=user_id),
    )
