from pprint import pprint
from requests import get, post, delete

pprint(get("http://localhost:8080/api/v2/jobs").json())

pprint(post("http://localhost:8080/api/v2/jobs", json={"id": 2, "team_leader": 1, "job": "123", "work_size": 3,
                                                       'collaborators': "2, 3", "is_finished": False}).json())

pprint(get("http://localhost:8080/api/v2/jobs/23").json())

pprint(get("http://localhost:8080/api/v2/jobs/2").json())

pprint(delete("http://localhost:8080/api/v2/jobs/25").json())

pprint(delete("http://localhost:8080/api/v2/jobs/2").json())

pprint(get("http://localhost:8080/api/v2/jobs").json())
