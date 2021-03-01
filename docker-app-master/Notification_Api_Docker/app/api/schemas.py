from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta


class NotificationBase(BaseModel):
    appointmentid :int 

class Notification(NotificationBase):
    id: int 
    dateandtime : datetime
    appointmentid : int
    class Config:
        orm_mode = True

class NotificationCreate(NotificationBase):
    appointmentid : int
