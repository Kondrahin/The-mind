import logging
from sqlalchemy import Column, String, ARRAY, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.crud.base import Base

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Player(Base):
    __tablename__ = 'players'
    id = Column(String(22), primary_key=True, unique=True)
    nick = Column(String(30), nullable=False)
    hand = Column(ARRAY(Integer))
    room_token = Column(String(22), ForeignKey('rooms.id'), nullable=False)

    def __repr__(self):
        return "<Player (id='{}', nick='{}', hand={}, room_token='{}')>" \
            .format(self.id, self.nick, self.hand, self.room_token)


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(String(6), primary_key=True, unique=True)
    admin = Column(String(22), nullable=False)
    level = Column(Integer, CheckConstraint('level>=0 and level<=12'))
    status = Column(String(10), nullable=False, default='created')
    pool = Column(ARRAY(Integer))
    lives = Column(Integer, nullable=False, default=0)
    shurikens = Column(Integer, nullable=False, default=0)
    end_level = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Room (id='{}', admin='{}', level='{}', status='{}', pool='{}', lives='{}', shurikens='{}', " \
               "end_level='{}')>" \
            .format(self.id, self.admin, self.level, self.status, self.pool, self.lives, self.shurikens, self.end_level)
