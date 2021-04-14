from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/booking')
def book():
    return render_template('book.html')

if __name__ == '__main__':
	app.run(debug=True)