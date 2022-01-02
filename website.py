from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__)) 

app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "users.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    encrypted_username = db.Column(db.String(255))
    
    def __init__ (self, username, password, encrypted_username):
        self.username = username
        self.password = password
        self.encrypted_username = encrypted_username

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
                else:
                    print("Logged in")
                    encrypted_username = i[3]
                    return redirect(f"userpage/{encrypted_username}")
                    
                    
        if current_id == False:
            print("Username not found")
            
    return render_template("login.html")

@app.route("/userpage/<encrypted_username>", methods=['POST', 'GET'])
def user_page(encrypted_username):
    table_name="users"
    user = db.session.execute("SELECT * FROM users WHERE username='" + encrypted_username + "';")
    for i in user:
        print(i)
    return render_template("userhome.html", user=user)

if __name__=="__main__":
    app.run()
