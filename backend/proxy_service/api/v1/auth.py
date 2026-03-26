from fastapi import APIRouter, Depends

from use_case.auth_proxy import AuthProxyUseCase
from util.dependencies import get_auth_proxy_use_case
from schema.auth import (
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthRegisterResponse,
    AuthRefreshRequest,
    AuthTokenResponse,
)

auth_proxy_router = APIRouter(prefix="/auth", tags=["proxy-auth"])


@auth_proxy_router.post(
    "/register",
    summary="Proxy: register",
    description="Passes registration request to auth service.",
    response_model=AuthRegisterResponse,
)
async def register(
    body: AuthRegisterRequest,
    use_case: AuthProxyUseCase = Depends(get_auth_proxy_use_case),
) -> AuthRegisterResponse:
    return await use_case.register(body.model_dump())


@auth_proxy_router.post(
    "/login",
    summary="Proxy: login",
    description="Passes login request to auth service.",
    response_model=AuthTokenResponse,
)
async def login(
    body: AuthLoginRequest,
    use_case: AuthProxyUseCase = Depends(get_auth_proxy_use_case),
) -> AuthTokenResponse:
    return await use_case.login(body.model_dump())


@auth_proxy_router.post(
    "/refresh",
    summary="Proxy: refresh token",
    description="Passes refresh request to auth service.",
    response_model=AuthTokenResponse,
)
async def refresh(
    body: AuthRefreshRequest,
    use_case: AuthProxyUseCase = Depends(get_auth_proxy_use_case),
) -> AuthTokenResponse:
    return await use_case.refresh(body.model_dump())
