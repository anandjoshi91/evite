import os

from flask import request, render_template, Flask, redirect, url_for, json

from model.model import db
import service.events as event_service
import service.users as user_service
import service.auth as auth_service
from flask_swagger_ui import get_swaggerui_blueprint
import config as cfg

project_dir = os.path.dirname(os.path.abspath(__file__))
SWAGGER_URL = '/api/docs'

app = Flask(__name__)

###################### Swagger Config ######################

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    '/static/swagger.json',
    config={  # Swagger UI config overrides
        'app_name': "Evite - Event Management made easy"
    }
)

app.register_blueprint(swaggerui_blueprint)

database_file = "sqlite:///{}".format(os.path.join(project_dir, "evitedatabase.db"))


app.config["SQLALCHEMY_DATABASE_URI"] = database_file


######################### Web - view routing  #############################


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/events", methods=["GET"])
def eventsView():
    e = event_service.getAllEvents()
    return render_template('events.html', events = e)

@app.route("/createEvent", methods=["POST"])
def createEventView():
    try:
        if request.form:
            event_service.createAnEvent(request.form)
            return redirect(url_for('eventsView'))
    except Exception as e:
        return registerView('Please check your input - event name should be unique. Date should be in mentioned format')


@app.route("/register")
def registerView(error=''):
    return render_template('register.html', error=error)

@app.route("/rsvp/<eventId>")
def rsvpView(eventId='', error=''):
    event = event_service.getEventById(eventId)
    return render_template('rsvp.html', event=event, error=error)

@app.route("/addUserToEvent", methods=["POST"])
def addUserToEventView():
    try:
        if request.form['email'] and request.form['event']:
            user_service.addUserToEvent(request.form['name'], request.form['email'], request.form['eventId'])
            return render_template('result.html', event=request.form['event'], person=request.form['name'])
    except Exception as e:
        print(str(e))
        return render_template('result.html', event=request.form['event'])

@app.route("/eventDetails/<eventId>")
def eventDetailsView(eventId='', error=''):
    event = event_service.getEventDetails(eventId)
    return render_template('details.html', event=event, error=error)



######################### Web - api routing  ############################# 


def getCommonErrorRes(err):
    return app.response_class(
        response=json.dumps({"error": str(err)}),
        status=500,
        mimetype='application/json'
    )

@app.route("/api/v1/events", methods=["GET"])
def getAllEvents():
    try:
        auth_service.validateApiKey(request.headers.get('apiKey'))
        events = event_service.getAllEvents()
        events = list(map(lambda e: e.data(), events))
        response = app.response_class(
        response=json.dumps(events),
        status=200,
        mimetype='application/json'
        )
        return response
    except Exception as e:
        print(str(e))
        return getCommonErrorRes(e)

@app.route("/api/v1/events/<eventId>", methods=["GET"])
def getEventById(eventId):
    try:
        auth_service.validateApiKey(request.headers.get('apiKey'))
        event = event_service.getEventById(eventId)
        response = app.response_class(
        response=json.dumps(event.data()),
        status=200,
        mimetype='application/json'
        )
        return response
    except Exception as e:
        print(str(e))
        return getCommonErrorRes(e)

@app.route("/api/v1/events", methods=["POST"])
def postEvent():
    try:
        auth_service.validateApiKey(request.headers.get('apiKey'))
        event = {'name': request.json['name'],
        'location': request.json['location'],
        'startDate': request.json['startDate'],
        'endDate': request.json['endDate']}
        res = event_service.createAnEvent(event)
        response = app.response_class(
        response=json.dumps(res),
        status=201,
        mimetype='application/json'
        )
        return response
    except Exception as e:
        print(str(e))
        return getCommonErrorRes(e)

@app.route("/api/v1/events/<eventId>/signup", methods=["POST"])
def signUpForEvent(eventId):
    try:
        auth_service.validateApiKey(request.headers.get('apiKey'))
        user_service.addUserToEvent(request.json['name'], request.json['email'], eventId)
        response = app.response_class(
        response=json.dumps({'result': 'User signed up successfully'}),
        status=201,
        mimetype='application/json'
        )
        return response
    except Exception as e:
        print(str(e))
        return getCommonErrorRes(e)

@app.route("/api/v1/events/<eventId>/signup", methods=["DELETE"])
def cancelSignUpForEvent(eventId):
    try:
        auth_service.validateApiKey(request.headers.get('apiKey'))
        user_service.removeUserInEvent(request.json['email'], eventId)
        response = app.response_class(
        response=json.dumps({'result': 'User removed from event'}),
        status=200,
        mimetype='application/json'
        )
        return response
    except Exception as e:
        print(str(e))
        return getCommonErrorRes(e)

@app.route("/api/v1/events/<eventId>/users", methods=["GET"])
def getUsersInEvent(eventId):
    try:
        auth_service.validateApiKey(request.headers.get('apiKey'))
        users = user_service.getUsersInEvent(eventId)
        response = app.response_class(
        response=json.dumps(users),
        status=200,
        mimetype='application/json'
        )
        return response
    except Exception as e:
        print(str(e))
        return getCommonErrorRes(e)

def init_db():
    db.init_app(app)
    db.app = app
    db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(host=cfg.host, port=cfg.port, debug=True)