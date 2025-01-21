from flask import Flask, url_for, request, render_template, session, redirect, flash

app = Flask(__name__)
app.secret_key = "meow"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        session["user"] = user
        flash("Login Successful!")
        return redirect(url_for("user_page"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user_page"))
        return render_template("login.html")

@app.route("/user")
def user_page():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user = user)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You've been logged out!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)