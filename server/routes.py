from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from server import app, db, bcrypt
from datetime import datetime
from server.models import User, Booking
from server.booking import checkSlots, bookSlots
from server.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/index.html')
@app.route('/')
def home():
    return render_template('index.html', main='True')

@app.route('/booking')
def book():
    return render_template('book.html', section='portfolio')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, battery = form.battery.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form= form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #Remembers previous requested area of user
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsucessful, Check email and password', 'danger')
    return render_template('login.html', form= form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/timing')
@login_required
def timing():
    table = checkSlots()
    return render_template('orion.html', table=table, section='portfolio')


@app.route('/_bookTime')
def bookTime():
    slotId = request.args.get('id', type=int)
    bookSlots(slotId)
    return str(1)