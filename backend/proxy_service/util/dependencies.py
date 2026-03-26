"""FastAPI dependency providers for proxy service."""

from fastapi import Depends

from use_case.auth_proxy import AuthProxyUseCase
from use_case.calendar_proxy import CalendarProxyUseCase
from use_case.goal_proxy import GoalProxyUseCase
from use_case.notification_proxy import NotificationProxyUseCase
from use_case.proxy_client import ProxyGatewayUseCase
from use_case.task_proxy import TaskProxyUseCase
from use_case.user_proxy import UserProxyUseCase


def get_proxy_gateway_use_case() -> ProxyGatewayUseCase:
    """Provide proxy gateway use case."""
    return ProxyGatewayUseCase()


def get_auth_proxy_use_case(
    gateway: ProxyGatewayUseCase = Depends(get_proxy_gateway_use_case),
) -> AuthProxyUseCase:
    """Provide auth proxy use case."""
    return AuthProxyUseCase(gateway=gateway)


def get_user_proxy_use_case(
    gateway: ProxyGatewayUseCase = Depends(get_proxy_gateway_use_case),
) -> UserProxyUseCase:
    """Provide user proxy use case."""
    return UserProxyUseCase(gateway=gateway)


def get_goal_proxy_use_case(
    gateway: ProxyGatewayUseCase = Depends(get_proxy_gateway_use_case),
) -> GoalProxyUseCase:
    """Provide goal proxy use case."""
    return GoalProxyUseCase(gateway=gateway)


def get_task_proxy_use_case(
    gateway: ProxyGatewayUseCase = Depends(get_proxy_gateway_use_case),
) -> TaskProxyUseCase:
    """Provide task proxy use case."""
    return TaskProxyUseCase(gateway=gateway)


def get_notification_proxy_use_case(
    gateway: ProxyGatewayUseCase = Depends(get_proxy_gateway_use_case),
) -> NotificationProxyUseCase:
    """Provide notification proxy use case."""
    return NotificationProxyUseCase(gateway=gateway)


def get_calendar_proxy_use_case(
    gateway: ProxyGatewayUseCase = Depends(get_proxy_gateway_use_case),
) -> CalendarProxyUseCase:
    """Provide calendar proxy use case."""
    return CalendarProxyUseCase(gateway=gateway)
