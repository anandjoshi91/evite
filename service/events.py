from model.model import Event
from model.model import db
from datetime import datetime
import service.users as user_service

def getAllEvents():
    events = Event.query.all()
    return events


def getEventById(id):
    if id:
        return Event.query.get(id)

def createAnEvent(event):
    print('Creating event'+str(event));
    if event:
        newEvent = Event(name=event['name'], location=event['location'],
         start_time=datetime.strptime(event['startDate'], '%d/%m/%Y %H:%M'),
          end_time=datetime.strptime(event['endDate'], '%d/%m/%Y %H:%M'))
        db.session.add(newEvent)
        db.session.commit()
        return {'result' : 'Event Created'}

def getEventDetails(eventId):
    event = getEventById(eventId)
    users = user_service.getUsersInEvent(eventId)
    event.users = users
    return event