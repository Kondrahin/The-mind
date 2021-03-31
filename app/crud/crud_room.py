import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions import NonAdmin, FewPlayers, RoomNotFound
from app.models import Room, Player

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class CRUDRoom:

    def create(self, db: Session, *, room_token, player_token) -> Room:
        db_obj = Room(
            id=room_token,
            admin=player_token,
            level=1,
            status='created',
            pool=[]

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, room_token) -> Optional[Room]:
        return db.query(Room).filter_by(id=room_token).first()

    def start_game(self, db: Session, *, room_token, player_token):
        room = db.query(Room).filter_by(id=room_token).first()
        if room:
            if room.admin == player_token:
                players = db.query(Player).filter_by(room_token=room_token).all()
                if len(players) == 1:
                    raise FewPlayers
                if len(players) == 2:
                    log.info(room_token)
                    db.query(Room).filter_by(id=room_token).update(
                        {'lives': 2, 'shurikens': 1, 'end_level': 12})
                    db.commit()
                    return {'result': 2}
                elif len(players) == 3:
                    db.query(Room).filter_by(id=room_token).update(
                        {'lives': 3, 'shurikens': 1, 'end_level': 10})
                    db.commit()
                    return {'result': 3}
                if len(players) == 4:
                    db.query(Room).filter_by(id=room_token).update(
                        {'lives': 4, 'shurikens': 1, 'end_level': 8})
                    db.commit()
                    return {'result': 4}
            else:
                raise NonAdmin
        else:
            raise RoomNotFound


room = CRUDRoom()
