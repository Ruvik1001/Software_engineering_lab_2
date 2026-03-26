from fastapi import APIRouter

from api.v1.auth import auth_proxy_router
from api.v1.calendar import calendar_proxy_router
from api.v1.goals import goal_proxy_router
from api.v1.notification import notification_proxy_router
from api.v1.tasks import task_proxy_router
from api.v1.users import user_proxy_router

proxy_router = APIRouter()
proxy_router.include_router(auth_proxy_router)
proxy_router.include_router(user_proxy_router)
proxy_router.include_router(goal_proxy_router)
proxy_router.include_router(task_proxy_router)
proxy_router.include_router(notification_proxy_router)
proxy_router.include_router(calendar_proxy_router)
