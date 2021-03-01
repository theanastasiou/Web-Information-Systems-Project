from sqlalchemy.orm import Session
from api import models, schemas
from api.db import SessionLocal
import asyncio
import hashlib, binascii, os
from sqlalchemy import literal
import logging
#loop = asyncio.get_event_loop()


import smtplib, ssl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_request():
    response = requests.get('https://hr.apografi.gov.gr/api/public/organizations')
    json_response = response.json()
    print(json_response)


def post_request():
    url = 'https://hr.apografi.gov.gr/api/public/organizations/search'
    mydata = {"code": "61928"}
    response = requests.post('https://hr.apografi.gov.gr/api/public/organizations/search', json={"preferredLabel": "ΑΚΑΔΗΜΙΑ ΑΘΗΝΩΝ"})
    json_response = response.json()
    print(json_response)


def save_carrier(db: Session, carrier: schemas.CarrierCreate):
    db_carrier = models.Carrier(id=carrier.id, name=carrier.name, userid=carrier.userid )
    db.add(db_carrier)
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


def get_carrierbyid(user_id :int ,db: Session):
    print('Helloo')
    db_carrier = db.query(models.Carrier).filter(models.Carrier.userid == user_id).first()
    return db_carrier