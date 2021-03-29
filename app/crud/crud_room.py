from typing import Optional

from sqlalchemy.orm import Session

from app.models import Room


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
        return db.query(Room).filter(Room.id == room_token).first()

room = CRUDRoom()
