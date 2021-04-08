from pprint import pprint
from requests import delete, post, get, put

pprint(get('http://localhost:8080/api/jobs').json())

# Несуществующий id
pprint(put('http://localhost:8080/api/jobs/999', json={"job": "text"}).json())

# Добавим работу
pprint(post("http://localhost:8080/api/jobs", json={
    'id': 999,
    'team_leader': 1,
    "job": "text",
    'work_size': 30,
    'collaborators': "2, 3",
    'is_finished': False
}))

# Такого ключа не существует
pprint(put("http://localhost:8080/api/jobs/999", json={"job1": "text2"}).json())

pprint(put("http://localhost:8080/api/jobs/999", json={"job": "text2"}).json())

pprint(get('http://localhost:8080/api/jobs').json())

pprint(delete('http://localhost:8080/api/jobs/999').json())
