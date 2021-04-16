from flask import Flask, render_template, url_for, redirect, request, jsonify, flash, Response
from booking import checkSlots, bookSlots
app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def book():
    return render_template('book.html')

@app.route('/timing1')
def orion():
    table = checkSlots()
    return render_template('orion.html', table=table)

@app.route('/_bookTime')
def bookTime():
    slotId = request.args.get('id', type=int)
    bookSlots(slotId)
    return str(1)

if __name__ == '__main__':
	app.run(debug=True)