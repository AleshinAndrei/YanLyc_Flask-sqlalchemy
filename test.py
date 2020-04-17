from requests import get, post, delete, put


print(get('http://localhost:5000/api/jobs').json())
print(put('http://localhost:5000/api/jobs/999').json())
print(put('http://localhost:5000/api/jobs/999', json={
    'team_leader': 2,
    'job': 'nothing 2',
    'work_size': 15,
    'collaborators': '',
    'is_finished': True,
}).json())
print(put('http://localhost:5000/api/jobs/a').json())
print(put('http://localhost:5000/api/jobs/').json())
print(put('http://localhost:5000/api/jobs/1').json())
print(put('http://localhost:5000/api/jobs/1', json={
    'team_leader': 2,
    'job': 'nothing 2',
    'work_size': 15,
    'collaborators': '',
    'is_finished': True,
}).json())
print(get('http://localhost:5000/api/jobs').json())
