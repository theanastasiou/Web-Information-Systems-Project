from fastapi import Depends, FastAPI, HTTPException
import requests
from typing import List
from sqlalchemy.orm import Session
from api import db_manager
from api import models
from api import schemas
import os; 
from api.db import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins=[
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:3000/carriers",
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

@app.get("/carrierbycarrierid/{carrierid}", response_model=schemas.Carrier)
def getCarrierbycarrierid(carrierid: int, db: Session = Depends(db_manager.get_db)):
    print("okgoogle")
    print(carrierid)
    db_carrier = db.query(models.Carrier).filter(models.Carrier.id == carrierid).first()
    print(db_carrier)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="carrier not found")
    return db_carrier

@app.get('/carriers')
async def get_carriers():
    response = requests.get('https://hr.apografi.gov.gr/api/public/organizations')
    json_response = response.json()
    return json_response

@app.get("/carrierbyuserid/{user_id}", response_model=schemas.Carrier)
def getCarrierbyuseri(user_id: int, db: Session = Depends(db_manager.get_db)):
    db_carrier = db_manager.get_carrierbyid(user_id = user_id, db = db)
    print(db_carrier)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="carrier not found")
    return db_carrier    

@app.get('/carrier/{carrierid}')
def get_carrier(carrierid: str):
    url = 'https://hr.apografi.gov.gr/api/public/organizations/'+carrierid
    response = requests.get(url)
    
    json_response = response.json()
    return json_response

@app.get('/carrierT/{title}')
def search_carrier(title: str): 
    response = requests.post('https://hr.apografi.gov.gr/api/public/organizations/search',
                             json={"preferredLabel": title})
    json_response = response.json()
    return json_response

@app.post("/createcarrier/",response_model=schemas.Carrier)
def save_carrier_(carrier: schemas.CarrierCreate, db: Session = Depends(db_manager.get_db)):
    return db_manager.save_carrier(db=db, carrier=carrier)

if __name__ == '__main__':
    # get_request()
    post_request()
