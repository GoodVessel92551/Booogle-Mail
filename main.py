from flask import Flask, render_template
from replit import web, db

app = Flask(__name__)
users = web.UserStore()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
@web.authenticated
def home():
    return render_template("home.html")

web.run(app, port=8080, debug=True)