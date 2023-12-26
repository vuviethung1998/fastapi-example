from typing import List, Union
from fastapi import APIRouter, Query, HTTPException, Request, Form, Depends 
import jwt
from decouple import config

from sqlalchemy.orm import Session 

from server.database.sqlalchemy import get_db 
from server.dms.auth_user_sqlalch import create_new_user
from server.schemas.user import UserModel

router = APIRouter()


@router.get("/random")
def generate_random(rand_num: int):
    return "Hello" + f"{rand_num}"


@router.post("/create_user")
async def create_user(user: UserModel, db: Session = Depends(get_db)):
    data = await create_new_user(db, user)
    return data 