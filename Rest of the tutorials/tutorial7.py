from flask import Flask, url_for, request, render_template, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "meow"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all() )
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        session["user"] = user

        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user_page"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user_page"))
        return render_template("login.html")

@app.route("/user", methods=["GET", "POST"])
def user_page():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name = user).first()
            found_user.email = email
            db.session.commit()
            flash("Email saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email = email)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You've been logged out!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)