from requests import get, post, delete, put


print(get('http://localhost:5000/api/v2/users/999').json())
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users', json={
    'surname': 'Al',
    'name': 'An',
    'age': 15,
    'position': 'captain',
    'speciality': 'engineer',
    'address': 'module_1',
    'email': 'aleshin_andrej@list.ru',
    'hashed_password': 'pbkdf2:sha256:150000$DLJX1X2C$f11d98fc92e8518b1793a8df77c522633b199202b6d82d1df860b9665062a09e',
}).json())
print(delete('http://localhost:5000/api/v2/users').json())
print(delete('http://localhost:5000/api/v2/users/999').json())
print(delete('http://localhost:5000/api/v2/users/2').json())

