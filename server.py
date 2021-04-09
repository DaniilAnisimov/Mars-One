from flask import Flask, render_template, redirect, request, url_for, abort, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api

from forms.loginform import LoginForm
from forms.emergency_access_form import EmergencyAccessForm
from forms.user import RegisterForm
from forms.jobs import JobForm
from forms.department import DepartmentsForm

from data import db_session, jobs_api, users_api
from data.jobs import Jobs
from data.users import User
from data.department import Department
from data import users_resources, jobs_resource

from requests import get

from tools.spn import spn

import requests
import datetime
import json
import os

app = Flask(__name__)
api = Api(app)

port = 8080
host = "127.0.0.1"

app.register_blueprint(jobs_api.blueprint)
app.register_blueprint(users_api.blueprint)

api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')

api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')

login_manager = LoginManager()
login_manager.init_app(app)

with open("settings.json") as file:
    data = json.load(file)
    app.config['SECRET_KEY'] = data["SECRET_KEY"]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
def list_prof(p_list):
    return render_template("list_prof.html", list=p_list)


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


@app.route("/emergency_access", methods=['GET', 'POST'])
def emergency_access():
    form = EmergencyAccessForm()
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


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = int(form.id.data)
        job.work_size = int(form.size.data)
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', form=form)


@app.route('/jobs_delete/<int:j_id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(j_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == j_id,
                                      (Jobs.leader == current_user) | (Jobs.team_leader == 1)
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/jobs/<int:j_id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(j_id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == j_id,
                                         (Jobs.leader == current_user) | (Jobs.team_leader == 1)
                                         ).first()
        if job:
            form.title.data = job.job
            form.id.data = str(job.team_leader)
            form.size.data = str(job.work_size)
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == j_id,
                                         (Jobs.leader == current_user) | (Jobs.team_leader == 1)
                                         ).first()
        if job:
            job.job = form.title.data
            job.team_leader = int(form.id.data)
            job.work_size = int(form.size.data)
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.add(job)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = current_user.id
        department.members = form.members.data
        department.email = form.email.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/department')
    return render_template('a_e_department.html', form=form)


@app.route('/department_delete/<int:d_id>', methods=['GET', 'POST'])
@login_required
def department_delete(d_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == d_id,
                                                  (Department.user == current_user) | (Department.chief == 1)
                                                  ).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/department')


@app.route('/edit_department/<int:d_id>', methods=['GET', 'POST'])
@login_required
def edit_department(d_id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == d_id,
                                                      (Department.user == current_user) | (Department.chief == 1)
                                                      ).first()
        if department:
            form.title.data = department.title
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Department).filter(Department.id == d_id,
                                                      (Department.user == current_user) | (Department.chief == 1)
                                                      ).first()
        if department:
            department.title = form.title.data
            department.chief = current_user.id
            department.members = form.members.data
            department.email = form.email.data
            db_sess.add(department)
            db_sess.commit()
            return redirect('/department')
        else:
            abort(404)
    return render_template('a_e_department.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route("/department")
def _department():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("department.html", departments=departments)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/users_show/<int:user_id>", methods=["GET"])
def users_show(user_id):
    user = get(f"http://localhost:8080/api/users/{user_id}").json()["user"]
    if user == {'error': 'Not found'}:
        pass
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": data["apikey"],
        "geocode": user["city_from"],
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return f"Ошибка выполнения запроса:\nHttp статус: {response.status_code} ( {response.reason} )"

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    delta = toponym["boundedBy"]["Envelope"]
    lon, lat = toponym["Point"]["pos"].split()
    params = {
        "ll": ",".join([lon, lat]),
        "l": "sat",
        "size": "450,450",
        "spn": spn(delta["lowerCorner"], delta["upperCorner"]),
        "pt": ",".join([str(float(lon) + 0.0003), str(float(lat) + 0.0001)]) + ",flag"
    }
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params).url
    return render_template("users_show.html", name=user["name"], surname=user["surname"],
                           city=user["city_from"], picture=response)


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run(port=port, host=host)
