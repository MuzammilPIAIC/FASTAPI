
from database import Base

from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text

from sqlalchemy import Column,Integer, String ,ForeignKey, BigInteger
from sqlalchemy import Text




class Sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
