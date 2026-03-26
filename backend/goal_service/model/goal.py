from dataclasses import dataclass


@dataclass
class Goal:
    id: int
    title: str
    owner_id: int
