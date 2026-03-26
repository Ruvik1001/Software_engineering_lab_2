"""Auth service request/response DTOs."""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Registration request payload."""

    login: EmailStr = Field(examples=["john@example.com"])
    password: str = Field(min_length=4, max_length=128, examples=["qwerty"])
    first_name: str = Field(min_length=1, max_length=64, examples=["John"])
    last_name: str = Field(min_length=1, max_length=64, examples=["Doe"])


class RegisterResponse(BaseModel):
    """Registration response payload."""

    user_id: int
    login: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    """Login request payload."""

    login: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Refresh token request payload."""

    refresh_token: str


class ValidateRequest(BaseModel):
    """Access token validation request payload."""

    token: str


class TokenPairResponse(BaseModel):
    """Access/refresh token pair response payload."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenResponse(BaseModel):
    """Access token response payload."""

    access_token: str
    token_type: str = "bearer"


class ValidateResponse(BaseModel):
    """Token validation response payload."""

    user_id: int
