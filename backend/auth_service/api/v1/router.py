from fastapi import APIRouter, Depends, HTTPException

from schema.auth import (
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenPairResponse,
    ValidateRequest,
    ValidateResponse,
)
from use_case.service import AuthService
from util.dependencies import get_auth_service

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/auth/register",
    response_model=RegisterResponse,
    summary="Register user",
    description="Creates a new user credential in auth service (login is email).",
    responses={400: {"description": "Login already exists"}},
)
def register_endpoint(req: RegisterRequest, service: AuthService = Depends(get_auth_service)) -> RegisterResponse:
    try:
        return RegisterResponse.model_validate(service.register(req.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@auth_router.post(
    "/auth/login",
    response_model=TokenPairResponse,
    summary="Login",
    description="Validates credentials and returns access/refresh tokens.",
    responses={401: {"description": "Invalid credentials"}},
)
def login_endpoint(req: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenPairResponse:
    try:
        return TokenPairResponse.model_validate(service.login(req.login, req.password))
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@auth_router.post(
    "/auth/refresh",
    response_model=AccessTokenResponse,
    summary="Refresh token",
    description="Creates new access token from a valid refresh token.",
    responses={401: {"description": "Invalid refresh token"}},
)
def refresh_endpoint(req: RefreshRequest, service: AuthService = Depends(get_auth_service)) -> AccessTokenResponse:
    try:
        return AccessTokenResponse.model_validate(service.refresh(req.refresh_token))
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@auth_router.post(
    "/auth/validate",
    response_model=ValidateResponse,
    summary="Validate access token",
    description="Validates JWT token and returns authenticated user_id (JWT.sub).",
    responses={401: {"description": "Invalid token"}},
)
def validate_endpoint(req: ValidateRequest, service: AuthService = Depends(get_auth_service)) -> ValidateResponse:
    try:
        return ValidateResponse.model_validate(service.validate(req.token))
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
