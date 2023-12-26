from typing import List, Union
from fastapi import APIRouter, Query, HTTPException, Request, Form
import jwt
from server.dto.login_dto import UserLoginDTO, UserSignupDTO
from decouple import config

from server.dms.auth_user import AuthUserService, check_user_by_email, create_access_token

router = APIRouter()
auth_service = AuthUserService()

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = config('SECRET_KEY')

@router.post('/login/')
async def login(input_login: UserLoginDTO):
    print(input_login.dict())
    token = await auth_service.login(input_login.dict())
    return token


@router.post('/register/')
async def register(input_login: UserSignupDTO):
    data_test = await auth_service.register(input_login.dict())
    return data_test
    
    
@router.get('/get_users/')
async def get_users():
    data = await auth_service.get_users()
    return data

