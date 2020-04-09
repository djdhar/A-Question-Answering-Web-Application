from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    state = db.Column(db.String(20), unique=False, nullable=False)
    zip = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String, unique=False, nullable=False)

class Question(db.Model):
    question = db.Column(db.String(40), unique=True, nullable=False, primary_key=True)
    answers = db.Column(db.String(5000), unique=False, nullable=False)

db.create_all()
db.session.commit()
users = User.query.all()
