from data import db_session
from data.users import User

list_user = [
    {
        "surname": "Scott",
        "name": "Ridley",
        "age": 21,
        "position": "captain",
        "speciality": "research engineer",
        "address": "module_1",
        "email": "scott_chief@mars.org"
    },
    {
        "surname": "Бин",
        "name": "Шон",
        "age": 25,
        "position": "помощник капитана",
        "speciality": "доктор",
        "address": "module_1",
        "email": "sean_bean@mars.org"
    },
    {
        "surname": "Уитни",
        "name": "Марк",
        "age": 23,
        "position": "бортинженер",
        "speciality": "инженер",
        "address": "module_1",
        "email": "mark_whitney@mars.org"
    },
    {
        "surname": "Уир",
        "name": "Энди",
        "age": 20,
        "position": "космонавт-исследователь",
        "speciality": "доктор",
        "address": "module_1",
        "email": "andy_weir@mars.org"
    }
]

db_session.global_init("../db/mars_explorer.db")
db_sess = db_session.create_session()
for data_user in list_user:
    user = User()
    user.surname = data_user["surname"]
    user.name = data_user["name"]
    user.age = data_user["age"]
    user.position = data_user["position"]
    user.speciality = data_user["speciality"]
    user.address = data_user["address"]
    user.email = data_user["email"]
    db_sess.add(user)
    db_sess.commit()
