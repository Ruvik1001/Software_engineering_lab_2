"""Proxy service error response DTOs."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Common error response shape."""

    detail: str
