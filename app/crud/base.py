import logging
import os
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'settings.ini')))

config.read("settings.ini")

print(config["db"]["username"])

engine = create_engine(f"postgresql://{config['db']['username']}:{config['db']['password']}@localhost:5432/{config['db']['name']}",
                       pool_pre_ping=True)

Base = declarative_base(bind=engine)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

log.info(__name__)

with engine.connect() as conn:
    with open(os.path.abspath('app/db/schema.sql')) as schema:
        conn.execute(schema.read())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
