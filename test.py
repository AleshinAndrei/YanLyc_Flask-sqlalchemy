from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/jobs/999').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 999,
    'job': 'nothing 2',
    'work_size': 15,
    'collaborators': '',
    'is_finished': True,
}).json())
print(post('http://localhost:5000/api/v2/jobs', json={
    'team_leader': 1,
    'job': 'nothing 2',
    'work_size': 15,
    'collaborators': '',
    'is_finished': True,
}).json())
print(delete('http://localhost:5000/api/v2/jobs').json())
print(delete('http://localhost:5000/api/v2/jobs/999').json())
print(delete('http://localhost:5000/api/v2/jobs/2').json())

