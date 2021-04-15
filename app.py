from flask import Flask, render_template, url_for, redirect, request, jsonify, flash, Response
from test import test
app = Flask(__name__)

table = [
    {
        'id': '1', 
        'time': '10 AM',
        'cost': 'INR 18',
        'saving': 'INR 1.8'
    },
    {
        'id': '2', 
        'time': '11 AM',
        'cost': 'INR 12.6',
        'saving': 'INR 7.2'
    },
    {
        'id': '3', 
        'time': '12 PM',
        'cost': 'INR 12.6',
        'saving': 'INR 7.2'
    },
    {
        'id': '4', 
        'time': '1 PM',
        'cost': 'INR 14.4',
        'saving': 'INR 5.4'
    },
    {
        'id': '5', 
        'time': '2 PM',
        'cost': 'INR 14.4',
        'saving': 'INR 5.4'
    },
    {
        'id': '6', 
        'time': '3 PM',
        'cost': 'INR 12.6',
        'saving': 'INR 7.2'
    },
    {
        'id': '7', 
        'time': '4 PM',
        'cost': 'INR 12.6',
        'saving': 'INR 7.2'
    }
]


@app.route('/index.html')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def book():
    return render_template('book.html')

@app.route('/timing1')
def orion():
    return render_template('orion.html', table=table)

@app.route('/_bookTime')
def bookTime():
    slotId = request.args.get('id', type=int)
    print(slotId)
    return str(1)

if __name__ == '__main__':
	app.run(debug=True)