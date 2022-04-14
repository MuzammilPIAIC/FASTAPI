from ntpath import join
from isort import file
from database import get_db
from fastapi import APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from database import engine
from . import schema as schema_user, models as model_user
import cloudinary
import cloudinary.uploader
from typing import List, Optional
from datetime import date
import random
import datetime
from sqlalchemy.dialects.postgresql import array_agg

from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schema import AuthDetails



model_user.Base.metadata.create_all(bind = engine)


router = APIRouter(
    prefix="/kpi_dashboard",
    #tags = ['User'],
    responses= {404: {'description':'Not Found'}}
)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Auth token ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

auth_handler = AuthHandler()
users = []

@router.post('/register', status_code=201, tags= ['Auth'])
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return{ 'message': "Successfully created!" }


@router.post('/login', tags= ['Auth'])
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }


@router.get('/unprotected', tags= ['Auth'])
def unprotected():
    return { 'hello': 'world' }


@router.get('/protected', tags= ['Auth'])
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }


