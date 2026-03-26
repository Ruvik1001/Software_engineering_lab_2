from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    login: EmailStr
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)


class UserResponse(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
