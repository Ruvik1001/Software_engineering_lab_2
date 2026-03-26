from pydantic import BaseModel, EmailStr, Field


class AuthRegisterRequest(BaseModel):
    login: EmailStr = Field(examples=["john@example.com"])
    password: str = Field(min_length=4, max_length=128, examples=["qwerty"])
    first_name: str = Field(min_length=1, max_length=64)
    last_name: str = Field(min_length=1, max_length=64)


class AuthRegisterResponse(BaseModel):
    user_id: int
    login: str
    first_name: str
    last_name: str


class AuthLoginRequest(BaseModel):
    login: EmailStr
    password: str


class AuthRefreshRequest(BaseModel):
    refresh_token: str


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class AuthValidateRequest(BaseModel):
    token: str


class AuthValidateResponse(BaseModel):
    user_id: int
