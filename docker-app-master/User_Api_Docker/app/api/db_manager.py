from sqlalchemy.orm import Session
from api import models, schemas
import requests
import asyncio
import hashlib, binascii, os
from sqlalchemy import literal
import logging
#loop = asyncio.get_event_loop()

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 10)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  10)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.userid == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hpassword =  hash_password(user.password)
    db_user = models.User(email=user.email, password=hpassword, username=user.username, name = user.name, surname = user.surname, role=user.role, dateofbirth=user.dateofbirth )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(db_user.email)
    url = 'http://0.0.0.0:8003/notificationsconfirm/'+db_user.email+'&'+ str(1)
    response = requests.post(url)

    return db_user

# async def add_user(payload: UserIn):
#     payload.password = hash_password(payload.password)
#     query = users.insert().values(**payload.dict())
#     return await database.execute(query=query)

# async def get_all_users():
#     query = users.select()
#     return await database.fetch_all(query=query)

# async def get_users(id):
#     query = users.select(users.c.id==id)
#     return await database.fetch_one(query=query)

# @asyncio.coroutine
# def get_user_byemail(username):
#     u = username 
#     print(username)
#     print(u)
#     query = users.select(users.c.username == u)
#     #print(literal(query))
#     result =  database.fetch_all(query=query)
#     print(result)
#     return result
