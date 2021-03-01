from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class AppointmentBase(BaseModel):
    number: int


class AppointmentCreate(AppointmentBase):
    number: int
    isselected : bool
    isreserved : bool
    carrierid : int
    dateofapp : date 
    userid : int

class Appointment(AppointmentBase):
    id: int
    number: int
    isselected : bool
    isreserved : bool
    carrierid : int
    dateofapp : date 
    userid : int
    class Config:
        orm_mode = True

class AppointmentUpdate(Appointment):
    #id:Optional[int] = None
    #number: Optional[int] = None
    isselected : Optional[bool] = None
    isreserved : Optional[bool] = None
    #carrierid : Optional[int] = None
    #dateofapp : Optional[date] = None 

