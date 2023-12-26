from fastapi import HTTPException

from server.dto.login_dto import UserLoginDTO, UserSignupDTO

from server.schemas.user import UserModel
import jwt
from passlib.context import CryptContext
from server.database.maria import MariaDB
from decouple import config  
import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = config('SECRET_KEY')

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def token_generator(user: UserModel):
    if not user:
        raise HTTPException(status_code=401, detail="Wrong password entered")

    token_data = {
        "email": user['email']
    }

    token = jwt.encode(token_data, SECRET_KEY)
    return token


async def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=SECURITY_ALGORITHM)
        return payload
    except:
        raise HTTPException(status_code=401, detail="Wrong password entered")


def check_user_by_email(email):
    query = f'''SELECT * FROM user WHERE email='{email}' ;'''
    check_exist = MariaDB().get_all_data_match_condition(query=query)
    check_exist = check_exist[0]
    return check_exist

def create_access_token(data, expire_minutes):
    token_data = {
        "data": data,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=expire_minutes)
    }
    token = jwt.encode(token_data, SECRET_KEY)

    return token
    

class AuthUserService():
    async def user_reset_password(self, email, password):
        pwd_after_hash = get_password_hash(password)
        res = MariaDB().upsert_many(table_name='user', data={(email, pwd_after_hash)}, cols=['email', 'password'], key_cols=['email'])
        token = await self.login({'username': email, 'password': password})
        return token

    async def register(self, input_register: UserSignupDTO):
        username = input_register['username']
        phone = input_register['phone']
        pwd = input_register['password']
        pwd_after_hash = get_password_hash(pwd)
        res = MariaDB().insert_many(table_name='user', data={(username, pwd_after_hash, phone)}, columns=['email', 'password', 'phone'])
        if 'Error' in res:
            raise HTTPException(status_code=401, detail="Email is already used")
        else:
            print(res)
            token = await self.login({'username': username, 'password': pwd})
            return token

    async def login(self, login_dto: UserLoginDTO):
        try:
            username = login_dto['username']
            pwd = login_dto['password']
            query = f'''SELECT * FROM user WHERE email='{username}' ;'''
            check_exist = MariaDB().get_all_data_match_condition(query=query)
            check_exist = check_exist[0]
            if check_exist and verify_password(pwd, check_exist['password']):
                token = await token_generator(check_exist)
                return token
            else:
                raise HTTPException(status_code=401, detail="Wrong password entered")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Wrong email or password entered")

    async def verify_token(token: str):
        try:
            payload = jwt.decode(
                token, SECRET_KEY, SECURITY_ALGORITHM)
            # item, code, msg = self.get(id=payload.get('id'))
            # if item:
            #     return item
        except Exception as e:
            print(e)

    async def get_users(self):
        query = f'''SELECT email FROM user;'''
        coll = MariaDB().get_all_data_match_condition(query=query)
        return coll