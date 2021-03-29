drop table if exists players;
drop table if exists rooms;
-------------------------------------------------
create table rooms (
    id varchar(6) unique primary key,
    admin varchar(22) not null,
    level integer check(level>=0 and level<=12),
    status varchar(10) not null default 'created',
    pool integer []
);

create table players (
    id varchar(22) unique primary key,
    nick varchar(30) not null,
    hand integer [],
    room_token varchar(22),
--     CONSTRAINT fk_room_token
      FOREIGN KEY(room_token)
	  REFERENCES rooms(id)
	  ON DELETE CASCADE
);

