from flask import Flask, render_template, redirect, request, url_for
from forms.loginform import LoginForm
import json
import datetime
import os
from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
port = 8080
host = "127.0.0.1"

with open("settings.json") as file:
    data = json.load(file)
    app.config['SECRET_KEY'] = data["SECRET_KEY"]


@app.route("/")
@app.route("/<title>")
def main(title=""):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("main.html", title=title, jobs=jobs)


@app.route("/training/<prof>")
def training(prof):
    return render_template("training.html", prof=prof, title=prof)


@app.route("/list_prof/<list>")
def list_prof(list):
    return render_template("list_prof.html", list=list)


@app.route("/answer")
@app.route("/auto_answer")
def answer():
    questionnaire = {"title": "Watny Mark",
                     "surname": "Watny", "name": "Mark",
                     "education": "выше среднего", "profession": "штурман марсохода",
                     "sex": "male",
                     "motivation": "Всегда мечтал застрять на Марсе!",
                     "ready": "True"}
    return render_template("auto_answer.html", title=questionnaire["title"], questionnaire=questionnaire)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/answer')
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/distribution")
def distribution():
    astronauts = ["Ридли Скотт", "Энди Уир", "Марк Уотни",
                  "Венката Капур", "Тедди Сандерс", "Шон Бин"]
    return render_template('distribution.html', astronauts=astronauts)


@app.route("/table/<string:sex>/<int:age>")
def table(sex, age):
    return render_template('table.html', title="", sex=sex, age=age)


@app.route("/member")
def member():
    with open("templates/crew.json", encoding="utf-8") as f:
        d = json.load(f)["crew members"]
    return render_template('member.html', data=d)


@app.route("/gallery", methods=["POST", "GET"])
def gallery():
    if request.method == "GET":
        filenames = []
        for name in os.listdir("static/img/gallery/"):
            filenames.append(url_for('static', filename=f'/img/gallery/{name}'))
        return render_template('gallery.html', filenames=filenames, l=len(filenames))
    elif request.method == "POST":
        if request.files["file"]:
            with open(f"""static/img/gallery/im-{
            datetime.datetime.now().strftime(f"%Y-%m-%dT%H-%M-%S.%f")[:-4] + "Z"}.png""", "wb") as i:
                i.write(request.files["file"].read())
        return redirect("/gallery")


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run(port=port, host=host)
