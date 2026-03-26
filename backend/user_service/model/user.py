from dataclasses import dataclass


@dataclass
class User:
    id: int
    login: str
    first_name: str
    last_name: str
