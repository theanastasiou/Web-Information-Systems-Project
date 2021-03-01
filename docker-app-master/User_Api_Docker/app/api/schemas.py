from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

# class UserIn(BaseModel):
#     name: str
#     surname: str
#     username: str
#     password:str
#     role: int
#     email: str
#     dateofbirth : date


# class UserOut(UserIn):
#     userid: int


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    name: str
    surname: str
    username: str
    role: int
    email: str
    dateofbirth : date

class User(UserBase):
    userid: int
    name: str
    surname: str
    username: str
    role: int
    email: str
    dateofbirth : date
    class Config:
        orm_mode = True

