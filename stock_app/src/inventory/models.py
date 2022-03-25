
from email.policy import default
from matplotlib import image
from numpy import imag
from database import Base

from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text

from sqlalchemy import Column,Integer, String ,ForeignKey, BigInteger
from sqlalchemy import Text
from ..user.models import UserModel

class testcall(Base):
    __tablename__ = 'testcall'
    id = Column(Integer, primary_key=True, nullable=False)
    #user_type_id = Column(Integer, ForeignKey("user_type.id"))
    name = Column(String, nullable=False)
    number = Column(BigInteger, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class testcall_2(Base):
    __tablename__ = 'testcall_2'
    id = Column(Integer, primary_key=True, nullable=False)
    #user_type_id = Column(Integer, ForeignKey("user_type.id"))
    name = Column(String, nullable=False)
    number = Column(String(20), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class ImageType(Base):
    __tablename__ = 'image_type'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class ANContact(Base):
    __tablename__ = 'an_contact'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(UserModel.id))
    type_id = Column(Integer, ForeignKey("type.id"))
    full_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    area = Column(String, nullable=False)
    city = Column(String, nullable=False)
    cell_no_1 = Column(String, nullable=False)
    cell_no_2 = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    cnic_no = Column(String, nullable=False)


class Images(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, nullable=False)
    contact_id = Column(Integer, ForeignKey("an_contact.id"))
    image_type_id = Column(Integer, ForeignKey("image_type.id"))
    image_url = Column(Text, nullable=False)
    

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_update = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"))
    qty = Column(Integer, nullable=False, default=0)
    


class AssignInventory(Base):
    __tablename__ = 'assign_inventory'

    id = Column(Integer, primary_key=True, nullable=False)
    contact_id = Column(Integer, ForeignKey("an_contact.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    qty = Column(Integer, nullable=False)
    