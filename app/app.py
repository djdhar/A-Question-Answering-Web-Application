from flask import Flask, render_template, request, send_from_directory, flash,redirect, url_for
import os, subprocess
import html
from flask_sqlalchemy import SQLAlchemy
import dbgen as mydb
from dbgen import User
from dbgen import Question
import time
from time import sleep

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite"
db = SQLAlchemy(app)

@app.route('/READ', methods=['POST'])
def READ():
    try:
        email = request.form['emailid']
        myquestion = request.form['myquestion']
        print(myquestion)
        myuser = User.query.filter_by(email=email).first()
        ask = Question.query.filter_by(question=str(myquestion)).first()
        questions = Question.query.all()
        print(questions[0].question)
        print(ask)
        list_ans = ask.answers.split('\u0001')
        if myquestion !="":
            return render_template('answers.html', ask=ask,email=email,firstname=myuser.firstname, anslist=list_ans)
    except:
        ans = request.form['ansarea']
        myquestion = request.form['myquestion']
        email = request.form['myemail']
        myuser = User.query.filter_by(email=email).first()
        ask = Question.query.filter_by(question=myquestion).first()
        prevans = ask.answers
        print(prevans)
        newans = prevans+"\u0001"+ans
        print("New Ans = "+newans)
        db.session.query(Question).filter_by(question=myquestion).update({"answers":newans})
        db.session.commit()
        sleep(2)
        #ask = Question.query.filter_by(question=myquestion).first()
        #ask.answers = newans
        #db.session.commit()
        ask2 = db.session.query(Question).filter_by(question=myquestion).first()
        print("Answer = "+ask2.answers)
        list_ans = ask2.answers.split('\u0001') 
        return render_template('answers.html', ask=ask2,email=email,firstname=myuser.firstname, anslist=list_ans)



@app.route('/profile', methods=['POST'])
def postquestion():
    myqsn = request.form['inputbox']
    email = request.form['email']
    myuser = User.query.filter_by(email=email).first()
    #print(email)
    try:
        db.session.add(Question(question=myqsn, answers=""))
        db.session.commit()
    except:
        garbage=0
    questions = Question.query.all()
    return render_template('profile.html', user=myuser, questions=questions)

@app.route('/profile')
def profile():
    username = request.args.get('username')
    myuser = User.query.filter_by(username=username).first()
    questions = Question.query.all()
    return render_template('profile.html', user=myuser, questions=questions)

@app.route('/')
def login():
    err=""
    try:
        err= request.args.get('err')
        if err==None:
            err=""
    except:
        gb=0
    return render_template('login.html',err=err)

@app.route('/', methods=['POST'])
def Loginevent() :
    useremail = request.form['useremail']
    password = request.form['password']
    print(useremail)
    print(password)
    myuserEmail = User.query.filter_by(email=useremail ,password=password ).first()
    myuserName = User.query.filter_by(username=useremail ,password=password ).first()
    #print(myuser)
    users = User.query.all()
    print(myuserEmail)
    print(myuserName)
    if myuserName is None:
        if myuserEmail is None:
            return render_template('login.html',err="** User not found. Retry login.")
        else:
            print(myuserName)
            #return redirect(url_for('profile',user=myuserName))
            return redirect(url_for('profile',username=myuserEmail.username))
    else:
        #return redirect(url_for('profile',user=myuserEmail))
        return redirect(url_for('profile',username=myuserName.username))

@app.route('/DibyajyotiDhar')
def details():
    users = User.query.all()
    #questions = Question.query.all()
    return render_template('result.html',users=users)

@app.route('/REG')
def index():
    return render_template('formpage.html',err="")

# Add Event to database
@app.route('/REG', methods=['POST'])
def createvent() :
    firstname =  request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    email = request.form['email']
    password = request.form['password']
    mylist = [firstname,lastname,username,city,state,zip,email,password]
    print(mylist)
    #db.execute("INSERT INTO events (user_id, title, description, place, start, end) VALUES (:user, :title, :description, :place, :start, :end)",
    #           user=session["user_id"], title=title, description=description, place=place, start=start, end=end)
    result = request.form
    ret = ""
    try:
        db.session.add(User(firstname=firstname,lastname=lastname,username=username,city=city,state=state,zip=zip,email=email,password=password))
        db.session.commit()
        users = User.query.all()
        for u in users:
            ret =ret + "{ "+ u.firstname +" , "+u.lastname+" , "+u.username+" , "+u.email+" }"
        return redirect(url_for('login',err="User Registered successfully"))
        #return render_template('login.html', msg = "Data Successfully Recorder")
    except:
        return render_template('formpage.html', err="**Email ID / Username already exsists, register with a new email address.")




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
