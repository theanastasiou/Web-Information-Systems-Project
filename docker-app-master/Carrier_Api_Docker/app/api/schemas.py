from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta



class CarrierBase(BaseModel):
    id: str
class CarrierCreate(CarrierBase):
    id: int
    name: str
    userid : int

class Carrier(CarrierBase):
    id: int
    name: str
    userid : int
    class Config:
        orm_mode = True
