from sqlalchemy.orm import Session
from api import models, schemas
from datetime import datetime
import asyncio
import hashlib, binascii, os
from sqlalchemy import literal
import logging
#loop = asyncio.get_event_loop()

import smtplib, ssl
def send_confirm_email(email_1,email_2,password,number):
	port = 587  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = email_1
	receiver_email = email_2
	if number == 1:
	    message = """\
    Subject: Registration Confirmed!

    Your registration has been confirmed! """
        
	if number == 2:
	    message = """\
    Subject: New Appointment Notify

    New appointment from user needs confirmation! Go check it out! """

	if number == 3:
	    message = """\
    Subject: Appointment Confirmation Notify

    Your appoingment has been confirmed. Thanks for using our platform! """

	if number == 4:
	    message = """\
    Subject: Appointment Submitted

    Your appointment has been submited,it may take some time to be confirmed by host user. Thanks for using our platform! """

	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
	    server.ehlo()  # Can be omitted
	    server.starttls(context=context)
	    server.ehlo()  # Can be omitted
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, message)
	    print("success")

def get_notification(db: Session, notification_id: int):
    print(notification_id)
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()

def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Notification).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: schemas.NotificationCreate):
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    db_notif = models.Notification(dateandtime = dt_string, appointmentid = notification.appointmentid )
    #send_confirm_email("myapp.2020.sept@gmail.com",user.email,"myapp1234")
    print("notifcreated")
    print(db_notif)
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif

def get_notification_byappointment(db: Session, appointment_id: int):
    print(appointment_id)
    return db.query(models.Notification).filter(models.Notification.appointmentid == appointment_id).all()
