from sqlalchemy.orm import Session
from api import models, schemas
from sqlalchemy import Boolean, Column, ForeignKey,Sequence, Integer, String,DateTime,Date
import asyncio
import hashlib, binascii, os
from sqlalchemy import literal
import logging
from datetime import date, datetime, time, timedelta
#loop = asyncio.get_event_loop()
import redis
import requests

import smtplib, ssl

def get_appointment(db: Session, appointment_id: int):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        return("Something went wrong! Appointment not found.")
    return appointment

def update_appointment_selected(db: Session, appointment_id : int, r : redis.Redis ):
    print(appointment_id)
    print("pl")
    update_view = get_appointment(db= db, appointment_id = appointment_id)
    if not update_view:
        return("Something went wrong! Appointment not found.")
    print(update_view.id)
    r.delete(update_view.id) #delete from redis cache afu pleon ginete confirmed
    #kanonika edo prepei na stelnei mail kai ston user oti to appointment tu egine confirm
    print(update_view.userid)
    url1 = "http://0.0.0.0:8000/users/"+str(update_view.userid)
    response2 = requests.get(url1)
    print("EMAIL")
    user  = response2.json()
    print(user["email"])
    url = 'http://0.0.0.0:8003/notifications/'+user["email"]+'&'+str(update_view.id)+'&'+str(3)
    response = requests.post(url)
    response = requests.post(url)
    if update_view:
        print ('update view found: ', update_view.id)
        update_view.isselected = True 
        update_view.isreserved = False
        db.add(update_view) 
        db.commit() 
        return update_view

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_appointment_by_carrier(db: Session, carrier_id: int):
    print(carrier_id)
    return db.query(models.Appointment).filter(models.Appointment.carrierid == carrier_id).all()

def get_appointment_by_userid(db: Session, user_id: int):
    print(user_id)
    return db.query(models.Appointment).filter(models.Appointment.userid == user_id).all()


def get_appointment_by_carrieranddate(db: Session, carrier_id: str, dateofapp: date):
    print(dateofapp)
    print(carrier_id)
    return db.query(models.Appointment).filter(models.Appointment.carrierid == carrier_id).filter(models.Appointment.dateofapp == dateofapp).all()

def get_appointment_by_carrier_NotConfirmed(db: Session, carrier_id: int):
    print(carrier_id)
    return db.query(models.Appointment).filter(models.Appointment.carrierid == carrier_id).filter(models.Appointment.isselected == False).filter(models.Appointment.isreserved == True).all()


def get_appointment_by_carrier_Confirmed(db: Session, carrier_id: int, ):
    print(carrier_id)
  
    return db.query(models.Appointment).filter(models.Appointment.carrierid == carrier_id).filter(models.Appointment.isselected == True).filter(models.Appointment.isreserved== False).all()


def get_appointment_by_date(db: Session, dateofapp: Date):
    print(dateofapp)
    return db.query(models.Appointment).filter(models.Appointment.dateofapp == dateofapp).all()


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    print('Helloo')
    db_appointment = models.Appointment(number=appointment.number, isselected=appointment.isselected, isreserved=appointment.isreserved,carrierid=appointment.carrierid, dateofapp = appointment.dateofapp, userid = appointment.userid)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    url3 = 'http://0.0.0.0:8000/users/'+str(db_appointment.userid)
    response3 = requests.get(url3)
    #print("EMAIL")
    useremail  = response3.json()
    print(useremail["email"])
    # print(useremail.email)
    # print("carrierid:")
    # print(db_appointment.carrierid)
    url = 'http://0.0.0.0:8001/carrierbycarrierid/'+str(db_appointment.carrierid)
    response = requests.get(url)
    # print(response)
    carrier  = response.json()
    # print(carrier)
    print(carrier["userid"])
    # print("EMAIL")
    # print()
    url2 = 'http://0.0.0.0:8000/users/'+str(carrier["userid"])
    response2 = requests.get(url2)
    #print("EMAIL")
    carrieruser  = response2.json()
    #print(carrieruser["email"])
    appint = str(db_appointment.id)

    #carrieremailjson = json.dumps(carrieruseremail, cls=AlchemyEncoder)
    # payload = {"carriermail": carrieruseremail.email, "appointmendit" :appint, "number" : 4 }

    url1 = 'http://0.0.0.0:8003/notifications/'+carrieruser["email"]+'&'+str(appint)+'&'+str(2)
    response1 = requests.post(url1)

    url4 = 'http://0.0.0.0:8003/notifications/'+useremail["email"]+'&'+str(appint)+'&'+ str(4)
    response4 = requests.post(url4)
    return db_appointment
    
def add_redis(redis, app_object, appointmentid):
#   print("Wtf")
#   print(app_object)
  #pip install redis==2.10.6 allios xtipaei se NONTYPE
  return redis.hmset(appointmentid,app_object)

def read_redis(redis, appointmentid):
  return redis.hgetall(appointmentid)

# add_redis(r,dict_object1, 0)
# add_redis(r,dict_object2,1)
# add_redis(r,dict_object3,2)
# print("redis from before")

# print(read_redis(r,1))
