from data import db_session
from data.users import User
from data.jobs import Jobs

db_session.global_init("../db/mars_explorer.db")
db_sess = db_session.create_session()

list_user = [
    {
        "surname": "Scott",
        "name": "Ridley",
        "age": 21,
        "position": "captain",
        "speciality": "research engineer",
        "address": "module_1",
        "email": "scott_chief@mars.org",
        "city_from": "Венеция"
    },
    {
        "surname": "Бин",
        "name": "Шон",
        "age": 25,
        "position": "помощник капитана",
        "speciality": "доктор",
        "address": "module_1",
        "email": "sean_bean@mars.org",
        "city_from": "Тунис"
    },
    {
        "surname": "Уитни",
        "name": "Марк",
        "age": 23,
        "position": "бортинженер",
        "speciality": "инженер",
        "address": "module_1",
        "email": "mark_whitney@mars.org",
        "city_from": "Афины"
    },
    {
        "surname": "Уир",
        "name": "Энди",
        "age": 20,
        "position": "космонавт-исследователь",
        "speciality": "доктор",
        "address": "module_1",
        "email": "andy_weir@mars.org",
        "city_from": "Арвидсъяур"
    }
]

for data_user in list_user:
    if data_user["email"] not in list(map(lambda x: x.email, db_sess.query(User).all())):
        user = User()
        user.surname = data_user["surname"]
        user.name = data_user["name"]
        user.age = data_user["age"]
        user.position = data_user["position"]
        user.speciality = data_user["speciality"]
        user.address = data_user["address"]
        user.email = data_user["email"]
        user.city_from = data_user["city_from"]
        db_sess.add(user)
        db_sess.commit()

list_job = [
    {
        "team_leader": 1,
        "job": "deployment of residential modules 1 and 2",
        "work_size": 15,
        "collaborators": "2, 3",
        "is_finished": False
    }
]


for data_job in list_job:
    job = Jobs()
    job.team_leader = data_job["team_leader"]
    job.job = data_job["job"]
    job.work_size = data_job["work_size"]
    job.collaborators = data_job["collaborators"]
    job.is_finished = data_job["is_finished"]
    db_sess.add(job)
    db_sess.commit()
