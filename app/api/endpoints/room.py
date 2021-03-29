import random
import string
from secrets import token_urlsafe

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.exceptions import SessionOverflow, SessionStarted
from app import crud

router = APIRouter()


@router.post("/create/")
async def create_room(player_nick: str, db: Session = Depends(get_db)):
    room_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(0, 5))
    player_token = token_urlsafe(16)
    player = crud.player.create(db, player_token=player_token, player_nick=player_nick)
    room = crud.room.create(db, room_token=room_token, player_token=player_token)
    crud.player.connect(db, player=player, room_token=room_token)
    return {"room_token": room_token, "player_token": player_token}


@router.post("/connect_to_room/")
async def connect_to_room(room_token: str, player_nick: str, db: Session = Depends(get_db)):
    player_token = token_urlsafe(16)
    player = crud.player.create(db, player_token=player_token, player_nick=player_nick)
    room = crud.room.get(db, room_token=room_token)
    if room:
        try:
            result = crud.player.connect(db, player=player, room_token=room_token)
            return {"result": result}
        except SessionOverflow as e:
            raise HTTPException(status_code=406, detail="Too much players in this room")
        except SessionStarted as e:
            raise HTTPException(status_code=406, detail="The game in this room have already started")
    raise HTTPException(status_code=404, detail="Room wasn't found")


@router.post("/is_admin/")
async def is_admin(room_token: str, player_token: str, db: Session = Depends(get_db)):
    room = crud.room.get(db, room_token=room_token)
    if room:
        if room.admin == player_token:
            return {"result": True}
        else:
            return {"result": False}
    raise HTTPException(status_code=404, detail="Room wasn't found")
