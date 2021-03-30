import logging
from sqlalchemy.orm import Session
from app.models import Player

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class CRUDPlayer:

    def create(self, db: Session, *, player_token: str, player_nick: str, room_token: str) -> Player:
        db_obj = Player(
            id=player_token,
            nick=player_nick,
            room_token=room_token
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, player_token):
        pass

    def connect(self, db: Session, *, player: Player, room_token):
        result = db.query(Player).filter_by(id=player.id).update({'room_token': room_token})
        db.commit()
        return result


player = CRUDPlayer()
