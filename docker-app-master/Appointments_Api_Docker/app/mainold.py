from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api import db_manager, models, schemas
from api.db import SessionLocal, engine

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

import os; 

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

@app.get("/appointments_carrier/{carrier_id}", response_model=schemas.Appointment)
def read_appointment_bycarrier(carrier_id: int, db: Session = Depends(get_db)):
    print(carrier_id)
    db_appointment = db_manager.get_appointment_by_carrier(db, carrier_id=carrier_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment for carrier not found")
    return db_appointment
