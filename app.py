from flask import Flask, render_template, url_for, redirect, request, jsonify, flash, Response
from booking import checkSlots, bookSlots
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '549ba1cdd689b65d9725eed6f1fcc666'

@app.route('/index.html')
@app.route('/')
def home():
    return render_template('index.html', main='True')

@app.route('/booking')
def book():
    return render_template('book.html', section='portfolio')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form= form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@nitt.edu' and form.password.data == '123':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsucessful', 'danger')
    return render_template('login.html', form= form)

@app.route('/timing1')
def orion():
    table = checkSlots()
    return render_template('orion.html', table=table, section='portfolio')

@app.route('/_bookTime')
def bookTime():
    slotId = request.args.get('id', type=int)
    bookSlots(slotId)
    return str(1)


if __name__ == '__main__':
	app.run(debug=True)