from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(basedir, "users.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    encrypted_username = db.Column(db.String(255))


class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(100))
    survey_name = db.Column(db.String(255))
    survey_type = db.Column(db.String(10))


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(100))
    survey_name = db.Column(db.String(255))
    question = db.Column(db.String(255))


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(255))
    survey = db.Column(db.String(255))
    question = db.Column(db.String(255))
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

        new_user = Users(username=new_username, password=new_password,
                         encrypted_username=encrypted_name)
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

                    return render_template("login.html",
                                           messages={
                                            'main': "Password does not match"})
                                        
                else:
                    print("Logged in")
                    encrypted_username = i[3]
                    return redirect(f"/user/{encrypted_username}")

        if current_id == False:
            print("Username not found")

    return render_template("login.html")


@app.route("/user/<encrypted_username>", methods=['POST', 'GET'])
def user_page(encrypted_username):

    user = db.session.execute(
        "SELECT * FROM users WHERE encrypted_username='" + encrypted_username + "';")
    for i in user:
        items = dict(i)

    encrypted_name = items['encrypted_username']
    username = items['username']
    create_survey_link = "/user/" + encrypted_name + "/create_survey/"

    users_surveys = db.session.execute(
        "SELECT id, survey_name FROM surveys WHERE username='" + username + "';"
    )
    
    surveys = []
    for survey_id, survey in users_surveys:
        survey_link = url_for("answer_survey", survey_id=survey_id)
        surveys.append([survey_link, survey])

    return render_template("userhome.html", user=user, username=username,
                           items=items, create_survey_link=create_survey_link, surveys=surveys,
                           encrypted_username=encrypted_name)


@app.route("/user/<encrypted_username>/create_survey/", methods=['POST', 'GET'])
def create_survey(encrypted_username):

    if request.method == "POST":

        current_survey_name = request.form["surveyname"]
        data = dict(request.form)
        questions = []

        for key, value in data.items():
            if key == "surveyname":
                pass
            else:
                questions.append(value)
        print(questions)

        user = db.session.execute(
            "SELECT * FROM users WHERE encrypted_username='" + encrypted_username + "';")
        for i in user:
            items = dict(i)
        survey_creator_username = items['username']

        new_survey = Surveys(username=survey_creator_username,
                             survey_name=current_survey_name)
        db.session.add(new_survey)

        for question in questions:
            new_question = Questions(
                username=survey_creator_username,  survey_name=current_survey_name, question=question)
            db.session.add(new_question)

        db.session.commit()

        return redirect(f"/user/{encrypted_username}/create_survey/{current_survey_name}/add_answers/")

    return render_template("create_survey.html")


@app.route("/user/<encrypted_username>/create_survey/<current_survey_name>/add_answers/", methods=["POST", "GET"])
def add_answer(encrypted_username, current_survey_name):
    
    user = db.session.execute(
            "SELECT * FROM users WHERE encrypted_username='" + encrypted_username + "';")
            
    for i in user:
        items = dict(i)

    current_username = items['username']
    
    
    questions = db.session.execute(
        "SELECT question FROM questions WHERE survey_name='" + current_survey_name + 
        "' AND username='" + current_username + "';")

    print(questions)

    if request.method == "POST":

        data = dict(request.form)
        for key, value in data.items():
            key = key[:-1].replace("_", " ")
            
            new_answer = Answers(username=current_username, survey=current_survey_name, question=key, answer=value, score=0)
            db.session.add(new_answer)

        db.session.commit()


        return jsonify({'redirect': url_for("user_page", encrypted_username=encrypted_username)})
    return render_template("add_answers.html", questions=questions)


@app.route("/user/<encrypted_username>/survey_results/<survey_name>/", methods=["POST", "GET"])
def survey_results(encrypted_username, survey_name):
    

    user = db.session.execute(
            "SELECT * FROM users WHERE encrypted_username='" + encrypted_username + "';")
            
    for i in user:
        items = dict(i)

    username = items['username']
    
    questions = db.session.execute("SELECT question FROM questions WHERE username='" +
                                                    username + "' AND survey_name='" + survey_name + "';")
    
    survey_questions = []
    
    for i in questions:
        items = dict(i)
        question = items['question']
        survey_questions.append(question)
    

        
    data = {}
    for question in survey_questions:
        answers = db.session.execute("SELECT * FROM answers WHERE survey='" +
                                                        survey_name + "' AND question='" + 
                                                        question + "' AND username='" +
                                                        username + "';")
        question_answers = []
        
        for i in answers:
            items = dict(i)
            question_answers.append([items['answer'], items['score']])
            
            
        data[question] = question_answers
        
        
    return render_template("survey_results.html", username=username,
                                        survey_name=survey_name, data=data)


@app.route("/answer_survey/<survey_id>", methods=['POST', 'GET'])
def answer_survey(survey_id):
    
    surveys = db.session.execute("SELECT * FROM surveys WHERE id=" + survey_id + ";")
    for i in surveys:
        items = dict(i)
        
    username = items['username']
    survey = items['survey_name']
    
    questions = db.session.execute("SELECT * FROM questions WHERE username='" +
                                                    username + "' AND survey_name='" +
                                                    survey + "';")
    
    current_questions = []
    for i in questions:
        current_questions.append(i[3])

        
    data = {}
    items_id = []
    for question in current_questions:

         answers = db.session.execute("SELECT * FROM answers WHERE survey='" +
                                                        survey + "' AND question='" + 
                                                        question + "' AND username='" +
                                                        username + "';")
   
         question_answers = []

         for i in answers:
             items = dict(i)
             items_id.append(items['id'])

             question_answers.append([items['id'], items['answer'], items['score']])
             
         data[question] = question_answers
    
    

    
    if request.method=='POST':

        for item in items_id:

            answer = request.form.getlist(str(item))
            
            if len(answer) > 0:
            
                print(answer, item)
                db.session.execute(f"UPDATE answers SET score=score+1 WHERE id={item};")
                db.session.commit()
        
        return redirect(url_for("survey_completed"))

        
    return render_template("answer_survey.html", data=data, survey_name=survey)


@app.route("/survey_completed/", methods=['POST', 'GET'])
def survey_completed():
    
    public_surveys = db.session.execute("SELECT * FROM surveys WHERE survey_type='public'")
    surveys = []
    for i in public_surveys:
        items = dict(i)
        surveys.append([items['survey_name'], items['id']])
            
    print(surveys)
    
    if request.method=='POST':
    
        survey_id = request.form.get("submit_button")
        print("-------")
        print(survey_id)
        return redirect(url_for("survey_completed"))

    return render_template("survey_completed.html", surveys=surveys)


if __name__ == "__main__":
    app.run(debug=True)

















