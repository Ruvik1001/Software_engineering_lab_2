from fastapi import APIRouter, Depends

from use_case.calendar_proxy import CalendarProxyUseCase
from util.auth import get_token_value, require_user
from util.dependencies import get_calendar_proxy_use_case
from schema.calendar import CalendarEventResponse

calendar_proxy_router = APIRouter(prefix="/calendar", tags=["proxy-calendar"])


@calendar_proxy_router.get(
    "/events",
    summary="Proxy: list calendar events",
    description="Authorized route. Calls mock calendar service.",
    response_model=list[CalendarEventResponse],
)
async def calendar_events(
    token: str = Depends(get_token_value),
    use_case: CalendarProxyUseCase = Depends(get_calendar_proxy_use_case),
) -> list[CalendarEventResponse]:
    await require_user(token)
    return await use_case.list_events(token=token)
