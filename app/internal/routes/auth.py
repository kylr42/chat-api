from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security, status
from starlette.responses import Response

from app.internal.services import Services
from app.internal.services.auth import AuthService
from app.pkg.jwt import (
    JWT,
    JwtAccessBearer,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
    refresh_security,
)
from app.pkg.models.auth import Auth, AuthCommand
from app.pkg.models.refresh_token import (
    CreateJWTRefreshTokenCommand,
    DeleteJWTRefreshTokenCommand,
    ReadJWTRefreshTokenQuery,
    ReadJWTRefreshTokenQueryByFingerprint,
    UpdateJWTRefreshTokenCommand,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# TODO: make it simple pls. And place me to AuthService.
@router.post(
    "/login",
    response_model=Auth,
    status_code=status.HTTP_200_OK,
    description="Route for authorize.",
)
@inject
async def auth_user(
    response: Response,
    cmd: AuthCommand,
    access: JwtAccessBearer = Depends(Provide[JWT.access]),
    refresh: JwtRefreshBearer = Depends(Provide[JWT.refresh]),
    auth_service: AuthService = Depends(Provide[Services.auth_service]),
):
    user = await auth_service.check_user_password(cmd=cmd)

    at = access.create_access_token(
        subject={"user_id": user.id, "scopes": [user.role_name]},
    )

    # TODO: raise EmptyResult and raising UnAuthorized.
    if rt := await auth_service.check_user_exist_refresh_token(
        query=ReadJWTRefreshTokenQueryByFingerprint(
            user_id=user.id,
            fingerprint=cmd.fingerprint,
        ),
    ):
        return Auth(
            access_token=at,
            refresh_token=rt.refresh_token,
        )

    crt = refresh.create_refresh_token(
        subject={
            "user_id": user.id,
            "fingerprint": cmd.fingerprint.get_secret_value(),
            "scopes": [user.role_name],
        },
    )
    await auth_service.create_refresh_token(
        cmd=CreateJWTRefreshTokenCommand(
            refresh_token=crt,
            fingerprint=cmd.fingerprint,
            user_id=user.id,
        ),
    )
    refresh.set_refresh_cookie(response=response, refresh_token=crt)

    return Auth(
        access_token=at,
        refresh_token=crt,
    )


# TODO: make it simple pls
@router.patch(
    "/refresh",
    response_model=Auth,
    description="Route for get new tokens pair.",
)
@inject
async def create_new_token_pair(
    access: JwtAccessBearer = Depends(Provide[JWT.access]),
    refresh: JwtRefreshBearer = Depends(Provide[JWT.refresh]),
    auth_service: AuthService = Depends(Provide[Services.auth_service]),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    fingerprint = credentials.subject.get("fingerprint")
    user_id = credentials.subject.get("user_id")

    await auth_service.check_refresh_token_exists(
        query=ReadJWTRefreshTokenQuery(
            user_id=user_id,
            refresh_token=credentials.raw_token,
        ),
    )

    at = access.create_access_token(
        subject={
            "user_id": user_id,
            "fingerprint": fingerprint,
            "scopes": credentials.subject.get("scopes"),
        },
    )
    rt = refresh.create_refresh_token(
        subject={
            "user_id": user_id,
            "fingerprint": fingerprint,
            "scopes": credentials.subject.get("scopes"),
        },
    )

    irt = await auth_service.update_refresh_token(
        cmd=UpdateJWTRefreshTokenCommand(
            user_id=user_id,
            refresh_token=rt,
            fingerprint=fingerprint,
        ),
    )
    return Auth(access_token=at, refresh_token=irt.refresh_token.get_secret_value())


# TODO: make it simple pls
@router.post("/logout", status_code=status.HTTP_200_OK, description="Route for logout.")
@inject
async def logout(
    auth_service: AuthService = Depends(Provide[Services.auth_service]),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    user_id = credentials.subject.get("user_id")
    fingerprint = credentials.subject.get("fingerprint")
    refresh_token = credentials.raw_token

    await auth_service.delete_refresh_token(
        cmd=DeleteJWTRefreshTokenCommand(
            user_id=user_id,
            fingerprint=fingerprint,
            refresh_token=refresh_token,
        ),
    )
