"""Goal service domain models."""

from dataclasses import dataclass


@dataclass
class Goal:
    """Goal entity."""

    id: int
    title: str
    owner_id: int
