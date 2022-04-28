from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib


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



@app.route("/index.html")
@app.route("/")
def index(methods=['POST', 'GET']):
    return render_template("index.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        new_password = request.form['password']
        second_password = request.form['password2']
        new_username = request.form['username']
        encrypted_name = ''.join(format(ord(x), "b") for x in new_username)

        used_usernames = db.session.execute("SELECT username FROM users;")
        usernames_taken = []
        for name in used_usernames:
            usernames_taken.append(name[0])


        if new_username in usernames_taken:

            message = "This username is already taken, please try another"
            return render_template("signup.html", message=message)

        elif new_password != second_password:
            message = "These passwords do not match, please try again"
            return render_template("signup.html", message=message)

        else:
            encrypted_password = hashlib.sha256(new_password.encode("UTF-8")).hexdigest()
            new_user = Users(username=new_username, password=encrypted_password,
                             encrypted_username=encrypted_name)
            db.session.add(new_user)
            db.session.commit()

            session['logged in'] = True
            return redirect(f"/user/{encrypted_name}")

    message = ""
    return render_template("signup.html", message=message)



@app.route("/login", methods=['POST', 'GET'])
def login():

    if not request.cookies.get("username"):


        current_username = False
        current_password = False
        if request.method == "POST":
            current_username = False
            current_password = False
            current_username = request.form['username']
            current_password = request.form['password']
            current_password = hashlib.sha256(current_password.encode("UTF-8")).hexdigest()
            print(current_username)

            users = db.session.execute("SELECT * FROM users;")
            current_id = False

            for i in users:

                if i[1] == current_username:
                    current_id = i[0]

                    if i[2] != current_password:
                        message = "Password does not match username, please try again"

                        return render_template("login.html",
                                               message=message)

                    else:
                        print("Logged in")
                        encrypted_username = i[3]

                        session['logged in'] = True
                        message = ""
                        res = make_response(redirect(f"/user/{encrypted_username}"))
                        res.set_cookie("username", current_username, max_age=60*60*24)
                        res.set_cookie("password", current_password, max_age=60*60*24)

                        return res

            if current_id == False:
                # message="Username not found, please try again"
                message=f"{current_username} not found, please try again"
                return render_template("login.html",
                                               message=message)

        else:
            message = ""
            return render_template("login.html", message=message)

    else:
        current_username = request.cookies.get("username")
        current_password = request.cookies.get("password")

        users = db.session.execute("SELECT * FROM users;")
        current_id = False

        for i in users:

            if i[1] == current_username:
                current_id = i[0]

                if i[2] != current_password:
                    message = "Password does not match username, please try again"

                    return render_template("login.html",
                                               message=message)

                else:
                    print("Logged in")
                    encrypted_username = i[3]

                    session['logged in'] = True

                    res = make_response(redirect(f"/user/{encrypted_username}"))
                    res.set_cookie("username", current_username, max_age=60*60*24)
                    res.set_cookie("password", current_password, max_age=60*60*24)

                    return res

    message = ""
    return render_template("login.html", message=message)



@app.route("/user/<encrypted_username>", methods=['POST', 'GET'])
def user_page(encrypted_username):


    print("----------------------")


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

    if request.method == "POST":

        print("............doing somethiung----")

        if "logout_button" in request.form:
            session['logged in'] = False
            res = make_response(redirect("/"))
            res.set_cookie("username", "", max_age=0)
            res.set_cookie("password", "", max_age=0)
            print("Logged Out")
            return res

        elif "delete_survey_button" in request.form:
            print(request.form["delete_survey_button"])

            survey_number = request.form["delete_survey_button"].split("/")[-1]
            print(survey_number)




            deletion = db.session.execute("DELETE FROM Surveys WHERE id=" + survey_number + ";")
            db.session.commit()

            return redirect(f"/user/{encrypted_username}")


    try:
        if session['logged in'] == True:
            return render_template("userhome.html", user=user, username=username,
                                   items=items, create_survey_link=create_survey_link, surveys=surveys,
                                   encrypted_username=encrypted_name)
        else:
            return redirect("/login")
    except Exception:
        return redirect("/login")




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
            question = question.replace("?", "").replace("'", "").replace('"', '').replace(" ", "_")
            new_question = Questions(
                username=survey_creator_username,  survey_name=current_survey_name, question=question)
            db.session.add(new_question)

        db.session.commit()

        return redirect(f"/user/{encrypted_username}/create_survey/{current_survey_name}/add_answers/")


    try:
        if session['logged in'] == True:
            return render_template("create_survey.html")
        else:
            return redirect("/login")
    except:
        return redirect("/login")


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
        print(data)
        for key, value in data.items():
            print(key, value)
            print(key[:-1])
            key = key[:-1].replace(" ", "_").replace("?", "")
            print(key)
            new_answer = Answers(username=current_username, survey=current_survey_name, question=key, answer=value, score=0)
            db.session.add(new_answer)

        db.session.commit()


        return jsonify({'redirect': url_for("user_page", encrypted_username=encrypted_username)})

    try:
        if session['logged in'] == True:
            return render_template("add_answers.html", questions=questions)
        else:
            return redirect("/login")
    except:
        return redirect("/login")

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


    try:
        if session['logged in'] == True:
            return render_template("survey_results.html", username=username,
                                            survey_name=survey_name, data=data)
        else:
            return redirect("/login")
    except:
        return redirect("/login")

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

         print(question_answers)
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
    app.run()

















