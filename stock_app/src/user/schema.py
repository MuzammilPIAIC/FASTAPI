from pydantic import BaseModel
from pydantic.networks import EmailStr


class user_type(BaseModel):
    name: str


class User(BaseModel):
    user_type_id :int
    name : str
    number : str
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

    
class LocationTracker(BaseModel):
    users_id : int
    latitude : str
    longitude : str
    date_time : str
