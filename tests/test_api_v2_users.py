from pprint import pprint
from requests import get, post, delete

pprint(get("http://localhost:8080/api/v2/users").json())

pprint(post("http://localhost:8080/api/v2/users", json={'id': 2, 'surname': "a", 'name': "b", 'age': 30,
                                                        'position': "of", 'speciality': "ph", 'address': "ktm",
                                                        "password": "125876", 'email': "sd",
                                                        "city_from": "Арвидсъяур"}).json())

pprint(get("http://localhost:8080/api/v2/users/23").json())

pprint(get("http://localhost:8080/api/v2/users/2").json())

pprint(delete("http://localhost:8080/api/v2/users/25").json())

pprint(delete("http://localhost:8080/api/v2/users/2").json())

pprint(get("http://localhost:8080/api/v2/users").json())
