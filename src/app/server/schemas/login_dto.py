from typing import Optional
from pydantic import BaseModel


class UserLoginDTO(BaseModel):
    username: str = 'uonghongminh07@gmail.com'
    password: str = '123456'

class UserSignupDTO(BaseModel):
    username: str = 'uonghongminh07@gmail.com'
    password: str = '123456'
    phone: Optional[str] = None