from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDTO:
    id: int
    username: str
    balance: int
    created_at: datetime
    updated_at: datetime