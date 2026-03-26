from dataclasses import dataclass


@dataclass
class AuthUser:
    id: int
    login: str
    password: str
    first_name: str
    last_name: str
