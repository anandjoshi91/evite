import smtplib
from email.message import EmailMessage
import config as cfg

def notifyAdmin(eventId, userEmail):
    """
    Send notification to admin
    """

    msg = EmailMessage()
    msg['Subject'] = 'User - '+str(userEmail)+' subscribed for event no - '+str(eventId)
    msg['From'] = 'subscription@evite.com'
    msg['To'] = cfg.adminEmail

    print('Email - '+str(msg))

    # with smtplib.SMTP('smtp.gmail.com', 587) as s:
    #     s.send_message(msg)