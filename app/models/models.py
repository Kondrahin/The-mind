import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ARRAY, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'
    id = Column(String(22), primary_key=True, unique=True)
    nick = Column(String(30), nullable=False)
    hand = Column(ARRAY(Integer))
    room_token = Column(String(22), ForeignKey('rooms.id'), nullable=False)
    room = relationship("Room", backref="room")

    def __repr__(self):
        return "<Player (token='{}', nick='{}', hand={})>" \
            .format(self.token, self.nick, self.hand)


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(String(6), primary_key=True, unique=True)
    admin = Column(String(16), nullable=False)
    level = Column(Integer, CheckConstraint('level>=0 and level<=12'))
    status = Column(String(10), nullable=False, default='created')
    pool = Column(ARRAY(Integer))

    def __repr__(self):
        return "<Room (token='{}', admin='{}', players={}, level={}, status={}, pool={})>" \
            .format(self.token, self.admin, self.players, self.level, self.status, self.pool)
