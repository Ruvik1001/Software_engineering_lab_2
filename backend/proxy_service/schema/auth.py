"""Proxy service auth DTOs."""

from pydantic import BaseModel, EmailStr, Field


class AuthRegisterRequest(BaseModel):
    """Registration request forwarded to auth service."""

    login: EmailStr = Field(examples=["john@example.com"])
    password: str = Field(min_length=4, max_length=128, examples=["qwerty"])
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)


class AuthRegisterResponse(BaseModel):
    """Registration response returned from auth service."""

    user_id: int
    login: str
    first_name: str
    last_name: str


class AuthLoginRequest(BaseModel):
    """Login request forwarded to auth service."""

    login: EmailStr
    password: str


class AuthRefreshRequest(BaseModel):
    """Refresh token request forwarded to auth service."""

    refresh_token: str


class AuthTokenResponse(BaseModel):
    """Token response returned from auth service."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class AuthValidateRequest(BaseModel):
    """Token validation request forwarded to auth service."""

    token: str


class AuthValidateResponse(BaseModel):
    """Token validation response returned from auth service."""

    user_id: int
