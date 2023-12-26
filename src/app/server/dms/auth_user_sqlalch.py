from sqlalchemy.orm import Session
from server.models import models
from server.schemas.user import UserModel
from passlib.context import CryptContext
import jwt
from passlib.context import CryptContext
from decouple import config  
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = config('SECRET_KEY')

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_new_user(db: Session, user: UserModel):
    hashed_pw  = get_password_hash(user.password)
    try:
        db_user = models.User(email=user.email, password=hashed_pw)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return "Successful"
    except Exception as e:
        print(e)
        return None 
