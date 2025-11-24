from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10))  # coach / client
    assigned_coach_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    coach_id = db.Column(db.Integer, nullable=False)


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))  # FIXED
    workout_plan = db.Column(db.Text)  # JSON string
    nutrition_plan = db.Column(db.Text)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))  # FIXED
    date = db.Column(db.Date)
    workout = db.Column(db.Text)
    measurements = db.Column(db.Text)
    photo = db.Column(db.String(200))
    approved = db.Column(db.Boolean, default=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    date = db.Column(db.Date)
    weight = db.Column(db.Float)
    workout_log = db.Column(db.Text)
    measurements = db.Column(db.Text)  # JSON string if needed
    photos = db.Column(db.Text)  
