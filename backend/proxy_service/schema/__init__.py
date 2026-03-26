"""Proxy service request/response DTO re-exports."""

from .auth import (
    AuthLoginRequest,
    AuthRefreshRequest,
    AuthRegisterRequest,
    AuthRegisterResponse,
    AuthTokenResponse,
    AuthValidateRequest,
    AuthValidateResponse,
)
from .calendar import CalendarEventResponse
from .goals import GoalCreateRequest, GoalResponse
from .notification import NotificationSendRequest, NotificationSendResponse
from .tasks import TaskCreateRequest, TaskResponse, TaskUpdateStatusRequest, TaskStatus
from .users import UserCreateRequest, UserResponse

__all__ = [
    "AuthRegisterRequest",
    "AuthRegisterResponse",
    "AuthLoginRequest",
    "AuthRefreshRequest",
    "AuthTokenResponse",
    "AuthValidateRequest",
    "AuthValidateResponse",
    "UserCreateRequest",
    "UserResponse",
    "GoalCreateRequest",
    "GoalResponse",
    "TaskStatus",
    "TaskCreateRequest",
    "TaskUpdateStatusRequest",
    "TaskResponse",
    "NotificationSendRequest",
    "NotificationSendResponse",
    "CalendarEventResponse",
]
