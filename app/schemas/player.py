from typing import List

from pydantic import BaseModel


class PlayerCreate(BaseModel):
    token: str
    nick: str


class Player(PlayerCreate):
    hand: List[int]
