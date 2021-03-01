from typing import List
from fastapi import Depends, FastAPI, HTTPException, Form
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm


import os; 

from fastapi_login import LoginManager
from api import db_manager
from api import models
from api import schemas
from api.db import SessionLocal, engine
from fastapi_login.exceptions import InvalidCredentialsException
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=[
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:3000/register",
    "http://localhost"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET = os.urandom(24).hex()



manager = LoginManager(SECRET, tokenUrl='/auth/token')

@app.post('/auth/tokens')
def log(username: str = Form(...),password: str = Form(...),db: Session = Depends(get_db)):
 return{"username": username, "pass": password}

@app.post('/auth/token')
def login(username: str = Form(...),password: str = Form(...),db: Session = Depends(get_db)):
#     username = data.username
#    password = data.password
    print("USER")
    print(username)
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    #logging.debug("--------------------")
    user = db_manager.get_user_by_email(db, email=username) # we are using the same function to retrieve the user
    print(user.role)
    #unhashed_pass = 
   # print(unhashed_pass)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif  db_manager.verify_password(user.password, password) != True:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=username)
    )
    return {'access_token': access_token, 'token_type': 'bearer','role': user.role,'userid': user.userid}

#@app.get('/protected')
#def protected_route(user=Depends(manager)):
#    print("Read user".format(user))

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db_manager.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_manager.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db_manager.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db_manager.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

