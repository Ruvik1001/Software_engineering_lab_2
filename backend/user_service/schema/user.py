"""User service request/response DTOs."""

from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    """User creation request payload."""

    login: EmailStr
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)


class UserResponse(BaseModel):
    """User response payload."""

    id: int
    login: str
    first_name: str
    last_name: str
