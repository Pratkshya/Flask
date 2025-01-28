from flask import Flask, render_template, request, url_for,session,flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import time

app = Flask(__name__)
app.secret_key = "piksy#3421"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable=False)
    pwd = db.Column(db.String(100), unique = True, nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    body = db.Column(db.Text, nullable=False)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
            username = request.form["username"]
            pwd = request.form["pwd"]
            if not username.strip() or not pwd.strip():
                 flash("Username and Password cannot be empty")
                 return redirect("/")
            session["user"] = username

            user = users.query.filter_by(username = username).first()
            if not user:
                 user = users(username = username, pwd = pwd)
                 db.session.add(user)
                 db.session.commit()

            flash("Login Successful!")     
            return redirect("/blog")
    return render_template("login.html")

@app.route("/blog", methods=["GET", "POST"])
def blog():
    if "user" not in session:
        flash("Please log in first!")
        return redirect("/")
    
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        if not title.strip() or not body.strip():
            flash("Title and Body cannot be empty!")
            return redirect("/blog")
        
        new_blog = Blog(title=title, body=body)
        db.session.add(new_blog)
        db.session.commit()
        flash("Blog entry added!")
    
    blogs = Blog.query.order_by(Blog.date.desc()).all()
    return render_template("blog.html", blogs=blogs, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect("/")
if __name__ == '__main__':
    with app.app_context():
         db.create_all()
    app.run(debug=True)
