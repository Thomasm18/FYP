from flask import Flask, render_template, url_for
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
    return render_template('orion.html')

if __name__ == '__main__':
	app.run(debug=True)