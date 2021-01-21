from model.model import Event, User, Rsvp
from model.model import db
import service.email as mail

def addUserToEvent(name, email, event_id):
    user = getUserByEmail(email)
    rsvp = getRsvp(event_id, email)

    if user is None:
        newUser = User(email=email, name=name)
        db.session.add(newUser)
        db.session.commit()

    if rsvp is None:
        newRsvp = Rsvp(event_id=event_id, user_email=email)
        db.session.add(newRsvp)
        db.session.commit()
        mail.notifyAdmin(event_id, email)


def removeUserInEvent(email, eventId):
    user = getUserByEmail(email)
    rsvp = getRsvp(eventId, email)

    if user is None or rsvp is None:
        raise Exception('Invalid user or event')

    db.session.delete(rsvp)
    db.session.commit()



def getUserByEmail(email):
    if email:
        return User.query.get(email)

def getRsvp(event_id, email):
    if event_id and email:
        return Rsvp.query.filter(Rsvp.event_id == event_id).filter(Rsvp.user_email == email).first()

def getUsersInEvent(eventId):
    if eventId:
        rsvpResult = Rsvp.query.filter(Rsvp.event_id == eventId).all()
        users = list(map(lambda e: e.user_email, rsvpResult))
        return users