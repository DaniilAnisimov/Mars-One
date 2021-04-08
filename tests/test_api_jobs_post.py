from pprint import pprint
from requests import post

# Отправим пустой запрос и получим ошибку Empty request
pprint(post("http://localhost:8080/api/jobs", json={}).json())

# Отсутствует ключ job, получим ошибку: Bad request
pprint(post("http://localhost:8080/api/jobs", json={
    'id': 1,
    'team_leader': 1,
    'work_size': 30,
    'collaborators': "2, 3",
    'is_finished': 0
}
            ).json())
# OK
pprint(post("http://localhost:8080/api/jobs", json={
    'id': 1,
    'team_leader': 1,
    "job": "text",
    'work_size': 30,
    'collaborators': "2, 3",
    'is_finished': False
}
            ).json())
# Такой id уже существует в бд, получим ошибку: Id already exists
pprint(post("http://localhost:8080/api/jobs", json={
    'id': 1,
    'team_leader': 1,
    "job": "text2",
    'work_size': 15,
    'collaborators': "1",
    'is_finished': 0
}
            ).json())
