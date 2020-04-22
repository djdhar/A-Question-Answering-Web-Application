from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbgen import Question
from dbgen import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite"
db = SQLAlchemy(app)
num_rows_deleted = db.session.query(Question).delete()
db.session.commit()