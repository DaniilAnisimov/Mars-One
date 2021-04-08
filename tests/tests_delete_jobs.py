from requests import delete, post, get

print(get('http://localhost:8080/api/jobs').json())

print(delete('http://localhost:8080/api/jobs/999').json())
# новости с id = 999 нет в базе

# Добавим работу
print(post("http://localhost:8080/api/jobs", json={
    'id': 999,
    'team_leader': 1,
    "job": "text",
    'work_size': 30,
    'collaborators': "2, 3",
    'is_finished': False
}))

print(get('http://localhost:8080/api/jobs').json())

print(delete('http://localhost:8080/api/jobs/999').json())

print(get('http://localhost:8080/api/jobs').json())
