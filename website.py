from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__)) 

app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "users.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()

db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    encrypted_username = db.Column(db.String(255))

class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    survey_name = db.Column(db.String(255))

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_name = db.Column(db.String(255))
    question = db.Column(db.String(255))
    
class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(255))
    score = db.Column(db.Integer)
            
db.create_all()
@app.route("/")
def index(methods=['POST', 'GET']):
    return render_template("index.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

            new_password = request.form['password']
            new_username = request.form['username']
            encrypted_name = ''.join(format(ord(x), "b") for x in new_username)

                
            new_user = Users(username=new_username, password=new_password, encrypted_username=encrypted_name)
            db.session.add(new_user)
            db.session.commit()
        
    return render_template("signup.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    current_username = False
    current_password = False
    if request.method == "POST":
        current_username = False
        current_password = False
        current_username = request.form['username']
        current_password = request.form['password']
        print(current_username)
        
        users = db.session.execute("SELECT * FROM users;")
        current_id = False
        for i in users:
            if i[1] == current_username:
                current_id = i[0]
                if i[2] != current_password:
                    print("Password does not match")
                    data = {
                        "message": "Password does not match"
                        }
                    return render_template("login.html", messages={'main': "Password does not match"})
                else:
                    print("Logged in")
                    encrypted_username = i[3]
                    return redirect(f"/user/{encrypted_username}")
                    
                    
        if current_id == False:
            print("Username not found")
            
    return render_template("login.html")


@app.route("/user/<encrypted_username>", methods=['POST', 'GET'])
def user_page(encrypted_username):
    
    user = db.session.execute("SELECT * FROM users WHERE encrypted_username='" + encrypted_username + "';")
    for i in user:
        items=dict(i)
    
    encrypted_name = items['encrypted_username']
    create_survey_link = "/user/" + encrypted_name + "/create_survey/"


    return render_template("userhome.html", user=user, items=items, create_survey_link=create_survey_link)



@app.route("/user/<encrypted_username>/create_survey/", methods=['POST', 'GET'])
def create_survey(encrypted_username):

    if request.method=="POST":
    
        current_survey_name = request.form["surveyname"]
        user = db.session.execute("SELECT * FROM users WHERE encrypted_username='" + encrypted_username + "';")
        for i in user:
            items=dict(i)
        survey_creator_username = items['username']
        
        
        new_survey = Surveys(username=survey_creator_username,  survey_name=current_survey_name)
        db.session.add(new_survey)
        db.session.commit()
        
        
    return render_template("create_survey.html")


if __name__=="__main__":
    app.run()
