from pprint import pprint
from requests import get, post, delete

# Получим всех пользователей
pprint(get("http://localhost:8080/api/v2/users").json())
# Добавим нового пользователя
pprint(post("http://localhost:8080/api/v2/users", json={'id': 2, 'surname': "a", 'name': "b", 'age': 30,
                                                        'position': "of", 'speciality': "ph", 'address': "ktm",
                                                        "password": "125876", 'email': "sd",
                                                        "city_from": "Арвидсъяур"}).json())
# Узнаем информацию о пользователе которого нет в бд
pprint(get("http://localhost:8080/api/v2/users/23").json())
# Узнаем информацию о пользователе
pprint(get("http://localhost:8080/api/v2/users/2").json())
# Удалим пользователя которого нет в бд: User 25 not found
pprint(delete("http://localhost:8080/api/v2/users/25").json())
# Удалим существующего пользователя
pprint(delete("http://localhost:8080/api/v2/users/2").json())
# Получим всех пользователей
pprint(get("http://localhost:8080/api/v2/users").json())
