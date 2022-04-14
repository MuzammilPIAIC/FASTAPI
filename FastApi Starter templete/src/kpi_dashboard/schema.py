
from numpy import str0
from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import List, Optional


class AuthDetails(BaseModel):
    username: str
    password: str


