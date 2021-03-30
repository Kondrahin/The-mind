import logging
import os
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

engine = create_engine("postgresql://postgres:password@host/db_name", pool_pre_ping=True)

Base = declarative_base(bind=engine)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

log.info(__name__)

with engine.connect() as conn:
    with open(os.path.abspath('app/db/schema.sql')) as schema:
        conn.execute(schema.read())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
