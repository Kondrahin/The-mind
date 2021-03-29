from typing import List

from pydantic import BaseModel


class RoomCreate(BaseModel):
    id: str
    admin: str


class Room(RoomCreate):
    level: int
    pool: List[int]
