from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
