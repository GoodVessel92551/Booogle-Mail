from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db
app = Flask(__name__)
users = web.UserStore()
@app.route('/')
def index():
    name = web.auth.name
    #print(len(db["names"]))
    if name != "":
        return redirect("/home")
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/home')
@web.authenticated
def home():
    names = db["names"]
    name = web.auth.name
    if name not in names:
        users.current["mails"] = [web.auth.name,"Booogle","Welcome","Hello "+web.auth.name+"\n\nWelcome to Booogle Mail we hope that you enjoy Booogle Mail and if you do make sure to leave a like. If you find any bug or want to suggest feedback press the button on the left. You can send mail to any one but they will only see it when they login to Booogle Mail. If you want you can mail me (GoodVessel92551). Put in the replit username NOT A EMAIL ADDRESSES. And thank you using Booogle Mail!",db["num"]]
        users.current["sent"] = []
        users.current["blocked"] = []
        db["names"].append(name)
    email = db["mail"]
    newmail = users.current["mails"]
    i = 0
    while i < len(email):
        if email[i] == web.auth.name.lower():
            if email[i] not in users.current["blocked"]:
                users.current["mails"].append(email[i])
                users.current["mails"].append(email[i+1])
                users.current["mails"].append(profanity.censor(email[i+2].title()))
                users.current["mails"].append(profanity.censor(email[i+3]))
                users.current["mails"].append(profanity.censor(email[i+4]))
            email.pop(i)
            email.pop(i)
            email.pop(i)
            email.pop(i)
            email.pop(i)
            db["mail"] = email
        print(i)
        i=i+5
    return render_template("home.html",newmail=users.current["mails"],name = web.auth.name)

@app.route('/write', methods=["POST", "GET"])
@web.authenticated
@web.per_user_ratelimit(
    max_requests = 10,
    period = 60,
    get_ratelimited_res=(lambda left: f"Too many requests, try again after {left} sec"),
)
def write():
    names = db["names"]
    name = web.auth.name
    mail = db["mail"]
    if request.method == "POST":
        if len(request.form["about"]) > 140 or len(request.form["about"]) < 1:
            return "Mail was to long or to short"
        if len(request.form["desc"]) > 1500 or len(request.form["desc"]) < 10:
            return "Mail was to long or to short"
        else:
            mail = db["mail"]
            mail.append(request.form["to"].lower())
            mail.append(web.auth.name)
            mail.append(request.form["about"])
            mail.append(request.form["desc"])
            mail.append(db["num"])
            users.current["sent"].append(request.form["to"].lower())
            users.current["sent"].append(web.auth.name)
            users.current["sent"].append(request.form["about"])
            users.current["sent"].append(request.form["desc"])
            users.current["sent"].append(db["num"])
            db["num"]=db["num"]+1
        return redirect("/home")
    else:
        return render_template("send.html",name = web.auth.name)

@app.route('/feedback', methods=["POST", "GET"])
@web.authenticated
@web.per_user_ratelimit(
    max_requests = 10,
    period = 60,
    get_ratelimited_res=(lambda left: f"Too many requests, try again after {left} sec"),
)
def feedback():
    names = db["names"]
    name = web.auth.name
    mail = db["mail"]
    if request.method == "POST":
        if len(request.form["about"]) > 140 or len(request.form["about"]) < 1:
            return "Mail was to long or to short"
        if len(request.form["desc"]) > 1500 or len(request.form["desc"]) < 10:
            return "Mail was to long or to short"
        else:
            mail.append(request.form["to"].lower())
            mail.append(web.auth.name)
            mail.append(profanity.censor(request.form["about"]))
            mail.append(profanity.censor(request.form["desc"]))
            mail.append(db["num"])
            users.current["sent"].append(request.form["to"].lower())
            users.current["sent"].append(web.auth.name)
            users.current["sent"].append(request.form["about"])
            users.current["sent"].append(request.form["desc"])
            users.current["sent"].append(db["num"])
            db["num"]=db["num"]+1
        return redirect("/home")
    else:
        return render_template("feedback.html",name = web.auth.name)

@app.route('/clear')
def clear():
    users.current["mails"] = []
    return redirect("/home")

@app.route('/sent')
def sent():
    return render_template("sent.html",name = web.auth.name, sent=users.current["sent"])

@app.route('/alive')
def alive():
    return "Admin"

@app.route('/delete')
def delete():
    id = request.args.get("id")
    try:
        int(id)
    except:
        return "Something Went Wrong"
    else:
        mail = users.current["mails"]
        for i in range(len(mail)):
            if mail[i] == str(id):
                users.current["mails"].pop(i-4)
                users.current["mails"].pop(i-4)
                users.current["mails"].pop(i-4)
                users.current["mails"].pop(i-4)
                users.current["mails"].pop(i-4)
        return redirect("/home")

@app.route('/sw.js', methods=['GET'])
def sw():
    return current_app.send_static_file('sw.js')

@app.route('/users', methods=["POST", "GET"])
def block():
    if request.method == "POST":
        block = request.form["block_it"]
        names = db["names"]
        if block in names:
            blocked = users.current["blocked"]
            if block in blocked:
                blocked.remove(block)
            else:
                blocked.append(block)
                users.current["blocked"] = blocked
                return redirect("/home")
        else:
            return "User dose not use Booogle Mail"
    return render_template("block.html",name = web.auth.name, blocked=users.current["blocked"])

@app.route('/admin')
def admin():
    if web.auth.name == "GoodVessel92551":
        return render_template("admin.html",name = web.auth.name, names=db["names"])
    else:
        return redirect("/home")
web.run(app, port=8080, debug=False)