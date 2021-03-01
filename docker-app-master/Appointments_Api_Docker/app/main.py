from dotenv import load_dotenv
from fastapi import FastAPI,Form, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List,Optional
from sqlalchemy.orm import Session
from datetime import date, datetime, time, timedelta
from sqlalchemy import Boolean, Column, ForeignKey,Sequence, Integer, String,DateTime,Date

import json
import os
import sys
from datetime import timedelta,date
import os
import httpx
import redis

from api import db_manager, models, schemas
from api.db import SessionLocal, engine

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from fastapi_login import LoginManager

load_dotenv()

redis_server=os.getenv("REDIS_SERVER", default="localhost")
redis_pass=os.getenv("REDIS_PASS", default="")
print("REDIS_SERVER = {}".format(redis_server))
print("REDIS_PASS = {}".format(redis_pass))
r = redis.StrictRedis(host=redis_server, port=6379,
        password=redis_pass,charset="utf-8", decode_responses=True)


app = FastAPI()


origins=[
    "http://localhost:3000/",
    "https://localhost:3000/",
    "http://localhost:3000/client",
    "http://localhost:3000/client/",
    "http://localhost/"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""]
)




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)       

@app.post("/appointments/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return db_manager.create_appointment(db=db, appointment=appointment)



@app.get("/appointments/", response_model=List[schemas.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = db_manager.get_appointments(db, skip=skip, limit=limit)
    return appointments


@app.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db_manager.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@app.get("/appointments_carrier/{carrier_id}", response_model=List[schemas.Appointment])
def read_appointment_bycarrier(carrier_id: int, db: Session = Depends(get_db)):
    print(carrier_id)
    db_appointment = db_manager.get_appointment_by_carrier(db, carrier_id=carrier_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment for carrier not found")
    return db_appointment

@app.get("/appointments_userid/{user_id}", response_model=List[schemas.Appointment])
def read_appointment_bycarrier(user_id: int, db: Session = Depends(get_db)):
    print(user_id)
    db_appointment = db_manager.get_appointment_by_userid(db, user_id=user_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment for User not found")
    return db_appointment

@app.post("/appointments_carrier_perday/{carrier_id}",response_model=List[schemas.Appointment])
def read_appointment_bycarrier(carrier_id: int, dateofapp: date = Form(...),db: Session = Depends(get_db)):
    print(carrier_id)
    print(dateofapp)
    db_appointment = db_manager.get_appointment_by_carrieranddate(db, carrier_id=carrier_id, dateofapp =dateofapp)
    #print(db_appointment)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment for carrier not found")
    return db_appointment

@app.get("/appointments_carrier_Confirmed",response_model=List[schemas.Appointment])
def read_appointment_bycarrier(carrier_id: int, db: Session = Depends(get_db)):
    print(carrier_id)
    db_appointment = db_manager.get_appointment_by_carrier_Confirmed(db, carrier_id=carrier_id)
    #print(db_appointment)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment for carrier not found")
    return db_appointment

@app.get("/appointments_carrier_NotConfirmed",response_model=List[schemas.Appointment])
def read_appointment_bycarrier(carrier_id: int, db: Session = Depends(get_db)):
    print(carrier_id)
    db_appointment = db_manager.get_appointment_by_carrier_NotConfirmed(db, carrier_id=carrier_id)
    #print(db_appointment)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment for carrier not found")
    return db_appointment

@app.put('/appointments_update/{id}', response_model=schemas.Appointment)
def update_appointments(appointment_id: int,  db: Session = Depends(get_db)):
    print("ok")
    print(appointment_id)
    appointment = db_manager.get_appointment(db = db,appointment_id = appointment_id )
    # print(appointment)
    # print(appointment.id)
    if not appointment:
        return("Something went wrong! Appointment not found.")
    db_appointments = db_manager.update_appointment_selected(db,appointment_id,r)
    #na stelnei email ston xristi tu forea
    return db_appointments


# dict_object1 =   {
#     "number": 1,
#     "id": 0,
#     "isselected": "false",
#     "isreserved": "false",
#     "carrierid": 1
#   }

# dict_object2 =   {
#     "number": 1,
#     "id": 1,
#     "isselected": "false",
#     "isreserved": "false",
#     "carrierid": 1
#   }
# dict_object3 =   {
#     "number": 1,
#     "id": 2,
#     "isselected": "false",
#     "isreserved": "false",
#     "carrierid": 1
#   }





#pernei tin imerominia apo tin forma kai epistrefei pisw ta rantebu tis sigkekrimenis imerominias
@app.post('/appointments_allcarriers_perday',response_model=List[schemas.Appointment])
def store_to_redis(dateofapp: date = Form(...), db: Session = Depends(get_db)):
    print("hello")
    print(dateofapp)
    db_appointments = db_manager.get_appointment_by_date(db, dateofapp = dateofapp)
    return db_appointments


@app.post('/storeappointmentstoredis',response_model=schemas.Appointment)
def store_appto_redis(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appointment = db_manager.create_appointment(db=db, appointment=appointment) #prosthetei to rantevu stin vasi mas me isreserver = true mexri na to kanei confirmed o foreas
    appointmentjson = json.dumps(appointment, cls=AlchemyEncoder)
    redis = db_manager.add_redis(r, json.loads(appointmentjson), appointment.id)  #prosthetei to rantevu me id tade stn cache 
    print("REDIS")
    print(appointment)
    # print("redis vals")
   
    # print(read_redis(r,48))
    # for key in keys: r.delete(key)  
    # for key in keys: print(read_redis(r,key))
    return appointment
	
if __name__ == '__app__':
  # get_request()
    post_request()