from dataclasses import dataclass


@dataclass
class Task:
    id: int
    goal_id: int
    title: str
    owner_id: int
    status: str
