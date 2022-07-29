from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db

app = Flask(__name__)
users = web.UserStore()
names = ["GoodVessel92551","bob","jeff"]
name = "GoodVessel92551"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
@web.authenticated
def home():
    email = db["mail"]
    newmail = users.current["mails"]
    for i in range(len(email)):
        if i < len(email):
            if email[i] == web.auth.name.lower() and i%4 == 0:
                print(email[i])
                users.current["mails"].append(email[i])
                users.current["mails"].append(email[i+1])
                users.current["mails"].append(email[i+2])
                users.current["mails"].append(email[i+3])
                email.pop(i)
                email.pop(i)
                email.pop(i)
                email.pop(i)
                print(email)
                db["mail"] = email
                print(db["mail"])
            else:
                break
    return render_template("home.html",newmail=users.current["mails"])

@app.route('/write', methods=["POST", "GET"])
@web.authenticated
def write():
    mail = db["mail"]
    if request.method == "POST":
        if request.form["to"] not in names:
            return "User dose not exsite on Booogle Mail"
        elif len(request.form["about"]) > 140 or len(request.form["about"]) < 1:
            return "Mail was to long or to short"
        if len(request.form["desc"]) > 1500 or len(request.form["desc"]) < 10:
            return "Mail was to long or to short"
        else:
            mail.append(request.form["to"].lower())
            mail.append(web.auth.name)
            mail.append(request.form["about"])
            mail.append(request.form["desc"])
        print(mail)
        return redirect("/home")
    else:
        return render_template("send.html")

web.run(app, port=8080, debug=True)