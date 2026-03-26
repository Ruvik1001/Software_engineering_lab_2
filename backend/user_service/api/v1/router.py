from fastapi import APIRouter, Depends, HTTPException, Query

from schema.user import CreateUserRequest, UserResponse
from use_case.service import UserService
from util.dependencies import get_user_service

user_router = APIRouter(tags=["users"])


@user_router.post(
    "/users",
    response_model=UserResponse,
    summary="Create user",
    description="Creates an executor profile for task planning.",
    responses={400: {"description": "Duplicate login"}},
)
def create(req: CreateUserRequest, service: UserService = Depends(get_user_service)) -> UserResponse:
    try:
        return UserResponse.model_validate(service.create_user(req.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@user_router.get(
    "/users/by-login/{login}",
    response_model=UserResponse,
    summary="Get user by login",
    description="Returns one user profile by exact login.",
    responses={404: {"description": "User not found"}},
)
def by_login(login: str, service: UserService = Depends(get_user_service)) -> UserResponse:
    user = service.get_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse.model_validate(user)


@user_router.get(
    "/users/search",
    response_model=list[UserResponse],
    summary="Search users by mask",
    description="Searches users by partial first/last name match.",
)
def search(mask: str = Query(min_length=1), service: UserService = Depends(get_user_service)) -> list[UserResponse]:
    return [UserResponse.model_validate(item) for item in service.search_by_mask(mask)]
