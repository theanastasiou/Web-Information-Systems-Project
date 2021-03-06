from sqlalchemy import Boolean, Column, ForeignKey,Sequence, Integer, String,DateTime,Date
from sqlalchemy.orm import relationship
from sqlalchemy.schema import  PrimaryKeyConstraint
from .db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'myuser'
    
    userid = Column(Integer, Sequence('myuser_userid_seq'), primary_key=True)
    name = Column( String(25))
    surname = Column( String(25))
    username = Column( String(15))
    email = Column( String(25))
    password = Column( String(50))
    dateofbirth = Column( DateTime)
    role = Column(Integer)
    userappointment = relationship("Appointment",back_populates="appointmentuser")


class Carrier(Base):
    __tablename__='carriers'

    id = Column(Integer, Sequence('carriers_id_seq'), primary_key=True)
    name = Column(String(25))
    userid = Column(Integer,ForeignKey("myuser.userid"))

    carrieruser = relationship("User")
    cappointments = relationship("Appointment",back_populates="appoitnmentcarrier")

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, Sequence('appointments_id_seq'), primary_key=True)
    number = Column( Integer)
    isreserved = Column(Boolean)
    isselected = Column(Boolean)
    carrierid = Column(Integer, ForeignKey('carriers.id', onupdate='CASCADE', ondelete='CASCADE'))
    appoitnmentcarrier = relationship("Carrier",back_populates="cappointments")
    dateofapp = Column(DateTime)
    userid = Column(Integer, ForeignKey('myuser.userid', onupdate='CASCADE', ondelete='CASCADE'))
    appointmentuser = relationship("User",back_populates="userappointment")
    notifications = relationship("Notification",back_populates="appointmentnotif")
 

class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, Sequence('notification_id_seq'), primary_key=True)
    dateandtime = Column( DateTime)
    appointmentid = Column(Integer, ForeignKey('appointments.id', onupdate='CASCADE', ondelete='CASCADE'))
    appointmentnotif = relationship("Appointment",back_populates="notifications")