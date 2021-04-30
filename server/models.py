from datetime import date
from server import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    battery = db.Column(db.Numeric, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    booking = db.relationship('Booking', backref='user', lazy = True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.battery}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.time}','{self.date}','{self.user_id}')"