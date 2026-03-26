"""Proxy service API router composition."""

from fastapi import APIRouter

from .auth import auth_proxy_router
from .calendar import calendar_proxy_router
from .goals import goal_proxy_router
from .notification import notification_proxy_router
from .tasks import task_proxy_router
from .users import user_proxy_router

proxy_router = APIRouter()
proxy_router.include_router(auth_proxy_router)
proxy_router.include_router(user_proxy_router)
proxy_router.include_router(goal_proxy_router)
proxy_router.include_router(task_proxy_router)
proxy_router.include_router(notification_proxy_router)
proxy_router.include_router(calendar_proxy_router)
