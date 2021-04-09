from pprint import pprint
from requests import get, post, put, delete

pprint(get("http://localhost:8080/api/users").json())

pprint(post("http://localhost:8080/api/users", json={'id': 2, 'surname': "a", 'name': "b", 'age': 30,
                                                     'position': "of", 'speciality': "ph", 'address': "ktm",
                                                     "password": "125876",
                                                     'email': "sd"}).json())

pprint(get("http://localhost:8080/api/users").json())

pprint(put("http://localhost:8080/api/users/2", json={'surname': "25"}).json())

pprint(get("http://localhost:8080/api/users").json())

pprint(delete("http://localhost:8080/api/users/2").json())

pprint(get("http://localhost:8080/api/users").json())


