"""User service domain models."""

from dataclasses import dataclass


@dataclass
class User:
    """User profile entity."""

    id: int
    login: str
    first_name: str
    last_name: str
