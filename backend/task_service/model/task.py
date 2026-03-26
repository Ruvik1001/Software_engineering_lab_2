"""Task service domain models."""

from dataclasses import dataclass


@dataclass
class Task:
    """Task entity."""

    id: int
    goal_id: int
    title: str
    owner_id: int
    status: str
