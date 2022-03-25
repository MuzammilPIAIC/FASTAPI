
from numpy import str0
from pydantic import BaseModel
from pydantic.networks import EmailStr


class Inventory(BaseModel):
    name : str
    number : str
    email : EmailStr
    password : str


class image_type(BaseModel):
    name : str


class type(BaseModel):
    name : str

class an_contact(BaseModel):
    user_id : int
    type_id : int
    full_name : str
    company_name : str
    address : str
    area : str
    city : str
    cell_no_1 : str
    cell_no_2 : str
    phone : str
    cnic_no : str

class images(BaseModel):
    contact_id : int
    image_type_id : int
    image_url : str


class product(BaseModel):
    name : str
    description : str

class stock(BaseModel):
    product_id : int
    qty : int


class assign_inventory(BaseModel):
    contact_id : int
    product_id : int
    qty : int

class stock_update(BaseModel):
    product_id : int
    qty : int


    
    

