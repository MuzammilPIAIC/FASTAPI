from typing import Optional
from unittest.util import _MAX_LENGTH
from database import Base
from pydantic import BaseModel, Field
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy import Column,Integer, String ,ForeignKey

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    user_type_id = Column(Integer, ForeignKey("user_type.id"))
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

class UserType(Base):
    __tablename__ = 'user_type'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class LocationTracking(Base):
    __tablename__ = 'location_tracking'
    id = Column(Integer, primary_key=True, nullable=False)
    users_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    date_time = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
