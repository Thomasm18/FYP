# Clears all data from User and Booking Table
from server import db
from server.models import User, Booking
User.query.delete()
Booking.query.delete()
db.session.commit()