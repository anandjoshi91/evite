from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    location = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def data(self):
        return {'id': self.id, 'name': self.name, 'location': self.location, 'start_time': self.start_time.strftime('%d/%m/%Y %H:%M'), 'end_time': self.end_time.strftime('%d/%m/%Y %H:%M')}

    def __repr__(self):
        return str(self.data())

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def data(self):
        return {'name': self.name, 'email': self.email}

    def __repr__(self):
        return str(self.data())

class Rsvp(db.Model):
    __tablename__ = 'rsvp'
    id = db.Column(db.Integer, primary_key = True , autoincrement = True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_email = db.Column(db.String(80), db.ForeignKey('user.email'))

    def data(self):
        return {'id': self.id, 'event_id': self.event_id, 'user_email': self.user_email}

    def __repr__(self):
        return str(self.data())