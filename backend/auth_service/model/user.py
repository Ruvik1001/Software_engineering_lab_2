"""Auth service domain models."""

from dataclasses import dataclass


@dataclass
class AuthUser:
    """Stored auth user credentials and profile."""

    id: int
    login: str
    password: str
    first_name: str
    last_name: str
