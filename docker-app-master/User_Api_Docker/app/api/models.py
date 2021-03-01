from sqlalchemy import Boolean, Column, ForeignKey,Sequence, Integer, String,DateTime,Date
from sqlalchemy.orm import relationship
from sqlalchemy.schema import  PrimaryKeyConstraint
from .db import Base

class User(Base):
    __tablename__ = 'myusers'
    
    userid = Column(Integer, primary_key=True)
    name = Column( String(25))
    surname = Column( String(25))
    username = Column( String(15))
    email = Column( String(25))
    password = Column( String(500))
    dateofbirth = Column( DateTime)
    role = Column(Integer)


