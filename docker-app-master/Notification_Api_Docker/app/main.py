from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api import db_manager, models, schemas
from api.db import SessionLocal, engine

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
import requests
import os; 
import jwt
import base64
from urllib import request

from base64 import b64decode 
from fastapi_login import LoginManager
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notifications/{carrieruseremail}&{appointmentid}&{number}",response_model=schemas.Notification)
def create_notification(carrieruseremail: str,appointmentid: int ,number :int,db: Session = Depends(get_db)):
    print("notificationsin")
    #print(data.number)
    print(appointmentid) #giati penri san id mono to teleutaio psifio?????
    print(carrieruseremail)
    print(number)
    notification = schemas.NotificationCreate(appointmentid = appointmentid)
    db_manager.send_confirm_email("myapp.2020.sept@gmail.com",carrieruseremail,"myapp1234",number)
    print("ok")
    return db_manager.create_notification(db=db, notification=notification)

@app.post("/notificationsconfirm/{useremail}&{number}")
def submition(useremail: str ,number :int,db: Session = Depends(get_db)):
    print("notificationsin")
    #print(data.number)
    db_manager.send_confirm_email("myapp.2020.sept@gmail.com",useremail,"myapp1234",number)
    print("ok")
    
@app.get("/notifications/", response_model=List[schemas.Notification])
def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notif = db_manager.get_notifications(db, skip=skip, limit=limit)
    print(notif)
    return notif


@app.get("/notification/{notification_id}", response_model=schemas.Notification)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notif = db_manager.get_notification(db, notification_id=notification_id)
    print(db_notif)
    if db_notif is None:
        raise HTTPException(status_code=404, detail="Notif not found")
    return db_notif


@app.get("/notificationbyappid/{appointment_id}", response_model=List[schemas.Notification])
def read_notification(appointment_id: int, db: Session = Depends(get_db)):
    db_notif = db_manager.get_notification_byappointment(db, appointment_id=appointment_id)
    print(db_notif)
    if db_notif is None:
        raise HTTPException(status_code=404, detail="Notif not found")
    return db_notif

