from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "meow"
app.permanent_session_lifetime = timedelta(days = 2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login(): 
    if request.method == "POST":
        session.permanent = True
        userName = request.form["name"]
        session["user"] = userName
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        userName = session["user"]
        return f"<h1> Hello {userName}! Have a nice day.</h1>"
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")    
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__" :
    app.run(debug=True)