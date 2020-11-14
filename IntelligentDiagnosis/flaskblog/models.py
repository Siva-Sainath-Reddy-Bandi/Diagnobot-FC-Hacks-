from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_patient(user_id):     # used in order to manage sessions
    return Patient.query.get(int(user_id))


class Patient(db.Model, UserMixin):   # creates a User database model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # defines the one to many relationship of a user to his/her posts
    # the author attribute is used to get the details of the user who created the post, from a post itself
    # the lazy argument means that SQLAlchemy will load all the data (posts) of a user in one go
    my_diagnoses = db.relationship('Report', backref='patient', lazy=True)

    # how the object is printed
    def __repr__(self):
        return f"Patient('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_doctor(user_id):     # used in order to manage sessions
    return Doctor.query.get(int(user_id))


class Doctor(db.Model, UserMixin):   # creates a User database model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    doctor_type = db.Column(db.String(50), nullable=False)
    payment = db.Column(db.String(10), nullable=False)
    # defines the one to many relationship of a user to his/her posts
    # the author attribute is used to get the details of the user who created the post, from a post itself
    # the lazy argument means that SQLAlchemy will load all the data (posts) of a user in one go
    reports = db.relationship('Report', backref='doctor', lazy=True)

    # how the object is printed
    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}')"


class Report(db.Model):   # creates a Post database model
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return f"Report('{self.date_posted}')"
