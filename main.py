from better_profanity import profanity
from flask import Flask, render_template, redirect, request, current_app
from replit import web, db

app = Flask(__name__)
users = web.UserStore()
@app.route('/')
def index():
    db["num"]=0
    name = web.auth.name
    if name != "":
        return redirect("/home")
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/home')
@web.authenticated
def home():
    num = db["num"]
    names = db["names"]
    name = web.auth.name
    if name not in names:
        users.current["mails"] = [web.auth.name,"Booogle","Welcome","Hello"++web.auth.name+"\nWelcome to Booogle Mail we hope that you enjoy Booogle Mail and if you do make sure to leave a like. If you find any bug or want to suggest feedback press the button on the left. You can only send mail to people that use Booogle Mail because we don't want mail clogging up the system. And thank you using Booogle Mail!",num]
        users.current["sent"]
        db["num"]+=1
        db["names"].append(name)
        print(db["names"])
    email = db["mail"]
    newmail = users.current["mails"]
    print(email)
    print(users.current["mails"])
    for i in range(len(email)):
        if i < len(email):
            if email[i] == web.auth.name.lower() and i%5 == 0:
                print(email[i])
                users.current["mails"].append(email[i])
                users.current["mails"].append(email[i+1])
                users.current["mails"].append(email[i+2].title())
                users.current["mails"].append(email[i+3])
                users.current["mails"].append(email[i+4])
                email.pop(i)
                email.pop(i)
                email.pop(i)
                email.pop(i)
                email.pop(i)
                print(email)
                db["mail"] = email
                print(db["mail"])
            else:
                break
    return render_template("home.html",newmail=users.current["mails"],name = web.auth.name)

@app.route('/write', methods=["POST", "GET"])
@web.authenticated
def write():
    names = db["names"]
    name = web.auth.name
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
            mail.append(db["num"])
            users.current["sent"].append(request.form["to"].lower())
            users.current["sent"].append(web.auth.name)
            users.current["sent"].append(request.form["about"])
            users.current["sent"].append(request.form["desc"])
            users.current["sent"].append(db["num"])
            db["num"]=db["num"]+1
        print(mail)
        return redirect("/home")
    else:
        return render_template("send.html",name = web.auth.name)

@app.route('/feedback', methods=["POST", "GET"])
@web.authenticated
def feedback():
    names = db["names"]
    name = web.auth.name
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
            users.current["sent"].append(request.form["to"].lower())
            users.current["sent"].append(web.auth.name)
            users.current["sent"].append(request.form["about"])
            users.current["sent"].append(request.form["desc"])
            users.current["sent"].append(db["num"])
            db["num"]+=1
        print(mail)
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

@app.route('/delete')
def delete():
    id = request.args.get("id")
    print(id)
    try:
        int(id)
    except:
        return "Something Went Wrong"
    else:
        print("Hi")
        mail = users.current["mails"]
        for i in range(len(mail)):
            print(mail[i])
            if mail[i] == int(id):
                for j in range(5):
                    print("hello")
                    users.current["mails"].pop(i-5)
        return redirect("/home")

@app.route('/sw.js', methods=['GET'])
def sw():
    return current_app.send_static_file('sw.js')


web.run(app, port=8080, debug=True)