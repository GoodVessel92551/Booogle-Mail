from flask import Flask, render_template
from replit import web, db

app = Flask(__name__)
users = web.UserStore()

email = ["GoodVessel92551","test","test","bob","test2","test2","jeff","test3","test3"]
name = "jeff"
@app.route('/')
def index():
    newmail = []
    for i in range(len(email)):
        if email[i] == name and i%3 == 0:
            newmail.append(email[i])
            newmail.append(email[i+1])
            newmail.append(email[i+2])
            print(newmail)
            i =+ 2
    return render_template("index.html")

@app.route('/home')
@web.authenticated
def home():
    return render_template("home.html")

@app.route('/write')
@web.authenticated
def write():
    return render_template("send.html")

web.run(app, port=8080, debug=True)