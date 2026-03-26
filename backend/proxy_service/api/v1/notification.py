from fastapi import APIRouter, Depends

from use_case.notification_proxy import NotificationProxyUseCase
from util.auth import get_token_value, require_user
from util.dependencies import get_notification_proxy_use_case
from schema.notification import NotificationSendRequest, NotificationSendResponse

notification_proxy_router = APIRouter(prefix="/notification", tags=["proxy-notification"])


@notification_proxy_router.post(
    "",
    summary="Proxy: send notification",
    description="Authorized route. Calls mock notification service.",
    response_model=NotificationSendResponse,
)
async def send_notification(
    body: NotificationSendRequest,
    token: str = Depends(get_token_value),
    use_case: NotificationProxyUseCase = Depends(get_notification_proxy_use_case),
) -> NotificationSendResponse:
    await require_user(token)
    return await use_case.send(token=token, payload=body.model_dump())
