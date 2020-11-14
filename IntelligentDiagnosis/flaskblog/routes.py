import os
import secrets  # allows to create random hex name so that picture file names do not repeat
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import PatientRegistrationForm, DoctorRegistrationForm, LoginForm, ChatForm, UserTypeForm
from flaskblog.models import Patient, Doctor, Report
from flask_login import login_user, current_user, logout_user, login_required

# note: shift + tab to indent one tab space backwards
# note: alt + j to select next occurrence of highlighted text


@app.route("/")  # decorator
@app.route("/home")
def home():
    return render_template('home.html')    # the variable posts can now be accessed from the html file


@app.route("/user_type", methods=['GET', 'POST'])
def user_type():
    form = UserTypeForm()
    if form.validate_on_submit():
        if form.user_type.data == 'Patient':
            return redirect(url_for('register_patient'))
        else:
            return redirect(url_for('register_doctor'))
    return render_template('user_type.html', title='User Type', form=form)


@app.route("/register/patient", methods=['GET', 'POST'])
def register_patient():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        # stores a string of random character (i.e. the hashed password) into hashed_password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        patient = Patient(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(patient)
        db.session.commit()
        # second argument is a bootstrap class
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('patient_register.html', title='Register', form=form)


@app.route("/register/doctor", methods=['GET', 'POST'])
def register_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        # stores a string of random character (i.e. the hashed password) into hashed_password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        doctor = Doctor(username=form.username.data, email=form.email.data, doctor_type=form.doctor_type.data, payment=form.payment.data, password=hashed_password)
        db.session.add(doctor)
        db.session.commit()
        # second argument is a bootstrap class
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('doctor_register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = None

        if Patient.query.filter_by(email=form.email.data).first():
            user = Patient.query.filter_by(email=form.email.data).first()
        elif Doctor.query.filter_by(email=form.email.data).first():
            user = Doctor.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/diagnoBot")
def diagnoBot():
    return render_template('diagnoBot.html', title='diagnoBot')


@app.route("/my_diagnoses")
def my_diagnoses():
    return render_template('my_diagnoses.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')