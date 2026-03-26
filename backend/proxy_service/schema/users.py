"""Proxy service user DTOs."""

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """User creation request forwarded to user service."""

    login: EmailStr
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)


class UserResponse(BaseModel):
    """User response returned from user service."""

    id: int
    login: str
    first_name: str
    last_name: str
