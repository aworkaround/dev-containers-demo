import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()


@app.get("/")
def home_get():
    return render_template("index.html", tasks=Tasks.query.all())


@app.post("/")
def home_post():
    task = Tasks(title=request.form["title"], description=request.form["description"])
    db.session.add(task)
    db.session.commit()

    return redirect(url_for("home_get"))
